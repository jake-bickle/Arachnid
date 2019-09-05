import json
import tldextract
import datetime

from timewidgets import Timer


class SetToList(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class DomainData:
    """The output of the crawler. Data is contained in sets, and converted to lists
       for json.dumps(). The purpose is to have unique data only."""

    def __init__(self, netloc):
        p_n = tldextract.extract(netloc)
        self.domain = p_n.domain
        self.suffix = p_n.suffix
        metadata = {"start_time": None,
                    "start_date": None,
                    "end_time": None,
                    "end_date": None,
                    "run_time": None,
                    "config": None}
        # The majority of the data is held within sets to prevent duplicate data.
        self.data = {"sites": list(),
                     "phone_numbers": set(),
                     "emails": set(),
                     "social_media": set(),
                     "custom_regex": set(),
                     "metadata": metadata}
        self._new_subdomain(netloc)
        self.run_time = Timer()
        
    def dumps(self, **kwargs):
        return json.dumps(self.data, cls=SetToList, **kwargs)

    def add_page(self, netloc, page):
        sub = self._ensure_subdomain(netloc)
        if not (page["code"] == 404 and page["on_fuzz_list"]):  # Failed fuzzes won't be added to reduce clutter
            sub["pages"].append(page)

    def add_phone(self, phone_number):
        self.data["phone_numbers"].add(phone_number)

    def add_email(self, email):
        self.data["emails"].add(email)

    def add_social(self, social_media):
        self.data["social_media"].add(social_media)

    def add_document(self, netloc, document):
        sub = self._ensure_subdomain(netloc)
        sub["documents"].append(document)

    def add_custom_regex(self, regex):
        self.data["custom_regex"].add(regex)

    def add_config(self, crawler_config):
        self.data["metadata"]["config"] = vars(crawler_config)

    def start(self):
        self.run_time.start()
        d = datetime.datetime.today()
        self.data["metadata"]["start_date"] = d.strftime("%d/%m/%Y")
        self.data["metadata"]["start_time"] = d.strftime("%H:%M:%S")

    def end(self):
        self.data["metadata"]["run_time"] = self.run_time.elapsed()
        d = datetime.datetime.today()
        self.data["metadata"]["end_date"] = d.strftime("%d/%m/%Y")
        self.data["metadata"]["end_time"] = d.strftime("%H:%M:%S")

    def _new_subdomain(self, netloc):
        self.throw_if_wrong_domain(netloc)
        sub = { "netloc": netloc,
                "pages": list(),        # pages and documents will never get duplicate data, as the crawler will
                "documents": list() }   # never crawl the same link twice. Meaning a set is not necessary
        self.data["sites"].append(sub);
        return sub

    def _retrieve_subdomain(self, netloc):
        for sub in self.data["sites"]:
            if sub["netloc"] == netloc:
                return sub
        return None

    def _ensure_subdomain(self, netloc):
        sub = self._retrieve_subdomain(netloc)
        if sub is None:
            return self._new_subdomain(netloc)
        return sub

    def throw_if_wrong_domain(self, netloc):
        p_n = tldextract.extract(netloc)
        if p_n.domain != self.domain or p_n.suffix != self.suffix:
            raise ValueError("{0} is not a subdomain of {1}.{2}".format(netloc, self.domain, self.suffix))

