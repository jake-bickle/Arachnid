import requests
import responseparser
import random
import urlparser
import timewidgets
import crawler_enums

from scheduler import Scheduler
from scraper import Scraper
from domaindata import DomainData

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
        self.schedule = Scheduler(self.seed)
        p_seed = urlparser.parse_url(seed)
        self.output = DomainData(p_seed.get_netloc())

    def crawl(self):
        timer = timewidgets.Timer()
        timer.start()
        next_url = self.schedule.next_url()
        while (next_url):
            sw = timewidgets.Stopwatch(random.choice(self.config.delay))
            sw.start()
            if timer.elapsed() > 30:  
                self.output_to_file("arachnid_data.json")
                timer.restart()
            self._crawl_page(next_url)
            next_url = self.schedule.next_url()
            sw.wait()  # Delay the crawler to throw off automated systems
        self.output_to_file("arachnid_data.json")

    def _crawl_page(self, url):
        print(url)
        p_url = urlparser.parse_url(url)
        r = requests.get(url, headers={"User-Agent": self.config.agent})
        if "text/html" in r.headers["content-type"]:
            self._parse_page(r, p_url)
        else:
            self._parse_document(r, p_url)

    def _parse_page(self, response, parsed_url):
        scraper = Scraper(response.text, "html.parser")
        netloc = parsed_url.get_netloc()
        if self.config.scrape_email:
            for email in scraper.find_all_emails():
                self.output.add_email(netloc, email)
        if self.config.scrape_phone_number:
            for number in scraper.find_all_phones():
                self.output.add_phone(netloc, number)
        if self.config.scrape_social_media:
            for social in scraper.find_all_social():
                self.output.add_social(netloc, social)
        if self.config.custom_regex:
            for regex in scraper.find_all_regex(self.config.custom_regex):
                self.output.add_custom_regex(netloc, regex)

        for href in Scraper(response.text, "html.parser").find_all_hrefs():
            self.schedule.schedule_url(urlparser.join_url(parsed_url.get_url(), href, allow_fragments=True))
        page_info = {"path": parsed_url.get_extension(),
                     "title": scraper.title.string if scraper.title.string else parsed_url.path.split("/")[-1],
                     "custom_string_occurances": scraper.string_occurances(self.config.custom_str, self.config.custom_str_case_sensitive) if self.config.custom_str else None,
                     "code": response.status_code}
        self.output.add_page(parsed_url.get_netloc(), page_info)

    def _parse_document(self, response, parsed_url):
        parser = responseparser.DocumentResponse(response, self.config.documents)
        data = parser.extract()
        if data:
            data["path"] = parsed_url.path
            self.output.add_document(parsed_url.get_netloc(), data)

    def output_to_file(self, filename):
        with open(filename, "w") as f:
            data = self.output.dumps(indent=4)
            f.write(data)
            
