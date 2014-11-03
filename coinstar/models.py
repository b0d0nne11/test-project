from coinstar import app

from flask.ext.sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ext_account_id = db.Column(db.String(80), unique=True)

    charges = db.relationship('Charge', backref='account')

    def __init__(self, ext_account_id):
        self.ext_account_id = ext_account_id

    def __repr__(self):
        return '<Account {}>'.format(self.ext_account_id)

    def value(self):
        return sum([charge.amount for charge in self.charges])

    def to_dict(self):
        return {
            'id': self.ext_account_id,
            'lifetime_value': self.value()
        }


class Charge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    amount = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)

    def __init__(self, account, amount, datetime):
        self.account = account
        self.amount = int(amount)
        self.datetime = datetime

    def __repr__(self):
        return '<Charge {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account.ext_account_id,
            'amount': self.amount,
            'datetime': self.datetime.isoformat()
        }
