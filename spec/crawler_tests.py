import unittest
from mock import Mock
from mock import MagicMock
from crawler.crawler import Crawler
from crawler.db_translator import Translator

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        translator2 = Translator()
        self.crawler = Crawler(translator2)
        self.crawler.crawl("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_translastor_called_in_crawl(self):
        translator = Translator()
        translator.write_url = MagicMock()
        crawler2 = Crawler(translator)
        crawler2.crawl("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")
        translator.write_url.assert_called_once_with("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)

    def test_translastor_called_in_return_content(self):
        translator3 = Translator()
        translator3.write_urls_and_titles = MagicMock()
        crawler2 = Crawler(translator3)
        crawler2.page = '<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title>\n</head></html>'
        crawler2.url = 'http://www.google.com'
        crawler2.return_content()
        translator3.write_urls_and_titles.assert_called_once_with('http://www.google.com', 'Cats and Dogs')
