from coinstar import app
from coinstar.errors import GenericError, BadRequest, NotFound
from coinstar.models import db, Account, Charge
from coinstar.pagination import Pagination

from flask import request
from datetime import datetime
import json
import re


@app.route('/api/v1/accounts/')
def accounts():
    app.logger.debug('Entering list accounts handler')

    # Validate the page limit
    try:
        page_limit = int(request.args.get('limit', default=100))
    except ValueError, e:
        raise BadRequest('Limit is not an integer')
    if page_limit < 1:
        raise BadRequest('Limit is too small')
    if page_limit > 1000:
        raise BadRequest('Limit is too large')

    # Validate the page object
    try:
        page = Pagination(Account, request.args)
    except ValueError, e:
        raise BadRequest('Failed to load page')

    return page.to_json()


@app.route('/api/v1/accounts/<account_id>')
def account(account_id):
    app.logger.debug('Entering get account handler')
    account = Account.query.filter_by(ext_account_id=account_id).first()
    if account is None:
        raise NotFound('Account not found')
    return account.to_json()


@app.route('/api/v1/charges/', methods=['GET', 'POST'])
def charges():
    if request.method == 'POST':
        return create_charge()
    else:
        return list_charges()


def list_charges():
    app.logger.debug('Entering list accounts handler')

    # Validate the page limit
    try:
        page_limit = int(request.args.get('limit', default=100))
    except ValueError, e:
        raise BadRequest('Limit is not an integer')
    if page_limit < 1:
        raise BadRequest('Limit is too small')
    if page_limit > 1000:
        raise BadRequest('Limit is too large')

    # Validate the page object
    try:
        page = Pagination(Charge, request.args)
    except ValueError, e:
        raise BadRequest('Failed to load page')

    return page.to_json()


def create_charge():
    app.logger.debug('Entering create account handler')

    # Validate the charge amount
    try:
        amount = int(request.form['amount'])
    except KeyError, e:
        raise BadRequest('Missing amount')
    except ValueError, e:
        raise BadRequest('Amount is not an integer')

    # Validate the charge timestamp
    try:
        timestamp = datetime.strptime(
            request.form['datetime'], '%Y-%m-%dT%H:%M:%S')
    except KeyError, e:
        raise BadRequest('Missing datetime')
    except ValueError, e:
        raise BadRequest('Bad datetime format')

    # Validate the charge account ID
    try:
        account_id = str(request.form['account_id'])
    except KeyError, e:
        raise BadRequest('Missing account ID')
    if account_id is None or account_id == '':
        raise BadRequest('Empty account ID')
    if len(account_id) > 80:
        raise BadRequest('Account ID is to long')
    if not re.match(r'^\w+$', account_id):
        raise BadRequest('Account ID contains invalid characters')

    # Load the charge account object...
    account = Account.query.filter_by(ext_account_id=account_id).first()

    # ... or create it if necessary
    if account is None:
        app.logger.debug('Account "{}" not found'.format(account_id))
        try:
            account = Account(account_id)
            db.session.add(account)
            db.session.commit()
            app.logger.debug('Created {}'.format(account))
        except:
            raise GenericError('Failed to create account object')

    # Create the charge object
    try:
        charge = Charge(account, amount, timestamp)
        db.session.add(charge)
        db.session.commit()
        app.logger.debug('Created {}'.format(charge))
    except:
        raise GenericError('Failed to create charge object')

    # Finally, return the charge object as JSON
    return charge.to_json()


@app.route('/api/v1/charges/<charge_id>')
def charge(charge_id):
    app.logger.debug('Entering get charge handler')
    charge = Charge.query.get(charge_id)
    if charge is None:
        raise NotFound('Charge not found')
    return charge.to_json()
