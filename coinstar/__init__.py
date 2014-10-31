from flask import Flask

app = Flask(__name__)
app.config.from_object('coinstar.default_settings')
app.config.from_envvar('COINSTAR_SETTINGS', silent=True)

import coinstar.views
