import argparse
import re
import random
import threading
import os
import sys
import webbrowser

from . import crawler
from .timewidgets import Stopwatch, Timer
from .arachnid_enums import Delay, Amount, Agent

base_dir = os.path.dirname(sys.modules["__main__"].__file__)
output_file = os.path.join(base_dir, "output/scraped_data/arachnid_data.json")
php_ip = "127.0.0.1:8080"
php_cmd = f"php -S {php_ip} -t {base_dir}/output -q >& /dev/null"


class AgentAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        aliases = { 'g': "google",
                    'b': "bing",
                    'y': "yahoo",
                    'd': "duckduckgo",
                    'bd': "baidu",
                    'yd': "yandex",
                    'f': "firefox",
                    'm': "android"}
        agent = aliases[value]
        full_user_agent = Agent[agent.upper()].value
        setattr(namespace, self.dest, full_user_agent)


class DelayAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        delay_range = Delay[value.upper()].value
        setattr(namespace, self.dest, delay_range)


class AmountAction(argparse.Action):
    def __call__(self, parser, namespace, value, arg):
        amount = Amount[value.upper()]
        setattr(namespace, self.dest, amount)


def is_url(url):
    link = re.compile(r"http[s]?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.\w{2,5}[0-9a-zA-Z$/\-_.+!*'()]*")
    if not re.match(link, url):
        msg = url + " is not a valid URL"
        raise argparse.ArgumentTypeError(msg)
    return url


parser = argparse.ArgumentParser(description="TODO: Create help description",
                                 argument_default=argparse.SUPPRESS)

parser.add_argument("seed",
                    type=is_url,
                    help="The URL for the Crawler to begin its search from")

parser.add_argument("-s", "--string",
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
                    default=Delay.NONE.value,
                    action=DelayAction,
                    help="TODO: timing help")

parser.add_argument("--robots",
                    dest="obey_robots",
                    action="store_false",
                    help="Crawl the links gathered by robots.txt")

parser.add_argument("-F", "--fuzz",
                    dest="fuzz",
                    nargs='?',
                    default='crawler/fuzz_list.txt',
                    help="TODO: Fuzz help")

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


def crawl():
    args = parser.parse_args()
    c = crawler.get_crawler(args)

    delay_sw = Stopwatch(random.choice(args.delay))
    timer = Timer()
    timer.start()
    while c.crawl_next():
        delay_sw.start()
        if timer.elapsed() > 30:
            with open(output_file, "w") as f:
                f.write(c.dumps(indent=4))
            timer.restart()
        delay_sw.wait()  # Delay the crawler to throw off automated systems
    with open(output_file, "w") as f:
        f.write(c.dumps(indent=4))
    input("Crawl complete. Press ENTER to exit.")


def main():
    php_server = threading.Thread(target=lambda: os.system(php_cmd), args=(), daemon=True)
    php_server.start()
    webbrowser.open_new_tab(f"{php_ip}")
    crawl()


if __name__ == "__main__":
    main()
