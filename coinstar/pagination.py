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


class Pagination():

    def __init__(self, obj, args):
        self.query = obj.query
        self.collection = p.plural(obj.__tablename__)
        self.opaque_page = args.get('page')

        if self.opaque_page is None:
            self.page_offset = 0
            self.page_limit = int(args.get('limit', default=100))
        else:
            page = decode(self.opaque_page)
            self.page_offset = int(page['offset'])
            self.page_limit = int(page['limit'])

        self.total_entries = self.query.count()

    def has_prev(self):
        return self.page_offset > 0

    def has_next(self):
        return self.page_offset + self.page_limit < self.total_entries

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
                'offset': self.page_offset - self.page_limit,
                'limit': self.page_limit
            })
        else:
            return None

    def next_link(self):
        if self.has_next():
            return self.link({
                'offset': self.page_offset + self.page_limit,
                'limit': self.page_limit
            })
        else:
            return None

    def items(self):
        return self.query.offset(self.page_offset).limit(self.page_limit).all()

    def to_dict(self):
        return {
            self.collection: [entry.to_dict() for entry in self.items()],
            'prev_page': self.prev_link(),
            'next_page': self.next_link()
        }
