import urllib.request as request
from urlparser import UrlParser
from objdict import ObjDict
from scraper import Scraper
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

class Path_Scheduler:
    def __init__(self, base):
        self.paths_to_crawl = deque()
        self.crawled_paths = set() 
        self.base = base

    def add_path(self, path):
        if self.path_exists(path):
            return False
        self.paths_to_crawl.append(path)
        return True

    # Perhaps this could be a generator
    def next_path(self):
        try:
            path = self.paths_to_crawl.popleft()
        except(IndexError):
            return None
        self.crawled_paths.add(path)
        return path

    def path_exists(self, path):
        return path in self.crawled_paths or self.paths_to_crawl


class Crawler:
    def __init__(self, config = Crawler_Config()):
        self.config = config
        self.output = list()

    def crawl(self, seed_url):
        seed = urlparser.urlparse(seed_url)
        domains_to_crawl = deque(tldextract.extract(seed_url)) # Different combinations of subdomains and suffix that are picked up during the crawl
        crawled_domains = deque
        paths_to_crawl = deque(seed.path)
        crawled_paths = deque

        while (domains_to_crawl):
            current_domain = domains_to_crawl.pop()
            current_domain_address = seed.shcheme + current_domain
            domain_data = ObjDict()
            domain_data.netloc = current_domain
            domain_data.path = list()

            while (paths_to_crawl):
                path = paths_to_crawl.pop()
                url = urlparser.join(current_domain_address, path)
                # TODO Wrap in try-catch
                page_contents = self.download(url)
                if (config.scrape_links):
                    paths = page_contents.scrape_hrefs()
                    for paths in paths:
                        if path not in crawled_paths:
                            if not paths.startswith('/'):
                                path = urlparser.join(url.geturl(), path)
                            paths_to_crawl.append(path)
                page_data = scrape_page_data(page_contents)
                page_data.path = path
                page_data.accessible = True
                domain_data.path.append(page_data)
                crawled_paths.append(path)

            crawled_domains.append(current_domain)
            self.output.append(domain_data)

        return self.output
         

    def download(self, url):
        req = request.Request(url, headers=None) #TODO headers should be what the class information we gathered
        open_page = request.urlopen(req)
        page = TextIOWrapper(open_page, encoding="utf-8")
        page_data = page.read()
        return Scraper(page_data, "html.parser") # html.parser might be replaced with lxml

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

