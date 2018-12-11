import urllib.request as request
from bs4 import BeautifulSoup as bs
from io import TextIOWrapper
import re
from enum import Enum
from collections import deque

class Amount(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Crawler_Config:
    def __init__(self):
        self.set_default()

    def set_default_options(self):
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.scrape_street_address = True
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.find_custom_str_occurances = False # TODO Does this need to be here? Or does custom_str do the trick?
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.NONE
        self.fuzz_level = Amount.LOW

    def set_stealth_options(self):
        self.scrape_links = True
        self.scrape_subdomains = False
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.scrape_street_address = True
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.find_custom_str_occurances = False # TODO Does this need to be here? Or does custom_str do the trick?
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.HIGH
        self.fuzz_level = Amount.NONE

    def set_aggressive_options(self):
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.scrape_street_address = True
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.find_custom_str_occurances = False # TODO Does this need to be here? Or does custom_str do the trick?
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.none 
        self.fuzz_level = Amount.HIGH

class URL:
    def __init__(self, url):
        # TODO Test if it's a valid url
        self.url = url

    def scheme(self):
        return self.url.split('/')[0][:-1]

    def domain(self):
        return self.url.split('/')[2].split(':')[0]

    def subdomain(self):
        return self.url.split('/')[2].split('.')[0] 

    def port(self):
        parts = self.url.split(':')
        if len(parts) < 3:
            return -1
        else:
            return int(parts[2].split('/')[0])

    def path(self):
        path_start_index = self._find_nth(self.url, '/', 3)
        fragment_start_index = self.url.find('#')
        query_start_index = self.url.find('?')

        if (fragment_start_index == -1 and query_start_index == -1):
            return self.url[path_start_index:]
        elif (fragment_start_index < query_start_index):
            return self.url[path_start_index:fragment_start_index]
        else:
            return self.url[path_start_index:query_start_index]

    def query(self):
        raw_query = self.url.split('?')[1].split('#')[0]
        pairs = raw_query.split('&')
        query_data = {}
        for pair in pairs:
            key, value = pair.split('=')
            query_data[key] = value
        return query_data

    def fragment(self):
        return self.url.split('#')[1]

    def homepage(self):
        path_start_index = self._find_nth(self.url, '/', 3)
        if path_start_index != -1:
            return self.url[:path_start_index]
        else:
            return self.url

    @staticmethod
    def _find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start + len(needle))
            n -= 1
        return start

class Crawler:
    def __init__(self):
        self.config = Crawler_Config

    def crawl(seed_url):
        seed = URL(seed_url)
        paths_to_crawl = deque 
        crawled_paths = deque

        # Download page, parse it, 
        while (stack):
            url = base + stack.pop()
            page_data = download(url)
         

    #TODO Wrap in try-catch
    def download(url):
        req = request.Request(url, headers=None) #TODO headers should be what the class information we gathered
        open_page = request.urlopen(req)
        page = TextIOWrapper(open_page, encoding="utf-8")
        page_data = page.read()
        return bs(page_data, "html.parser") # html.parser might be replaced with lxml

    def generate_fuzz_list():
        pass
