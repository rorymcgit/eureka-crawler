import unittest
import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.db_translator2 import Translator

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator('postgresql://localhost/beetle_crawler_test')
        self.test_database_connection = self.translator.connection


    def tearDown(self):
        # statement = select([self.translator.weburls])
        # _delete = delete(statement)
        # self.translator.connection.execute(_delete)
        self.translator.connection.close()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_database_writes_urls(self):
        self.translator.write_url("translator2test.com")
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('translator2test.com', results.fetchone()['weburl'])
