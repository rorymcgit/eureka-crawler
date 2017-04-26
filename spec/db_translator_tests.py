import unittest
from crawler.db_translator import Translator
from mock import Mock
import psycopg2

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        conn = psycopg2.connect("dbname=beetle_crawler_test")
        cur = conn.cursor()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)

    def test_database_environment_set(self):
        self.translator = Mock( {"set_environment" : "dbname=beetle_crawler_test"})
        self.assertEqual(self.translator.set_environment(), "dbname=beetle_crawler_test")

# >>> from mock import Mock
# >>> myMock = Mock( {"foo" : "you called foo"} )
# >>> myMock.foo()
# 'you called foo'
# >>> f = myMock.foo
# >>> f
# <mock.MockCaller instance at 15d46d0>
# >>> f() 'you called foo'
# >>> f( "wibble" )
# 'you called foo'
# >>>
