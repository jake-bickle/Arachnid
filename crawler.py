import requests
import timewidgets
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

class CrawlerConfig:
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

# TODO: Fix: New subdomains won't have fuzz or robots added 
class Crawler:
    def __init__(self, seed="https://www.calcharter.com", config=CrawlerConfig()):
        self.config = config
        self.output = list()

    # def crawl_next(self):
        # url_to_crawl = schedular.next_url()
        # request = requests.get(url_to_crawl, headers={})
        # page_data = Scraper(request.text, "html.parser")

    def crawl(seed):
        self.scheduler = Scheduluer(seed)
        sw = timewidgets.Stopwatch(self.config.crawler_delay)
        timer = timewidgets.Timer()
        timer.start()
        next_url = self.scheduler.next_url()
        while (next_url):
            sw.start()
            if timer.elapsed() > 30:
                timer.restart()
                # Overwrite json file
            self.crawl_page(next_url)
            next_url = self.scheduler.next_url()
            sw.wait()  # Delay the crawler to throw off automated systems
        # Overwrite output one last time


    def crawl_page(url):
        p_url = urlparser.parse_url(url)
        netloc_output = self._get_netloc_from_output(p_url.get_netloc())
        if netloc_output is None:
            netloc_output = dict()
            netloc_output["netloc"] = p_url.get_netloc()
            netloc_output["pages"] = list()
            netloc_output["documents"] = list()
            self.output.append(netloc_output)
        request = requests.get(url_to_crawl, headers={}) # TODO Adjust header info
        if "text/html" not in request.headers["content-type"]:
            doc_output = dict()
            doc_output["path"] = p_url.path
            cd = request.headers["content-disposition"]
            f_s = cd.find("filename")+10
            f_e = cd.find("\"", filename_s)
            doc_output["name"] = cd[f_s:f_e]  # filename must be parsed from content-disposition
            doc_output["type"] = request.headers["content-type"]
            netloc_output["documents"].append(doc_output)
        else:
            page_data = Scraper(r.text)
            netloc_output["pages"].append(self.extract_page_data(page_data))
            anchors = page_data.find_all("a")
            for a in anchors:
                if a.href:
                    url = urlparser.parse_url(a.href)

    def _write_output():
        with open("crawled_site.json", "w") as output:
            pass
            
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

