import requests
import threading

from collections import deque, namedtuple

from arachnid.crawler import url_functions
from arachnid.crawler import warning_issuer
from arachnid.crawler.crawler_url import CrawlerURL
from arachnid.crawler.robotparser import RobotFileParser
from arachnid.crawler.aopic_bank import AOPICBank

FuzzingOptions = namedtuple("FuzzingOptions", ["paths_list_loc", "subs_list_loc"])


class Scheduler:
    def __init__(self, c_url, useragent="", fuzzing_options=None, respect_robots=True, allow_subdomains=True,
                 blacklist_dirs=[]):
        self.seed = c_url
        self.bank = AOPICBank(self.seed)
        self.prev_c_url = None
        self.prev_c_url_is_supplemental = False
        self.supplemental_c_url_queue = deque()  # A URL from robots.txt or Fuzz of any kind
        self.allow_subdomains = allow_subdomains
        self.blacklist_dirs = set(blacklist_dirs)
        self.respect_robots = respect_robots
        self.robot_cache = dict()  # Key netloc string: Value RobotFileParser object
        self.useragent = useragent
        self.paths_to_fuzz = []
        self.subs_to_fuzz = []
        self.fuzz_paths = False
        if fuzzing_options:
            self.apply_fuzzing_options(fuzzing_options)
        self._add_new_subdomain(self.seed)

    def report_found_urls(self, found_c_urls):
        """ Reports back to the scheduler of the URLs (found_c_urls) found from previously sent c_url
        This performs a modified version of the AOPIC algorithm. Refer to the following issue for more info:
        https://github.com/jake-bickle/Arachnid/issues/6
        """
        sanitized_urls = [c_url for c_url in found_c_urls if self.will_schedule(c_url)]
        self.bank.disperse_credits(self.prev_c_url, sanitized_urls, is_supplemental=self.prev_c_url_is_supplemental)
        for c_url in sanitized_urls:
            if c_url.get_netloc() not in self.robot_cache.keys():
                self._add_new_subdomain(c_url)
            if c_url.get_url_parts().path in self.paths_to_fuzz:
                c_url.set_on_fuzz(True)

    def next_url(self):
        try:
            c_url = self.supplemental_c_url_queue.pop()
            self.prev_c_url_is_supplemental = True
        except IndexError:
            c_url = self.bank.highest_priority_c_url()
            self.prev_c_url_is_supplemental = False
        self.prev_c_url = c_url
        return c_url

    def get_crawl_delay(self):
        if self.respect_robots and self.prev_c_url:
            robots = self._get_robots(self.prev_c_url)
            if robots.crawl_delay(self.useragent):
                return robots.crawl_delay(self.useragent)
            elif robots.request_rate(self.useragent):
                reqrate = robots.request_rate(self.useragent)
                return reqrate.seconds // reqrate.requests
        return 0

    def will_schedule(self, c_url):
        """ Returns whether a c_url will be scheduled or not. The rules are as follows:
        - c_url must be a subdomain of the seed c_url
        - If subdomains are not allowed, then c_url must have the same netloc as the seed c_url
        - If respecting robots, the c_url along with the scheduler's useragent must be allowed as per the subdomain's
          robots.txt rules
        - The c_url path must not have a blacklisted directory
        """
        if not url_functions.is_subdomain(c_url, self.seed):
            return False
        if not self.allow_subdomains and self.seed.get_netloc() != c_url.get_netloc():
            return False
        if self.blocked_by_robots(c_url):
            return False
        for dir in c_url.get_url_parts().path.split("/"):
            if dir in self.blacklist_dirs:
                return False
        return True

    def blocked_by_robots(self, c_url):
        if self.respect_robots:
            robots = self._get_robots(c_url)
            return not robots.can_fetch(self.useragent, c_url.get_url())

    def _add_new_subdomain(self, c_url):
        robots = self._get_robots(c_url)
        if not self.respect_robots:
            for path in robots.all_paths():
                new_url = url_functions.join_url(c_url.get_base(), path)
                c_url = CrawlerURL(new_url, in_robots=True)
                self.supplemental_c_url_queue.append(c_url)
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

    def _get_robots(self, c_url):
        try:
            return self.robot_cache[c_url.get_netloc()]
        except KeyError:
            new_sub_robots = RobotFileParser(url_functions.get_robots(c_url))
            new_sub_robots.read()
            self.robot_cache[c_url.get_netloc()] = new_sub_robots
            return new_sub_robots

    def apply_fuzzing_options(self, fuzzing_options):
        if fuzzing_options.paths_list_loc:
            with open(fuzzing_options.paths_list_loc) as f:
                self.paths_to_fuzz = set("/" + line.strip() for line in f)
            self.fuzz_paths = True
        if fuzzing_options.subs_list_loc:
            with open(fuzzing_options.subs_list_loc) as f:
                self.subs_to_fuzz = set(line.strip() for line in f)
            threading.Thread(target=self._add_sub_fuzz_to_sq).start()
