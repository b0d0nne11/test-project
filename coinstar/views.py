from coinstar import app
from coinstar.models import db, Account, Charge

import json


@app.route('/api/v1/accounts/')
def list_accounts():
    accounts = Account.query.all()
    return json.dumps(
        {
            'accounts': [account.to_hash() for account in accounts],
            'prev_page': None,
            'next_page': None
        }
    )


@app.route('/api/v1/accounts/<account_id>')
def get_account(account_id):
    account = Account.query.filter_by(ext_account_id=account_id).first_or_404()
    return account.to_json()


@app.route('/api/v1/charges/')
def list_charges():
    charges = Charge.query.all()
    return json.dumps(
        {
            'charges': [charge.to_hash() for charge in charges],
            'prev_page': None,
            'next_page': None
        }
    )


@app.route('/api/v1/charges/<int:charge_id>')
def get_charge(charge_id):
    charge = Charge.query.get_or_404(charge_id)
    return charge.to_json()
