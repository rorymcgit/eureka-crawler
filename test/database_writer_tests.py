import unittest
import sqlalchemy
import mock
from mock import MagicMock
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.database_writer import DatabaseWriter

class TestingDatabaseWriter(unittest.TestCase):

    def setUp(self):
        self.url_checker = MagicMock()
        self.url_splicer = MagicMock()
        self.database_reader = MagicMock()
        self.database_reader.get_weburls_table_size = MagicMock(return_value = 0)
        self.database_writer = DatabaseWriter('postgresql://localhost/eureka_test',
                                                1000,
                                                self.url_checker,
                                                self.url_splicer,
                                                self.database_reader)
        self.test_database_connection = self.database_writer.connection
        self.test_metadata_dictionary = {'url': 'http://example.com',
                                        'title': 'example title',
                                        'description': 'example description',
                                        'keywords': 'example keywords'}

    def tearDown(self):
        delete_weburl_table = delete(self.database_writer.weburls)
        delete_weburl_and_content_table = delete(self.database_writer.weburlsandcontent)
        self.database_writer.connection.execute('TRUNCATE TABLE weburls RESTART IDENTITY;')
        self.database_writer.connection.execute(delete_weburl_table)
        self.database_writer.connection.execute(delete_weburl_and_content_table)
        self.database_writer.connection.close()

    def test_database_writer_set_up_database(self):
        self.assertIsInstance(self.database_writer.weburls, Table)
        self.assertIsInstance(self.database_writer.weburlsandcontent, Table)

    def test_database_writer_initializes_with_a_database_limit_of_1000(self):
        self.assertEqual(self.database_writer.database_limit, 1000)

    def test_database_writer_is_instance_of_DatabaseWriter(self):
        self.assertIsInstance(self.database_writer, DatabaseWriter)

    def test_database_writer_initializes_with_tables(self):
        self.assertIsInstance(self.database_writer.weburls, Table)
        self.assertIsInstance(self.database_writer.weburlsandcontent, Table)

    def test_database_writer_changeable_database_limit(self):
        self.low_limit_database_writer = DatabaseWriter('postgresql://localhost/eureka_test', 35)
        self.assertEqual(self.low_limit_database_writer.database_limit, 35)


    def test_prepare_urls_for_writing_to_db_calls_write_url(self):
        self.database_writer.write_url = MagicMock()
        retrieved_weburls = ['http://www.dogs.com', 'http://www.cats.com']
        self.database_writer.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.database_writer.write_url.call_count, 2)


    def test_write_url_WONT_save_url_when_weburls_is_full(self):
        self.database_reader.get_weburls_table_size = MagicMock(return_value=1000)
        self.assertEqual(self.database_writer.write_url('http://database_writer2test.com'), "Weburls table is full")


    def test_write_urls_and_content_saves_everything_to_database(self):
        self.database_writer.write_urls_and_content(self.test_metadata_dictionary)
        statement = select([self.database_writer.weburlsandcontent])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://example.com', results.fetchone()['weburl'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example title', results.fetchone()['title'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example description', results.fetchone()['description'])
        results = self.test_database_connection.execute(statement)
        self.assertIn('example keywords', results.fetchone()['keywords'])

    def test_write_url_calls_cut_url(self):
        self.database_writer.url_splicer.cut_url = MagicMock(return_value='https://www.example.com/home/')
        self.database_writer.write_url('https://www.example.com/home/page')
        self.database_writer.url_splicer.cut_url.assert_called_once_with('https://www.example.com/home/page')

    def test_write_url_saves_urls_to_database(self):
        self.database_writer.url_splicer.cut_url = MagicMock(return_value = 'http://database_writertest.com')
        self.database_reader.url_is_in_database = MagicMock(return_value = False)
        self.database_writer.write_url('http://database_writertest.com')
        statement = select([self.database_writer.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://database_writertest.com', results.fetchone()['weburl'])

    def test_write_url_WONT_save_duplicate_urls_when_url_is_in_database(self):
        test_url = 'http://alreadyindb.com'
        self.database_reader.url_is_in_database = MagicMock(return_value = True)
        self.database_writer.write_url(test_url)
        select_statement = self.database_writer.weburls.select(self.database_writer.weburls.c.weburl == test_url)
        result_proxy = self.test_database_connection.execute(select_statement)
        self.assertEqual(len(result_proxy.fetchall()), 0)

    def test_write_url_calls_url_is_in_database(self):
        self.database_reader.url_is_in_database = MagicMock()
        test_url = 'http://www.checkmydb.com'
        self.database_writer.write_url(test_url)
        self.database_reader.url_is_in_database.assert_called_once()
