import views
import importlib
import collections
import models as m
from auth import auth_blueprint, get_login_user
from flask import Flask, g
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from contrib.utils.proxy import Proxy
from contrib.ext.sqlalchemy_ext import create_engine
from contrib.middlewares.sqlalchemymiddleware import SQLAlchemyMiddleware
from sqlalchemy_imageattach import context
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

class App(Flask):
    """Base Flask app for Issue tracker API
    """
    pass

self = importlib.import_module(__name__)

def create_app(config):
    """Creates flask application with configuration
    """
    app = App(__name__)

    # Configure application
    app.config.setdefault('DATABASE', 'db.db')
    if isinstance(config, collections.Mapping):
        app.config.update(config)
    else:
        app.config.from_object(config)

    # View registering
    views.register_views(app)

    # DB connection
    app.db_engine = create_engine(app.config['DATABASE'])
    m.Base.metadata.bind = app.db_engine
    m.Session.configure(bind=app.db_engine)

    # Image Store
    app.store = HttpExposedFileSystemStore('images', 'images/')
    app.wsgi_app = app.store.wsgi_middleware(app.wsgi_app)
    @app.before_request
    def store_before_request():
        context.push_store_context(app.store)

    @app.teardown_request
    def store_teardown_request(exception=None):
        context.pop_store_context()

    # Auth
    app.register_blueprint(auth_blueprint)

    @app.before_request
    def before_request():
        g.user = get_login_user()


    # Middlewares
    SQLAlchemyMiddleware(m.Session, app)

    # Admin
    def get_session():
        session = getattr(self, '_session', None)
        if (session is None) or not session.is_active:
            session = m.Session()
            setattr(self, '_session', session)
        return session
    session = Proxy(get_session)
    admin = Admin(app)
    admin.add_view(ModelView(m.Issue, session, category='models'))
    admin.add_view(ModelView(m.User, session, category='models'))

    return app
