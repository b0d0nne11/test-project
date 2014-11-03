from coinstar import app

from flask import jsonify, make_response


class GenericError(Exception):
    message = 'An unexpected error has occured'
    status_code = 500
    headers = {'Content-Type': 'application/json'}

    def __init__(self, message=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        app.logger.error('Caught exception: {}'.format(self.message))

    def response(self):
        r = {'error': self.message}
        return make_response(jsonify(r), self.status_code, self.headers)


class BadRequest(GenericError):
    status_code = 400
    message = 'Bad request'


class NotFound(GenericError):
    status_code = 404
    message = 'Not found'


class MethodNotAllowed(GenericError):
    status_code = 405
    message = 'Method not allowed'
