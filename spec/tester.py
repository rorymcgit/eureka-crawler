import unittest
from crawler.crawler import Crawler

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.crawler.crawl("https://en.wikipedia.org/wiki") # insert our double here!

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_crawl_returns_status_code(self):
        self.assertEqual(self.crawler.response_page.status_code, 200)

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Wikipedia", self.crawler.webpage_title)
