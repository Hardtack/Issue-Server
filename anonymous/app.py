import views
import collections
import models as m
from flask import Flask
from contrib.ext.sqlalchemy_ext import create_engine
from contrib.middlewares.babelmiddleware import BabelMiddleware
from contrib.middlewares.contentnegotiationmiddleware import (
    ContentNegotiationMiddleware)
from contrib.middlewares.sessionmiddleware import SessionMiddleware
from contrib.middlewares.sqlalchemymiddleware import SQLAlchemyMiddleware

class App(Flask):
    """Base Flask app for CAUCSE API
    """
    pass

def create_app(config):
    """Creates flask application with configuration
    """
    app = App(__name__)

    # Configure application
    app.config.setdefault('DB', 'db.db')
    if isinstance(config, collections.Mapping):
        app.config.update(config)
    else:
        app.config.from_object(config)

    # View registering
    views.register_views(app)

    # DB connection
    app.db_engine = create_engine(app.config['DB'])
    m.Base.metadata.bind = app.db_engine
    m.Session.configure(bind=app.db_engine)

    # Middlewares
    SQLAlchemyMiddleware(m.Session, app)
    ContentNegotiationMiddleware(app)
    BabelMiddleware(app)
    return app
