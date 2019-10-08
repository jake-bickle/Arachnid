import re
import urllib.parse
import tldextract

from collections import namedtuple
from . import crawler_url

URLParts = namedtuple("URLParts", ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"])
url_regex = re.compile(r"http[s]?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.\w{2,5}[0-9a-zA-Z$/\-_.+!*'()]*")


def is_url(url):
    return re.match(url_regex, url)


def join_url(base="", path="", allow_fragments=True):
    return urllib.parse.urljoin(base, path, allow_fragments)


def is_subdomain(url1, url2):
    """ Returns whether url1 and url2 are subdomains of each other. That is, both their domain and suffix are the same.

        Both arguments may either be a string or a CrawlerURL object.
    """
    # Does not return true if they are the same netloc
    if not isinstance(url1, crawler_url.CrawlerURL):
        url1 = crawler_url.CrawlerURL(url1)
    if not isinstance(url2, crawler_url.CrawlerURL):
        url2 = crawler_url.CrawlerURL(url2)
    url1_parts = url1.get_url_parts()
    url2_parts = url2.get_url_parts()
    return url1_parts.domain == url2_parts.domain and url1_parts.suffix == url2_parts.suffix


def same_netloc(url1="", url2=""):
    url1_netloc = urllib.parse.urlparse(url1).netloc
    url2_netloc = urllib.parse.urlparse(url2).netloc
    return url1_netloc == url2_netloc


def change_subdomain(new_subdomain="", dest=""):
    """ Converts the subdomain in dest.
        IE. change_subdomain('en', 'https://www.google.com') would return 'https://en.google.com'
    """
    parsed_dest = urllib.parse.urlparse(dest)
    dest_netloc_parts = tldextract.extract(parsed_dest.netloc)
    return unparse((parsed_dest[0], new_subdomain, dest_netloc_parts[1], dest_netloc_parts[2], parsed_dest[2],
                    parsed_dest[3], parsed_dest[4], parsed_dest[5]))


def get_robots(url):
    if not isinstance(url, crawler_url.CrawlerURL):
        url = crawler_url.CrawlerURL(url)
    return "{}/robots.txt".format(url.get_base())


def equiv_url(url_parts):
    """ Returns an equivalent URL from given URLParts """
    subdomain = url_parts.subdomain if url_parts.subdomain else "www"
    path = url_parts.path[:-1] if url_parts.path.endswith('/') else url_parts.path
    return unparse([url_parts[0], subdomain, url_parts[2], url_parts[3], path, url_parts[5], url_parts[6], ''])


def equiv_url_s(url_parts):
    """ Like equiv_url, but forces a secure connection """
    eq_url = equiv_url(url_parts)
    if eq_url.startswith("http") and eq_url[4] != 's':
        return eq_url[:4] + 's' + eq_url[5:]
    return eq_url


def equiv_url_is(url_parts):
    """ Like equiv_url, but forces an insecure connection"""
    eq_url = equiv_url(url_parts)
    if eq_url.startswith("https"):
        return eq_url[:4] + eq_url[5:]
    return eq_url


def parse(url, allow_query=True):
    u_rslt = urllib.parse.urlparse(url)
    e_rslt = tldextract.extract(u_rslt.netloc)
    query = u_rslt.query if allow_query else ""
    return URLParts(u_rslt.scheme, e_rslt.subdomain, e_rslt.domain, e_rslt.suffix, u_rslt.path,
                    u_rslt.params, query, u_rslt.fragment)


def unparse(url_parts):
    """ Similar to urllib.parse.urlunparse, except that it allows more arguments for the subdomain, domain, and suffix
        url_parts = ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"]
    """
    if url_parts[1]:
        netloc = '.'.join([url_parts[1], url_parts[2], url_parts[3]])
    else:
        netloc = '.'.join([url_parts[2], url_parts[3]])

    return urllib.parse.urlunparse([url_parts[0], netloc, url_parts[4], url_parts[5],
                                    url_parts[6], url_parts[7]])


# https://www.media.com/profile-page
class _CommonProfileFormat:
    def __init__(self, domain=None):
        self.domain = domain

    def follows_pattern(self, url_parts):
        dir_count = len([path for path in url_parts.path.split("/") if path])
        return dir_count == 1


# https://www.media.com/sub-dir/profile-page
class _OneDirDeepProfileFormat:
    def __init__(self, domain=None, prof_dirs=None):
        self.domain = domain
        self.prof_dirs = prof_dirs

    def follows_pattern(self, url_parts):
        directories = [path for path in url_parts.path.split("/") if path]
        return len(directories) == 2 and directories[0] in self.prof_dirs


# https://profile-page.media.com/
class _SubdomainProfileFormat:
    def __init__(self, domain=None, forbidden_subdomains=None):
        self.domain = domain
        self.forbidden_subdomains = forbidden_subdomains

    def follows_pattern(self, url_parts):
        dir_count = len([path for path in url_parts.path.split("/") if path])
        for forbidden in self.forbidden_subdomains:
            if url_parts.subdomain == forbidden:
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


def is_social_media_profile(c_url=""):
    c_url = crawler_url.CrawlerURL(c_url)
    parts = c_url.get_url_parts()
    for social_media_profile_format in _SOCIAL_MEDIA:
        if social_media_profile_format.domain == parts.domain:
            return social_media_profile_format.follows_pattern(parts)
    return False
