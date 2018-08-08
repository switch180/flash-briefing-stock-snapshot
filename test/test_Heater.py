from unittest import TestCase
from unittest.mock import patch
from chalicelib.Heater import Heater


class test_Heater(TestCase):
    def mocked_requests(*args, **kwargs):
        class MockGet:
            def __init__(self, json_body, status):
                self.json_body = json_body
                self.status = status
            def json(self):
                return self.json_body
            @property
            def status_code(self):
                return self.status
        if 'warm' in args[0].split('/'):
            return MockGet({'status': 200}, 200)
        return MockGet(None, 418)

    def setUp(self):
        self.heater = Heater()
    @patch('chalicelib.Heater.requests.get', side_effect=mocked_requests)
    def test_warm(self, mocked_requests):
        req = self.heater.heat_warm()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json()['status'], 200)
