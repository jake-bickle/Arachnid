import tldextract  
import urllib.parse
from collections import namedtuple


_url_parts_nt = namedtuple("Url_parts", ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"])


class CrawlerURL:
    def __init__(self, url="", allow_fragments=True, is_fuzzed=False):
        if not allow_fragments:
            url = urllib.parse.urldefrag(url)[0]
        u_rslt = urllib.parse.urlparse(url)
        e_rslt = tldextract.extract(u_rslt.netloc)
        self.url_parts = _url_parts_nt(u_rslt.scheme, e_rslt.subdomain, e_rslt.domain, e_rslt.suffix, u_rslt.path,
                                      u_rslt.params, u_rslt.query, u_rslt.fragment)
        self.is_fuzzed = is_fuzzed

    def get_url(self, trim_parameters=False):
        url = self.get_base()
        if trim_parameters:
            url += self.url_parts.path
        else:
            url += self.get_extension()
        return url

    def get_base(self):
        url = ""
        if self.url_parts.scheme:
            url += self.url_parts.scheme + "://"
        url += self.get_netloc()
        return url

    def get_netloc(self):
        url = ""
        url += self.url_parts.subdomain
        if self.url_parts.domain:
            if self.url_parts:
                url += '.'
            url += self.url_parts.domain
        if self.url_parts.suffix:
            if self.url_parts.subdomain or self.url_parts.domain:
                url += '.'
            url += self.url_parts.suffix
        return url

    def get_extension(self):
        url = ""
        url += self.url_parts.path
        if self.url_parts.params:
            url += ';' + self.url_parts.params
        if self.url_parts.query:
            url += '?' + self.url_parts.query
        if self.url_parts.fragment:
            url += '#' + self.url_parts.fragment
        return url

    def is_fuzzed(self):
        return self.is_fuzzed

    def get_url_parts(self):
        return self.url_parts

    def __str__(self):
        return self.get_url()


def parse_url(url="", allow_fragments=True):
    if not allow_fragments:
        url = urllib.parse.urldefrag(url)[0]
    u_rslt = urllib.parse.urlparse(url)
    e_rslt = tldextract.extract(u_rslt.netloc)
    return ParseResult(u_rslt.scheme, e_rslt.subdomain, e_rslt.domain, e_rslt.suffix, u_rslt.path,
                       u_rslt.params, u_rslt.query, u_rslt.fragment)


def join_url(base="", path="", allow_fragments=True):
    return urllib.parse.urljoin(base, path, allow_fragments)


def same_domain(url1, url2):
    if not isinstance(url1, ParseResult):
        url1 = parse_url(url1)
    if not isinstance(url2, ParseResult):
        url2 = parse_url(url2)
    return url1.domain == url2.domain and url1.suffix == url2.suffix


def is_subdomain(url1, url2):
    if not isinstance(url1, ParseResult):
        url1 = parse_url(url1)
    if not isinstance(url2, ParseResult):
        url2 = parse_url(url2)
    # Does not return true if they are the same netloc
    return same_domain(url1, url2) and url1.subdomain != url2.subdomain


def same_netloc(url1="", url2=""):
    url1_netloc = urllib.parse.urlparse(url1).netloc
    url2_netloc = urllib.parse.urlparse(url2).netloc
    return url1_netloc == url2_netloc 


# https://www.media.com/profile-page
class _CommonProfileFormat:
    def __init__(self, domain=None):
        self.domain = domain

    def follows_pattern(self, parsed_url):
        dir_count = len([path for path in parsed_url.path.split("/") if path])
        return dir_count == 1


# https://www.media.com/sub-dir/profile-page
class _OneDirDeepProfileFormat:
    def __init__(self, domain=None, prof_dirs=None):
        self.domain = domain
        self.prof_dirs = prof_dirs

    def follows_pattern(self, parsed_url):
        directories = [path for path in parsed_url.path.split("/") if path]
        return len(directories) == 2 and directories[0] in self.prof_dirs


# https://profile-page.media.com/
class _SubdomainProfileFormat:
    def __init__(self, domain=None, forbidden_subdomains=None):
        self.domain = domain
        self.forbidden_subdomains = forbidden_subdomains

    def follows_pattern(self, parsed_url):
        dir_count = len([path for path in parsed_url.path.split("/") if path])
        for forbidden in self.forbidden_subdomains:
            if parsed_url.subdomain == forbidden:
                return False
        return dir_count == 0


_SOCIAL_MEDIA = (_CommonProfileFormat("facebook"),
                 _CommonProfileFormat("twitter"),
                 _CommonProfileFormat("twitch"),
                 _CommonProfileFormat("pintrest"),
                 _CommonProfileFormat("github"),
                 _CommonProfileFormat("myspace"),
                 _CommonProfileFormat("instagram"),
                 _CommonProfileFormat("deviantart"),
                 _SubdomainProfileFormat("tumblr", forbidden_subdomains={'www'}),
                 _OneDirDeepProfileFormat("flickr", prof_dirs={'photos'}),
                 _OneDirDeepProfileFormat("linkedin", prof_dirs={'in'})
                )


def is_social_media_profile(url=""):
    url = parse_url(url)
    for social_media_profile_format in _SOCIAL_MEDIA:
        if social_media_profile_format.domain == url.domain:
            return social_media_profile_format.follows_pattern(url)
    return False

