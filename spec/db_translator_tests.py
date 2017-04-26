import unittest
from crawler.db_translator import Translator
import psycopg2

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        conn = self.translator.set_environment("dbname=beetle_crawler_test")

    def tearDown(self):
        self.translator.database_cursor.execute("DELETE FROM weburls WHERE weburl='http://example.com'")

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_database_writes_urls(self):
        self.translator.write_url("http://example.com/")
        test_database_cursor = self.translator.database_cursor
        test_database_cursor.execute("SELECT * FROM weburls;")
        self.assertIn("http://example.com/", test_database_cursor.fetchone())
