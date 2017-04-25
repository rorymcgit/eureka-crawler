import unittest
from crawler.test import hello

class TestingCrawler(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(hello("hellooo"), "hellooo")
