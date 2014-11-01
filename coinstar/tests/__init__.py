from coinstar import app
from coinstar.models import db

import os
import tempfile
import unittest


class CoinstarUnitTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)


if __name__ == '__main__':
    unittest.main()
