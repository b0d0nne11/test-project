from coinstar.tests import CoinstarUnitTest

import json


class SimpleDataTests(CoinstarUnitTest):

    def setUp(self):
        super(SimpleDataTests, self).setUp()
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            cents=100,
            datetime='2014-10-27T09:44:55'
        ))

    def test_list_accounts(self):
        r = self.app.get('/api/v1/accounts/')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['accounts'], [
            {
                'id': 'testid',
                'lifetime_value': 100
            }
        ])
        self.assertIsNone(json_data['prev_page'])
        self.assertIsNone(json_data['next_page'])

    def test_get_account(self):
        r = self.app.get('/api/v1/accounts/testid')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['id'], 'testid')
        self.assertEqual(json_data['lifetime_value'], 100)

    def test_account_not_found(self):
        r = self.app.get('/api/v1/accounts/gobbledygook')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json_data['error'], 'Account not found')

    def test_list_charges(self):
        r = self.app.get('/api/v1/charges/')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['charges'], [
            {
                'id': 1,
                'account_id': 'testid',
                'cents': 100,
                'datetime': '2014-10-27T09:44:55'
            }
        ])
        self.assertIsNone(json_data['prev_page'])
        self.assertIsNone(json_data['next_page'])

    def test_get_charge(self):
        r = self.app.get('/api/v1/charges/1')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['account_id'], 'testid')
        self.assertEqual(json_data['cents'], 100)
        self.assertEqual(json_data['datetime'], '2014-10-27T09:44:55')

    def test_charge_not_found(self):
        r = self.app.get('/api/v1/charges/100')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json_data['error'], 'Charge not found')
