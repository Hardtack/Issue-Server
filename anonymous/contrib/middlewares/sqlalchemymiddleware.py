from flask import g
from sqlalchemy.orm import scoped_session
class SQLAlchemyMiddleware(object):
    def __init__(self, session, app=None):
        self.app = app
        self.session = session
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def before_request():
            g.session = scoped_session(self.session)()

        @app.teardown_request
        def teardown_request(exception):
            if hasattr(g, 'session'):
                g.session.close()
