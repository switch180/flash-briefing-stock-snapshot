from unittest import TestCase
from etc import sample_rh_quote
from copy import copy
from chalicelib.RobinhoodSource import RobinhoodQuote


class test_RobinhoodSource(TestCase):
    def setUp(self):
        self.quote = RobinhoodQuote(sample_rh_quote)
    def test_loading(self):
        for name in sample_rh_quote.keys():
            try:
                self.assertEqual(getattr(self.quote, name), sample_rh_quote[name])
            except Exception as err:
                print("Exception comparing key {}".format(key))
                raise err
    def test_attrs(self):
        for key in self.quote._attrs:
            setattr(self.quote, key, None)
    def test_getattr(self):
        for key in self.quote._attrs:
            getattr(self.quote, key)
        with self.assertRaises(AttributeError):
            getattr(self.quote, 'a cat is a friend indeed')
