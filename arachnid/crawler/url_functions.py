import urllib.parse

from . import crawler_url


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
