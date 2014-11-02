from coinstar import app
from coinstar.models import db, Account, Charge

from flask import request
from datetime import datetime
import json
import re


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


@app.route('/api/v1/charges/', methods=['GET', 'POST'])
def charges():
    if request.method == 'POST':
        return create_charge()
    else:
        return list_charges()


def list_charges():
    charges = Charge.query.all()
    return json.dumps(
        {
            'charges': [charge.to_hash() for charge in charges],
            'prev_page': None,
            'next_page': None
        }
    )


def create_charge():
    # Validate the charge amount
    try:
        amount = int(request.form['amount'])
    except KeyError, e:
        return '{"error": "Missing amount"}', 400
    except ValueError, e:
        return '{"error": "Amount is not an integer"}', 400

    # Validate the charge timestamp
    try:
        timestamp = datetime.strptime(
            request.form['datetime'], '%Y-%m-%dT%H:%M:%S')
    except KeyError, e:
        return '{"error": "Missing datetime"}', 400
    except ValueError, e:
        return '{"error": "Bad datetime format"}', 400

    # Validate the charge account ID
    try:
        account_id = str(request.form['account_id'])
    except KeyError, e:
        return '{"error": "Missing account ID"}', 400
    if account_id is None or account_id == '':
        return '{"error": "Empty account ID"}', 400
    if len(account_id) > 80:
        return '{"error": "Account ID is to long"}', 400
    if not re.match(r'^\w+$', account_id):
        return '{"error": "Account ID contains invalid characters"}', 400

    # Load the charge account object...
    account = Account.query.filter_by(ext_account_id=account_id).first()

    # ... or create it if necessary
    if account is None:
        try:
            account = Account(account_id)
            db.session.add(account)
        except:
            return '{"error": "Failed to create account object"}', 500

    # Create the charge object
    try:
        charge = Charge(account, amount, timestamp)
        db.session.add(charge)
    except:
        return '{"error": "Failed to create charge object"}', 500

    # Commit the DB changes
    db.session.commit()

    # Finally, return the charge object as JSON
    return charge.to_json()


@app.route('/api/v1/charges/<int:charge_id>')
def get_charge(charge_id):
    charge = Charge.query.get_or_404(charge_id)
    return charge.to_json()
