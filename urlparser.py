import tldextract  
import urllib.parse
from collections import namedtuple

import pdb

class ParseResult(namedtuple("ParseResult", ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"])):
    def get_url(self):
        url = self.get_base()
        url += self.path
        if self.params:
            url += ';' + self.params
        if self.query:
            url += '?' + self.query
        if self.fragment:
            url += '#' + self.fragment
        return url

    def get_base(self):
        url = ""
        if self.scheme:
            url += self.scheme + "://"
        url += self.subdomain
        if self.domain:
            if self.subdomain:
                url += '.' + self.domain
            else:
                url += domain
        if self.suffix:
            if self.subdomain or self.domain:
                url += '.' + self.suffix
            else:
                url += self.suffix
        return url

class UrlParser:
    """ Wrapper class that combines urllib.parse and tldextract. """
    def parse_url(url=""):
        u_rslt = urllib.parse.urlparse(url)
        e_rslt = tldextract.extract(u_rslt.netloc)
        return ParseResult(u_rslt.scheme, e_rslt.subdomain, e_rslt.domain, e_rslt.suffix, u_rslt.path, u_rslt.params, u_rslt.query, u_rslt.fragment)

    def join_url(base="", url ="", allow_fragments=True):
        return urllib.urljoin(url, other)

    def is_subdomain(url1="", url2=""):
        url1_netloc = tldextract.extract(url1) 
        url2_netloc = tldextract.extract(url2)
        # Does not return true if they are the same netloc
        return url1_netloc.domain == url2_netloc.domain and url1_netloc != url2_netloc

    def same_netloc(url1="", url2=""):
        url1_netloc = urllib.parse.urlparse(url1).netloc
        url2_netloc = urllib.parse.urlparse(url2).netloc
        return url1_netloc == url2_netloc 


# https://www.media.com/profile-page
class CommonProfileFormat:
    def __init__(self, domain=None):
        self.domain = domain

    def follows_pattern(self, parsed_url):
        dir_count = len([path for path in parsed_url.path.split("/") if path])
        return dir_count == 1

# https://www.media.com/sub-dir/profile-page
class OneDirDeepProfileFormat:
    def __init__(self, domain=None, prof_dirs=None):
        self.domain = domain
        self.prof_dirs = prof_dirs

    def follows_pattern(self, parsed_url):
        directories = [path for path in parsed_url.path.split("/") if path]
        return directories[0] in self.prof_dirs and len(directories) == 2

# https://profile-page.media.com/
class SubdomainProfileFormat:
    def __init__(self, domain=None, forbidden_subdomains=None):
        self.domain = domain
        self.forbidden_subdomains = forbidden_subdomains

    def follows_pattern(self, parsed_url):
        dir_count = len([path for path in parsed_url.path.split("/") if path])
        for forbidden in self.forbidden_subdomains:
            if parsed_url.subdomain == forbidden:
                return False
        return dir_count == 0

class Format:
    COMMON_PROFILE_FORMAT = (CommonProfileFormat("facebook"),
                             CommonProfileFormat("twitter"),
                             CommonProfileFormat("twitch"),
                             CommonProfileFormat("pintrest"),
                             CommonProfileFormat("github"),
                             CommonProfileFormat("myspace"),
                             CommonProfileFormat("instagram"),
                             CommonProfileFormat("deviantart"))
    SUBDOMAIN_PROFILE_FORMAT = (SubdomainProfileFormat("tumblr", forbidden_subdomains={'www'}),)
    ONE_DIR_DEEP_PROFILE_FORMAT = (OneDirDeepProfileFormat("flickr", prof_dirs={'photos'}),
                                   OneDirDeepProfileFormat("linkedin", prof_dirs={'in'}))
    SOCIAL_MEDIA = COMMON_PROFILE_FORMAT + SUBDOMAIN_PROFILE_FORMAT + ONE_DIR_DEEP_PROFILE_FORMAT


class SocialMediaParser():
    def is_profile(url=""):
        url = UrlParser.parse_url(url)
        for social_media_profile_format in Format.SOCIAL_MEDIA:
            if social_media_profile_format.domain == url.domain:
                return social_media_profile_format.follows_pattern(url)
        return False

