from flask import Flask
import logging
import logging.config
import yaml

app = Flask(__name__)
app.config.from_object('coinstar.default_settings')
app.config.from_envvar('COINSTAR_SETTINGS', silent=True)

if not app.debug:
    logging.config.dictConfig(yaml.load(open('logging.yml')))

import coinstar.views
import coinstar.errors


@app.errorhandler(coinstar.errors.GenericError)
def handle_bad_request(error):
    return error.response()
