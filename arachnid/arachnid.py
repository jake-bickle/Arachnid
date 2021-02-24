import os
from arachnid.crawler import crawler
from arachnid.timewidgets import Timer
from arachnid.arachnid_arg_parser import arachnid_cl_parser

from arachnid import url_functions
from arachnid import responseparser
from arachnid import warning_issuer
from arachnid.scraper import Scraper
from arachnid.crawler import url_functions
from arachnid.crawler import responseparser
from arachnid.crawler import warning_issuer
from arachnid.crawler.scraper import Scraper

__version__ = "0.9.5.1"

class Arachnid:
    def __init__(self, cli_args=None):
        """ cli_args is a list of command line arguments. If left empty, Arachnid will read sys.argv instead
        EX. args = ["https://www.example.com", "--stealth", "--time-limit", "5"]
        """
        if cli_args:
            ns = arachnid_cl_parser.parse_args(cli_args)
        else:
            ns = arachnid_cl_parser.parse_args()
        self.crawler = crawler.get_crawler_from_namespace(ns)
        self.pages_crawled = 0
        self.page_limit = ns.page_limit if ns.page_limit >= 0 else None
        self.time_limit = ns.time_limit if ns.time_limit >= 0 else None
        self.time_limit_timer = Timer()
        self.output_file = os.path.join(ns.output, "arachnid_results.json")

    def start(self):
        self.time_limit_timer.start()
        while not self.is_done() :
            c_url, response = self.crawler.crawl_next()
            self.pages_crawled += 1
            if "content-type" in response.headers.keys():  # TODO What happens if there is no response type??
                if "text/html" in response.headers["content-type"]:
                    self._parse_page(r, c_url)
                else:
                    self._parse_document(r, c_url)

        self.close()

    def is_done(self):
        return self.above_time_limit() or self.above_page_limit() or not self.crawler.has_next_page()

    def _parse_page(self, crawler_url, response):
        """ 
            Parses the page and writes information to output directory.
            crawler_url is a CrawlerURL associated with the page.
            response is a requests.response containing the page.
        """
        scraper = Scraper(response.text, "html.parser")
        if self.config.scrape_email:
            for email in scraper.find_all_emails():
                self.output.add_email(email)
        if self.config.scrape_phone_number:
            for number in scraper.find_all_phones():
                self.output.add_phone(number)
        if self.config.scrape_social_media:
            for social in scraper.find_all_social():
                self.output.add_social(social)
        if self.config.custom_regex:
            for regex in scraper.find_all_regex(self.config.custom_regex):
                self.output.add_custom_regex(regex)
        found_urls = []
        if self.config.scrape_links:
            for page in scraper.find_all_http_refs():
                page = page.strip().replace(" ", "%20")
                url = url_functions.join_url(crawler_url.get_url(), page)
                found_urls.append(url)
        self.schedule.report_found_urls(found_urls)

        backup_title = crawler_url.get_url_parts().path.split("/")[-1]
        page_info = {"path": crawler_url.get_extension(),
                     "title": scraper.title.string if scraper.title and scraper.title.string else backup_title,
                     "custom_string_occurances": scraper.string_occurances(self.config.custom_str, self.config.custom_str_case_sensitive) if self.config.custom_str else None,
                     "on_fuzz_list": crawler_url.is_fuzzed(),
                     "on_robots": crawler_url.in_robots(),
                     "code": response.status_code}
        self.output.add_page(crawler_url.get_netloc(), page_info)

    
    def _parse_document(self, crawler_url, response):
        """ 
            Parses the page and writes information to output directory.
            crawler_url is a CrawlerURL associated with the document.
            response is a requests.response containing the document.
        """
        parser = responseparser.DocumentResponse(response, self.config.documents)
        data = parser.extract()
        self.schedule.report_found_urls([])
        if data:
            data["path"] = crawler_url.get_url_parts().path
            self.output.add_document(crawler_url.get_netloc(), data)

    def close(self):
        input("Crawl complete. Press ENTER to exit.")

    def above_time_limit(self):
        return self.time_limit_timer.elapsed() >= self.time_limit * 60 if self.time_limit else False

    def above_page_limit(self):
        return self.pages_crawled >= self.page_limit if self.page_limit else False

    @staticmethod
    def clear_file(file_loc):
        with open(file_loc, 'w') as f:
            f.write("")
