import unittest
import sqlalchemy
import mock
from mock import MagicMock
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.database_reader import DatabaseReader
from crawler.database_writer import DatabaseWriter

class TestingDatabaseReader(unittest.TestCase):

    def setUp(self):
        self.database_writer = MagicMock()
        self.database_reader = DatabaseReader('postgresql://localhost/beetle_crawler_test')
        self.test_database_connection = self.database_reader.connection

    def tearDown(self):
        delete_weburl_table = delete(self.database_reader.weburls)
        self.database_reader.connection.execute('TRUNCATE TABLE weburls RESTART IDENTITY;')
        self.database_reader.connection.execute(delete_weburl_table)
        self.database_reader.connection.close()

    def insert_url_to_weburls_table(self, url):
        statement = insert(self.database_reader.weburls).values(weburl = url)
        self.test_database_connection.execute(statement)

    def test_database_reader_set_up_database(self):
        self.assertIsInstance(self.database_reader.weburls, Table)

    def test_database_reader_is_instance_of_database_reader(self):
        self.assertIsInstance(self.database_reader, DatabaseReader)

    def test_database_reader_initializes_with_current_id_variable_of_1(self):
        self.assertEqual(self.database_reader.current_id, 1)


    def test_get_next_url_increases_current_id_by_1(self):
        self.insert_url_to_weburls_table('http://getnexturl_test.com')
        self.insert_url_to_weburls_table('http://getnexturl_test2.com')
        self.database_reader.get_next_url()
        self.assertEqual(self.database_reader.current_id, 2)

    def test_get_weburls_table_size(self):
        self.insert_url_to_weburls_table("http://www.website.com")
        self.insert_url_to_weburls_table("http://www.another_website.com")
        self.assertEqual(self.database_reader.get_weburls_table_size(), 2)
