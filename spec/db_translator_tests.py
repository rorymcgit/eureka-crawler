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
        self.translator.connection.execute(delete_weburl_table)
        self.translator.connection.execute(delete_weburl_and_content_table)
        self.translator.connection.close()


    def test_translator_is_instance_of_Translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_translator_initializes_with_tables(self):
        self.assertIsInstance(self.translator.weburls, Table)
        self.assertIsInstance(self.translator.weburlsandcontent, Table)


    def test_prepare_urls_for_writing_to_db_calls_write_url(self):
        self.translator.write_url = MagicMock()
        retrieved_weburls = ['http://www.dogs.com', 'http://www.cats.com']
        self.translator.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.translator.write_url.call_count, 2)

    def test_prepare_urls_for_writing_to_db_WONT_exceed_database_limit(self):
        self.translator.get_weburls_table_size = MagicMock(return_value=1000)
        self.assertRaises(Exception, self.translator.prepare_urls_for_writing_to_db, ['www.somecats.com'])


    def test_write_urls_saves_urls_to_database(self):
        self.translator.write_url('http://translator2test.com')
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://translator2test.com', results.fetchone()['weburl'])


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


    def test_get_weburls_table_size(self):
        self.translator.write_url('http://translator3test.com')
        self.translator.write_url('http://translator4test.com')
        self.assertEqual(self.translator.get_weburls_table_size(), 2)


    def test_url_checker_is_called_by_write_url(self):
        self.translator.url_checker = MagicMock()
        self.translator.write_url('https://www.example.com/')
        self.translator.url_checker.assert_called_once_with('https://www.example.com/')

    def test_url_checker_saves_only_urls_beginning_http(self):
        self.assertEqual(self.translator.check_url_beginning('https://www.example.com/'), True)
        self.assertEqual(self.translator.check_url_beginning('www.example.com/'), False)

    def test_url_checker_saves_only_urls_ending_com_or_uk(self):
        self.assertEqual(self.translator.check_url_domain('https://www.example.com/'), True)
        self.assertEqual(self.translator.check_url_domain('https://www.example.co.uk/'), True)
        self.assertEqual(self.translator.check_url_domain('https://www.example.cz/'), False)
