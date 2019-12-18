import os
import json

from argparse import ArgumentTypeError
from cli import arachnid_enums

this_dir = os.path.dirname(os.path.abspath(__file__))
cli_root = os.path.abspath(this_dir + "/../../")
data_dir = os.path.abspath(cli_root + "/data")
predefined_scans_file_loc = os.path.abspath(cli_root + "/predefined-scans.json")



class CrawlerConfig:
    """
    The CrawlerConfig class stores the parameters for the Crawler all in one place.
    "Default", "Stealth", and "Aggressive" are three predefined settings defined in Arachnid/arachnid/predefined-scans.json
    """
    def __init__(self):
        self.set_default()

    @staticmethod
    def get_predefined_settings(scan_type):
        with open(predefined_scans_file_loc) as f:
            data = json.load(f)
        return data[scan_type]

    def _apply_settings(self, settings):
        """
        The methods in CrawlerConfig simply read the data from "predefined-scans.json" and apply them to this object.
        While most of the data is straight-forward, there are a few translations that need to take place to apply the
        data correctly.
        """
        self.scrape_links = settings["scrape_links"]
        self.scrape_subdomains = settings["scrape_subdomains"]
        self.scrape_phone_number = settings["scrape_phone_number"]
        self.scrape_email = settings["scrape_email"]
        self.scrape_social_media = settings["scrape_social_media"]
        self.obey_robots = settings["obey_robots"]
        self.allow_query = settings["allow_query"]
        self.custom_str = settings["custom_str"]
        self.custom_str_case_sensitive = settings["custom_str_case_sensitive"]
        self.custom_regex = settings["custom_regex"]
        self.paths_list_file_loc = os.path.join(cli_root, settings["paths_list_file_loc"])
        self.subs_list_file_loc = os.path.join(cli_root, settings["subs_list_file_loc"])
        self.fuzz_paths = settings["fuzz_paths"]
        self.fuzz_subs = settings["fuzz_paths"]
        self.blacklisted_directories = settings["blacklisted_directories"]
        self.documents = set()
        if settings["scrape_common_documents"]:
            with open(data_dir + "/common_documents.txt") as f:
                for doc_extension in f:
                    self.documents.add(doc_extension)
        for doc_extension in settings["custom_documents"]:
            self.documents.add(doc_extension)
        agent_enum = settings["useragent"].upper()
        agent_enum = agent_enum[:-3] if agent_enum.endswith("BOT") else agent_enum  # These two actions convert the
                                                                                    # string into the Agent enum format
        self.agent = eval(f"arachnid_enums.Agent.{agent_enum}.value")
        delay_enum = settings["default_delay"].upper()
        self.default_delay = eval(f"arachnid_enums.Delay.{delay_enum}.value")

    def set_default(self):
        settings = self.get_predefined_settings("default")
        self._apply_settings(settings)

    def set_stealth(self):
        settings = self.get_predefined_settings("stealth")
        self._apply_settings(settings)

    def set_aggressive(self):
        settings = self.get_predefined_settings("aggressive")
        self._apply_settings(settings)


def generate_crawler_config(namespace):
    """ Converts namespace given by arachnid_cl_parser to a CrawlerConfig object.
        This is necessary as argparse does not provide enough functionality to apply a few necessary settings.
    """
    config = CrawlerConfig()
    apply_pre_configurations(namespace, config)
    apply_direct_translation_options(namespace, config)
    if hasattr(namespace, "custom_doc"):
        config.documents.update(namespace.custom_doc)
    if "find" in namespace:
        apply_find_options(namespace, config)
    return config


def apply_pre_configurations(namespace, config):
    if "stealth" in namespace:
        config.set_stealth()
    elif "aggressive" in namespace:
        config.set_aggressive()


def apply_find_options(namespace, config):
    supplied_options = [opt.lower() for opt in namespace.find]
    if "all" in supplied_options and "none" in supplied_options:
        msg = "\"all\" and \"none\" options are mutually exclusive in the --find option"
        raise ArgumentTypeError(msg)
    has_occurred = {
        "phone": False,
        "email": False,
        "social": False,
        "docs": False,
    }
    if "all" in supplied_options:
        for k in has_occurred:
            has_occurred[k] = True
    elif "none" in supplied_options:
        for k in has_occurred:
            has_occurred[k] = False
    else:
        for k in has_occurred:
            if k in supplied_options:
                has_occurred[k] = True
    config.scrape_phone_number = has_occurred["phone"]
    config.scrape_email = has_occurred["email"]
    config.scrape_social_media = has_occurred["social"]
    if not has_occurred["docs"]:
        config.documents = set()


def apply_direct_translation_options(namespace, config):
    """ Many 'dest's in the namespace have the same name and value type as attributes found in CrawlerConfig. This
        function simply assigns those like-named 'dest's to the config
    """
    for k, v in vars(namespace).items():
        if hasattr(config, k):
            setattr(config, k, v)
