import unittest
import mock
import os
from mock import MagicMock
from bs4 import BeautifulSoup
from crawler.parser import Parser

class TestingParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.test_soup = BeautifulSoup('<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title> \n<meta name="description" content="Page about cats and dogs"> \n <meta name="keywords" content="cats,dogs">\n</head><body><a href="www.dogs.com">Dogs</a><a href="www.cats.com">Cats</a></body></html>', 'html.parser')
        self.bad_test_soup = BeautifulSoup('<!DOCTYPE html>\n<html>', 'html.parser')

    def test_parser_is_instance_of_Parser(self):
        self.assertIsInstance(self.parser, Parser)

    def test_parse_webpage_content_returns_dictionary(self):
        run_parse_webpage_content = self.parser.parse_webpage_content(self.test_soup)
        self.assertEqual(run_parse_webpage_content, {"title": "Cats and Dogs", "description": "Page about cats and dogs", "keywords": "cats,dogs"})

    def test_parse_webpage_content_returns_empty_dictionary_if_values_are_empty(self):
        run_parse_webpage_content = self.parser.parse_webpage_content(self.bad_test_soup)
        self.assertEqual(run_parse_webpage_content, {})

    def test_parse_webpage_content(self):
        self.parser.find_webpage_title = MagicMock()
        self.parser.parse_webpage_content(self.test_soup)
        self.parser.find_webpage_title.assert_called_once_with(self.test_soup)

    def test_parse_webpage_content_calls_webpage_metadata_description(self):
        self.parser.find_webpage_metadata = MagicMock(return_value = "keywords")
        self.parser.parse_webpage_content(self.test_soup)
        self.parser.find_webpage_metadata.assert_called_with(self.test_soup, 'keywords')

    def test_find_webpage_title_return_title(self):
        run_find_webpage_title = self.parser.find_webpage_title(self.test_soup)
        self.assertEqual(run_find_webpage_title, 'Cats and Dogs')

    def test_find_webpage_title_returns_empty_string_when_no_title(self):
        run_find_webpage_title = self.parser.find_webpage_title(self.bad_test_soup)
        self.assertEqual(run_find_webpage_title, '')

    def test_find_webpage_metadata_returns_description(self):
        run_find_webpage_metadata = self.parser.find_webpage_metadata(self.test_soup, 'description')
        self.assertEqual(run_find_webpage_metadata, 'Page about cats and dogs')

    def test_find_webpage_metadata_returns_empty_string_when_no_description(self):
        run_find_webpage_metadata = self.parser.find_webpage_metadata(self.bad_test_soup, 'description')
        self.assertEqual(run_find_webpage_metadata, '')

    def test_find_webpage_metadata_returns_keywords(self):
        run_find_webpage_metadata = self.parser.find_webpage_metadata(self.test_soup, 'keywords')
        self.assertEqual(run_find_webpage_metadata, 'cats,dogs')

    def test_find_webpage_metadata_returns_empty_string_when_no_keywords(self):
        run_find_webpage_metadata = self.parser.find_webpage_metadata(self.bad_test_soup, 'keywords')
        self.assertEqual(run_find_webpage_metadata, '')


    def test_check_empty_titles_and_descriptions_returns_true(self):
        title = ''
        description = ''
        self.assertTrue(self.parser.check_empty_titles_and_descriptions(title, description))

    def test_check_empty_titles_and_descriptions_returns_false(self):
        title = "The best website ever"
        description = "This is clearly the best website, you want to visit it"
        self.assertFalse(self.parser.check_empty_titles_and_descriptions(title, description))


    def test_parse_webpages_links_returns_an_array(self):
        run_parse_webpages_links = self.parser.parse_webpages_links(self.test_soup)
        self.assertIn("www.dogs.com", run_parse_webpages_links)
        self.assertIn("www.cats.com", run_parse_webpages_links)
