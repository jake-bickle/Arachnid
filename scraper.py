import re
import urlparser
from bs4 import BeautifulSoup

import pdb

class Social:
    def __init__(self,link=""):
        self.link = link
        self.site = urlparser.parse_url(link).domain

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
    LINK = re.compile(r"http[s]?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.\w{2,5}[0-9a-zA-Z$/\-_.+!*'()]*")
    EMAIL = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    # TODO This does NOT include German phone numbers. Possible fix in future patch
    PHONE = re.compile(r"[+]?[0-9]{0,3}[-\s]?[(]?[0-9]{3}[\s.)-]*?[0-9]{3}[\s.-]*?[0-9]{4}")

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
        string_phones = [phone for phone in self.find_all(string=self.PHONE)]
        href_phones = [anchor.get("href") for anchor in self.find_all(href=re.compile(r"tel:"))]
        sanitised_phones = []
        for phone in string_phones:
            phones = re.findall(self.PHONE, phone)
            for phone in phones:
                sanitised_phones.append(phone.strip())
        for phone in href_phones:
            sanitised_phones.append(phone[4:])
        return sanitised_phones

    def find_all_social(self):
        found_social = list()
        html_doc = str(self)
        links = self.LINK.findall(html_doc) 
        if links is not None:
            for link in links:
                if urlparser.is_social_media_profile(link):
                    found_social.append(Social(link))
        return found_social

    def find_all_regex(self, string=""):
        regex = re.compile(string)
        sanitized_strings = []
        strings_with_patterns = [string for string in self.find_all(string=re.compile(regex))]
        for string in strings_with_patterns:
            found_patterns = re.findall(regex, string)
            for pattern in found_patterns:
                sanitized_strings.append(pattern)
        return sanitized_strings

    def string_occurances(self, string="", case_sensitive=False):
        if (case_sensitive):
            return len([tag for tag in self.find_all(string=re.compile(string))])
        else:
            return len([tag for tag in self.find_all(string=re.compile(string, re.IGNORECASE))])

