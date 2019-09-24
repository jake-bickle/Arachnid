import requests

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
        self.bank = {c_url: 100000}
        self.virtual_cache = 0
        self.supplemental_c_url_queue = deque()  # A URL from robots.txt or Fuzz of any kind
        self.respect_robots = respect_robots
        self.useragent = useragent
        self.allow_subdomains = allow_subdomains
        self.current_delay = 0
        if fuzzing_options:
            self.fuzz_paths = fuzzing_options.fuzz_for_paths
            self.fuzz_subs = fuzzing_options.fuzz_for_subs
            if fuzzing_options.paths_list_loc:
                with open(fuzzing_options.paths_list_loc) as f:
                    self.paths_to_fuzz = set("/" + line.strip() for line in f)  # Add to supplemental on a thread
            if fuzzing_options.subs_list_loc:
                with open(fuzzing_options.subs_list_loc) as f:
                    self.subs_to_fuzz = set(line.strip() for line in f)  # Add to supplemental on a thread

    #TODO What about new subdomains?? Their fuzz, their robots, etc.
    def report_found_urls(self, found_c_urls, crawled_c_url):
        if crawled_c_url.is_fuzzed() or crawled_c_url.in_robots():
            # Slight mod to AOPIC: Any supplemental crawled_c_url is given 1000 cache
            cache = 1000
        else:
            cache = self.bank[crawled_c_url]
            self.bank[crawled_c_url] = 0
        cleaned_urls = [c_url for c_url in found_c_urls if self.will_schedule(c_url)]
        tax = cache / 10
        self.virtual_cache += tax
        if len(cleaned_urls) > 0:
            cache_per_page = (cache - tax) / len(cleaned_urls)
            for c_url in cleaned_urls:
                try:
                    # Slight mod to AOPIC: Do not give credit to any c_url with 0 cache. This has already been crawled
                    if self.bank[c_url] != 0:
                        self.bank[c_url] += cache_per_page
                except KeyError:
                    self.bank[c_url] = cache_per_page
        if max(self.bank, key=self.bank.get) < self.virtual_cache:
            bonus = self.virtual_cache / len(tuple(c_url for c_url, credit in self.bank if credit != 0))
            for c_url, credit in self.bank:
                if credit != 0:
                    self.bank[c_url] += bonus
            self.virtual_cache = 0

    def next_url(self):
        """
        if not self.blocks_to_crawl and self.fuzz_subs:
            self._fuzz_for_domainblocks()
        if not self.blocks_to_crawl:
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        c_url = block_to_crawl.next_url()
        if not block_to_crawl.has_pages_to_crawl():
            self.blocks_to_crawl.popleft()
        if c_url.get_url_parts().path in self.paths_to_fuzz:
            c_url.set_on_fuzz(True)
        self.crawled_urls.add(c_url)
        self.current_delay = block_to_crawl.crawl_delay
        return c_url
        """

    def get_crawl_delay(self):
        return self.current_delay

    def will_schedule(self, c_url):
        if not url_functions.is_subdomain(c_url, self.seed):
            # Must always be a subdomain
            return False
        if not self.allow_subdomains and not self.seed.get_netloc() == c_url.get_netloc():
            # If subdomains is not allowed, then c_url must be of the same netloc
            return False

    def _get_domain_block(self, c_url):
        for block in self.blocks_to_crawl:
            if block.same_netloc(c_url):
                return block
        return None

    def _ensure_domain_block(self, c_url):
        block = self._get_domain_block(c_url)
        if block is None:
            block = DomainBlock(c_url, useragent=self.useragent, respect_robots=self.respect_robots,
                                fuzz_list=self.paths_to_fuzz if self.fuzz_paths else set())
            self.blocks_to_crawl.append(block)
        return block

    def _fuzz_for_domainblocks(self):
        self.fuzz_subs = False  # The function is activated by fuzz_subs. Don't activate it again
        for prefix in self.subs_to_fuzz:
            sub_to_check = CrawlerURL(url_functions.change_subdomain(prefix.strip(), self.seed.get_url()),
                                      is_fuzzed=True)
            print(sub_to_check.get_url())
            try:
                requests.head(sub_to_check.get_url(), headers={"User-Agent": self.useragent}, timeout=30)
                self.schedule_url(sub_to_check)
            except BaseException as e:
                # Ignore ConnectionError base class as that represents a subdomain that doesn't exist in this context.
                # Written as such because we are interested in SSL errors which is inherently a ConnectionError but
                # doesn't necessarily mean that there isn't an available subdomain.
                if not e.__class__.__name__ == "ConnectionError":
                    warning_issuer.issue_warning_from_exception(e, sub_to_check.get_url())


class DomainBlock:
    """ Holds a stack of parsed URLs to be crawled for a specific netloc """
    def __init__(self, c_url, fuzz_list=set(), respect_robots=True, useragent=""):
        self.seed = c_url
        self.useragent = useragent
        self.respect_robots = respect_robots
        self.crawl_delay = 0
        self.pages_to_crawl = deque()  # To be used as a stack
        self.robots = RobotFileParser("{0}/robots.txt".format(c_url.get_base()))
        self.robots.read()
        self.fuzz_iter = iter(fuzz_list)  # Must iterate through fuzz over time, as scheduling all paths as
                                          # CrawlerURL objects at once is quite slow
        if self.respect_robots:
            if self.robots.crawl_delay(self.useragent):
                self.crawl_delay = self.robots.crawl_delay(self.useragent)
            else:
                reqrate = self.robots.request_rate(self.useragent)
                if reqrate:
                    self.crawl_delay = reqrate.seconds // reqrate.requests
        else:
            for path in self.robots.all_paths():
                new_url = url_functions.join_url(c_url.get_base(), path)
                self.add_page(CrawlerURL(new_url, in_robots=True))
        self.add_page(c_url)

    def add_page(self, c_url):
        if c_url in self.pages_to_crawl or self.respect_robots and not self.robots.can_fetch(self.useragent, c_url.get_url()):
            return False
        self.pages_to_crawl.append(c_url)
        return True

    def next_url(self):
        """ Returns the next_url in the stack. Since there are many pages to fuzz and converting all of them to
            CrawlerURL objects at the same time halts the program for a substantial amount of time, the Domainblock
            splits the work up by adding a page each time next_url is called. """
        self._add_next_fuzz_page()
        return self.pages_to_crawl.pop()

    def has_pages_to_crawl(self):
        return not not self.pages_to_crawl  # "not not" to return the deque's implicit truth if it has items

    def same_netloc(self, c_url):
        return self.seed.get_netloc() == c_url.get_netloc()

    def _add_next_fuzz_page(self):
        path = next(self.fuzz_iter, None)
        if path:
            url = url_functions.join_url(self.seed.get_base(), path)
            self.add_page(CrawlerURL(url, is_fuzzed=True))
