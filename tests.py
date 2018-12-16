import unittest
from scraper import Scraper

class test_scraper(unittest.TestCase):
    def setUp(self):
        with open("test_website/index.html") as myfile:
            self.html_doc = myfile.read()
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
