import re
from bs4 import BeautifulSoup
import urllib.parse as urlparser     
import tldextract  # parse domain,subdomain information

import pdb

class Social:
    def __init__(self,link=""):
        self.link = link
        self.site = tldextract.extract(link).domain

    def __eq__(self, other):
        if isinstance(other, Social):
            return self.link == other.link
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Social):
            return self.link < other.link
        else:
            return NotImplemented

    def __str__(self):
        return self.link

    def __repr__(self):
        return "Social(link=\"" + self.link + "\" site=\"" + self.site + "\")"

    def __hash__(self):
        return hash(str(self))

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

    def find_all_social(self):
        pass

    def find_all_regex(self, regex):
        pass

    def string_occurances(self, string, case_sensitive=False):
        pass

