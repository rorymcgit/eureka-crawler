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
        test_url = "https://l.facebook.com/l.php?u=http%3A%2F%2Fbit.ly%2F2oIOj1d&h=ATNX92Yjs558O-DYMPJ31lQUT97uPCPCfPwZ9vUu4i7-zLT3ACP-1k_LLp5TKMLE_ZwUrkTRFvWWu6Sqo3sRZc51wD7uKcTgIRN1gf3XlBB6xqHd35ZxeHg&enc=AZOWulTNzLIKwRbWMKuj53x6BMSr61jcGJ1tdCnCjorzT1BaIo7uV-x188113_h2g5B-HUdbKrFky3bAMnh5A21v6Egd6aJNRwfs-Q8Cq3zWkZbgMYyRt_cWdpQDxrR_oUHFEdyGUU6Zl1whDgL-SBgjJXuLDUbGGKKtHJJPJhUD83_RKYkMbXGuA7tNhqyp5jz8SdneOc5iqrqIQRXylGLP&s=1"
        self.assertTrue(self.url_checker.is_low_quality_link(test_url))

    def test_is_low_quality_link_returns_false_for_good_link(self):
        test_url = "https://www.interestingwebsite.com/cool-article"
        self.assertFalse(self.url_checker.is_low_quality_link(test_url))
