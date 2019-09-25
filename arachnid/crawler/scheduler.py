import requests
import threading

from collections import deque, namedtuple

from . import url_functions
from . import warning_issuer
from .crawler_url import CrawlerURL
from .robotparser import RobotFileParser

FuzzingOptions = namedtuple("FuzzingOptions", ["paths_list_loc", "subs_list_loc"])


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, c_url, useragent="", fuzzing_options=None, respect_robots=True, allow_subdomains=True):
        """ Sets up the scheduler to send out by a queue of domainblocks (aka a subdomain).
            Each domainblock will send out all of its available c_urls before being removed from queue.
        """
        self.seed = c_url
        self.previous_c_url = None
        self.bank = {c_url: 100000}
        self.supplemental_c_url_queue = deque()  # A URL from robots.txt or Fuzz of any kind
        self.virtual_cache = 0
        self.allow_subdomains = allow_subdomains
        self.respect_robots = respect_robots
        self.robot_db = dict()  # Key netloc string: Value RobotFileParser object
        self.useragent = useragent
        self.current_delay = 0
        self.fuzz_paths = False
        if fuzzing_options:
            if fuzzing_options.paths_list_loc:
                with open(fuzzing_options.paths_list_loc) as f:
                    self.paths_to_fuzz = set("/" + line.strip() for line in f)  # Add to supplemental on a thread
                self.fuzz_paths = True
            if fuzzing_options.subs_list_loc:
                with open(fuzzing_options.subs_list_loc) as f:
                    self.subs_to_fuzz = set(line.strip() for line in f)  # Add to supplemental on a thread
                threading.Thread(target=self._add_sub_fuzz_to_sq())
        self._add_new_subdomain(self.seed)

    def report_found_urls(self, found_c_urls):
        """ Reports back to the scheduler of the URLs (found_c_urls) found from previously sent c_url
        This performs a modified version of the AOPIC algorithm. Refer to the following issue for more info:
        https://github.com/jake-bickle/Arachnid/issues/6
        """
        if self.previous_c_url.is_fuzzed() or self.previous_c_url.in_robots():
            # Slight mod to AOPIC: Any supplemental previous_c_url is given 1000 cache
            cache = 1000
        else:
            cache = self.bank[self.previous_c_url]
            self.bank[self.previous_c_url] = 0
        cleaned_urls = [c_url for c_url in found_c_urls if self.will_schedule(c_url)]
        tax = cache / 10
        self.virtual_cache += tax
        if len(cleaned_urls) > 0:
            cache_per_page = (cache - tax) / len(cleaned_urls)
            for c_url in cleaned_urls:
                if c_url.get_netloc() not in self.robot_db.keys():
                    self._add_new_subdomain(c_url)
                try:
                    # Slight mod to AOPIC: Do not give credit to any c_url with 0 cache. This has already been crawled
                    if self.bank[c_url] != 0:
                        self.bank[c_url] += cache_per_page
                except KeyError:
                    self.bank[c_url] = cache_per_page
        num_uncrawled = len(tuple(c_url for c_url, credit in self.bank.items()))
        if max(self.bank.values()) < self.virtual_cache and num_uncrawled != 0:
            bonus = self.virtual_cache / num_uncrawled
            for c_url, credit in self.bank.items():
                if credit != 0:
                    self.bank[c_url] += bonus
            self.virtual_cache = 0

    def next_url(self):
        try:
            c_url = self.supplemental_c_url_queue.pop()
        except IndexError:
            c_url = max(self.bank, key=self.bank.get)
            if self.bank[c_url] == 0:
                # Since a c_url with a cache of 0 means its been crawled, then all c_urls have been crawled
                return None
        if c_url.get_url_parts().path in self.paths_to_fuzz:
            c_url.set_on_fuzz(True)
        self.current_delay = self.calculate_crawl_delay(c_url)
        self.previous_c_url = c_url
        return c_url

    def get_crawl_delay(self):
        return self.current_delay

    def will_schedule(self, c_url):
        """ Returns whether a given c_url will be scheduled or not """
        if not url_functions.is_subdomain(c_url, self.seed):
            # Must always be a subdomain
            return False
        if not self.allow_subdomains and not self.seed.get_netloc() == c_url.get_netloc():
            # If subdomains is not allowed, then c_url must be of the same netloc
            return False
        if self.respect_robots:
            # Don't crawl if robots.txt disallows it and scheduler is respecting it
            robots = self._ensure_robots(c_url)
            if not robots.can_fetch(self.useragent, c_url.get_url()):
                return False
        return True

    def calculate_crawl_delay(self, c_url):
        if self.respect_robots:
            robots = self._ensure_robots(c_url)
            if robots.crawl_delay(self.useragent):
                return robots.crawl_delay(self.useragent)
            elif robots.request_rate(self.useragent):
                reqrate = robots.request_rate(self.useragent)
                return reqrate.seconds // reqrate.requests
        return 0

    def _add_new_subdomain(self, c_url):
        robots = self._ensure_robots(c_url)
        if not self.respect_robots:
            for path in robots.all_paths():
                new_url = url_functions.join_url(c_url.get_base(), path)
                self.supplemental_c_url_queue.append((CrawlerURL(new_url, in_robots=True)))
        if self.fuzz_paths:
            fuzz_thread = threading.Thread(target=self._add_path_fuzz_to_sq, args=(c_url.get_base(),))
            fuzz_thread.start()

    def _add_path_fuzz_to_sq(self, url_base=""):
        """ Given a url_base (That is, everything in the URL up to the beginning of the path), add all permutations of
            the url_base and the paths in the paths_to_fuzz list to the supplemental queue

            Depending on the length of paths_to_fuzz, this function may take a long time to complete and is recommended
            to be called using a separate thread to prohibit stalling of the crawler.
        """
        for path in self.paths_to_fuzz:
            c_url = CrawlerURL(url_functions.join_url(url_base, path), is_fuzzed=True)
            self.supplemental_c_url_queue.append(c_url)

    def _add_sub_fuzz_to_sq(self):
        """ Create all permutations of the prefixes in subs_to_fuzz and the seed domain to get a list of possible
            subdomains to add to the supplemental queue. Only URLs that actually exist will be added.

            Depending on the length of subs_to_fuzz, this function may take a long time to complete and is recommended
            to be called using a separate thread to prohibit stalling of the crawler.
        """
        for prefix in self.subs_to_fuzz:
            sub_to_check = CrawlerURL(url_functions.change_subdomain(prefix.strip(), self.seed.get_url()),
                                      is_fuzzed=True)
            try:
                # Checks to see if URL exists. This prevents scheduler from generating thousands of fuzzed links from a
                # subdomain that doesn't exist
                requests.head(sub_to_check.get_url(), headers={"User-Agent": self.useragent}, timeout=30)
                self._add_new_subdomain(sub_to_check)
            except BaseException as e:
                # Ignore ConnectionError base class as that represents a subdomain that doesn't exist in this context.
                # Written as such because we are interested in SSL errors which is inherently a ConnectionError but
                # doesn't necessarily mean that there isn't an available subdomain.
                if not e.__class__.__name__ == "ConnectionError":
                    warning_issuer.issue_warning_from_exception(e, sub_to_check.get_url())

    def _ensure_robots(self, c_url):
        try:
            return self.robot_db[c_url.get_netloc()]
        except KeyError:
            new_sub_robots = RobotFileParser(url_functions.get_robots(c_url))
            new_sub_robots.read()
            self.robot_db[c_url.get_netloc()] = new_sub_robots
            return new_sub_robots
