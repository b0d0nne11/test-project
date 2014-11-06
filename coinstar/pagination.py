from coinstar import app

from base64 import b64encode, b64decode
import json
import inflect
from flask import url_for

p = inflect.engine()


def encode(data):
    return b64encode(json.dumps(data))


def decode(page):
    return json.loads(b64decode(page))


class Page():

    def __init__(self, model, args):
        self.model = model
        self.collection = p.plural(model.__tablename__)
        self.opaque_page = args.get('page')

        if self.opaque_page is None:
            self.page = {
                'last_id': 0,
                'limit': int(args.get('limit', default=100))
            }
        else:
            self.page = decode(self.opaque_page)

        self.total_entries = self.model.query.count()

    def has_prev(self):
        return self.page['last_id'] > 0

    def has_next(self):
        return self.page['last_id'] + self.page['limit'] < self.total_entries

    def link(self, page_data):
        return '{proto}://{server_name}{url}?page={opaque_page}'.format(
            proto=app.config['PREFERRED_URL_SCHEME'],
            server_name=app.config['SERVER_NAME'],
            url=url_for('list_{}'.format(self.collection)),
            opaque_page=encode(page_data)
        )

    def prev_link(self):
        if self.has_prev():
            return self.link({
                'last_id': self.page['last_id'] - self.page['limit'],
                'limit': self.page['limit']
            })
        else:
            return None

    def next_link(self):
        if self.has_next():
            return self.link({
                'last_id': self.page['last_id'] + self.page['limit'],
                'limit': self.page['limit']
            })
        else:
            return None

    def items(self):
        return self.model.query.filter(
            self.model.id > self.page['last_id']
        ).limit(self.page['limit']).all()

    def to_dict(self):
        return {
            self.collection: [entry.to_dict() for entry in self.items()],
            'prev_page': self.prev_link(),
            'next_page': self.next_link()
        }
