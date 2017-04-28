import unittest
import sqlalchemy
from mock import MagicMock
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.db_translator import Translator


class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator('postgresql://localhost/beetle_crawler_test')
        self.test_database_connection = self.translator.connection

    def tearDown(self):
        delete_table = delete(self.translator.weburls)
        self.translator.connection.execute(delete_table)
        self.translator.connection.close()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_database_writes_urls(self):
        self.translator.write_url("translator2test.com")
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('translator2test.com', results.fetchone()['weburl'])

    def test_prepare_urls_for_writing_to_db(self):
        self.translator.write_url = MagicMock()
        retrieved_weburls = ['www.dogs.com', 'www.cats.com']
        self.translator.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.translator.write_url.call_count, 2)

    def test_prepare_urls_for_writing_to_db_WONT_exceed_database_limit(self):
        self.translator.get_database_size = MagicMock(return_value=1000)
        self.assertRaises(Exception, self.translator.prepare_urls_for_writing_to_db, ['www.somecats.com'])

    def test_database_writes_urls_and_content(self):
        self.translator.write_urls_and_content("http://example.com", "example title", "example description", "example keywords")
        statement = select([self.translator.weburlsandcontent])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://example.com', results.fetchone()['weburl'])
        self.assertIn('example title', results.fetchone()['title'])
        self.assertIn('example description', results.fetchone()['description'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example keywords', results.fetchone()['keywords'])
