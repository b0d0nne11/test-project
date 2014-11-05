from coinstar.tests import CoinstarUnitTest
from coinstar import app

import json


class PaginationDataTests(CoinstarUnitTest):

    def setUp(self):
        super(PaginationDataTests, self).setUp()
        self.total_entries = 20
        for i in range(self.total_entries):
            r = self.app.post('/api/v1/charges/', data=dict(
                account_id='testid{}'.format(i),
                cents=100,
                datetime='2014-10-27T09:44:55'
            ))

    def test_accounts_pagination(self):
        self._generic_pagination_test('accounts')

    def test_charges_pagination(self):
        self._generic_pagination_test('charges')

    def test_negative_limit(self):
        r = self.app.get('/api/v1/accounts/?limit=-1')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Limit is too small')

    def test_zero_limit(self):
        r = self.app.get('/api/v1/accounts/?limit=0')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Limit is too small')

    def test_large_limit(self):
        r = self.app.get('/api/v1/accounts/?limit=1001')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Limit is too large')

    def test_bad_limit(self):
        r = self.app.get('/api/v1/accounts/?limit=notanumber')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Limit is not an integer')

    def test_empty_page(self):
        r = self.app.get('/api/v1/accounts/?page=')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Failed to load page')

    def test_bad_page(self):
        r = self.app.get('/api/v1/accounts/?page=gobbledygook')
        json_data = json.loads(r.data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_data['error'], 'Failed to load page')

    def _generic_pagination_test(self, collection):
        for limit in [1, 2, 5, 10, 20, 100]:

            r = self.app.get('/api/v1/{collection}/?limit={limit}'.format(
                collection=collection, limit=limit))
            json_data = json.loads(r.data)

            # Count total entries paging forward

            entries = 0

            while True:
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    len(json_data[collection]), min(limit, self.total_entries))

                entries += len(json_data[collection])

                if json_data['next_page'] is None:
                    break
                else:
                    server_url = '{}://{}'.format(
                        app.config['PREFERRED_URL_SCHEME'],
                        app.config['SERVER_NAME']
                    )
                    next_page = json_data['next_page'].replace(server_url, '')
                    r = self.app.get(next_page)
                    json_data = json.loads(r.data)

            self.assertEqual(entries, self.total_entries)

            # Count total entries paging backward

            entries = 0

            while True:
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    len(json_data[collection]), min(limit, self.total_entries))

                entries += len(json_data[collection])

                if json_data['prev_page'] is None:
                    break
                else:
                    server_url = '{}://{}'.format(
                        app.config['PREFERRED_URL_SCHEME'],
                        app.config['SERVER_NAME']
                    )
                    next_page = json_data['prev_page'].replace(server_url, '')
                    r = self.app.get(next_page)
                    json_data = json.loads(r.data)

            self.assertEqual(entries, self.total_entries)
