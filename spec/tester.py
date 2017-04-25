import unittest
from crawler.crawler import Crawler

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_crawl_is_a_function(self):
        self.crawler.crawl()
        self.assertEqual(self.crawler.page.status_code, 200)
