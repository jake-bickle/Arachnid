import urlparser
from collections import deque


class DomainBlock:
    def __init__(self, url, starter_credits=100000):
        self.netloc = url.get_netloc()
        self.virtual_credits = 0
        self.history = {url: starter_credits}  # URL ParseResult with their associated credits

    def do_aopic(self, urls, crawled_url):
        credits = self.history[crawled_url]
        tax = credits / 10
        self.virtual_credits += tax
        print("Virtual credits at: " + str(self.virtual_credits))
        self.history[crawled_url] = 0
        if len(urls) > 0:
            per_page = (credits - tax) / len(urls)
            for url in urls:
                try:
                    self.history[url] += per_page
                except KeyError:
                    self.history[url] = per_page
        if self._greatest_url()[1] < self.virtual_credits:
            bonus = self.virtual_credits / len(self.history)
            self.virtual_credits = 0
            self.history = {key: value + bonus for key, value in self.history.items()}

    # TODO This will never return None when domain block is ready
    def next_url(self):
        # Debugging purposes
        greatest = self._greatest_url()
        print(greatest[0].get_url() + "\n   Credits: " + str(greatest[1]))
        # Done debugging
        return self._greatest_url()[0]

    def _greatest_url(self):
        greatest = ("", 0)
        for key, value in self.history.items():
            if value > greatest[1]:
                greatest = (key, value)
        if greatest[1] <= 0:
            return None
        return greatest


class Scheduler:
    """ Holds a queue of DomainBlocks for an arbitrary domain """

    def __init__(self, url=""):
        self.seed_url = urlparser.parse_url(url)
        self.blocks_to_crawl = deque([DomainBlock(self.seed_url)])  # To be used as a queue
        #self.filters = [URLDiffFilter.URLDiffFilter()]
        self.filters = []

    def schedule_urls(self, found_urls, crawled_url, allow_fragments=False):
        """ Schedule a URL to be crawled at a later time. A URL will not be scheduled if:
            - It is not a subdomain of the domain the Scheduler object has been created for
            - It has already been crawled
            - It has already been scheduled
            - It has not passed the URLDiffFilter
        """

        # TODO This only works with same_netloc, not subdomains
        cleaned_urls = [urlparser.parse_url(url, allow_fragments) for url in found_urls
                        if urlparser.same_netloc(url, self.seed_url.get_url())]
        block = self._ensure_domain_block(crawled_url)
        return block.do_aopic(cleaned_urls, crawled_url)

    def next_url(self):
        if not self.blocks_to_crawl: 
            return None
        block_to_crawl = self.blocks_to_crawl[0]
        url = block_to_crawl.next_url()
        if url is None:
            self.blocks_to_crawl.popleft()
        return url

    def _get_domain_block(self, parsed_url):
        for block in self.blocks_to_crawl:
            if block.netloc == parsed_url.get_netloc():
                return block
        return None

    def _ensure_domain_block(self, parsed_url):
        block = self._get_domain_block(parsed_url)
        if block is None:
            block = DomainBlock(parsed_url.get_url())
            self.blocks_to_crawl.append(block)
        return block
