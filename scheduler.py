from urlparser import UrlParser
from collections import deque

class DomainBlock:
    """ Holds a stack of paths to be crawled for an arbitrary net location """
    def __init__(self, parsed_url):
        self.parsed_url = parsed_url
        self.paths_to_crawl = deque()  # To be used as a stack
        if not self.parsed_url.path:
            self.paths_to_crawl.append("/")
        else:
            self.paths_to_crawl.append(parsed_url.path)

    def add_path(self, path):
        if self.path_already_added(path):
            return False
        self.paths_to_crawl.append(path)
        return True

    def next_url(self):
        try:
            path = self.paths_to_crawl.pop()
        except(IndexError):
            return None
        url = UrlParser.join_url(self.parsed_url.get_url(), path)
        return url

    def path_already_added(self, path):
        return path in self.paths_to_crawl

class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """
    def __init__(self, url=""):
        self.blocks_to_crawl = deque()  # To be used as a queue
        self.crawled_urls = set()
        self.seed_url = UrlParser.parse_url(url)
        self.schedule_url(url)

    def schedule_url(self, url=""):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
        """
        parsed_url = UrlParser.parse_url(url)
        if self.url_has_been_crawled(url):
            return False
        if not UrlParser.same_domain(parsed_url, self.seed_url):
            return False
        block = self._get_domain_block(parsed_url)
        if block is None:
            block = DomainBlock(parsed_url)
            self.blocks_to_crawl.append(block)
            return True
        else:
            return block.add_path(parsed_url.path)

    def next_url(self):
        if not self.blocks_to_crawl: 
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        url = block_to_crawl.next_url()
        if not block_to_crawl.paths_to_crawl:
            self.blocks_to_crawl.popleft()
        self.crawled_urls.add(url)
        return url

    def url_has_been_crawled(self, url):
        return url in self.crawled_urls

    def _get_domain_block(self, url):
        for block in self.blocks_to_crawl:
            if block.parsed_url.subdomain == url.subdomain:
                return block
        return None

