import unittest
from crawler.url_splicer import URLSplicer

class TestingURLSplicer(unittest.TestCase):

    def setUp(self):
        self.url_splicer = URLSplicer()

    def test_url_splicer_is_instance_of_URLSplicer(self):
        self.assertIsInstance(self.url_splicer, URLSplicer)

    
