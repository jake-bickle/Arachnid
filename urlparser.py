import tldextract  
import urllib.parse
from collections import namedtuple

_result = namedtuple("ParseResult", ["scheme", "subdomain", "domain", "suffix", "path", "params", "query", "fragment"])
class ParseResult(_result):
    def get_url(self):
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
        url += self.path
        if self.params:
            url += ';' + self.params
        if self.query:
            url += '?' + self.query
        if self.fragment:
            url += '#' + self.fragment

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
