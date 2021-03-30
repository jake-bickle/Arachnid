import os
from arachnid import enums

from argparse import ArgumentTypeError

this_dir = os.path.dirname(os.path.abspath(__file__))


class Config:
    def __init__(self):
        self.set_default()

    def set_default(self):
        self.seed = None
        self.scrape_links = True
        self.scrape_subdomains = True
        self.scrape_phone_number = True
        self.scrape_email = True
        self.scrape_social_media = True
        self.flagged_document_types = []
        self.obey_robots = True
        self.allow_query = True
        self.agent = enums.Agent.FIREFOX.value
        self.custom_str = None
        self.custom_str_case_sensitive = False
        self.custom_regex = None
        self.default_delay = enums.Delay.NONE.value
        self.paths_list_file_loc = os.path.join(this_dir, "data/fuzz_list.txt")
        self.subs_list_file_loc = os.path.join(this_dir, "data/subdomain_fuzz_list.txt")
        self.fuzz_paths = False
        self.fuzz_subs = False
        self.blacklisted_directories = []

    def set_stealth(self):
        self.obey_robots = True
        self.agent = enums.Agent.GOOGLE.value
        self.default_delay = enums.Delay.HIGH.value
        self.fuzz_paths = False
        self.fuzz_subs = False

    def set_aggressive(self):
        self.obey_robots = False
        self.default_delay = enums.Delay.NONE.value
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


def generate_config(namespace):
    """ Given a namespace provided by argparse, convert to a config the crawler can interpret """
    config = Config()
    apply_pre_configurations(namespace, config)
    apply_direct_translation_options(namespace, config)
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


def apply_direct_translation_options(namespace, config):
    """ Many 'dest's in the namespace have the same name and value type as attributes found in Config. This
        function simply assigns those like-named 'dest's to the config
    """
    for k, v in vars(namespace).items():
        if hasattr(config, k):
            setattr(config, k, v)
