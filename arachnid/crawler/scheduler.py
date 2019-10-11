import requests
import threading

from collections import deque, namedtuple

from . import url_functions
from . import warning_issuer
from .crawler_url import CrawlerURL
from .robotparser import RobotFileParser

FuzzingOptions = namedtuple("FuzzingOptions", ["paths_list_loc", "subs_list_loc"])


class Scheduler:
    def __init__(self, c_url, useragent="", fuzzing_options=None, respect_robots=True, allow_subdomains=True,
                 blacklist_dirs=[]):
        self.seed = c_url
        self.prev_c_url = None
        self.prev_c_url_is_supplemental = False
        self.bank = {c_url: 100000}
        self.supplemental_c_url_queue = deque()  # A URL from robots.txt or Fuzz of any kind
        self.virtual_credit = 0
        self.allow_subdomains = allow_subdomains
        self.blacklist_dirs = set(blacklist_dirs)
        self.respect_robots = respect_robots
        self.robot_cache = dict()  # Key netloc string: Value RobotFileParser object
        self.useragent = useragent
        self.current_delay = 0
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
        if self.prev_c_url_is_supplemental:
            # Slight mod to AOPIC: Any supplemental prev_c_url is given 1000 credits
            creds = 1000
        else:
            creds = self.bank[self.prev_c_url]
            self.bank[self.prev_c_url] = 0
        sanitized_urls = [c_url for c_url in found_c_urls if self.will_schedule(c_url)]
        creds = self.tax_credits(creds)
        self.disperse_credits(creds, sanitized_urls)
        self.disperse_virtual_credits_if_necessary()

    def tax_credits(self, creds):
        tax = creds / 10
        self.virtual_credit += tax
        return creds - tax

    def disperse_credits(self, credits, c_urls):
        if len(c_urls) > 0:
            credits_per_page = credits / len(c_urls)
            for c_url in c_urls:
                try:
                    # Slight mod to AOPIC: Do not give credit to any c_url with 0 credits. This has already been crawled
                    if self.bank[c_url] != 0:
                        self.bank[c_url] += credits_per_page
                except KeyError:
                    # c_url isn't in the bank, add it
                    if c_url.get_url_parts().path in self.paths_to_fuzz:
                        c_url.set_on_fuzz(True)
                    self.bank[c_url] = credits_per_page
                if c_url.get_netloc() not in self.robot_cache.keys():
                    self._add_new_subdomain(c_url)

    def disperse_virtual_credits_if_necessary(self):
        pages_to_receive_bonus = self.uncrawled_pages()
        if max(self.bank.values()) < self.virtual_credit and len(pages_to_receive_bonus) != 0:
            bonus = self.virtual_credit / len(pages_to_receive_bonus)
            for c_url in pages_to_receive_bonus:
                self.bank[c_url] += bonus
            self.virtual_credit = 0

    def uncrawled_pages(self):
        uncrawled_pages = list()
        for c_url, creds in self.bank.items():
            if creds > 0:
                uncrawled_pages.append(c_url)
        return uncrawled_pages

    def next_url(self):
        try:
            c_url = self.supplemental_c_url_queue.pop()
            self.prev_c_url_is_supplemental = True
        except IndexError:
            c_url = max(self.bank, key=self.bank.get)
            self.prev_c_url_is_supplemental = False
            if self.bank[c_url] == 0:
                # Since a c_url with 0 credits means it has been crawled, then all c_urls have been crawled
                return None
        self.current_delay = self.calculate_crawl_delay(c_url)
        self.prev_c_url = c_url
        return c_url

    def get_crawl_delay(self):
        return self.current_delay

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

    def calculate_crawl_delay(self, c_url):
        if self.respect_robots:
            robots = self._get_robots(c_url)
            if robots.crawl_delay(self.useragent):
                return robots.crawl_delay(self.useragent)
            elif robots.request_rate(self.useragent):
                reqrate = robots.request_rate(self.useragent)
                return reqrate.seconds // reqrate.requests
        return 0

    def _add_new_subdomain(self, c_url):
        robots = self._get_robots(c_url)
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
