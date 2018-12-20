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
    EMAIL = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    # TODO This does NOT include German phone numbers. Possible fix in future patch
    PHONE = re.compile(r"^[+]?[0-9]{0,3}[-\s]?[(]?[0-9]{3}[\s.)-]*?[0-9]{3}[\s.-]*?[0-9]{4}$")
    COMMON_DOCUMENT = re.compile(r".+\.\w{3,4}?")
    COMMON_DOCUMENT_FORMATS = ("doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "ods", "odp", "pdf", "txt", "rtf", "zip", "7z", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg")
    SOCIAL = re.compile(r".+\.\w{2,5}")
    COMMON_SOCIAL = ["facebook", "twitter", "twitch", "pintrest", "github", "myspace", "plus.google", "instagram", "tumblr", "flickr", "deviantart"]

class Scraper(BeautifulSoup, regex_patterns):
    def find_all_emails(self):
        string_emails = [email for email in self.find_all(string=self.EMAIL)]
        href_emails = [email.get("href") for email in self.find_all(href=re.compile(r"mailto:"))]
        sanitised_emails = []
        for email in string_emails:
            emails = re.findall(self.EMAIL, email)
            for email in emails:
                sanitised_emails.append(email)
        for email in href_emails:
            sanitised_emails.append(email[7:])  # Strip away "mailto:"
        return sanitised_emails

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

