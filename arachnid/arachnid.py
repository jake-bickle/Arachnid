import os
from arachnid.crawler import crawler
from arachnid.timewidgets import Timer
from arachnid.arachnid_arg_parser import arachnid_cl_parser

__version__ = "0.9.4"

class Arachnid:
    def __init__(self, cli_args=None):
        """ cli_args is a list of command line arguments. If left empty, Arachnid will read sys.argv instead
        EX. args = ["https://www.example.com", "--stealth", "--time-limit", "5"]
        """
        if cli_args:
            ns = arachnid_cl_parser.parse_args(cli_args)
        else:
            ns = arachnid_cl_parser.parse_args()
        self.crawler = crawler.get_crawler_from_namespace(ns)
        self.pages_crawled = 0
        self.page_limit = ns.page_limit if ns.page_limit >= 0 else None
        self.time_limit = ns.time_limit if ns.time_limit >= 0 else None
        self.file_write_timer = Timer()
        self.time_limit_timer = Timer()
        self.output_file = os.path.join(ns.output, "arachnid_results.json")

    def start(self):
        self.save()
        self.file_write_timer.start()
        self.time_limit_timer.start()
        while not self.is_done() and self.crawler.crawl_next():
            self.pages_crawled += 1
            if self.file_write_timer.elapsed() > 15:
                self.save()
        self.close()

    def is_done(self):
        return self.above_time_limit() or self.above_page_limit()

    def save(self):
        with open(self.output_file, "w") as f:
            f.write(self.crawler.dumps(indent=4, sort_keys=True))

    def close(self):
        self.crawler.finish()
        self.save()
        input("Crawl complete. Press ENTER to exit.")

    def above_time_limit(self):
        return self.time_limit_timer.elapsed() >= self.time_limit * 60 if self.time_limit else False

    def above_page_limit(self):
        return self.pages_crawled >= self.page_limit if self.page_limit else False

    @staticmethod
    def clear_file(file_loc):
        with open(file_loc, 'w') as f:
            f.write("")
