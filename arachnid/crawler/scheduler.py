from collections import deque

from . import url_functions


class DomainBlock:
    """ Holds a stack of parsed URLs to be crawled for a specific netloc """
    def __init__(self, parsed_url):
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

    def __init__(self, parsed_url, fuzz_list=None):
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed = parsed_url
        self.filters = []
        self.schedule_url(self.seed)
        if fuzz_list:
            with open(fuzz_list) as f:
                self.fuzz_list = [line for line in f]

    def schedule_url(self, c_url):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
            - It has not passed any of other filters
        """
        if not url_functions.is_subdomain(c_url, self.seed) or c_url in self.crawled_urls:
            return False
        for filter in self.filters:
            if filter.is_filtered(c_url):
                return False
        block = self._ensure_domain_block(c_url)
        return block.add_page(c_url)

    def next_url(self):
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

