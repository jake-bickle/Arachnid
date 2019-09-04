import unittest
from crawler.scraper import Scraper

from crawler.crawler_url import ParseResult
class test_urlparser(unittest.TestCase):
    def test_parse_url_with_all_components(self):
        url = "https://www.example.com/path/to/location;param1=value1&param2=value2?param3=value3#frag"
        result = url.parse_url(url)
        correct_output = ParseResult("https", "www", "example", "com", "/path/to/location", "param1=value1&param2=value2", "param3=value3", "frag")
        self.assertEqual(result, correct_output)

    def test_parse_url_with_some_components(self):
        url = "https://www.example.com/path/to/location"
        result = url.parse_url(url)
        correct_output = ParseResult("https", "www", "example", "com", "/path/to/location", "", "", "")
        self.assertEqual(result, correct_output)

    def test_get_url_with_all_components(self):
        url = "https://www.example.com/path/to/location;param1=value1&param2=value2?param3=value3#frag"
        result = url.parse_url(url).get_url()
        self.assertEqual(result, url)

    def test_get_url_with_some_components(self):
        url = "https://www.example.com/path/to/location"
        result = url.parse_url(url).get_url()
        self.assertEqual(result, url)

    def test_is_subdomain_true(self):
        url1 = "https://social.example.com"
        url2 = "https://www.example.com"
        self.assertTrue(crawler_url.is_subdomain(url1, url2))

    def test_is_subdomain_parsed_results(self):
        url1 = "https://social.example.com"
        url2 = "https://www.example.com"
        url1 = crawler_url.parse_url(url1)
        url2 = crawler_url.parse_url(url2)
        self.assertTrue(crawler_url.is_subdomain(url1, url2))

    def test_is_subdomain_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(crawler_url.is_subdomain(url1, url2))

    def test_is_subdomain_same_website(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(crawler_url.is_subdomain(url1, url2))

    def test_same_subdomain_true(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertTrue(crawler_url.same_domain(url1, url2))

    def test_same_subdomain_different_suffix(self):
        url1 = "https://www.example.org/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(crawler_url.same_domain(url1, url2))

    def test_same_subdomain_different_domain(self):
        url1 = "https://www.myexample.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertFalse(crawler_url.same_domain(url1, url2))

    def test_same_netloc_true(self):
        url1 = "https://www.example.com/path"
        url2 = "https://www.example.com/path/to/location"
        self.assertTrue(crawler_url.same_netloc(url1, url2))

    def test_same_netloc_false(self):
        url1 = "https://www.example.com"
        url2 = "https://www.otherwebsite.com"
        self.assertFalse(crawler_url.same_netloc(url1, url2))

class test_social_media_parser(unittest.TestCase):
    def test_parse_facebook_profile(self):
        url = "https://www.facebook.com/jake-bickle"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_facebook_profile_too_few_paths(self):
        url = "https://www.facebook.com/"
        self.assertFalse(url.is_social_media_profile(url))

    def test_parse_facebook_profile_too_many_dirs(self):
        url = "https://www.facebook.com/some/random/location"
        self.assertFalse(url.is_social_media_profile(url))

    def test_parse_instagram_profile_with_params_query_frag(self):
        url = "https://www.instagram.com/jake-bickle?lang=en;key=value#here"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_twitch_profile(self):
        url = "https://www.twitch.com/jake-bickle"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_github_profile(self):
        url = "https://www.github.com/jake-bickle"
        self.assertTrue(url.is_social_media_profile(url))

    def test_non_social_media(self):
        url = "https://www.non-media.com/location"
        self.assertFalse(url.is_social_media_profile(url))

    def test_parse_flickr_profile(self):
        url = "https://www.flickr.com/photos/tobin-shields"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_flickr_profile_too_many_dirs(self):
        url = "https://www.flickr.com/photos/path/to/location"
        self.assertFalse(url.is_social_media_profile(url))

    def test_parse_flickr_profile_wrong_dir(self):
        url = "https://www.flickr.com/some/location"
        self.assertFalse(url.is_social_media_profile(url))

    def test_parse_linkedin_profile(self):
        url = "https://www.linkedin.com/in/tobin-shields"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_tumblr_profile(self):
        url = "https://some-profile.tumblr.com/"
        self.assertTrue(url.is_social_media_profile(url))

    def test_parse_tumblr_profile_with_normal_subdomain(self):
        url = "https://www.tumblr.com/"
        self.assertFalse(url.is_social_media_profile(url))

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

    def test_find_all_social(self):
        social = self.scraper.find_all_social()
        correct_output = [{"link": "https://www.linkedin.com/in/jacob-bickle", "domain": "linkedin"},
                          {"link": "https://www.facebook.com/BillGates/", "domain": "facebook"},
                          {"link": "https://some-person.tumblr.com/", "domain": "tumblr"},
                          {"link": "https://www.github.com/TobinShields", "domain": "github"}]
        self.assertEqual(social, correct_output)

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


# from crawler import Path_Scheduler
# class test_path_scheduler(unittest.TestCase):
    # def test_add_new_path(self):
        # example_site = Path_Scheduler("https://www.example.com")
        # example_site.add_path("/path/to/location")
        # self.assertEqual(example_site.paths_to_crawl, deque(["/path/to/location"]))

    # def test_add_existing_uncrawled_path(self):
        # example_site = Path_Scheduler("https://www.example.com")
        # path = "/path/to/location"
        # example_site.add_path(path)
        # self.assertFalse(example_site.add_path(path))

    # def test_add_existing_crawled_path(self):
        # example_site = Path_Scheduler("https://www.example.com")
        # path = "/path/to/location"
        # example_site.add_path(path)
        # example_site.next_path()
        # self.assertFalse(example_site.add_path(path))

    # def test_next_path(self):
        # example_site = Path_Scheduler("https://www.example.com")
        # path = "/path/to/location"
        # example_site.add_path(path)
        # self.assertEqual(example_site.next_path(), path)

    # def test_next_path_empty_container(self):
        # example_site = Path_Scheduler("https://www.example.com")
        # self.assertEqual(example_site.next_path(), None)

from crawler.scheduler import DomainBlock
from collections import deque
class test_domain_block(unittest.TestCase):
    def test_constructor_extensions_to_crawl_base_directory(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/")
        block = DomainBlock(parsed_url)
        correct_output = deque(["/"])
        self.assertEqual(block.pages_to_crawl, correct_output)

    def test_constructor_extensions_to_crawl_no_path(self):
        parsed_url = crawler_url.parse_url("https://www.example.com")
        block = DomainBlock(parsed_url)
        correct_output = deque(["/"])
        self.assertEqual(block.pages_to_crawl, correct_output)

    def test_constructor_extensions_to_crawl_with_path(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        correct_output = deque(["/path/to/location"])
        self.assertEqual(block.pages_to_crawl, correct_output)

    def test_add_extension(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        block.add_page("/other/path")
        correct_output = deque(["/path/to/location", "/other/path"])
        self.assertEqual(sorted(block.pages_to_crawl), sorted(correct_output))

    def test_add_extension_already_added(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        block.add_page("/other/path")
        correct_output = deque(["/path/to/location", "/other/path"])
        self.assertFalse(block.add_page("/other/path"))

    def test_next_url(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        correct_output = "https://www.example.com/path/to/location"
        self.assertEqual(block.next_url(), correct_output)

    def test_next_next_url_multiple_adds(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        block.add_page("/other/page")
        block.add_page("/other")
        correct_output = "https://www.example.com/other"
        self.assertEqual(block.next_url(), correct_output)

    def test_next_url_empty(self):
        parsed_url = crawler_url.parse_url("https://www.example.com/path/to/location")
        block = DomainBlock(parsed_url)
        block.next_url()
        self.assertFalse(block.next_url())

from crawler.scheduler import Scheduler
class test_scheduler(unittest.TestCase):
    def test_schedule_one_url(self):
        schedule = Scheduler("https://www.example.com/path/to/location") # Constructor calls upon schedule_url
        block = schedule.blocks_to_crawl.pop()
        ext = block.extensions_to_crawl[0]
        correct_output = "/path/to/location"
        self.assertEqual(ext, correct_output)

    def test_schedule_multiple_url_same_netloc(self):
        schedule = Scheduler("https://www.example.com/path/to/location") # Constructor calls upon schedule_url
        schedule.schedule_url("https://www.example.com/path/to")
        block = schedule.blocks_to_crawl.pop()
        correct_output = deque(["/path/to", "/path/to/location"])
        self.assertEqual(sorted(block.extensions_to_crawl), sorted(correct_output))

    def test_schedule_multiple_url_different_subdomain(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        schedule.schedule_url("https://www.example.com/path/to")
        www_example = schedule.blocks_to_crawl.pop()
        my_example = schedule.blocks_to_crawl.pop()
        self.assertNotEqual(www_example, my_example)
        self.assertTrue(www_example.next_url())
        self.assertTrue(my_example.next_url())

    def test_schedule_same_url_twice(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.com/path/to/location")
        self.assertFalse(has_been_scheduled)

    def test_schedule_url_different_domain(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.org/path/to/location")
        self.assertFalse(has_been_scheduled)

    def test_schedule_url_fragment(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.com/path/to/location#maincontent")
        self.assertTrue(has_been_scheduled)

    def test_schedule_url_query(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.com/path/to/location?key=val")
        self.assertTrue(has_been_scheduled)

    def test_schedule_url_params(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.com/path/to/location;key=val")
        self.assertTrue(has_been_scheduled)

    def test_schedule_url_variety(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        has_been_scheduled = schedule.schedule_url("https://my.example.com/path/to/location?key1=val1;key2=val2#frag")
        self.assertTrue(has_been_scheduled)

    def test_next_url(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        correct_output = "https://my.example.com/path/to/location"
        self.assertEqual(schedule.next_url(), correct_output)

    def test_next_url_empty_queue(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        schedule.next_url()
        self.assertFalse(schedule.next_url())

    def test_next_url_new_domain_block(self):
        my_example = "https://my.example.com/"
        www_example = "https://www.example.com/"
        schedule = Scheduler(my_example) # Constructor calls upon schedule_url
        schedule.schedule_url(www_example)
        self.assertEqual(schedule.next_url(), my_example)
        self.assertEqual(schedule.next_url(), www_example)

    def test_next_url_extensions(self):
        schedule = Scheduler("https://my.example.com/path/to/location") # Constructor calls upon schedule_url
        schedule.schedule_url("https://my.example.com/path/to/location?key=val;word=bird#frag")
        correct_output = "https://my.example.com/path/to/location?key=val;word=bird#frag" 
        self.assertEqual(schedule.next_url(), correct_output)

    def test_schedule_url_already_crawled(self):
        url = "https://my.example.com/path/to/location"
        schedule = Scheduler(url) # Constructor calls upon schedule_url
        schedule.next_url()
        self.assertFalse(schedule.schedule_url(url))


from crawler import CrawlerConfig, crawler_url
import arachnid_enums


class test_responseparser(unittest.TestCase):
    pass


from arachnid import generate_crawler_config, parser


class test_generate_config(unittest.TestCase):
    def get_namespace(self, cli):
        return parser.parse_args(cli.split())

    def test_default(self):
        cli = "https://www.example.com"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        self.assertEqual(vars(c), vars(CrawlerConfig()))

    def test_aggressive(self):
        cli = "https://www.example.com --aggressive"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.set_aggressive()
        self.assertEqual(vars(c), vars(correct_output))

    def test_stealth(self):
        cli = "https://www.example.com --stealth"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.set_stealth()
        self.assertEqual(vars(c), vars(correct_output))

    def test_delay(self):
        cli = "https://www.example.com -T high"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.default_delay = arachnid_enums.Delay.HIGH.value

    def test_stealth_modified(self):
        cli = "https://www.example.com -T none --stealth"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.set_stealth()
        correct_output.default_delay = arachnid_enums.Delay.NONE.value
        self.assertEqual(vars(c), vars(correct_output))

    def test_agent(self):
        cli = "https://www.example.com -a g"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.agent = arachnid_enums.Agent.GOOGLE.value
        self.assertEqual(vars(c), vars(correct_output))
    
    def test_doc(self):
        cli = "https://www.example.com --doc zip"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.documents.add("zip")
        self.assertEqual(vars(c), vars(correct_output))

    def test_doc_and_no_docs(self):
        cli = "https://www.example.com --find phone email social --doc zip"
        namespace = self.get_namespace(cli)
        c = generate_crawler_config(namespace)
        correct_output = CrawlerConfig()
        correct_output.documents = {"zip"}
        self.assertEqual(vars(c), vars(correct_output))

    class test_find(unittest.TestCase):
        def get_namespace(self, cli):
            return parser.parse_args(cli.split())

        def test_none(self):
            cli = "https://www.example.com --find none"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number  = False
            correct_output.scrape_email = False
            correct_output.scrape_social_media  = False
            correct_output.documents = {}
            self.assertEqual(vars(c), vars(correct_output))

        def test_all(self):
            cli = "https://www.example.com --find all"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            self.assertEqual(vars(c), vars(correct_output))

        def test_docs(self):
            cli = "https://www.example.com --find docs"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number = False
            correct_output.scrape_email = False
            correct_output.scrape_social_media  = False
            self.assertEqual(vars(c), vars(correct_output))

        def test_social_media(self):
            cli = "https://www.example.com --find social"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number = False
            correct_output.scrape_email = False
            correct_output.scrape_social_media  = True
            correct_output.documents = {}
            self.assertEqual(vars(c), vars(correct_output))

        def test_phone_number(self):
            cli = "https://www.example.com --find phone"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number = True
            correct_output.scrape_email = False
            correct_output.scrape_social_media  = False
            correct_output.documents = {}
            self.assertEqual(vars(c), vars(correct_output))

        def test_email(self):
            cli = "https://www.example.com --find email"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number = False
            correct_output.scrape_email = True
            correct_output.scrape_social_media  = False
            correct_output.documents = {}
            self.assertEqual(vars(c), vars(correct_output))

        def test_multiple(self):
            cli = "https://www.example.com --find email phone social docs"
            namespace = self.get_namespace(cli)
            c = generate_crawler_config(namespace)
            correct_output = CrawlerConfig()
            correct_output.scrape_phone_number = True
            correct_output.scrape_email = True
            correct_output.scrape_social_media  = True
            self.assertEqual(vars(c), vars(correct_output))


if __name__ == "__main__":
    unittest.main()
