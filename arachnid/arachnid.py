import os
import webbrowser

from . import crawler
from .timewidgets import Timer
from .arachnid_arg_parser import arachnid_cl_parser
from .php.server import PHPServer

__version__ = "0.9.2.1"


this_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(this_dir, "output")
output_file = os.path.join(output_dir, "scraped_data/arachnid_data.json")
warning_file = os.path.join(output_dir, "scraped_data/warnings.json")
php_ip = "127.0.0.1:8080"


def crawl():
    args = arachnid_cl_parser.parse_args()
    c = crawler.get_crawler(args)
    with open(output_file, "w") as f:
        f.write(c.dumps())
    webbrowser.open_new_tab(f"http://{php_ip}")

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


def main():
    p = PHPServer(output_dir, php_ip)
    p.start()
    clear_file(output_file)
    clear_file(warning_file)
    crawl()
    p.stop()


if __name__ == "__main__":
    main()
