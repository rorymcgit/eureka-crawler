import unittest
from mock import MagicMock
from crawler.url_checker import URLChecker

class TestingURLChecker(unittest.TestCase):

    def setUp(self):
        self.url_checker = URLChecker()

    def test_url_checker_is_instance_of_URLChecker(self):
        self.assertIsInstance(self.url_checker, URLChecker)



    def test_url_is_valid_saves_only_urls_beginning_http(self):
        self.assertEqual(self.url_checker.check_url_beginning('https://www.example.com/'), True)
        self.assertEqual(self.url_checker.check_url_beginning('www.example.com/'), False)

    def test_url_is_valid_saves_only_urls_ending_com_or_uk(self):
        self.assertEqual(self.url_checker.check_url_domain('https://www.example.com/'), True)
        self.assertEqual(self.url_checker.check_url_domain('https://www.example.co.uk/'), True)
        self.assertEqual(self.url_checker.check_url_domain('https://www.example.org/'), True)
        self.assertEqual(self.url_checker.check_url_domain('https://www.example.cz/'), False)
