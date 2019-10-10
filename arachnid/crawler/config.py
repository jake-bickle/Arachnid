import os
import arachnid_enums

this_dir = os.path.dirname(os.path.abspath(__file__))


class CrawlerConfig:
    def __init__(self):
        self.set_default()

    def set_default(self):
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.documents = {"doc", "docx", "ppt", "pptx", "pps", "xls", "xlsx", "csv", "odt", "odp", "pdf", "txt",
                          "zip", "rar", "dmg", "exe", "apk", "bin", "rpm", "dpkg"}
        self.obey_robots = True
        self.allow_query = True
        self.agent = arachnid_enums.Agent.FIREFOX.value
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.default_delay = arachnid_enums.Delay.NONE.value
        self.paths_list_file_loc = os.path.join(this_dir, "data/fuzz_list.txt")
        self.subs_list_file_loc = os.path.join(this_dir, "data/subdomain_fuzz_list.txt")
        self.fuzz_paths = False
        self.fuzz_subs = False
        self.blacklisted_directories = []

    def set_stealth(self):
        self.obey_robots = True
        self.agent = arachnid_enums.Agent.GOOGLE.value
        self.default_delay = arachnid_enums.Delay.HIGH.value
        self.fuzz_paths = False
        self.fuzz_subs = False

    def set_aggressive(self):
        self.obey_robots = False
        self.default_delay = arachnid_enums.Delay.NONE.value
        self.fuzz_paths = True
        self.fuzz_subs = True

    def set_layout_only(self):
        self.scrape_subdomains = False
        self.scrape_phone_number = False
        self.scrape_email = False
        self.scrape_social_media = False
        self.documents = {}
        self.custom_str = None
        self.custom_regex = None
