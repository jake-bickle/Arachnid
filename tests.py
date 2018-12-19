import unittest
from scraper import Scraper, Social

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


if __name__ == "__main__":
    unittest.main()
