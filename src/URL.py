import urlparser
from collections import namedtuple

_cnt = namedtuple("Credits", ["Lambda", "Per_page"])


class URL:
    def __init__(self, url="", credits=0, allow_fragments=True):
        self.parsed_url = urlparser.parse_url(url, allow_fragments)
        self.credits = credits

    def get_url(self, trim_extension=False):
        return self.parsed_url.get_url(self, trim_extension)

    def get_base(self):
        return self.parsed_url.get_base()

    def get_netloc(self):
        return self.parsed_url.get_netloc()

    def get_extension(self):
        return self.parsed_url.get_extension()

    def add_credits(self, credits):
        if credits < 0:
            raise ValueError(credits + " cannot be below zero")
        self.credits += credits

    def relinquish_credits(self, num_of_pages):
        dispersed_credits = _cnt(self._calc_lambda_credits(), self._calc_page_credits(num_of_pages))
        self.credits = 0
        return dispersed_credits

    def _calc_lambda_credits(self):
        return self.credits / 10

    def _calc_page_credits(self, num_of_pages):
        return (self.credits - self._calc_lambda_credits()) / num_of_pages
