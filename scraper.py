import re
from bs4 import BeautifulSoup
import urllib.parse as urlparser

import pdb

class regex_patterns:
    URL = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    EMAIL = re.compile(r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.\s-]{1,64}@[a-zA-Z0-9-]+\.{1}[a-zA-Z0-9-]+$")

    # TODO This does NOT include German phone numbers. Possible fix in future patch
    PHONE = re.compile(r"^[+]?[0-9]{0,3}[-\s]?[(]?[0-9]{3}[\s.)-]*?[0-9]{3}[\s.-]*?[0-9]{4}$")
    COMMON_DOCUMENT = re.compile(r".+\.\w{3,4}?")
    COMMON_DOCUMENT_FORMATS = ("doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "ods", "odp", "pdf", "txt", "rtf", "zip", "7z", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg")
    SOCIAL = re.compile(r".+\.\w{2,5}")
    COMMON_SOCIAL = ["facebook", "twitter", "twitch", "pintrest", "github", "myspace", "plus.google", "instagram", "tumblr", "flickr", "deviantart"]

class Scraper(BeautifulSoup, regex_patterns):
    def find_all_paths(self):
        anchors = self.findAll('a')
        paths = list()
        for anchor in anchors:
            href = anchor.get("href")
            if (re.match(self.URL, href)):
                paths.append(urlparser.urlparse(href).path)
        return paths

    # TODO Doesn't work 
    def find_all_emails(self):
        # We want this search to find emails in mailtos and in plain text
        unsanitised_emails = list()
        def search(tag):
            if tag.has_attr("href"):
                return "mailto" in tag.get("href")
            elif tag.string is not None:
                return re.match(self.EMAIL_REGEX, tag.string)
        unsanitised_emails = self.find_all(search)
        return unsanitised_emails

    def find_all_phones(self):
        pass

    def find_all_documents(self, types=()):
        # Finds all documents of common type
        pass

    def find_all_regex(self, regex):
        pass

    def has_string_occurance(self, string, case_sensitive=False):
        pass

