from coinstar import app
from coinstar.errors import GenericError, BadRequest, NotFound

from flask.ext.sqlalchemy import SQLAlchemy
import json
import re
from datetime import datetime

db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ext_account_id = db.Column(db.String(80), unique=True)

    charges = db.relationship('Charge', backref='account')

    def __init__(self, ext_account_id):
        self.ext_account_id = ext_account_id

    def __repr__(self):
        return '<Account {}>'.format(self.ext_account_id)

    def to_dict(self):
        return {
            'id': self.ext_account_id,
            'lifetime_value': int(self.lifetime_value)
        }

    @db.validates('ext_account_id')
    def validate_ext_account_id(self, key, ext_account_id):
        if ext_account_id is None or ext_account_id == '':
            raise BadRequest('Empty account ID')
        if len(ext_account_id) > 80:
            raise BadRequest('Account ID is to long')
        if not re.match(r'^\w+$', ext_account_id):
            raise BadRequest('Account ID contains invalid characters')
        return ext_account_id


class Charge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    cents = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)

    def __init__(self, account, cents, datetime):
        self.account = account
        self.cents = cents
        self.datetime = datetime

    def __repr__(self):
        return '<Charge {} {}>'.format(self.account.ext_account_id, self.cents)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account.ext_account_id,
            'cents': self.cents,
            'datetime': self.datetime.isoformat()
        }

    @db.validates('cents')
    def validates_cents(self, key, cents):
        if not isinstance(cents, int):
            try:
                cents = int(cents)
            except (ValueError, TypeError), e:
                raise BadRequest('Cents is not an integer')
        return cents

    @db.validates('datetime')
    def validates_timestamp(self, key, timestamp):
        if not isinstance(timestamp, datetime):
            try:
                timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
            except (ValueError, TypeError), e:
                raise BadRequest('Bad datetime format')
        return timestamp


Account.lifetime_value = db.column_property(
    db.session.query(
        db.func.sum(Charge.cents)
    ).filter(Account.id == Charge.account_id).label('lifetime_value')
)
