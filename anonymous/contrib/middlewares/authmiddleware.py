""":mod:`meetytools.middleware/authmiddleware` --- Authenticate middleware
===========================================================================

Provides authenticate middleware of meetytools.  
"""
from flask import g
from meetytools.auth import Auth
from meetytools.content_negotiation import render

class AuthMiddleware(object):
    """Auth middleware.  
    How to use

       app = Flask(__name__)
       AuthMiddleware(app, 'AuthName', 'tablename', Base, User)

    """
    def __init__(self, app, authname, tablename, base, user_model,
        user_pk_name='id', db_session_getter=lambda:g.session,
        render=lambda:render):
        self.app = app
        self.db_session_getter = db_session_getter
        self.init_app(app, authname, tablename, base, user_model, user_pk_name,
            db_session_getter)

    def init_app(self, app, authname, tablename, base, user_model,
        user_pk_name='id', db_session_getter=None):
        if db_session_getter is None:
            db_session_getter = self.db_session_getter
        auth = Auth(user_model, app.config['AUTH'])
        auth.token_auth.initialize_model_class(authname, tablename, base,
            user_model, user_pk_name)

        @auth.session_getter
        def session_getter():
            return db_session_getter()

        @auth.renderer_getter
        def renderer_getter():
            return render

        app.auth = auth
        @app.before_request
        def before_request():

            g.user = auth.get_logged_in_user()
        app.register_blueprint(auth.blueprint, url_prefix='/auth')

        # Error handling
        f = app.handle_exception
        def handle_exception(e):
            r = app.auth.handle_auth_error(e)
            if r:
                return r
            else:
                return f(e)
        app.handle_exception = handle_exception
