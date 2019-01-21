import re
import urlparser
from bs4 import BeautifulSoup

class RegexPatterns:
    LINK = re.compile(r"http[s]?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.\w{2,5}[0-9a-zA-Z$/\-_.+!*'()]*")
    EMAIL = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    # TODO This does NOT include German phone numbers. Possible fix in future patch
    PHONE = re.compile(r"[+]?[0-9]{0,3}[-\s]?[(]?[0-9]{3}[\s.)-]*?[0-9]{3}[\s.-]*?[0-9]{4}")

class Scraper(BeautifulSoup):
    def find_all_hrefs(self):
        anchors = self.find_all("a")
        hrefs = []
        for a in anchors:
            try:
                hrefs.append(a["href"])
            except:
                pass  # Ignore anchors without href
        return hrefs

    def find_all_emails(self):
        string_emails = [email for email in self.find_all(string=RegexPatterns.EMAIL)]
        href_emails = [email.get("href") for email in self.find_all(href=re.compile(r"mailto:"))]
        sanitised_emails = []
        for email in string_emails:
            emails = re.findall(RegexPatterns.EMAIL, email)
            for email in emails:
                sanitised_emails.append(email)
        for email in href_emails:
            sanitised_emails.append(email[7:])  # Strip away "mailto:"
        return sanitised_emails

    def find_all_phones(self):
        string_phones = [phone for phone in self.find_all(string=RegexPatterns.PHONE)]
        href_phones = [anchor.get("href") for anchor in self.find_all(href=re.compile(r"tel:"))]
        sanitised_phones = []
        for phone in string_phones:
            phones = re.findall(RegexPatterns.PHONE, phone)
            for phone in phones:
                sanitised_phones.append(phone.strip())
        for phone in href_phones:
            sanitised_phones.append(phone[4:])
        return sanitised_phones

    def find_all_social(self):
        found_social = list()
        html_doc = str(self)
        links = RegexPatterns.LINK.findall(html_doc) 
        if links is not None:
            for link in links:
                if urlparser.is_social_media_profile(link):
                    media = {"link": link, "domain": urlparser.parse_url(link).domain}
                    found_social.append(media)
        return found_social

    def find_all_regex(self, pattern=""):
        regex = re.compile(pattern)
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

