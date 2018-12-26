import unittest
import re
from collections import deque
from scraper import Scraper, Social
from urlparser import UrlParser, ParseResult

import pdb

class test_scraper(unittest.TestCase):
    def setUp(self):
        with open("test_website/index.html") as myfile:
            self.html_doc = myfile.read()
        self.scraper = Scraper(self.html_doc, "html.parser")

    def test_find_all_email(self):
        emails = self.scraper.find_all_emails()
        correct_output = ["tobinshields@example.com","jakebickle@example.com", "webmaster@example.com", "jondoe@example.com"]
        self.assertEqual(sorted(emails), sorted(correct_output))

    def test_find_all_phones(self):
        phone_numbers = self.scraper.find_all_phones()
        correct_output = ["1-800-123-4567", "1-200-300-4000", "8001234567", "12-123-123-1234", "212-500-3024"]
        self.assertEqual(sorted(phone_numbers), sorted(correct_output))

    def test_find_all_documents(self):
        documents = self.scraper.find_all_documents(["txt", "docx"])
        correct_output = ["myfile.txt", "some_text.docx"]
        self.assertEqual(sorted(documents), sorted(correct_output))

        documents = self.scraper.find_all_documents(["cpp", "pdf", "pptx"])
        correct_output = ["SPECIAL_DOCUMENT.cpp", "test.pdf", "presentation.pptx"]
        self.assertEqual(sorted(documents), sorted(correct_output))

    def test_find_all_documents_no_arguments(self):
        documents = self.scraper.find_all_documents()
        correct_output = []
        self.assertEqual(documents, correct_output)

    def test_find_all_social(self):
        social = self.scraper.find_all_social()
        correct_output = [Social("https://www.linkedin.com/in/jacob-bickle"),
                          Social("https://www.facebook.com/BillGates/"),
                          Social("https://www.github.com/TobinShields"),
                          Social("https://some-person.tumblr.com/")]
        self.assertEqual(sorted(social), sorted(correct_output))

    def test_find_all_regex(self):
        visa_regex_string = r"4[0-9]{12}(?:[0-9]{3})?"
        visa_cards = self.scraper.find_all_regex(visa_regex_string)
        self.assertEqual(visa_cards, ["4123456789012345"] )

    def test_find_all_regex_tags(self):
        address_tags = self.scraper.find_all_regex(r"<address>")
        self.assertEqual(address_tags, [])

    def test_string_occurances_case_insensitive(self):
        occurances = self.scraper.string_occurances("bazinga")
        self.assertEqual(occurances, 1)

        occurances = self.scraper.string_occurances("Doesn'texist")
        self.assertEqual(occurances, 0)

    def test_string_occurances_case_sensitive(self):
        occurances = self.scraper.string_occurances("bazinga", case_sensitive=True)
        self.assertEqual(occurances, 0)

        occurances = self.scraper.string_occurances("Bazinga", case_sensitive=True)
        self.assertEqual(occurances, 1)

        occurances = self.scraper.string_occurances("Doesn'texist")
        self.assertEqual(occurances, 0)

    def test_string_occurances_of_tags(self):
        occurances = self.scraper.string_occurances("<p>")
        self.assertEqual(occurances, 0)


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
        url1 = "https://social.example.com"
        url2 = "https://www.example.com"
        self.assertTrue(UrlParser.is_subdomain(url1, url2))

    def test_is_subdomain_parsed_results(self):
        url1 = "https://social.example.com"
        url2 = "https://www.example.com"
        url1 = UrlParser.parse_url(url1)
        url2 = UrlParser.parse_url(url2)
        self.assertTrue(UrlParser.is_subdomain(url1, url2))

    def test_is_subdomain_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(UrlParser.is_subdomain(url1, url2))

    def test_is_subdomain_same_website(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(UrlParser.is_subdomain(url1, url2))

    def test_same_subdomain_true(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertTrue(UrlParser.same_domain(url1, url2))

    def test_same_subdomain_different_suffix(self):
        url1 = "https://www.example.org/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(UrlParser.same_domain(url1, url2))

    def test_same_subdomain_different_domain(self):
        url1 = "https://www.myexample.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(UrlParser.same_domain(url1, url2))

    def test_same_netloc_true(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertTrue(UrlParser.same_netloc(url1, url2))

    def test_same_netloc_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(UrlParser.same_netloc(url1, url2))

from urlparser import SocialMediaParser
class test_social_media_parser(unittest.TestCase):
    def test_parse_facebook_profile(self):
        url = "https://www.facebook.com/jake-bickle"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_facebook_profile_too_few_paths(self):
        url = "https://www.facebook.com/"
        self.assertFalse(SocialMediaParser.is_profile(url))

    def test_parse_facebook_profile_too_many_dirs(self):
        url = "https://www.facebook.com/some/random/location"
        self.assertFalse(SocialMediaParser.is_profile(url))

    def test_parse_instagram_profile_with_params_query_frag(self):
        url = "https://www.instagram.com/jake-bickle?lang=en;key=value#here"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_twitch_profile(self):
        url = "https://www.twitch.com/jake-bickle"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_github_profile(self):
        url = "https://www.github.com/jake-bickle"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_non_social_media(self):
        url = "https://www.non-media.com/location"
        self.assertFalse(SocialMediaParser.is_profile(url))

    def test_parse_flickr_profile(self):
        url = "https://www.flickr.com/photos/tobin-shields"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_flickr_profile_too_many_dirs(self):
        url = "https://www.flickr.com/photos/path/to/location"
        self.assertFalse(SocialMediaParser.is_profile(url))

    def test_parse_flickr_profile_wrong_dir(self):
        url = "https://www.flickr.com/some/location"
        self.assertFalse(SocialMediaParser.is_profile(url))

    def test_parse_linkedin_profile(self):
        url = "https://www.linkedin.com/in/tobin-shields"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_tumblr_profile(self):
        url = "https://some-profile.tumblr.com/"
        self.assertTrue(SocialMediaParser.is_profile(url))

    def test_parse_tumblr_profile_with_normal_subdomain(self):
        url = "https://www.tumblr.com/"
        self.assertFalse(SocialMediaParser.is_profile(url))


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
