import argparse
import re
import threading
import os
import webbrowser

from . import crawler
from .timewidgets import Timer
from .arachnid_enums import Delay, Agent

__version__ = "0.9.1"

this_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(this_dir, "output/scraped_data/arachnid_data.json")
warning_file = os.path.join(this_dir, "output/scraped_data/warnings.json")
php_ip = "127.0.0.1:8080"
php_cmd = f"php -S {php_ip} -t {this_dir}/output -q >& /dev/null"


class AgentAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        aliases = {('g', "google"): "google",
                   ('b', 'bing'): "bing",
                   ('y', "yahoo"): "yahoo",
                   ('d', "duckduckgo"): "duckduckgo",
                   ('bd', "baidu"): "baidu",
                   ('yd', "yandex"): "yandex",
                   ('f', "firefox"): "firefox",
                   ('m', "mobile", "android"): "android"}
        for k, v in aliases.items():
            if value in k:
                user_agent = Agent[v.upper()].value
                setattr(namespace, self.dest, user_agent)
                return


class DelayAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        delay_range = Delay[value.upper()].value
        setattr(namespace, self.dest, delay_range)


class FuzzAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        if value:
            file_path = os.path.expanduser(value)
            file_path = os.path.abspath(file_path)
            if os.path.exists(file_path):
                setattr(namespace, self.dest, file_path)
            else:
                msg = "The file {} does not exist".format(file_path)
                raise argparse.ArgumentTypeError(msg)
        namespace.fuzz_paths = True


class SubfuzzAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        if value:
            file_path = os.path.expanduser(value)
            file_path = os.path.abspath(file_path)
            if os.path.exists(file_path):
                setattr(namespace, self.dest, file_path)
            else:
                msg = "The file {} does not exist".format(file_path)
                raise argparse.ArgumentTypeError(msg)
        namespace.fuzz_subs = True


def is_url(url):
    link = re.compile(r"http[s]?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.\w{2,5}[0-9a-zA-Z$/\-_.+!*'()]*")
    if not re.match(link, url):
        msg = url + " is not a valid URL"
        raise argparse.ArgumentTypeError(msg)
    return url


parser = argparse.ArgumentParser(prog="Arachnid",
                                 description="TODO: Create help description",
                                 argument_default=argparse.SUPPRESS)

parser.add_argument("seed",
                    type=is_url,
                    help="The URL for Arachnid to begin its search from.")

parser.add_argument("-s", "--string",
                    dest="custom_str",
                    help="Find the occurrences of string on each web page.")

parser.add_argument("--case-sensitive",
                    dest="custom_str_case_sensitive",
                    action="store_true",
                    help="States that the --string argument is case sensitive.")

parser.add_argument("-d", "--doc",
                    dest="custom_doc",
                    nargs='+',
                    default=[],
                    help="When enabled, the user may add file extensions to also be scraped including the default")

# TODO: Feature not in place yet
# parser.add_argument("--doc-grab",
                    # dest="download_doc",
                    # action="store_true",
                    # help="Download documents found by the -d option")

parser.add_argument("-r", "--regex",
                    dest="custom_regex",
                    help="A regular expression to be searched throughout the crawl. Only items matching the pattern will be returned.")

parser.add_argument("-f", "--find",
                    dest="find",
                    nargs='+',
                    choices=['phone', 'email', 'social', 'docs', 'all', 'none'],
                    help="The default scan looks for a predefined list of interesting information. When --find is enabled, it will only search for the categories that the user supplies.")

parser.add_argument("-t", "--delay",
                    dest="default_delay",
                    choices=["none", "low", "medium", "high"],
                    default=Delay.NONE.value,
                    action=DelayAction,
                    help="States how much delay occurs between page requests.")

parser.add_argument("-F", "--fuzz",
                    dest="paths_list_file_loc",
                    nargs='?',
                    action=FuzzAction,
                    help="Fuzzes for web pages on each subdomain that may be unlisted. Users may provide a URL to their own list to override the default.")

parser.add_argument("-a", "--agent",
                    dest="agent",
                    choices=['g', 'google',
                             'b', 'bing',
                             'y', 'yahoo',
                             'd', 'duckduckgo',
                             'bd', 'baidu',
                             'yd', 'yandex',
                             'f', 'firefox',
                             'm', 'mobile', 'android'],
                    action=AgentAction,
                    help="The useragent the crawler will use when requesting pages.")

parser.add_argument("--page-only",
                    dest="scrape_links",
                    action="store_false",
                    help="Scrape information about the given URL only, no additional crawling will be performed.")

parser.add_argument("--no-query",
                     dest="allow_query",
                     action="store_false",
                     help="Disables GET requests on the same web page with differing URL queries. Enabling this may miss some pages, but also can fix errors and/or speed up scans")

aggressions = parser.add_mutually_exclusive_group()
aggressions.add_argument("--stealth",
                    dest="stealth",
                    action="store_true",
                    help="Use a preset of options to crawl quietly.")

aggressions.add_argument("--aggressive",
                    dest="aggressive",
                    action="store_true",
                    help="Use a preset of options to crawl loudly")

subdomains = parser.add_mutually_exclusive_group()
subdomains.add_argument("-S", "--fuzz-subdomains",
                    dest="subs_list_file_loc",
                    nargs="?",
                    action=SubfuzzAction,
                    help="Fuzzes for common subdomains that may be unlisted. PUsers may provide a URL to their own list to override the default.")

subdomains.add_argument("--no-subdomain",
                    dest="scrape_subdomains",
                    action="store_false",
                    help="Any subdomains found will NOT be crawled")

robots = parser.add_mutually_exclusive_group()
robots.add_argument("-R", "--disobey-robots",
                    dest="obey_robots",
                    action="store_false",
                    help="Ignore robots.txt rules and crawl the links located in it. Default is to obey.")

robots.add_argument("--obey-robots",
                    dest="obey_robots",
                    action="store_true",
                    help="Respect robots.txt rules, and do not crawl the pages listed.")


def crawl():
    args = parser.parse_args()
    c = crawler.get_crawler(args)
    with open(output_file, "w") as f:
        f.write(c.dumps())
    webbrowser.open_new_tab(f"{php_ip}")

    timer = Timer()
    timer.start()
    while c.crawl_next():
        if timer.elapsed() > 30:
            with open(output_file, "w") as f:
                f.write(c.dumps())
            timer.restart()
    with open(output_file, "w") as f:
        f.write(c.dumps())
    input("Crawl complete. Press ENTER to exit.")


def clear_file(file_loc):
    with open(file_loc, 'w') as f:
        f.write("")


def main():
    php_server = threading.Thread(target=lambda: os.system(php_cmd), args=(), daemon=True)
    php_server.start()
    clear_file(output_file)
    clear_file(warning_file)
    crawl()


if __name__ == "__main__":
    main()
