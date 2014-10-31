test-project
============

This demo project collects charges associated with accounts in order to determine the value of those accounts.

API Usage
---------

List accounts
^^^^^^^^^^^^^

Path::

  /api/v1/accounts/?page={page_id} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameters | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| page_id    | integer  | no        | 1        |
+------------+----------+-----------+----------+

Notes:

* Lifetime value is expressed in cents.
* Pages are limited to 20 entries.
* Pages that contain 0 entries will return a '404 Not Found'

Sample request::

  curl -vvv http://localhost/api/v1/accounts/

Sample response::

  {
    "accounts": [
      {
        "id": "testid",
        "lifetime_value": 1234
      }
    ]
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

  /api/v1/charges/?page={page_id} (GET)

Parameters:

+------------+----------+-----------+----------+
| Parameter  | Type     | Required? | Default  |
+------------+----------+-----------+----------+
| page_id    | integer  | no        | 1        |
+------------+----------+-----------+----------+

Notes:

* Pages are limited to 20 entries.
* Pages that contain 0 entries will return a '404 Not Found'

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
    ]
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

