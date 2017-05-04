import unittest
from crawler.url_checker import URLChecker

class TestingURLChecker(unittest.TestCase):

    def setUp(self):
        self.url_checker = URLChecker()


    def test_url_checker_is_instance_of_URLChecker(self):
        self.assertIsInstance(self.url_checker, URLChecker)


    def test_url_is_valid_returns_true_only_for_http_link(self):
        returned_with_valid_url = self.url_checker.url_is_http('https://www.example.com/')
        self.assertEqual(returned_with_valid_url, True)

    def test_url_is_valid_returns_false_only_for_non_http_link(self):
        returned_with_invalid_url = self.url_checker.url_is_http('www.example.com/')
        self.assertEqual(returned_with_invalid_url, False)

    def test_url_is_valid_saves_only_urls_ending_com_or_uk(self):
        self.assertEqual(self.url_checker.url_domain_is_good('https://www.example.com/'), True)
        self.assertEqual(self.url_checker.url_domain_is_good('https://www.example.co.uk/'), True)
        self.assertEqual(self.url_checker.url_domain_is_good('https://www.example.org/'), True)
        self.assertEqual(self.url_checker.url_domain_is_good('https://www.example.cz/'), False)


    def test_is_low_quality_link_returns_true_for_bad_link(self):
        test_url = "https://l.facebook.com/l.php?u=http%3A%2F%"
        self.assertTrue(self.url_checker.is_low_quality_link(test_url))

    def test_is_low_quality_link_returns_false_for_good_link(self):
        test_url = "https://www.interestingwebsite.com/cool-article"
        self.assertFalse(self.url_checker.is_low_quality_link(test_url))
