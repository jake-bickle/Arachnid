import requests

from collections import deque, namedtuple

from . import url_functions
from . import warning_issuer
from .crawler_url import CrawlerURL
from .robotparser import RobotFileParser

FuzzingOptions = namedtuple("FuzzingOptions", ["paths_list_loc", "subs_list_loc", "fuzz_for_paths", "fuzz_for_subs"])


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, c_url, useragent="", fuzzing_options=None, respect_robots=True, allow_subdomains=True):
        """ Sets up the scheduler to send out by a queue of domainblocks (aka a subdomain).
            Each domainblock will send out all of its available c_urls before being removed from queue.
        """
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed = c_url
        self.respect_robots = respect_robots
        self.useragent = useragent
        self.allow_subdomains = allow_subdomains
        self.current_delay = 0
        self.fuzz_paths = False
        self.fuzz_subs = False
        self.paths_to_fuzz = set()
        self.subs_to_fuzz = set()
        if fuzzing_options:
            self.fuzz_paths = fuzzing_options.fuzz_for_paths
            self.fuzz_subs = fuzzing_options.fuzz_for_subs
            if fuzzing_options.paths_list_loc:
                with open(fuzzing_options.paths_list_loc) as f:
                    self.paths_to_fuzz = set("/" + line.strip() for line in f)
            if fuzzing_options.subs_list_loc:
                with open(fuzzing_options.subs_list_loc) as f:
                    self.subs_to_fuzz = set(line.strip() for line in f)
        self.schedule_url(self.seed)

    def schedule_url(self, c_url):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
        """
        if not url_functions.is_subdomain(c_url, self.seed) or c_url in self.crawled_urls:
            return False
        if not self.allow_subdomains and c_url.get_netloc() != self.seed.get_netloc():
            return False
        block = self._ensure_domain_block(c_url)
        return block.add_page(c_url)

    def next_url(self):
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

    def get_crawl_delay(self):
        return self.current_delay

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
