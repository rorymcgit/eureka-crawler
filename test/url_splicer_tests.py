import unittest
from mock import MagicMock
from crawler.url_splicer import URLSplicer

class TestingURLSplicer(unittest.TestCase):

    def setUp(self):
        self.url_splicer = URLSplicer()

    def test_url_splicer_is_instance_of_URLSplicer(self):
        self.assertIsInstance(self.url_splicer, URLSplicer)


    def test_find_nth_finds_nth_character_in_string(self):
        find_nth_example = self.url_splicer.find_nth('https://www.example.com/home/page', '/', 3)
        self.assertEqual(find_nth_example, 28)


    def test_cut_url_cuts_url_at_fourth_forward_slash(self):
        self.url_splicer.find_nth = MagicMock(return_value = 28)
        url_to_cut = self.url_splicer.cut_url('https://www.example.com/home/page')
        self.assertEqual(url_to_cut, 'https://www.example.com/home')
