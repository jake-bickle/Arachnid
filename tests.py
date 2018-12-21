import unittest
from collections import deque
from scraper import Scraper, Social
from urlparser import UrlParser, ParseResult

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
        correct_output = ["jakebickle@example.com", "webmaster@example.com", "jondoe@example.com"]
        self.assertEqual(sorted(emails), correct_output)

    def test_find_all_phones(self):
        phone_numbers = self.scraper.find_all_phones()
        correct_output = ["1-800-123-4567","1-200-300-4000", "180012344567", "(1)212-500-3024", "212-500-3024" ]
        self.assertEqual(sorted(phone_numbers), sorted(correct_output))

    def test_find_all_documents(self):
        documents = self.scraper.find_all_documents()
        correct_output = ["myfile.txt", "some_text.docx"]
        self.assertEqual(sorted(documents), sorted(correct_output))

    def test_find_all_social(self):
        social = self.scraper.find_all_social()
        correct_output = [Social("https://www.linkedin.com/in/jacob-bickle"),
                          Social("https://www.facebook.com/BillGates/"),
                          Social("https://www.github.com/TobinShields")]
        self.assertEqual(sorted(social), sorted(correct_output))

    def test_find_all_regex(self):
        visa_regex = re.compilie(r"^4[0-9]{12}(?:[0-9]{3})?$")
        visa_cards = self.find_all_regex(visa_regex)
        self.assertEqual(visa_cards, ["4123456789012345"] )

    def test_find_all_regex_tags(self):
        address_tags = self.find_all_regex(r"<address>")
        self.asserEqual(address_tags, ["<address>"])

    def test_string_occurances_case_insensitive(self):
        has_string = self.string_occurances("bazinga")
        self.assertTrue(has_string)

        has_string = self.string_occurances("Doesn'texist")
        self.assertFalse(has_string)

    def test_string_occurances_case_sensitive(self):
        has_string = self.string_occurances("bazinga")
        self.assertFalse(has_string)

        has_string = self.string_occurances("Bazinga")
        self.assertTrue(has_string)

    def test_string_occurances_of_tags(self):
        has_string = self.string_occurances("<p>")
        self.assertFalse(has_string)


class test_urlparser(unittest.TestCase):
    def test_parse_url_with_all_components(self):
        url = "https://www.example.com/path/to/location;param1=value1&param2=value2?param3=value3#frag"
        result = UrlParser.parse_url(url)
        correct_output = ParseResult("https", "www", "example", "com", "/path/to/location", "param1=value1&param2=value2", "param3=value3", "frag")
        self.assertEqual(result, correct_output)

    def test_parse_url_with_some_components(self):
        url = "https://www.example.com/path/to/location"
        result = UrlParser.parse_url(url)
        correct_output = ParseResult("https", "www", "example", "com", "/path/to/location", "", "", "")
        self.assertEqual(result, correct_output)

    def test_get_url_with_all_components(self):
        url = "https://www.example.com/path/to/location;param1=value1&param2=value2?param3=value3#frag"
        result = UrlParser.parse_url(url).get_url()
        self.assertEqual(result, url)

    def test_get_url_with_some_components(self):
        url = "https://www.example.com/path/to/location"
        result = UrlParser.parse_url(url).get_url()
        self.assertEqual(result, url)

    def test_is_subdomain_true(self):
        url1 = "https://www.example.com"
        url2 = "https://www.example.io"
        self.assertTrue(UrlParser.is_subdomain(url1, url2))

    def test_is_subdomain_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(UrlParser.is_subdomain(url1, url2))

    def test_is_subdomain_same_website(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(UrlParser.is_subdomain(url1, url2))

    def test_same_netloc_true(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertTrue(UrlParser.same_netloc(url1, url2))

    def test_same_netloc_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(UrlParser.same_netloc(url1, url2))

from crawler import Path_Scheduler
class test_path_scheduler(unittest.TestCase):
    def test_add_new_path(self):
        example_site = Path_Scheduler("https://www.example.com")
        example_site.add_path("/path/to/location")
        self.assertEqual(example_site.paths_to_crawl, deque(["/path/to/location"]))

    def test_add_existing_uncrawled_path(self):
        example_site = Path_Scheduler("https://www.example.com")
        path = "/path/to/location"
        example_site.add_path(path)
        self.assertFalse(example_site.add_path(path))

    def test_add_existing_crawled_path(self):
        example_site = Path_Scheduler("https://www.example.com")
        path = "/path/to/location"
        example_site.add_path(path)
        example_site.next_path()
        self.assertFalse(example_site.add_path(path))

    def test_next_path(self):
        example_site = Path_Scheduler("https://www.example.com")
        path = "/path/to/location"
        example_site.add_path(path)
        self.assertEqual(example_site.next_path(), path)

    def test_next_path_empty_container(self):
        example_site = Path_Scheduler("https://www.example.com")
        self.assertEqual(example_site.next_path(), None)

if __name__ == "__main__":
    unittest.main()
