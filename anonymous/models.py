import sqlalchemy as s
from sqlalchemy.orm import (validates, relationship, scoped_session,
    sessionmaker)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from contrib.utils.validators import validate_email
from contrib.ext.sqlalchemy_ext import Query

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = s.Column(s.Integer, primary_key=True)

    #username definitions
    _username = s.Column('username', s.String(20), nullable=False, unique=True)

    @hybrid_property
    def username(self):
        """User's unique name
        """
        return self._username

    @username.setter
    def username(self, username):
        if not username is None:
            username = username.lower()
        self._username = username

    @validates('_username')
    def _validate_username(self, key, username):
        # FIXME
        return username

session_factory = sessionmaker(query_cls=Query)
Session = scoped_session(session_factory)

# Query Property
Base.query = Session.query_property()

def create_tables():
    Base.metadata.create_all()

def drop_tables():
    Base.metadata.drop_all()
