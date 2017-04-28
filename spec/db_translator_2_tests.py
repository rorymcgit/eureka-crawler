import unittest
import sqlalchemy
from mock import MagicMock
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.db_translator2 import Translator


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
