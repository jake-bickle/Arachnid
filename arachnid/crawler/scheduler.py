import requests

from collections import deque

from . import url_functions
from . import warning_issuer
from .crawler_url import CrawlerURL
from .robotparser import RobotFileParser


class DomainBlock:
    """ Holds a stack of parsed URLs to be crawled for a specific netloc """
    def __init__(self, c_url, fuzz_list=tuple(), respect_robots=True, useragent=""):
        self.netloc = c_url.get_netloc()
        self.useragent = useragent
        self.respect_robots = respect_robots
        self.crawl_delay = 0
        self.pages_to_crawl = deque()  # To be used as a stack
        for path in fuzz_list:
            fuzzed_page = CrawlerURL(url_functions.join_url(c_url.get_url(), path),
                                     is_fuzzed=True, allow_fragments=False)
            self.add_page(fuzzed_page)
        self.robots = RobotFileParser("{0}/robots.txt".format(c_url.get_base()))
        self.robots.read()
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
                self.add_page(CrawlerURL(new_url, in_robots=True, allow_fragments=False))
        self.add_page(c_url)

    def add_page(self, c_url):
        if c_url in self.pages_to_crawl or self.respect_robots and not self.robots.can_fetch(self.useragent, c_url.get_url()):
            return False
        self.pages_to_crawl.append(c_url)
        return True

    def next_url(self):
        try:
            c_url = self.pages_to_crawl.pop()
        except IndexError:
            return None
        return c_url

    def has_pages_to_crawl(self):
        return not not self.pages_to_crawl  # "not not" to return the deque's implicit truth if it has items

    def same_netloc(self, c_url):
        return self.netloc == c_url.get_netloc()


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, c_url, useragent="", respect_robots=True, fuzzing_options=None, allow_subdomains=True):
        """ Sets up the scheduler to send out by a queue of domainblocks (aka a subdomain).
            Each domainblock will send out all of its available c_urls before being removed from queue.

            c_url is a CrawlerURL object
            fuzzing_options is an optional tuple that decides which aspects of the crawl to fuzz.
            fuzzing_options[0] Is a file location that holds a list of URL paths to try on each sub domain. It may be None type as well.
            fuzzing_options[1] Is a file location that holds a list of subdomain prefixes (IE. 'www', 'en', etc.) to test if they exist. It may be None type as well.
        """
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed = c_url
        self.respect_robots = respect_robots
        self.useragent = useragent
        self.allow_subdomains = allow_subdomains
        self.paths_to_fuzz = ()
        self.subs_to_fuzz = ()
        self.activate_sub_fuzz = False
        if fuzzing_options[0] or fuzzing_options[1]:
            print("Loading list data for fuzzing operations. Some lists are quite large and may take some time.")
            if fuzzing_options[0]:
                with open(fuzzing_options[1]) as f:
                    self.paths_to_fuzz = tuple(line.strip() for line in f)
            if fuzzing_options[1]:
                self.activate_sub_fuzz = True
                with open(fuzzing_options[1]) as f:
                    self.subs_to_fuzz = tuple(line.strip() for line in f)
        self.schedule_url(self.seed)
        self.current_delay = 0

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
        if not self.blocks_to_crawl and self.activate_sub_fuzz:
            self._fuzz_for_domainblocks()
        if not self.blocks_to_crawl:
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        c_url = block_to_crawl.next_url()
        if not block_to_crawl.has_pages_to_crawl():
            self.blocks_to_crawl.popleft()
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
                                fuzz_list=self.paths_to_fuzz)
            self.blocks_to_crawl.append(block)
        return block

    def _fuzz_for_domainblocks(self):
        self.activate_sub_fuzz = False
        for prefix in self.subs_to_fuzz:
            sub_to_check = CrawlerURL(url_functions.change_subdomain(prefix.strip(), self.seed.get_url()),
                                      is_fuzzed=True, allow_fragments=False)

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

