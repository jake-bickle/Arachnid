from collections import deque

from . import urlparser


class DomainBlock:
    """ Holds a stack of extensions to be crawled for an arbitrary net location 
        An extension is the portion of the URL that occurs after the suffix

        https://www.example.com/path/to/location;key1=value1?key2=value2#content
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    def __init__(self, parsed_url):
        self.base = parsed_url.get_base()
        self.extensions_to_crawl = deque()  # To be used as a stack
        if parsed_url.get_extension():
            self.add_extension(parsed_url.get_extension())
        else:
            self.add_extension("/")

    def add_extension(self, ext):
        if self.extension_already_added(ext):
            return False
        self.extensions_to_crawl.append(ext)
        return True

    def next_url(self):
        try:
            ext = self.extensions_to_crawl.pop()
        except IndexError:
            return None
        url = urlparser.join_url(self.base, ext) 
        return url

    def extension_already_added(self, extension):
        return extension in self.extensions_to_crawl


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, parsed_url):
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed = parsed_url
        self.filters = []
        self.schedule_url(self.seed)

    def schedule_url(self, parsed_url):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
            - It has not passed any of other filters
        """
        if not urlparser.same_domain(parsed_url, self.seed) or self.has_been_crawled(parsed_url.get_url()):
            return False
        for filter in self.filters:
            if filter.is_filtered(parsed_url):
                return False
        block = self._ensure_domain_block(parsed_url)
        return block.add_extension(parsed_url.get_extension())

    def next_url(self):
        if not self.blocks_to_crawl: 
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        url = block_to_crawl.next_url()
        if not block_to_crawl.extensions_to_crawl:
            self.blocks_to_crawl.popleft()
        self.crawled_urls.add(url)
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