import argparse
import os

from .arachnid_enums import Delay, Agent
from .crawler.url_functions import is_url

arachnid_cl_parser = argparse.ArgumentParser(prog="Arachnid",
                                             description="TODO: Create help description",
                                             argument_default=argparse.SUPPRESS)


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


def valid_url(url):
    if not is_url(url):
        msg = url + " is not a valid URL"
        raise argparse.ArgumentTypeError(msg)
    return url


def time_format(time):
    sections = time.split(":")
    for n in range(len(sections)):
        try:
            float(sections[n])
        except ValueError:
            if sections[n].isspace() or sections[n] == "":
                # Empty/Space sections are considered ZERO
                sections[n] = 0
            else:
                raise argparse.ArgumentTypeError("{} is not a number".format(sections[n]))
        if float(sections[n]) < 0:
            raise argparse.ArgumentTypeError("Please enter only non-negative numbers")
        sections[n] = float(sections[n])
    if len(sections) == 1:
        # m format
        return sections[0]
    elif len(sections) == 2:
        # h:m format
        return sections[0] * 60 + sections[1]
    elif len(sections) == 3:
        # h:m:s format
        return sections[0] * 60 + sections[1] + sections[2] / 60
    else:
        msg = "Must follow m, h:m, or h:m:s format"
        raise argparse.ArgumentTypeError(msg)


arachnid_cl_parser.add_argument("seed",
                                type=valid_url,
                                help="The URL for Arachnid to begin its search from.")

arachnid_cl_parser.add_argument("-s", "--string",
                                dest="custom_str",
                                help="Find the occurrences of string on each web page.")

arachnid_cl_parser.add_argument("--case-sensitive",
                                dest="custom_str_case_sensitive",
                                action="store_true",
                                help="States that the --string argument is case sensitive.")

arachnid_cl_parser.add_argument("-d", "--doc",
                                dest="custom_doc",
                                nargs='+',
                                default=[],
                                help="TODO: doc help")

# TODO: Feature not in place yet
# arachnid_cl_parser.add_argument("--doc-grab",
                    # dest="download_doc",
                    # action="store_true",
                    # help="Download documents found by the -d option")

arachnid_cl_parser.add_argument("-r", "--regex",
                                dest="custom_regex",
                                help="A regular expression to be searched throughout the crawl.")

arachnid_cl_parser.add_argument("-f", "--find",
                                dest="find",
                                nargs='+',
                                choices=['phone', 'email', 'social', 'docs', 'all', 'none'],
                                help="Find various information from a page. See man page for more details.")

arachnid_cl_parser.add_argument("-t", "--delay",
                                dest="default_delay",
                                choices=["none", "low", "medium", "high"],
                                default=Delay.NONE.value,
                                action=DelayAction,
                                help="States how much delay occurs between page requests.")

arachnid_cl_parser.add_argument("-F", "--fuzz",
                                dest="paths_list_file_loc",
                                nargs='?',
                                action=FuzzAction,
                                help="Fuzzes for web pages on each subdomain that may be unlisted. Provide a file path to supply your own list to fuzz.")

arachnid_cl_parser.add_argument("-a", "--agent",
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

arachnid_cl_parser.add_argument("--page-only",
                                dest="scrape_links",
                                action="store_false",
                                help="Scrape information about the given URL only.")

arachnid_cl_parser.add_argument("--no-query",
                                dest="allow_query",
                                action="store_false",
                                help="Disables requests on the same web page with differing URL queries.")

arachnid_cl_parser.add_argument("--page-limit",
                                dest="page_limit",
                                type=int,
                                default=-1,
                                help="The amount of pages Arachnid will crawl before stopping.")

arachnid_cl_parser.add_argument("--time-limit",
                                dest="time_limit",
                                type=time_format,
                                default=-1,
                                help="The amount of time Arachnid will crawl before stopping. Valid formats are m, h:m, or h:m:s")

arachnid_cl_parser.add_argument("--blacklist-dir",
                                dest="blacklisted_directories",
                                nargs="+",
                                help="The URL path directories that Arachnid is forbidden to access.")

aggressions = arachnid_cl_parser.add_mutually_exclusive_group()
aggressions.add_argument("--stealth",
                    dest="stealth",
                    action="store_true",
                    help="Use a preset of options to crawl quietly")

aggressions.add_argument("--aggressive",
                    dest="aggressive",
                    action="store_true",
                    help="Use a preset of options to crawl loudly")

subdomains = arachnid_cl_parser.add_mutually_exclusive_group()
subdomains.add_argument("-S", "--fuzz-subdomains",
                    dest="subs_list_file_loc",
                    nargs="?",
                    action=SubfuzzAction,
                    help="Fuzzes for common subdomains that may be unlisted. Provide a file path to supply your own list to fuzz.")

subdomains.add_argument("--no-subdomain",
                    dest="scrape_subdomains",
                    action="store_false",
                    help="Don't crawl any subdomains.")

robots = arachnid_cl_parser.add_mutually_exclusive_group()
robots.add_argument("-R", "--disobey-robots",
                    dest="obey_robots",
                    action="store_false",
                    help="Ignore robots.txt rules and crawl the links located in it")

robots.add_argument("--obey-robots",
                    dest="obey_robots",
                    action="store_true",
                    help="Respect robots.txt rules")
