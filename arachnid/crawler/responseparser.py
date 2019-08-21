import mimetypes

from . import crawler_url


def _get_matching_element(a, b):
    for x in a:
        for y in b:
            if x == y:
                return x
    return None


class DocumentResponse:
    def __init__(self, response, applicable_types):
        self.response = response
        self.applicable_types = applicable_types

    def extract(self):
        data = dict()
        data["name"] = self._get_filename() 
        data["code"] = self.response.status_code
        possible_extensions = [t.lstrip(".") for t in mimetypes.guess_all_extensions(self.response.headers["content-type"])]
        data["type"] = _get_matching_element(self.applicable_types, possible_extensions)
        if data["type"]:
            return data 
        return None

    def _get_filename(self):
        try:
            cd = self.response.headers["content-disposition"]
            f_s = cd.find("filename") + 10  # Get index after filename="
            f_e = cd.find("\"", f_s)
            return cd[f_s:f_e]
        except KeyError:
            path = crawler_url.CrawlerURL(self.response.url).get_url_parts().path
            return path.split("/")[-1]

