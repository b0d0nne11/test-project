test-project
============

This demo project collects charges associated with accounts in order to determine the value of those accounts.

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
| amount     | integer  | yes       |          |
+------------+----------+-----------+----------+
| datetime   | datetime | yes       |          |
+------------+----------+-----------+----------+

Notes:

* Parameters should be submitted as form data with a Content-Type of application/x-www-form-urlencoded.
* Account IDs are limited to 80 characters.
* Account IDs that don't exist will be created.
* Amount should be a whole number of cents.
* Datetime should be expressed according to ISO 8601 (i.e. YYYY-MM-DDTHH:MM:SS+HH:MM).

Sample request::

  curl -vvv \
    -d 'account_id=testid' \
    -d 'amount=100' \
    -d 'datetime=2014-10-27T09:44:55+00:00' \
    http://localhost/api/v1/charges/

Sample response::

  {
    "id": 1,
    "account_id": "testid",
    "amount": 100,
    "datetime": "2014-10-27T09:44:55+00:00"
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
    "datetime": "2014-10-27T09:44:55+00:00"
  }

