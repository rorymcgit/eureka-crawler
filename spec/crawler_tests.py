import unittest
from crawler.crawler import Crawler

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.crawler.crawl("file:///Users/vicky/Programmes/beetlecrawler/spec/website/index.html") # insert our double here!

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    # This test wont work with the local file.
    # def test_crawl_returns_status_code(self):
    #     self.assertEqual(self.crawler.page.status_code, 200)

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)
