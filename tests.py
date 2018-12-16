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
                <a href="/direct/path">Link</a>
                <a href="relative/path">Link</a>
                and they lived at the bottom of a well.</p>

                <p class="story">...</p>

                <a href="tel:1-800-123-4567">Call this number for any questions about this story.</a>
                <a href="tel:0-123-4567">This number is fake, don't scrape it.</a>
                <ul>The following phone numbers are plain text
                    <li> 1-200-300-4000 </li>
                    <li> 180012344567 </li>
                    <li> (1) 500-3024 </li>
                    <li> (1) 212-500-3024 </li>
                    <li> 212-500-3024 </li>
                </ul>
                <ul>These phone numbers are bogus
                    <li> 12-123-123-1234 </li>
                    <li> 123-123-12343 </li>
                    <li> 23-123-1234 </li>
                    <li> 123-1231-1234 </li>
                    <li> 1231-1234 </li>
                </ul>

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


    def test_find_all_paths(self):
        paths = self.scraper.find_all_paths()
        correct_output = ['/elsie', '/lacie', '/tillie', 'relative/path', "/direct/path"]
        self.assertEqual(sorted(correct_output), sorted(paths))

    def test_find_all_email(self):
        emails = self.scraper.find_all_emails()
        correct_output = ["jbickle@example.com", "webmaster@example.com"]
        self.assertEqual(sorted(emails), correct_output)

    def test_find_all_phones(self):
        phone_numbers = self.scraper.find_all_phones()
        correct_output = ["1-800-123-4567","1-200-300-4000", "180012344567", "(1) 500-3024","(1) 212-500-3024", "212-500-3024" ]
        self.assertEqual(sorted(phone_numbers), sorted(correct_output))

    def test_find_all_documents(self):
        documents = self.scraper.find_all_documents()

    def test_find_all_regex(self):
        occurances = self.find_all_regex("some regex")

    def test_find_all_regex_tags(self):
        occurances = self.find_all_regex(r"<p>")
        self.asserEqual(occurances, [])

    def test_has_string_occurance_case_insensitive(self):
        has_string = self.has_string_occurance("lacie")
        self.assertTrue(has_string)

        has_string = self.has_string_occruance("Doesn'texist")
        self.assertFalse(has_string)

    def test_has_string_occurance_case_sensitive(self):
        has_string = self.has_string_occurance("lacie")
        self.assertFalse(has_string)

        has_string = self.has_string_occurance("Lacie")
        self.assertTrue(has_string)

    def test_has_string_occurance_tags(self):
        has_string = self.has_string_occurance("<p>")
        self.assertFalse(has_string)


if __name__ == "__main__":
    unittest.main()
