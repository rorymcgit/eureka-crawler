import unittest
from mock import Mock
from mock import MagicMock
from crawler.crawler import Crawler
from crawler.db_translator import Translator
from bs4 import BeautifulSoup
import os

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.translator = MagicMock()
        self.crawler = Crawler(self.translator)
        self.local_html_file = "file://" + (os.path.abspath("spec/website/index.html"))
        self.crawler.crawl(self.local_html_file)

    def test_crawler_is_instance_of_crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_translator_called_in_crawl(self):
        self.translator.write_url = MagicMock()
        self.crawler.crawl(self.local_html_file)
        self.translator.write_url.assert_called_once_with(self.local_html_file)

    def test_crawl_returns_content(self):
        self.crawler.return_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)

    def test_translator_called_in_return_content(self):
        self.translator.write_urls_and_titles = MagicMock()
        self.crawler.page = '<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title>\n</head></html>'
        self.crawler.url = 'http://www.google.com'
        self.crawler.return_content()
        self.translator.write_urls_and_titles.assert_called_once_with('http://www.google.com', 'Cats and Dogs')

    def test_return_content_saves_all_urls_from_webpage(self):
        self.crawler.return_content()
        self.assertIn("www.dogs.com", self.crawler.webpage_urls)

    def test_translator_called_in_save_found_weburls(self):
        self.translator.prepare_urls_for_writing_to_db = MagicMock()
        self.crawler.soup = BeautifulSoup('<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title>\n</head><body><a href="www.dogs.com">Dogs</a><a href="www.cats.com">Cats</a></body></html>', 'html.parser')
        self.crawler.save_found_weburls()
        test_urls_array = ['www.dogs.com', 'www.cats.com']
        self.translator.prepare_urls_for_writing_to_db.assert_called_once_with(test_urls_array)

    def test_crawl_returns_all_content(self):
        self.crawler.return_all_content()
        self.assertIn("Cats and Dogs", self.crawler.webpage_title)
        self.assertIn("Page about cats and dogs", self.crawler.webpage_description)
        self.assertIn("cats,dogs", self.crawler.webpage_keywords)

    def test_translator_called_in_return_all_content(self):
        self.translator.write_urls_and_content = MagicMock()
        self.crawler.return_all_content()
        self.translator.write_urls_and_content.assert_called_once_with(self.local_html_file, 'Cats and Dogs', 'Page about cats and dogs', 'cats,dogs')
