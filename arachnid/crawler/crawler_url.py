from . import url_functions as uf


class CrawlerURL:
    def __init__(self, url="", allow_query=True, is_fuzzed=False, in_robots=False):
        non_uniform_parts = uf.parse(url, allow_query)
        uniform_url = uf.equiv_url(non_uniform_parts)
        self.url_parts = uf.parse(uniform_url)
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

    def set_on_fuzz(self, bool):
        self.on_fuzz_list = bool

    def in_robots(self):
        return self.on_robots_list

    def get_url_parts(self):
        return self.url_parts

    def __str__(self):
        return self.get_url()

    def __eq__(self, other):
        """ CrawlerURLs are considered equivalent if they lead to the same page, ignoring SSL"""
        return uf.equiv_url_s(other.get_url_parts()) == uf.equiv_url_s(self.get_url_parts())

    def __hash__(self):
        return hash(uf.equiv_url_s(self.get_url_parts()))
