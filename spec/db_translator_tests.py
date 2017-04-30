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
        delete_weburl_table = delete(self.translator.weburls)
        delete_weburl_and_content_table = delete(self.translator.weburlsandcontent)
        self.translator.connection.execute('TRUNCATE TABLE weburls RESTART IDENTITY;')
        self.translator.connection.execute(delete_weburl_table)
        self.translator.connection.execute(delete_weburl_and_content_table)
        self.translator.connection.close()


    def test_translator_is_instance_of_Translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_translator_initializes_with_tables(self):
        self.assertIsInstance(self.translator.weburls, Table)
        self.assertIsInstance(self.translator.weburlsandcontent, Table)

    def test_translator_initializes_with_id_variable_of_1(self):
        self.assertEqual(self.translator.current_id, 1)


    def test_prepare_urls_for_writing_to_db_calls_write_url(self):
        self.translator.write_url = MagicMock()
        retrieved_weburls = ['www.dogs.com', 'www.cats.com']
        self.translator.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.translator.write_url.call_count, 2)

    def test_prepare_urls_for_writing_to_db_WONT_exceed_database_limit(self):
        self.translator.get_weburls_table_size = MagicMock(return_value=1000)
        self.assertRaises(Exception, self.translator.prepare_urls_for_writing_to_db, ['www.somecats.com'])


    def test_write_urls_saves_urls_to_database(self):
        self.translator.write_url('translator2test.com')
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('translator2test.com', results.fetchone()['weburl'])


    def test_write_urls_and_content_saves_everything_to_database(self):
        self.translator.write_urls_and_content('http://example.com', 'example title', 'example description', 'example keywords')
        statement = select([self.translator.weburlsandcontent])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://example.com', results.fetchone()['weburl'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example title', results.fetchone()['title'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example description', results.fetchone()['description'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example keywords', results.fetchone()['keywords'])

    def test_write_urls_and_content_increases_current_id_by_1(self):
        self.translator.write_urls_and_content('http://example.com', 'example title', 'example description', 'example keywords')

        my_url = select([self.translator.weburls]).where(self.translator.weburls.c.id == 1)
        result_proxy = self.test_database_connection.execute(my_url)
        print(result_proxy.fetchall())

        self.assertEqual(self.translator.current_id, 2)


    def test_get_weburls_table_size(self):
        self.translator.write_url('translator3test.com')
        self.translator.write_url('translator4test.com')
        self.assertEqual(self.translator.get_weburls_table_size(), 2)


    def test_get_next_url_exists(self):
        self.assertTrue(self.translator.get_next_url)

    # def test_get_next_url_retrieves_second_url_in_table(self):



    # def test_write_urls_and_content_calls_get_next_url(self):
    #     self.translator.get_next_url = MagicMock()
    #     self.translator.write_urls_and_content('http://example.com', 'example title', 'example description', 'example keywords')
    #     self.assertCalled(self.translator.get_next_url)
