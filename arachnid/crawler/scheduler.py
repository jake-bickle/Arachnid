import requests

from collections import deque

from . import crawler_url
from . import url_functions


class DomainBlock:
    """ Holds a stack of parsed URLs to be crawled for a specific netloc """
    def __init__(self, parsed_url, fuzz_list=[]):
        self.netloc = parsed_url.get_netloc()
        self.pages_to_crawl = deque()  # To be used as a stack
        self.add_page(parsed_url)

    def add_page(self, parsed_url):
        if parsed_url in self.pages_to_crawl:
            return False
        self.pages_to_crawl.append(parsed_url)
        return True

    def next_url(self):
        try:
            p_url = self.pages_to_crawl.pop()
        except IndexError:
            return None
        return p_url

    def has_pages_to_crawl(self):
        return not not self.pages_to_crawl  # "not not" to return the deque's implicit truth if it has items

    def same_netloc(self, parsed_url):
        return self.netloc == parsed_url.get_netloc()


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, c_url, fuzzing_options=None):
        """ Sets up the scheduler to send out by a queue of domainblocks (aka a subdomain).
            Each domainblock will send out all of its available c_urls before being removed from queue.

            c_url is a CrawlerURL object
            fuzzing_options is an optional tuple that decides which aspects of the crawl to fuzz.
            fuzzing_options[0] must be a dict of header information to test whether a given c_url exists.
            fuzzing_options[1] Is a file location that holds a list of URL paths to try on each sub domain. It may be None type as well.
            fuzzing_options[2] Is a file location that holds a list of subdomain prefixes (IE. 'www', 'en', etc.) to test if they exist. It may be None type as well.
        """
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed = c_url
        self.headers = {}
        self.paths_to_fuzz = []
        self.subs_to_fuzz = []
        self.activate_sub_fuzz = False
        if fuzzing_options:
            self.headers = fuzzing_options[0]
            if fuzzing_options[1]:
                with open(fuzzing_options[1]) as f:
                    self.paths_to_fuzz = [line for line in f]
            if fuzzing_options[2]:
                self.activate_sub_fuzz = True
                with open(fuzzing_options[2]) as f:
                    self.subs_to_fuzz = [line for line in f]
        self.schedule_url(self.seed)

    def schedule_url(self, c_url):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
            - It has not passed any of other filters
        """
        if not url_functions.is_subdomain(c_url, self.seed) or c_url in self.crawled_urls:
            return False
        block = self._ensure_domain_block(c_url)
        return block.add_page(c_url)

    def next_url(self):
        if not self.blocks_to_crawl and self.activate_sub_fuzz:
            self._fuzz_for_domainblocks()
        if not self.blocks_to_crawl:
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        p_url = block_to_crawl.next_url()
        if not block_to_crawl.has_pages_to_crawl():
            self.blocks_to_crawl.popleft()
        self.crawled_urls.add(p_url)
        return p_url

    def _get_domain_block(self, parsed_url):
        for block in self.blocks_to_crawl:
            if block.same_netloc(parsed_url):
                return block
        return None

    def _ensure_domain_block(self, parsed_url):
        block = self._get_domain_block(parsed_url)
        if block is None:
            block = DomainBlock(parsed_url)
            self.blocks_to_crawl.append(block)
        return block

    def _fuzz_for_domainblocks(self):
        self.activate_sub_fuzz = False
        for prefix in self.subs_to_fuzz:
            sub_to_check = crawler_url.CrawlerURL(url_functions.change_subdomain(prefix, self.seed.get_url()),
                                                  is_fuzzed=True, allow_fragments=False)
            r = requests.head(sub_to_check.get_url(), headers=self.headers)
            if r.status_code != '404':
                self.schedule_url(sub_to_check)
