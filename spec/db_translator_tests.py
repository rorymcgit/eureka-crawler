import unittest
import sqlalchemy
import mock
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

    def test_translator_initializes_with_a_database_limit_of_1000(self):
        self.assertEqual(self.translator.database_limit, 1000)

    def test_translator_is_instance_of_Translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_translator_initializes_with_tables(self):
        self.assertIsInstance(self.translator.weburls, Table)
        self.assertIsInstance(self.translator.weburlsandcontent, Table)

    def test_translator_initializes_with_id_variable_of_1(self):
        self.assertEqual(self.translator.current_id, 1)

    def test_translator_changeable_database_limit(self):
        self.low_limit_translator = Translator('postgresql://localhost/beetle_crawler_test', 35)
        self.assertEqual(self.low_limit_translator.database_limit, 35)


    def test_prepare_urls_for_writing_to_db_calls_write_url(self):
        self.translator.write_url = MagicMock()
        retrieved_weburls = ['http://www.dogs.com', 'http://www.cats.com']
        self.translator.prepare_urls_for_writing_to_db(retrieved_weburls)
        self.assertEqual(self.translator.write_url.call_count, 2)


    def test_write_url_saves_urls_to_database(self):
        self.translator.write_url('http://translatortest.com')
        statement = select([self.translator.weburls])
        results = self.test_database_connection.execute(statement)
        self.assertIn('http://translatortest.com', results.fetchone()['weburl'])

    def test_write_url_WONT_save_url_when_weburls_is_full(self):
        self.translator.get_weburls_table_size = MagicMock(return_value=1000)
        self.assertEqual(self.translator.write_url('http://translator2test.com'), "Weburls table is full")


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


    def test_get_next_url_increases_current_id_by_1(self):
        self.translator.write_url('http://getnexturl_test.com')
        self.translator.write_url('http://getnexturl_test2.com')
        self.translator.get_next_url()
        self.assertEqual(self.translator.current_id, 2)


    def test_write_url_calls_cut_string(self):
        self.translator.cut_string = MagicMock(return_value='https://www.example.com/home/')
        self.translator.write_url('https://www.example.com/home/page')
        self.translator.cut_string.assert_called_once_with('https://www.example.com/home/page')


    def test_get_weburls_table_size(self):
        self.translator.write_url('http://translator3test.com')
        self.translator.write_url('http://translator4test.com')
        self.assertEqual(self.translator.get_weburls_table_size(), 2)

    def test_get_weburls_and_content_table_size(self):
        self.translator.write_urls_and_content('http://someexample.com', 'some example title', 'some example description', 'some example keywords')
        self.translator.write_urls_and_content('http://example.com', 'another example title', 'another example description', 'another example keywords')
        self.assertEqual(self.translator.get_weburls_and_content_table_size(), 2)


    def test_get_next_url_exists(self):
        self.assertTrue(self.translator.get_next_url)

    def test_get_next_url_retrieves_second_url_in_table(self):
        self.translator.write_url('https://www.example1.com')
        test_weburls_array = ["https://www.dogs.com", "https://www.cats.com"]
        self.translator.prepare_urls_for_writing_to_db(test_weburls_array)
        self.translator.write_urls_and_content('http://example.com', 'example title', 'example description', 'example keywords')
        self.assertEqual(self.translator.get_next_url(), 'https://www.dogs.com')


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
        self.assertEqual(self.translator.check_url_domain('https://www.example.org/'), True)
        self.assertEqual(self.translator.check_url_domain('https://www.example.cz/'), False)

    def test_write_url_WONT_save_duplicate_urls(self):
        test_url = 'http://notsavedtwice.com'
        self.translator.write_url(test_url)
        self.translator.write_url(test_url)
        select_statement = self.translator.weburls.select(self.translator.weburls.c.weburl == test_url)
        result_proxy = self.test_database_connection.execute(select_statement)
        results = [item[1] for item in result_proxy.fetchall()]
        self.assertEqual(len(results), 1)


    def test_write_url_calls_url_is_in_database(self):
        self.translator.url_is_in_database = MagicMock()
        test_url = 'http://www.checkmydb.com'
        self.translator.write_url(test_url)
        self.translator.url_is_in_database.assert_called_once()


    def test_find_nth_finds_nth_character_in_string(self):
        find_nth_example = self.translator.find_nth('https://www.example.com/home/page', '/', 3)
        self.assertEqual(find_nth_example, 28)


    def test_cut_string_cuts_url_at_fourth_forward_slash(self):
        self.translator.find_nth = MagicMock(return_value = 28)
        url_to_cut = self.translator.cut_string('https://www.example.com/home/page')
        self.assertEqual(url_to_cut, 'https://www.example.com/home')

    def test_is_low_quality_link_returns_true_for_bad_link(self):
        test_url = "https://l.facebook.com/l.php?u=http%3A%2F%2Fbit.ly%2F2oIOj1d&h=ATNX92Yjs558O-DYMPJ31lQUT97uPCPCfPwZ9vUu4i7-zLT3ACP-1k_LLp5TKMLE_ZwUrkTRFvWWu6Sqo3sRZc51wD7uKcTgIRN1gf3XlBB6xqHd35ZxeHg&enc=AZOWulTNzLIKwRbWMKuj53x6BMSr61jcGJ1tdCnCjorzT1BaIo7uV-x188113_h2g5B-HUdbKrFky3bAMnh5A21v6Egd6aJNRwfs-Q8Cq3zWkZbgMYyRt_cWdpQDxrR_oUHFEdyGUU6Zl1whDgL-SBgjJXuLDUbGGKKtHJJPJhUD83_RKYkMbXGuA7tNhqyp5jz8SdneOc5iqrqIQRXylGLP&s=1"
        self.assertTrue(self.translator.is_low_quality_link(test_url))

    def test_is_low_quality_link_returns_false_for_good_link(self):
        test_url = "https://www.interestingwebsite.com/cool-article"
        self.assertFalse(self.translator.is_low_quality_link(test_url))
