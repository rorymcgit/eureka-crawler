import unittest
from crawler.db_translator import Translator
import psycopg2
from mock import MagicMock

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        self.conn = self.translator.set_environment("dbname=beetle_crawler_test")

    def tearDown(self):
        # self.translator.database_cursor.execute("DELETE FROM weburls;")
        # self.translator.database_cursor.execute("DELETE FROM weburlsandtitles;")
        self.translator.database.commit()
        self.translator.database_cursor.close()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_database_writes_urls(self):
        self.translator.write_url("http://example.com/")
        test_database_cursor = self.translator.database_cursor
        test_database_cursor.execute("SELECT * FROM weburls;")
        self.assertIn("http://example.com/", test_database_cursor.fetchone())

    def test_database_writes_urls_and_titles(self):
        self.translator.write_urls_and_titles("http://example.com", "title")
        test_database_cursor = self.translator.database_cursor
        test_database_cursor.execute("SELECT * FROM weburlsandtitles;")
        self.assertIn('title', test_database_cursor.fetchone())
        self.assertIn('http://example.com', test_database_cursor.fetchone())

    def test_prepare_urls_for_writing_to_db(self):
        self.translator.write_url = MagicMock()
        retrieved_weburls = ['www.dogs.com', 'www.cats.com']
        self.translator.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.translator.write_url.call_count, 2)
