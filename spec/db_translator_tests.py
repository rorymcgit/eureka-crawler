import unittest
from crawler.db_translator import Translator

class TestingTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()

    def test_translator_is_instance_of_translator(self):
        self.assertIsInstance(self.translator, Translator)
