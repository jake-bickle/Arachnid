import requests
import requestparser
import urlparser
import timewidgets
import json

from scheduler import Scheduler
from scraper import Scraper
from enum import Enum

import pdb

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
        self.documents = {"doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "odp", "pdf", "txt",
                          "zip", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg"}
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
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
        self.documents = {"doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "odp", "pdf", "txt",
                          "zip", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg"}
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
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
        self.documents = {"doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "odp", "pdf", "txt",
                          "zip", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg"}
        self.scrape_robots = False
        self.agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.find_custom_regex_occurances = False # TODO Does this need to be here? Or does custom_regexdo the trick?
        self.crawler_delay = Amount.none 
        self.fuzz_level = Amount.HIGH

# TODO: Fix: New subdomains won't have fuzz or robots added 
class Crawler:
    def __init__(self, seed, config=CrawlerConfig()):
        self.config = config
        self.seed = seed
        self.output = list()

    def crawl(self):
        self.schedule = Scheduler(self.seed)
        sw = timewidgets.Stopwatch(0) # TODO: make work with enum self.config.crawler_delay
        timer = timewidgets.Timer()
        timer.start()
        next_url = self.schedule.next_url()
        while (next_url):
            sw.start()
            if timer.elapsed() > 30:  
                self.output_to_file("arachnid_data.json")
                timer.restart()
            self.crawl_page(next_url)
            next_url = self.schedule.next_url()
            sw.wait()  # Delay the crawler to throw off automated systems
        self.output_to_file("arachnid_data.json")

    def crawl_page(self, url):
        print(url)
        p_url = urlparser.parse_url(url)
        netloc_data = self._get_netloc_from_output(p_url.get_netloc())
        if netloc_data is None:
            netloc_data = dict()
            netloc_data["netloc"] = p_url.get_netloc()
            netloc_data["pages"] = list()
            netloc_data["documents"] = list()
            self.output.append(netloc_data)
        r = requests.get(url, headers={"User-Agent": self.config.agent}) 
        if "text/html" in r.headers["content-type"]:
            parser = requestparser.HTMLRequest(r, self.config)
            data = parser.extract()
            data["path"] = p_url.get_extension()
            for href in Scraper(r.text, "html.parser").find_all_hrefs():
                self.schedule.schedule_url(urlparser.join_url(url, href))
            netloc_data["pages"].append(data)
        else:
            parser = requestparser.DocumentRequest(r, self.config.documents)
            data = parser.extract()
            if data:
                data["path"] = p_url.get_extension()
                netloc_data["documents"].append(data)

    def _get_netloc_from_output(self, netloc):
        for dictionary in self.output:
            if dictionary["netloc"] == netloc:
                return dictionary
        return None

    def output_to_file(self,  filename):
        with open(filename, "w") as f:
            data = json.dumps(self.output, indent=4)
            f.write(data)
            
