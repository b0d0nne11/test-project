from coinstar.tests import CoinstarUnitTest

import json


class SubmitChargeTests(CoinstarUnitTest):

    def test_submit_good_charge(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            amount=100,
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['account_id'], 'testid')
        self.assertEqual(json_data['amount'], 100)
        self.assertEqual(json_data['datetime'], '2014-10-27T09:44:55')

    def test_submit_w_missing_form(self):
        r = self.app.post('/api/v1/charges/')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)

    def test_submit_w_missing_account_id(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            amount=100,
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Missing account ID')

    def test_submit_w_empty_account_id(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='',
            amount=100,
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Empty account ID')

    def test_submit_w_long_account_id(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='a'*100,
            amount=100,
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Account ID is to long')

    def test_submit_w_bad_account_id(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='#$%^&*()',
            amount=100,
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            json_data['error'], 'Account ID contains invalid characters')

    def test_submit_w_missing_amount(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Missing amount')

    def test_submit_w_empty_amount(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='',
            amount='notanumber',
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Amount is not an integer')

    def test_submit_w_bad_amount(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            amount='notanumber',
            datetime='2014-10-27T09:44:55'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Amount is not an integer')

    def test_submit_w_missing_datetime(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            amount=100
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Missing datetime')

    def test_submit_w_empty_datetime(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            amount=100,
            datetime=''
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Bad datetime format')

    def test_submit_w_bad_datetime(self):
        r = self.app.post('/api/v1/charges/', data=dict(
            account_id='testid',
            amount=100,
            datetime='notadatetime'
        ))
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Bad datetime format')
