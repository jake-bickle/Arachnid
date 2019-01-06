import requests
import responseparser
import random
import urlparser
import timewidgets
import json
import crawler_enums

from scheduler import Scheduler
from scraper import Scraper

import pdb

class CrawlerConfig:
    def __init__(self):
        self.set_default()

    def set_default(self):
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.documents = {"doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "odp", "pdf", "txt",
                          "zip", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg"}
        self.obey_robots = True
        self.agent = crawler_enums.Agent.FIREFOX.value
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.delay = crawler_enums.Delay.NONE.value
        self.fuzz_level = crawler_enums.Amount.LOW

    def set_stealth(self):
        self.obey_robots = True
        self.agent = crawler_enums.Agent.GOOGLE.value
        self.delay = crawler_enums.Delay.HIGH.value
        self.fuzz_level = crawler_enums.Amount.NONE

    def set_aggressive(self):
        self.obey_robots = False 
        self.delay = crawler_enums.Delay.NONE.value
        self.fuzz_level = crawler_enums.Amount.HIGH
    
    def set_layout_only(self):
        self.scrape_subdomains = False
        self.scrape_phone_number = False 
        self.scrape_email = False
        self.scrape_social_media = False
        self.documents = {}
        self.custom_str = None
        self.custom_regex = None

# TODO: Fix: New subdomains won't have fuzz or robots added 
class Crawler:
    def __init__(self, seed, config=CrawlerConfig()):
        self.config = config
        self.seed = seed
        self.output = list()

    def crawl(self):
        self.schedule = Scheduler(self.seed)
        timer = timewidgets.Timer()
        timer.start()
        next_url = self.schedule.next_url()
        while (next_url):
            sw = timewidgets.Stopwatch(random.choice(self.config.delay))
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
            parser = responseparser.HTMLResponse(r, self.config)
            data = parser.extract()
            data["path"] = p_url.get_extension()
            for href in Scraper(r.text, "html.parser").find_all_hrefs():
                self.schedule.schedule_url(urlparser.join_url(url, href, allow_fragments=True))
            netloc_data["pages"].append(data)
        else:
            parser = responseparser.DocumentResponse(r, self.config.documents)
            data = parser.extract()
            if data:
                data["path"] = p_url.get_extension()
                netloc_data["documents"].append(data)

    def _get_netloc_from_output(self, netloc):
        for dictionary in self.output:
            if dictionary["netloc"] == netloc:
                return dictionary
        return None

    def output_to_file(self, filename):
        with open(filename, "w") as f:
            data = json.dumps(self.output, indent=4)
            f.write(data)
            
