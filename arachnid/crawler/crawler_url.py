import tldextract  
import urllib.parse
from collections import namedtuple


_url_parts_nt = namedtuple("URL_parts", ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"])


class CrawlerURL:
    def __init__(self, url="", allow_fragments=True, is_fuzzed=False, in_robots=False):
        if not allow_fragments:
            url = urllib.parse.urldefrag(url)[0]
        u_rslt = urllib.parse.urlparse(url)
        e_rslt = tldextract.extract(u_rslt.netloc)
        self.url_parts = _url_parts_nt(u_rslt.scheme, e_rslt.subdomain, e_rslt.domain, e_rslt.suffix, u_rslt.path,
                                      u_rslt.params, u_rslt.query, u_rslt.fragment)
        self.on_fuzz_list = is_fuzzed
        self.on_robots_list = in_robots

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
            if self.url_parts.subdomain:
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
        return self.on_fuzz_list

    def in_robots(self):
        return self.on_robots_list

    def get_url_parts(self):
        return self.url_parts

    def __str__(self):
        return self.get_url()

    def __eq__(self, other):
        return other.url_parts == self.url_parts

    def __hash__(self):
        return hash(self.get_url())





