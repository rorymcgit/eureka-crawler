import unittest
from mock import Mock
from mock import MagicMock
from crawler.crawler import Crawler
from crawler.db_translator import Translator

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        translator2 = Translator()
        self.crawler = Crawler(translator2)
        self.crawler.crawl("file:///Users/Hyper/git/beetle-crawler/spec/website/index.html")

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_translastor_called_in_crawl(self):
        translator = Translator()
        translator.write_url = MagicMock()
        crawler2 = Crawler(translator)
        crawler2.crawl("file:///Users/Hyper/git/beetle-crawler/spec/website/index.html")
        translator.write_url.assert_called_once_with("file:///Users/Hyper/git/beetle-crawler/spec/website/index.html")

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)
