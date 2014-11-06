test-project
============

This demo project collects charges associated with accounts in order to determine the value of those accounts.

Setup
-----

Install the application dependancies with::

    pip install -r requirements.txt

Setup the database with::

    mysqladmin -h localhost -u root -p create coinstar
    mysql -h localhost -u root -p -D coinstar < coinstar.sql

Start the development application with::

    python run.py

Testing
-------

Run the test suite with::

    python -m unittest discover

API Usage
---------

List accounts
^^^^^^^^^^^^^

Path::

  /api/v1/accounts/?limit={limit} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameters | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| limit      | integer  | no        | 100      |
+------------+----------+-----------+----------+

Notes:

* Limit must be a positive integer
* Limit must be less than 1000
* Lifetime value is expressed in cents.

Sample request::

  curl -vvv http://localhost/api/v1/accounts/

Sample response::

  {
    "accounts": [
      {
        "id": "testid",
        "lifetime_value": 1234
      }
    ],
    "next_page": null,
    "prev_page": null
  }

Get account
^^^^^^^^^^^

Path::

  /api/v1/accounts/{account_id} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameter  | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| account_id | string   | yes       |          |
+------------+----------+-----------+----------+

Notes:

* Lifetime value is expressed in cents.

Sample request::

  curl -vvv http://localhost/api/v1/accounts/testid

Sample response::

  {
    "id": "testid",
    "lifetime_value": 1234
  }

List charges
^^^^^^^^^^^^

Path::

  /api/v1/charges/?limit={limit} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameter  | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| limit      | integer  | no        | 100      |
+------------+----------+-----------+----------+

Notes:

* Limit must be a positive integer
* Limit must be less than 1000

Sample request::

  curl -vvv http://localhost/api/v1/charges/

Sample response::

  {
    "charges": [
      {
        "id": 1,
        "account_id": "testid",
        "amount": 100,
        "datetime": "2014-10-27T09:44:55+00:00"
      }
    ],
    "next_page": null,
    "prev_page": null
  }

Submit charge
^^^^^^^^^^^^^

Path::

  /api/v1/charges/ (POST)

Parameters:

+------------+----------+-----------+----------+
| Parameter  | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| account_id | string   | yes       |          |
+------------+----------+-----------+----------+
| cents      | integer  | yes       |          |
+------------+----------+-----------+----------+
| datetime   | datetime | yes       |          |
+------------+----------+-----------+----------+

Notes:

* Parameters should be submitted as form data with a Content-Type of application/x-www-form-urlencoded.
* Account IDs are limited to 80 characters.
* Account IDs are limited to the following characters: [A-Za-z0-9\_].
* Account IDs that don't exist will be created.
* Datetime should be expressed according to ISO 8601 (i.e. YYYY-MM-DDTHH:MM:SS).

Sample request::

  curl -vvv \
    -d 'account_id=testid' \
    -d 'amount=100' \
    -d 'datetime=2014-10-27T09:44:55' \
    http://localhost/api/v1/charges/

Sample response::

  {
    "id": 1,
    "account_id": "testid",
    "amount": 100,
    "datetime": "2014-10-27T09:44:55"
  }

Get charge
^^^^^^^^^^

Path::

  /api/v1/charges/{charge_id} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameter  | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| charge_id  | integer  | yes       |          |
+------------+----------+-----------+----------+

Sample request::

  curl -vvv http://localhost/api/v1/charges/1

Sample response::

  {
    "id": 1,
    "account_id": "testid",
    "amount": 100,
    "datetime": "2014-10-27T09:44:55"
  }

