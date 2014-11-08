from coinstar import app
from coinstar.errors import GenericError, BadRequest, NotFound
from coinstar.models import db, Account, Charge
from coinstar.pagination import Page

from flask import request, jsonify, make_response, render_template
from datetime import datetime
import re


def make_json_response(payload):
    return make_response(
        jsonify(payload), 200, {'Content-Type': 'application/json'})


@app.route('/')
@app.route('/overview')
def overview():
    charges = Charge.query.order_by('id desc').limit(10)
    accounts = Account.query.order_by('lifetime_value desc').limit(10)
    return render_template('overview.html', charges=charges, accounts=accounts)


@app.route('/api/v1/accounts/')
def list_accounts():
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
        page = Page(Account, request.args)
    except ValueError, e:
        raise BadRequest('Failed to load page')

    return make_json_response(page.to_dict())


@app.route('/api/v1/accounts/<account_id>')
def get_account(account_id):
    app.logger.debug('Entering get account handler')
    account = Account.query.filter_by(ext_account_id=account_id).first()
    if account is None:
        raise NotFound('Account not found')
    return make_json_response(account.to_dict())


@app.route('/api/v1/charges/', methods=['GET'])
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
        page = Page(Charge, request.args)
    except ValueError, e:
        raise BadRequest('Failed to load page')

    return make_json_response(page.to_dict())


@app.route('/api/v1/charges/', methods=['POST'])
def create_charge():
    app.logger.debug('Entering create account handler')

    account_id = request.form.get('account_id')
    cents = request.form.get('cents', type=int)
    timestamp = request.form.get('datetime')

    # Load the charge account object...
    account = Account.query.filter_by(ext_account_id=account_id).first()

    # ... or create it if necessary
    if account is None:
        account = Account(account_id)
        db.session.add(account)
        app.logger.debug('Created {}'.format(account))

    # Create the charge object
    charge = Charge(account, cents, timestamp)
    db.session.add(charge)
    app.logger.debug('Created {}'.format(charge))

    try:
        db.session.commit()
    except:
        raise GenericError('Failed to save DB changes')

    # Finally, return the charge object as JSON
    return make_json_response(charge.to_dict())


@app.route('/api/v1/charges/<charge_id>')
def get_charge(charge_id):
    app.logger.debug('Entering get charge handler')
    charge = Charge.query.get(charge_id)
    if charge is None:
        raise NotFound('Charge not found')
    return make_json_response(charge.to_dict())
