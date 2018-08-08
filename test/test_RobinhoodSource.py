from unittest import TestCase
from unittest.mock import patch
from etc import sample_rh_quote
from chalicelib.RobinhoodSource import RobinhoodSource


class FakeRobinhood(object):
    def __init__(self, **kwargs):
        pass
    def login(self, **kwargs):
        return True

class test_RobinhoodSource(TestCase):
    stock = 'XYZ'
    friendly_name = 'Example Inc'
    username = 'some_username'
    password = 'some_password'


    def setUp(self):
        pass


    @patch('chalicelib.RobinhoodSource.Robinhood')
    def test_init(self, mocked_robinhood):
        mocked_robinhood.return_value.login.return_value = True
        mocked_robinhood.return_value.quote_data.return_value = sample_rh_quote
        rh = RobinhoodSource(self.stock, self.friendly_name, self.username, self.password)
        ar = rh.get_response()
        resp = ar.get_resp()
        for key in ['uid', 'titleText', 'mainText', 'updateDate']:
            self.assertIn(key, resp)
        main_text = resp['mainText']
        self.assertTrue('2.4%,' in main_text)
        self.assertTrue('is down' in main_text)
        rh.set_position(1000, 10, 20)
