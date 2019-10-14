import os
import socket
import webbrowser

from . import crawler
from .php.finder import get_php_path
from .php.server import PHPServer
from .timewidgets import Timer
from .arachnid_arg_parser import arachnid_cl_parser

__version__ = "0.9.3.1"


this_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(this_dir, "output")
output_file = os.path.join(output_dir, "scraped_data/arachnid_data.json")
warning_file = os.path.join(output_dir, "scraped_data/warnings.json")
default_ip = "127.0.0.1:8080"


def main():
    app = Arachnid()
    app.start()


class Arachnid:
    def __init__(self, args=None):
        """ args is a list of command line arguments. If left empty, Arachnid will read sys.argv instead
        EX. args = ["https://www.example.com", "--stealth", "--time-limit", "5"]
        """
        if args:
            ns = arachnid_cl_parser.parse_args(args)
        else:
            ns = arachnid_cl_parser.parse_args()
        self.crawler = crawler.get_crawler_from_namespace(ns)
        self.pages_crawled = 0
        self.page_limit = ns.page_limit if ns.page_limit >= 0 else None
        self.time_limit = ns.time_limit if ns.time_limit >= 0 else None
        self.file_write_timer = Timer()
        self.time_limit_timer = Timer()
        self.server_address = self.get_unused_server_address()
        self.server = PHPServer(output_dir, self.server_address, install_loc=get_php_path())

    def start(self):
        self.overwrite_output_files()
        self.file_write_timer.start()
        self.time_limit_timer.start()
        if self.server:
            self.open_server()
        while not self.is_done() and self.crawler.crawl_next():
            self.pages_crawled += 1
            if self.file_write_timer.elapsed() > 15:
                self.save()
        self.close()

    def is_done(self):
        return self.above_time_limit() or self.above_page_limit()

    def open_server(self):
        self.server.start()
        webbrowser.open_new_tab(f"http://{self.server_address}")

    def overwrite_output_files(self):
        self.clear_file(output_file)
        self.clear_file(warning_file)
        self.save()

    def save(self):
        with open(output_file, "w") as f:
            f.write(self.crawler.dumps())

    def close(self):
        self.crawler.finish()
        self.save()
        input("Crawl complete. Press ENTER to exit.")
        self.server.stop()

    def above_time_limit(self):
        return self.time_limit_timer.elapsed() >= self.time_limit * 60 if self.time_limit else False

    def above_page_limit(self):
        return self.pages_crawled >= self.page_limit if self.page_limit else False

    @staticmethod
    def clear_file(file_loc):
        with open(file_loc, 'w') as f:
            f.write("")

    @staticmethod
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
