import os
import csv
from datetime import datetime

from arachnid.crawler.crawler_url import CrawlerURL

class Payload:
    """ Consumes PageInfo objects and outputs content into a directory with various files. """
    def __init__(self, config):
        self.config = config
        self.output_directory_name = None
        self.direct_links = {}
        self.emails = {}
        self.phones = {}
        self.social_handle_direct_links = {}
        self.regex_patterns = {}
        self.string_occurrence_direct_links = {}

    def make_output_directory(self):
        if self.output_directory_name is None:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            url_parts = CrawlerURL(self.config.seed).get_url_parts()
            directory_base_name = f"{url_parts.domain}.{url_parts.suffix}_{timestamp}"
            self.output_directory_name = make_unique_directory(directory_base_name)

    def consume_pageinfo(self, pageinfo):
        output_directory = self.make_output_directory()
        cwd = os.getcwd()
        os.chdir(output_directory)
        self._update_payload_directory(pageinfo)
        os.chdir(cwd)
    
    def _update_payload_directory(self, pageinfo):
        self._update_sitemap(pageinfo)
    
    def _update_sitemap(self, pageinfo):
        if pageinfo.link not in self.direct_links:
            self.direct_links.add(pageinfo.link)
            with AppendCSV("sitemaps.csv", ["netloc", "title", "direct_link", "status_code", "on_fuzz_list", "on_robots", "type"]) as csv_file:
                row = [pageinfo.netloc, pageinfo.title, pageinfo.link, pageinfo.status_code, pageinfo.on_fuzz_list, pageinfo.on_robots_txt, pageinfo.type]
                csv_file.writerow(row)
    
class AppendCSV:
    """
    csv.writer context manager, allowing easy creation and appending to CSV files. 
    """
    def __init__(self, file_name, columns):
        self.file_name = file_name
        self.columns = columns
        self._opened_file = None

    def __enter__(self):
        self.ensure_file_exists()
        self._opened_file = open(self.file_name, 'a') 
        return csv.writer(self._opened_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    def __exit__(self):
        self._opened_file.close()
        self._opened_file = None
    
    def ensure_file_exists(self):
        if not os.path.exists(self.file_name):
            header = ",".join(self.columns) + '\n'
            with open(self.file_name) as f:
                f.write(header)


def make_unique_directory(directory_name):
    """ 
    Creates a directory, adding an appropriate number extension if needed to make it unique. Returns directory name.
    EG. If "my_cool_directory" already exists, this will make "my_cool_directory (1)"
    """
    index = 1
    new_directory_name = directory_name
    while True:
        try:
            os.mkdir(directory_name)
            return new_directory_name
        except FileExistsError:
            index += 1
            new_directory_name = f"{directory_name} ({index})"
