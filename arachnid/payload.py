import os
import csv
import json
from datetime import datetime

from arachnid.crawler.crawler_url import CrawlerURL

class Payload:
    """ Consumes PageInfo objects and outputs content into a directory with various files. """
    def __init__(self, config):
        self.config = config
        self.output_directory_name = None
        self.direct_links = set()
        self.emails = set()
        self.phones = set()
        self.social_handles = set()
        self.regex_patterns = set()
        self.string_occurrence_direct_links = set()
        self.start_time = None
        self.end_time = None

    def make_output_directory(self):
        if self.output_directory_name is None:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            url_parts = CrawlerURL(self.config.seed).get_url_parts()
            directory_base_name = f"{url_parts.domain}.{url_parts.suffix}_{timestamp}"
            self.output_directory_name = make_unique_directory(directory_base_name)

    def consume_pageinfo(self, pageinfo):
        self.make_output_directory()
        cwd = os.getcwd()
        os.chdir(self.output_directory_name)
        self._update_payload_directory(pageinfo)
        self._update_emails(pageinfo)
        self._update_phones(pageinfo)
        self._update_social_handles(pageinfo)
        self._update_regex_patterns(pageinfo)
        os.chdir(cwd)
    
    def _update_payload_directory(self, pageinfo):
        self._update_link_related_data(pageinfo)

    def _update_link_related_data(self, pageinfo):
        """
        Updates the following files:
            sitemap.csv
            flagged_documents.csv
            pages_of_interest.txt
        """
        if pageinfo.link in self.direct_links:
            return
        self.direct_links.add(pageinfo.link)
        with AppendCSV("sitemap.csv", ["link", "title", "netloc", "status_code", "on_fuzz_list", "on_robots", "type"]) as csv_file:
            row = [pageinfo.link, pageinfo.title, pageinfo.netloc, pageinfo.status_code, pageinfo.on_fuzz_list, pageinfo.on_robots_txt, pageinfo.type]
            csv_file.writerow(row)
        if pageinfo.on_fuzz_list or pageinfo.on_robots_txt or pageinfo.status_code:
            with open("pages_of_interest.txt", 'a') as f:
                f.write(pageinfo.link + "\n")
        if pageinfo.type in self.config.flagged_document_types:
            with AppendCSV("flagged_documents.csv", ["link", "title", "netloc", "status_code", "on_fuzz_list", "on_robots", "type"]) as csv_file:
                row = [pageinfo.link, pageinfo.title, pageinfo.netloc, pageinfo.status_code, pageinfo.on_fuzz_list, pageinfo.on_robots_txt, pageinfo.type]
                csv_file.writerow(row)
        if pageinfo.string_occurrences is not pageinfo.NOT_APPLICABLE and pageinfo.string_occurrences > 0:
            with open("string_occurrences.txt", 'a') as f:
                f.write(pageinfo.link + "\n")
    
    def _update_emails(self, pageinfo):
        if pageinfo.emails is not pageinfo.NOT_APPLICABLE:
            for email in pageinfo.emails:
                if email not in self.emails:
                    self.emails.add(email)
                    with open("emails.txt", 'a') as f:
                        f.write(email + '\n')

    def _update_phones(self, pageinfo):
        if pageinfo.phone_numbers is not pageinfo.NOT_APPLICABLE:
            for phone in pageinfo.phone_numbers:
                if phone not in self.phones:
                    self.phones.add(phone)
                    with open("phones.txt", 'a') as f:
                        f.write(phone + '\n')
    
    def _update_social_handles(self, pageinfo):
        if pageinfo.social_handles is not pageinfo.NOT_APPLICABLE:
            for social_handle in pageinfo.social_handles:
                if social_handle not in self.social_handles:
                    self.social_handles.add(social_handle)
                    with open("social_handles.txt", 'a') as f:
                        f.write(social_handle + '\n')

    def _update_regex_patterns(self, pageinfo):
        if pageinfo.regex_patterns is not pageinfo.NOT_APPLICABLE:
            for regex_pattern in pageinfo.regex_patterns:
                if regex_pattern not in self.regex_patterns:
                    self.regex_patterns.add(regex_pattern)
                    with open("regex_patterns.txt", 'a') as f:
                        f.write(regex_pattern + '\n')

    def summarize(self):
        cwd = os.getcwd()
        os.chdir(self.output_directory_name)
        summary = {
            "Start time": self.start_time.strftime("%Y/%m/%d %H:%M:%S"),
            "End time": self.end_time.strftime("%Y/%m/%d %H:%M:%S"),
            "Total time (In seconds)": (self.end_time - self.start_time).total_seconds()
        }
        with open("summary.json", 'w') as f:
            json.dump(summary, f, indent=4)
        os.chdir(cwd)


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

    def __exit__(self, exc_type, exc_value, traceback):
        self._opened_file.close()
        self._opened_file = None
    
    def ensure_file_exists(self):
        if not os.path.exists(self.file_name):
            header = ",".join(self.columns) + '\n'
            with open(self.file_name, 'w') as f:
                f.write(header)


def make_unique_directory(directory_name):
    """ 
    Creates a directory, adding an appropriate number extension if needed to make it unique. Returns directory name.
    EG. If "my_cool_directory" already exists, this will make "my_cool_directory (1)"
    """
    index = 0
    new_directory_name = directory_name
    while True:
        try:
            os.mkdir(new_directory_name)
            return new_directory_name
        except FileExistsError:
            index += 1
            new_directory_name = f"{directory_name} ({index})"
