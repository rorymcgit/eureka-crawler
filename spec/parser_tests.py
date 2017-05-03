import unittest
import mock
import os
from mock import MagicMock
from bs4 import BeautifulSoup
from crawler.parser import Parser

class TestingParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parser_is_instance_of_Parser(self):
        self.assertIsInstance(self.parser, Parser)

    def test_parse_webpage_content(self):
        test_soup = BeautifulSoup('<!DOCTYPE html>\n<html>\n\n<head>\n <title>Cats and Dogs</title> \n<meta name="description" content="Page about cats and dogs"> \n <meta name="keywords" content="cats,dogs">\n</head><body><a href="www.dogs.com">Dogs</a><a href="www.cats.com">Cats</a></body></html>', 'html.parser')
        self.parser.find_webpage_title = MagicMock()
        self.parser.parse_webpage_content(test_soup)
        self.parser.find_webpage_title.assert_called_once_with(test_soup)
