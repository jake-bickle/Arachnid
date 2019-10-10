import os
import socket
import webbrowser
import php.server
import php.finder

from . import crawler
from .timewidgets import Timer
from .arachnid_arg_parser import arachnid_cl_parser

__version__ = "0.9.2.1"


this_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(this_dir, "output")
output_file = os.path.join(output_dir, "scraped_data/arachnid_data.json")
warning_file = os.path.join(output_dir, "scraped_data/warnings.json")
default_ip = "127.0.0.1:8080"


def main():
    ip = get_unused_server_address()
    p = php.server.PHPServer(output_dir, ip, install_loc=php.finder.get_php_path())
    p.start()
    clear_file(output_file)
    clear_file(warning_file)
    webbrowser.open_new_tab(f"http://{ip}")
    crawl()
    p.stop()


def crawl():
    args = arachnid_cl_parser.parse_args()
    c = crawler.get_crawler(args)
    with open(output_file, "w") as f:
        f.write(c.dumps())

    file_write_timer = Timer()
    crawler_limit_timer = Timer()
    file_write_timer.start()
    crawler_limit_timer.start()
    pages_crawled = 0
    while pages_crawled < args.page_limit and crawler_limit_timer.elapsed() / 60 < args.time_limit and c.crawl_next():
        if file_write_timer.elapsed() > 15:
            with open(output_file, "w") as f:
                f.write(c.dumps())
            file_write_timer.restart()
        pages_crawled += 1
    c.finish()
    with open(output_file, "w") as f:
        f.write(c.dumps())
    input("Crawl complete. Press ENTER to exit.")


def clear_file(file_loc):
    with open(file_loc, 'w') as f:
        f.write("")


def get_unused_server_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip, port = default_ip.split(":")
    port = int(port)
    bound = False
    while not bound:
        try:
            s.bind((ip, port))
            bound = True
        except OSError:
            port += 1
    s.close()
    return f"{ip}:{str(port)}"
