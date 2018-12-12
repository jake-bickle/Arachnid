import urllib.request as request
import urllib.parse as urlparser
from objdict import ObjDict
from bs4 import BeautifulSoup as bs
from io import TextIOWrapper
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
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.NONE
        self.fuzz_level = Amount.LOW

    def set_stealth(self):
        self.scrape_links = True
        self.scrape_subdomains = False
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.HIGH
        self.fuzz_level = Amount.NONE

    def set_aggressive(self):
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.scrape_common_documents = True
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_doc = None
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.none 
        self.fuzz_level = Amount.HIGH

class netloc:
    def __init__(self, name, path = list()):
        self.name = name
        self.inaccesable_paths = 0
        self.path = path

class Crawler:
    def __init__(self):
        self.config = Crawler_Config
        self.output = list()

    def crawl(self, seed_url):
        seed = urlparser.urlparse(seed_url)
        paths_to_crawl = deque(seed.path)
        crawled_paths = deque

        # Create netloc object and place into output
            current_netloc = netloc(seed.netloc)
            current_netloc_index = 0
            self.output.append(current_netloc)

        # Download page, parse it, add to output, move onto next path
        while (paths_to_crawl):
            path = paths_to_crawl.pop()
            url = urlparser.join(seed_url, path)
            page_contents = download(url)
            page_data = list()
            page_data.name = path

            # Grab links and add to paths_to_crawl
            if (config.scrape_links):
                hrefs = self.scrape_href(page_contents)
                paths_to_crawl.append(href for href in hrefs)

            # Grab phone_numbers and add to output
            if (config.scrape_email):
                emails = scrape_email(page_contents)
                #TODO This index number must be changed according to the current netloc
                page_data.email = list(email for email in emails)

            output[0].path = page_data
                

         

    #TODO Wrap in try-catch
    def download(self, url):
        req = request.Request(url, headers=None) #TODO headers should be what the class information we gathered
        open_page = request.urlopen(req)
        page = TextIOWrapper(open_page, encoding="utf-8")
        page_data = page.read()
        return bs(page_data, "html.parser") # html.parser might be replaced with lxml

    def scrape_href(self, page_contents):
        anchors = page_data.findAll('a')
        return list(anchor.get('href') for anchor in anchors)

    def scrape_email(self, page_contents):
        pass

    def generate_fuzz_list():
        pass
