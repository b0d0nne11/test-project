from coinstar import app
from coinstar.errors import GenericError, BadRequest, NotFound

from base64 import b64encode, b64decode
import json
import inflect
from flask import url_for

p = inflect.engine()


def encode(data):
    try:
        page = b64encode(json.dumps(data))
    except ValueError, e:
        raise BadRequest('Failed to encode next page')
    return page


def decode(page):
    try:
        data = json.loads(b64decode(page))
    except ValueError, e:
        raise BadRequest('Failed to load page')
    return data


class Page():

    def __init__(self, model, args):
        self.model = model
        self.collection = p.plural(model.__tablename__)
        self.opaque_page = args.get('page')

        if self.opaque_page is None:
            self.page = {
                'last_id': 0,
                'limit': args.get('limit', default=100)
            }
            self.validate_page_limit()
        else:
            self.page = decode(self.opaque_page)

        self.total_entries = self.model.query.count()

    def validate_page_limit(self):
        try:
            self.page['limit'] = int(self.page['limit'])
        except (ValueError, TypeError), e:
            raise BadRequest('Limit is not an integer')
        if self.page['limit'] < 1:
            raise BadRequest('Limit is too small')
        if self.page['limit'] > 1000:
            raise BadRequest('Limit is too large')

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
