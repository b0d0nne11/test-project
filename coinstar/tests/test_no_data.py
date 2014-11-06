from coinstar.tests import CoinstarUnitTest

import json


class NoDataTests(CoinstarUnitTest):

    def test_list_accounts(self):
        r = self.app.get('/api/v1/accounts/')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['accounts'], [])
        self.assertIsNone(json_data['prev_page'])
        self.assertIsNone(json_data['next_page'])

    def test_get_account(self):
        r = self.app.get('/api/v1/accounts/testid')
        self.assertEqual(r.status_code, 404)

    def test_list_charges(self):
        r = self.app.get('/api/v1/charges/')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['charges'], [])
        self.assertIsNone(json_data['prev_page'])
        self.assertIsNone(json_data['next_page'])

    def test_get_charge(self):
        r = self.app.get('/api/v1/charges/1')
        self.assertEqual(r.status_code, 404)
