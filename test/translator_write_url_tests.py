import unittest
import sqlalchemy
import mock
from mock import MagicMock
from sqlalchemy import create_engine, select, insert, MetaData, Table, delete
from crawler.translator import Translator

class TestingTranslatorMethods2(unittest.TestCase):

    def setUp(self):
        self.url_checker = MagicMock()
        self.url_splicer = MagicMock()
        self.translator = Translator('postgresql://localhost/beetle_crawler_test', 1000, self.url_checker)
        self.test_database_connection = self.translator.connection
        self.test_metadata_dictionary = {'url': 'http://example.com',
                                        'title': 'example title',
                                        'description': 'example description',
                                        'keywords': 'example keywords'}

    def tearDown(self):
        delete_weburl_table = delete(self.translator.weburls)
        delete_weburl_and_content_table = delete(self.translator.weburlsandcontent)
        self.translator.connection.execute('TRUNCATE TABLE weburls RESTART IDENTITY;')
        self.translator.connection.execute(delete_weburl_table)
        self.translator.connection.execute(delete_weburl_and_content_table)
        self.translator.connection.close()

    def test_write_url_saves_urls_to_database(self):
        self.translator.write_url('http://translatortest.com')
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        # print(results.fetchone()['weburl'])
        self.assertIn('http://translatortest.com', results.fetchone()['weburl'])
