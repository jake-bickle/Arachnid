import urlparser
from URL import URL
from filters import URLDiffFilter
from collections import deque


class DomainBlock:
    """ Holds a stack of extensions to be crawled for an arbitrary net location 
        An extension is the portion of the URL that occurs after the suffix

        https://www.example.com/path/to/location;key1=value1?key2=value2#content
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    def __init__(self, url):
        self.domain = url.get_domain()
        self.lamb = 0
        self.frontier = deque()  # To be used as a stack
        self.add_url(url)

    def add_url(self, url):
        if self.url_already_added(url):
            return False
        self.frontier.append(url)
        return True

    def next_url(self):
        try:
            url = self.frontier.pop()
            credits = url.relinquish_credits()
            self.lamb += credits[0]
            return url
        except IndexError:
            return None

    def extension_already_added(self, extension):
        return extension in self.extensions_to_crawl


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, url=""):
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed_url = urlparser.parse_url(url)
        self.filters = [URLDiffFilter.URLDiffFilter()]
        self.schedule_url(url)

    def schedule_url(self, url_str="", allow_fragments=False):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
            - It has not passed the URLDiffFilter
        """
        url = URL(url_str, allow_fragments)
        if not urlparser.same_domain(url.get_url(), self.seed_url) or self.has_been_crawled(url.get_url()):
            return False
        for filter in self.filters:
            if filter.is_filtered(url):
                return False
        block = self._ensure_domain_block(url)
        return block.add_extension(url.get_extension())

    def next_url(self):
        if not self.blocks_to_crawl: 
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        url = block_to_crawl.next_url()
        if not block_to_crawl.extensions_to_crawl:
            self.blocks_to_crawl.popleft()
        self.crawled_urls.add(url.get_url())
        return url

    def has_been_crawled(self, url):
        return url in self.crawled_urls

    def _get_domain_block(self, parsed_url):
        for block in self.blocks_to_crawl:
            if block.base == parsed_url.get_base():
                return block
        return None

    def _ensure_domain_block(self, parsed_url):
        block = self._get_domain_block(parsed_url)
        if block is None:
            block = DomainBlock(parsed_url)
            self.blocks_to_crawl.append(block)
        return block
