import unittest
import sqlalchemy
from sqlalchemy import create_engine
from crawler.db_translator2 import Translator

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)
