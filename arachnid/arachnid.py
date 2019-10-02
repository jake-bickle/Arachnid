import threading
import os
import webbrowser

from . import crawler
from .timewidgets import Timer
from .arachnid_arg_parser import arachnid_cl_parser

__version__ = "0.9.2.1"


this_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(this_dir, "output/scraped_data/arachnid_data.json")
warning_file = os.path.join(this_dir, "output/scraped_data/warnings.json")
php_ip = "127.0.0.1:8080"
php_cmd = f"php -S {php_ip} -t {this_dir}/output -q >& /dev/null"


def crawl():
    args = arachnid_cl_parser.parse_args()
    c = crawler.get_crawler(args)
    with open(output_file, "w") as f:
        f.write(c.dumps())
    webbrowser.open_new_tab(f"{php_ip}")

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
    php_server = threading.Thread(target=lambda: os.system(php_cmd), args=(), daemon=True)
    php_server.start()
    clear_file(output_file)
    clear_file(warning_file)
    crawl()


if __name__ == "__main__":
    main()
