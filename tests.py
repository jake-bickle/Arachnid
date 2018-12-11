import unittest
import recon

# TODO Basic tests are made, need to make more 
class test_url(unittest.TestCase):
    def test_domain(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.domain(), "www.example.org")

        url = recon.URL("https://www.example.org.uk:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.domain(), "www.example.org.uk")

        url = recon.URL("https://www.example.org/")
        self.assertEqual(url.domain(), "www.example.org")

    def test_subdomain(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.subdomain(), "www")

        url = recon.URL("https://www.example.org")
        self.assertEqual(url.subdomain(), "www")

    def test_scheme(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.scheme(), "https")

    def test_path(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.path(), "/something/this.html")

        url = recon.URL("https://www.example.org:80/something/this.html#here")
        self.assertEqual(url.path(), "/something/this.html")

        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2")
        self.assertEqual(url.path(), "/something/this.html")

        url = recon.URL("https://www.example.org:80/something/this.html")
        self.assertEqual(url.path(), "/something/this.html")

    def test_port(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.port(), 80)

        url = recon.URL("https://www.example.org/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.port(), -1)
    
    def test_query(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.query(), {"param1": "value1", "param2": "value2"})

    def test_fragment(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.fragment(), "here")

    def test_homepage(self):
        url = recon.URL("https://www.example.org:80/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.homepage(), "https://www.example.org:80")

        url = recon.URL("https://www.example.org/something/this.html?param1=value1&param2=value2#here")
        self.assertEqual(url.homepage(), "https://www.example.org")

        url = recon.URL("https://www.example.org")
        self.assertEqual(url.homepage(), "https://www.example.org")


if __name__ == "__main__":
    unittest.main()
