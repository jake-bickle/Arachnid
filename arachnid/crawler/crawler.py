import requests
import random

from arachnid.timewidgets import Timer
from arachnid.crawler.config import CrawlerConfig, generate_crawler_config
from arachnid.crawler.scheduler import Scheduler, FuzzingOptions
from arachnid.crawler.domaindata import DomainData
from arachnid.crawler.crawler_url import CrawlerURL


class Crawler:
    """
    TODO Delete this comment
    Does the crawling.
    Returns a scraper object.
    """
    def __init__(self, seed, configuration=CrawlerConfig()):
        seed = CrawlerURL(seed)
        self.config = configuration
        self.headers = {"User-Agent": self.config.agent}
        fuzzing_options = FuzzingOptions(self.config.paths_list_file_loc if self.config.fuzz_paths else None,
                                         self.config.subs_list_file_loc if self.config.fuzz_subs else None)
        self.schedule = Scheduler(seed,
                                  useragent=self.config.agent,
                                  fuzzing_options=fuzzing_options,
                                  respect_robots=self.config.obey_robots,
                                  allow_subdomains=self.config.scrape_subdomains,
                                  blacklist_dirs=self.config.blacklisted_directories)
        self.output = DomainData(seed.get_netloc())
        self.output.start()
        self.output.add_config(self.config)
        self.delay_sw = Timer()
        self._update_crawl_delay()
        self.delay_sw.start()

    def crawl_next(self):
        """
        Crawls the next page in the scheduler. Returns a (CrawlerURL, requests.response) tuple.
        """
        c_url = self.schedule.next_url()
        if c_url is None:
            self.finish()
            return False
        print(c_url)
        self.delay_sw.wait()
        r = requests.get(c_url.get_url(), headers=self.headers, timeout=30)
        self._update_crawl_delay()
        self.delay_sw.start()
        return r

    def has_next_page(self):
        # TODO
        pass

    def report_found_urls(self, urls):
        """ Given a list of strings, report back a list of URLs to be crawled at a later time. """
        crawler_urls = [CrawlerURL(url, allow_query=self.config.allow_query) for url in urls]
        self.schedule.report_found_urls(crawler_urls)

    def _update_crawl_delay(self):
        default_delay = random.choice(self.config.default_delay)
        s_delay = self.schedule.get_crawl_delay()
        self.delay_sw = Timer(default_delay if default_delay > s_delay else s_delay)

    def dumps(self, **kwargs):
        return self.output.dumps(**kwargs)


def get_crawler_from_namespace(namespace):
    return Crawler(namespace.seed, configuration=generate_crawler_config(namespace))
