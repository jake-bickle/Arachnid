import requests
from scheduler import Scheduler
from scraper import Scraper
from urlparser import UrlParser
from objdict import ObjDict
from enum import Enum

class Amount(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Crawler_Config:
    def __init__(self):
        self.set_default_options()

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

# I would like to do this, but ObjDict doesn't seem to work completely? dumps() suppress or exclude_nulls doesn't work
# class netloc(ObjDict):
    # __keys__ = "name path"
    # def __init__(self, name, path = list()):
        # self.name = name
        # self.path = path

class Crawler:
    def __init__(self, config = Crawler_Config()):
        self.config = config
        self.output = list()

    def crawl(self, seed_url="https://www.calcharter.com"):
        seed = UrlParser.parse_url(seed_url)
        # TODO: Fix: New subdomains won't have fuzz or robots added 
        scheduler = Scheduler(seed)

        url_to_crawl = schedular.next_url()
        while (url_to_crawl):
            request = requests.get(url_to_crawl, headers={})
            page_data = Scraper(request.text, "html.parser")
            
    def scrape_page(page_contents):
        page_data = ObjDict()
        page_data.name = path

        if (config.scrape_email):
            page_data.email = page_contents.find_all_emails(page_contents)
        if (config.scrape_subdomains):
            pass
        if (config.scrape_phone_number):
            page_data.phone = page_contents.find_all_phone_numbers(page_contents)
        if (config.scrape_social_media):
            page_data.social = page_contents.find_all_socials(page_contents)
        if (config.scrape_common_docs):
            if (config.custom_doc is None):
                page_data.document = page_contents.find_all_documents()
            else:
                pass
        if (config.custom_str is not None):
            #TODO config needs to gather custom_str
            if config.custom_str_case_sensitive:
                page_data.custom_string_occurance = page_contents.has_string_occurance("I NEED SOMETHING", case_sensitive=True)
            else:
                page_data.custom_string_occurance = page_contents.has_string_occurance("I NEED SOMETHING", case_sensitive=False)

        if (config.custom_regex is not None):
            pass


    def generate_fuzz_list():
        pass

