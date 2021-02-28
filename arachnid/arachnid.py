"""
TODO Pass over all docstrings and update them.
"""
import mimetypes
from arachnid.config import generate_config
from arachnid.crawler.crawler import Crawler
from arachnid.timewidgets import Timer
from arachnid.arachnid_arg_parser import arachnid_cl_parser

from arachnid import url_functions
from arachnid import documentparser
from arachnid import warning_issuer
from arachnid.scraper import Scraper

HTML_DOCUMENT_TYPE = "html"
UNKOWN_DOCUMENT_TYPE = "unkown"

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
        self.config = generate_config(ns) 
        self.crawler = Crawler(seed=self.config.seed, configuration=self.config)
        self.pages_crawled = 0
        self.page_limit = ns.page_limit if ns.page_limit >= 0 else None
        self.time_limit = ns.time_limit if ns.time_limit >= 0 else None
        self.time_limit_timer = Timer()

    def start(self):
        self.time_limit_timer.start()
        while not self.is_done():
            pageinfo = self.get_next_pageinfo()

    def get_next_pageinfo(self):
        """ Pulls next page and scrapes its data. Returns a dictionary with applicable data. """
        c_url, response = self.crawler.crawl_next()
        self.pages_crawled += 1
        if "content-type" in response.headers.keys():  # TODO What happens if there is no response type??
            if "text/html" in response.headers["content-type"]:
                return self._parse_page(response, c_url)
            else:
                return self._parse_document(response, c_url)

    def is_done(self):
        return self.above_time_limit() or self.above_page_limit() or not self.crawler.has_next_page()

    def _parse_page(self, response, crawler_url):
        scraper = Scraper(response.text, "html.parser")
        pageinfo = PageInfo()
        pageinfo.type = HTML_DOCUMENT_TYPE
        backup_title = crawler_url.get_url_parts().path.split("/")[-1]
        pageinfo.link = crawler_url.get_url()
        pageinfo.netloc = crawler_url.get_netloc()
        pageinfo.title = scraper.title.string if scraper.title and scraper.title.string else backup_title 
        pageinfo.on_fuzz_list = crawler_url.is_fuzzed()
        pageinfo.on_robots_txt = crawler_url.in_robots()
        pageinfo.status_code = response.status_code
        if self.config.scrape_email:
            pageinfo.emails = scraper.find_all_emails() 
        if self.config.scrape_phone_number:
            pageinfo.phone_numbers = scraper.find_all_phones()
        if self.config.scrape_social_media:
            pageinfo.social_handles = scraper.find_all_social()
        if self.config.custom_regex:
            pageinfo.regex_patterns = scraper.find_all_regex()
        if self.config.custom_str:
            pageinfo.string_occurrences = scraper.string_occurances(self.config.custom_str, self.config.custom_str_case_sensitive) 

        found_urls = []
        if self.config.scrape_links:
            for page in scraper.find_all_http_refs():
                page = page.strip().replace(" ", "%20")
                url = url_functions.join_url(crawler_url.get_url(), page)
                found_urls.append(url)
        self.crawler.report_found_urls(found_urls)

        return pageinfo 
    
    def _parse_document(self, response, crawler_url):
        """ 
            Parses the page and writes information to output directory.
            response is a requests.response containing the document.
            crawler_url is a CrawlerURL associated with the document.
        """
        pageinfo = PageInfo()
        pageinfo.link = crawler_url.get_url()
        pageinfo.netloc = crawler_url.get_netloc()
        pageinfo.on_fuzz_list = crawler_url.is_fuzzed()
        pageinfo.on_robots_txt = crawler_url.in_robots()
        pageinfo.status_code = response.status_code
        possible_file_types = [t.lstrip(".") for t in mimetypes.guess_all_extensions(response.headers["content-type"])]
        if len(possible_file_types) != 0:
            flagged_types = list( set(self.config.flagged_document_types) & set(possible_file_types) )
            if len(flagged_types) != 0:
                pageinfo.type = flagged_types[0]
            else:
                pageinfo.type = possible_file_types[0]
        else:
            pageinfo.type = UNKOWN_DOCUMENT_TYPE
        try:
            cd = response.headers["content-disposition"]
            file_name_start_index = cd.find("filename") + 10  # Get index after filename="
            file_name_end_index = cd.find("\"", file_name_start_index)
            file_name = cd[file_name_start_index : file_name_end_index]
        except KeyError:  # Responses don't have to contain "content-disposition"
            path = crawler_url.get_url_parts().path
            file_name = path.split("/")[-1]
        pageinfo.title = file_name
        self.schedule.report_found_urls([])
        return pageinfo

    def _get_any_matching_element(a, b):
        """ Given list a and list b, returns any element that exists within both of them. """
        for x in a:
            for y in b:
                if x == y:
                    return x
        return None

    def above_time_limit(self):
        return self.time_limit_timer.elapsed() >= self.time_limit * 60 if self.time_limit else False

    def above_page_limit(self):
        return self.pages_crawled >= self.page_limit if self.page_limit else False

class PageInfo:
    def __init__(self):
        self.netloc = None
        self.link = None
        self.title = None
        self.file_type = None  # String. Could be "html", "jpg", "pdf", etc.
        self.status_code = None
        self.on_fuzz_list = None
        self.on_robots_txt = None
        self.emails = None
        self.phone_numbers = None
        self.social_handles = None
        self.regex_patterns = None
        self.string_occurrences = None
