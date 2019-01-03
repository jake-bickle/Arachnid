import requests
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
        self.scheduler = Scheduler(self.seed)
        sw = timewidgets.Stopwatch(0) # TODO: make work with enum self.config.crawler_delay
        timer = timewidgets.Timer()
        timer.start()
        next_url = self.scheduler.next_url()
        while (next_url):
            sw.start()
            if timer.elapsed() > 5:
                self.output_to_file("arachnid_data.json")
                timer.restart()
            self.crawl_page(next_url)
            next_url = self.scheduler.next_url()
            sw.wait()  # Delay the crawler to throw off automated systems
        self._write_to_file("arachnid_data.json")

    def crawl_page(self, url):
        print(url)
        p_url = urlparser.parse_url(url)
        netloc_output = self._get_netloc_from_output(p_url.get_netloc())
        if netloc_output is None:
            netloc_output = dict()
            netloc_output["netloc"] = p_url.get_netloc()
            netloc_output["pages"] = list()
            netloc_output["documents"] = list()
            self.output.append(netloc_output)
        request = requests.get(url, headers={"User-Agent": self.config.agent}) 
        if "text/html" not in request.headers["content-type"]:
            pass
            # doc_output = dict()
            # doc_output["path"] = p_url.path
            # cd = request.headers["content-disposition"]
            # f_s = cd.find("filename")+10
            # f_e = cd.find("\"", filename_s)
            # doc_output["name"] = cd[f_s:f_e]  # filename must be parsed from content-disposition
            # doc_output["type"] = request.headers["content-type"]
            # netloc_output["documents"].append(doc_output)
        else:
            page_data = Scraper(request.text, "html.parser")  #TODO May change to different parser
            anchors = page_data.find_all("a")
            for a in anchors:
                try:
                    new_url = urlparser.join_url(url, a["href"])
                    self.scheduler.schedule_url(new_url)
                except AttributeError:
                    pass  # If the anchor has no href, move on
            page_dict = self._extract_page_data(page_data)
            page_dict["path"] = p_url.path
            netloc_output["pages"].append(page_dict)

    def _get_netloc_from_output(self, netloc):
        for dictionary in self.output:
            if dictionary["netloc"] == netloc:
                return dictionary
        return None

    def output_to_file(self,  filename):
        with open(filename, "w") as f:
            data = json.dumps(self.output, indent=4)
            f.write(data)
            
    def _extract_page_data(self, page_contents):
        page_data = dict()
        if (self.config.scrape_email):
            page_data["email"] = page_contents.find_all_emails()
        if (self.config.scrape_phone_number):
            page_data["phone"] = page_contents.find_all_phones()
        if (self.config.scrape_social_media):
            page_data["social"] = page_contents.find_all_social()
        if (self.config.custom_str):
            if self.config.custom_str_case_sensitive:
                page_data["custom_string_occurances"] = page_contents.string_occurances(self.config.custom_str, case_sensitive=True)
            else:
                page_data["custom_string_occurances"] = page_contents.string_occurances(self.config.custom_str, case_sensitive=False)
        if (self.config.custom_regex):
            page_data["custom_regex"] = page_contents.find_all_regex(self.config.custom_regex)
        return page_data

