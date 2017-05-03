import unittest
from mock import Mock
from mock import MagicMock
from crawler.crawler import Crawler
from bs4 import BeautifulSoup
import os

class TestingCrawler(unittest.TestCase):

    def setUp(self):
        self.translator = MagicMock()
        self.parser = MagicMock()
        self.translator.get_weburls_table_size = MagicMock(return_value=50)
        self.translator.get_weburls_and_content_table_size = MagicMock(return_value=10)
        self.translator.get_next_url = MagicMock(return_value = None)
        self.translator.both_tables_are_not_full_yet = MagicMock(return_value=False)
        self.translator.database_limit = 10
        self.crawler = Crawler(self.translator, self.parser)
        self.local_index_html_file = "file://" + os.path.abspath("spec/website/index.html")
        self.crawler.crawl(self.local_index_html_file)

    def get_test_soup(self):
        test_soup = BeautifulSoup('<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title> \n<meta name="description" content="Page about cats and dogs"> \n <meta name="keywords" content="cats,dogs">\n</head><body><a href="www.dogs.com">Dogs</a><a href="www.cats.com">Cats</a></body></html>', 'html.parser')
        return test_soup

    def test_crawler_is_instance_of_Crawler(self):
        self.assertIsInstance(self.crawler, Crawler)

    def test_crawl_calls_translator_write_url(self):
        self.translator.write_url = MagicMock()
        self.crawler.crawl(self.local_index_html_file)
        self.translator.write_url.assert_called_once_with(self.local_index_html_file)

    def test_crawl_accepts_and_assigns_url(self):
        self.assertEqual(self.crawler.url, self.local_index_html_file)


    def test_return_all_content_calls_translator_write_urls_and_content(self):
        self.crawler.translator.write_urls_and_content = MagicMock()
        self.crawler.return_all_content()
        self.crawler.translator.write_urls_and_content.assert_called_once()

    def test_return_all_content_calls_crawl_next_url(self):
        self.crawler.crawl_next_url = MagicMock()
        self.crawler.return_all_content()
        self.crawler.crawl_next_url.assert_called_once()

    def test_return_all_content_calls_parser_create_soup_and_save_content(self):
        self.crawler.page = bytes()
        self.crawler.save_found_weburls = MagicMock()
        self.parser.create_soup_and_save_content = MagicMock()
        self.crawler.return_all_content()
        self.parser.create_soup_and_save_content.assert_called_once()

    def test_save_found_weburls_calls_translator_prepare_urls_for_writing_to_db(self):
        self.translator.prepare_urls_for_writing_to_db = MagicMock()
        self.crawler.save_found_weburls()
        test_urls_array = ["www.dogs.com", "www.cats.com"]
        self.translator.prepare_urls_for_writing_to_db.assert_called_once()

    def test_crawl_next_url_calls_translator_get_next_url(self):
        self.crawler.crawl_next_url()
        self.translator.get_next_url.assert_called()
