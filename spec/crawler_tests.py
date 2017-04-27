import unittest
from mock import Mock
from mock import MagicMock
from crawler.crawler import Crawler
from crawler.db_translator import Translator

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        self.translator.set_environment("dbname=beetle_crawler_test")
        self.crawler = Crawler(self.translator)
        self.crawler.crawl("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_translastor_called_in_crawl(self):
        self.translator.write_url = MagicMock()
        crawler_two = Crawler(self.translator)
        crawler_two.crawl("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")
        self.translator.write_url.assert_called_once_with("file:///Users/clemcapelbird/Desktop/Projects/python-final-project/beetle-crawler/spec/website/index.html")

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)

    def test_translastor_called_in_return_content(self):
        self.translator.write_urls_and_titles = MagicMock()
        crawler_three = Crawler(self.translator)
        crawler_three.page = '<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title>\n</head></html>'
        crawler_three.url = 'http://www.google.com'
        crawler_three.return_content()
        self.translator.write_urls_and_titles.assert_called_once_with('http://www.google.com', 'Cats and Dogs')
