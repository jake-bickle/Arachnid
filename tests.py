import unittest
from scraper import Scraper

class test_scraper(unittest.TestCase):
    def setUp(self):
        self.html_doc = """
            <html><head><title>The Dormouse's story</title></head>
            <body>
                <p class="title"><b>The Dormouse's story</b></p>

                <p class="story">Once upon a time there were three little sisters; and their names were
                <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                and they lived at the bottom of a well.</p>

                <p class="story">...</p>
                <address>
                Written by <a href="mailto:webmaster@example.com">Jon Doe</a>.<br> 
                Visit us at:<br>
                Example.com<br>
                Box 564, Disneyland<br>
                USA
                This is a text of an email jbickle@example.com
                </address>
            </body>
            """
        self.scraper = Scraper(self.html_doc, "html.parser")


    def test_scrape_paths(self):
        paths = self.scraper.scrape_paths()
        self.assertTrue(paths = ['/elsie', '/lacie', '/tillie'])

    def test_scrape_email(self):
        emails = self.scraper.scrape_email(page_contents)
        self.assertTrue (emails = ["webmaster@example.com", "jbickle@example.com"])

if __name__ == "__main__":
    unittest.main()
