import argparse
import crawler_enums

from crawler import Crawler, CrawlerConfig

class AgentAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        aliases = { 'g': "google",
                    'b': "bing",
                    'y': "yahoo",
                    'd': "duckduckgo",
                    'bd': "baidu",
                    'yd': "yandex",
                    'f': "firefox",
                    'm': "android" }
        agent = aliases[value]
        full_user_agent = crawler_enums.Agent[agent.upper()].value
        setattr(namespace, self.dest, full_user_agent)

class DelayAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        delay_range = crawler_enums.Delay[value.upper()].value
        setattr(namespace, self.dest, delay_range)

class AmountAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        amount = crawler_enums.Amount[value.upper()]
        setattr(namespace, self.dest, amount)

parser = argparse.ArgumentParser(description="TODO: Create help description",
                                 argument_default=argparse.SUPPRESS)

parser.add_argument("seed", 
                    help="The URL for the Crawler to begin its search from")

parser.add_argument("-s", "--string",  # TODO Could this use nargs?
                    dest="custom_str", 
                    help="TODO: string help")

parser.add_argument("--case-sensitive", 
                    dest="custom_str_case_sensitive",
                    action="store_true",
                    help="TODO") 

parser.add_argument("-d", "--doc", 
                    dest="custom_doc", 
                    nargs='+', 
                    default=[],
                    help="TODO: doc help")

# TODO: Feature not in place yet
# parser.add_argument("--doc-grab", 
                    # dest="download_doc",
                    # action="store_true", 
                    # help="Download documents found by the -d option")

parser.add_argument("-r", "--regex", 
                    dest="custom_regex", 
                    help="A regular expression to be searched")

parser.add_argument("-f", "--find", 
                    dest="find",
                    nargs='+', 
                    choices=['phone', 'email', 'social', 'docs', 'all', 'none'], 
                    help="Find various information from a page. See man page for more details")

parser.add_argument("-T", "--delay", 
                    dest="delay", 
                    choices=["none", "low", "medium", "high"],
                    action=DelayAction, 
                    help="TODO: timing help")

parser.add_argument("--robots",
                    dest="obey_robots",
                    action="store_false",
                    help="Crawl the links gathered by robots.txt")

# TODO: Feature not in place yet
# parser.add_argument("-F", "--fuzz", 
                    # dest="fuzz",  
                    # choices=["none","low","medium","high","insane"], 
                    # action=AmountAction
                    # help="TODO: Fuzz help")

parser.add_argument("-a", "--agent", 
                    dest="agent", 
                    choices=['g', 'b', 'y', 'd', 'bd', 'yd', 'f', 'm'], 
                    action=AgentAction,
                    help="TODO: agent help")

# TODO: Feature not in place yet
# parser.add_argument("--page-only", 
                    # dest="scrape_links", 
                    # action="store_false", 
                    # help="Find information about the given URL only")

parser.add_argument("--no-subdomain", 
                    dest="scrape_subdomains", 
                    action="store_false", 
                    help="Don't crawl subdomains of the seed URL")

aggressions = parser.add_mutually_exclusive_group()
aggressions.add_argument("--stealth", 
                    dest="stealth", 
                    action="store_true", 
                    help="Use a preset of options to crawl quietly")

aggressions.add_argument("--aggressive", 
                    dest="aggressive", 
                    action="store_true", 
                    help="Use a preset of options to crawl loudly")

def generate_crawler_config(namespace):
    config = CrawlerConfig()
    # Apply pre-configs
    if "stealth" in namespace:
        config.set_stealth()
    elif "aggressive" in namespace:
        config.set_aggressive()

    # Parse --find options given by user
    if "find" in namespace:
        supplied_options = [opt.lower() for opt in namespace.find]
        if "all" in supplied_options and "none" in supplied_options:
            print("\"all\" and \"none\" options are mutually exclusive in --find")
            raise SystemExit
        has_occurred = {
                    "phone": False,
                    "email": False,
                    "social": False,
                    "docs": False,
                     }
        if "all" in supplied_options:
            for v in has_occurred.values():
                v = True
        elif "none" in supplied_options:
            for v in has_occurred.values():
                v = False
        else:
            for k in has_occurred:
                if k in supplied_options:
                    has_occurred[k] = True
        config.scrape_phone_number = has_occurred["phone"]
        config.scrape_email = has_occurred["email"]
        config.scrape_social_media = has_occurred["social"]
        if not has_occurred["docs"]:
            config.documents = {}

    config.documents.update(namespace.custom_doc)
    
    # Apply all argparse arguments that are can be directly translated
    for k, v in vars(namespace).items():
        if hasattr(config, k):
            setattr(config, k, v)

    return config

def generate_crawler():
    args = parser.parse_args()
    c = Crawler(args.seed)
    config = generate_crawler_config(args)
    c.config = config
    return c

def main():
    c = generate_crawler()
    c.crawl()

if __name__ == "__main__":
    main()

