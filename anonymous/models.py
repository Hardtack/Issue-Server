import hashlib
import sqlalchemy as s
from sqlalchemy import func
from sqlalchemy.orm import (validates, relationship, scoped_session,
    sessionmaker)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from contrib.ext.sqlalchemy_ext import Query
from sqlalchemy_imageattach.entity import Image, image_attachment

Base = declarative_base()

def make_password(raw):
    md5 = hashlib.md5()
    md5.update(raw)
    return md5.hexdigest()

class User(Base):
    __tablename__ = 'user'
    __with__ = ('image_url', )
    __ex__ = ('password', )

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

    #password definitions
    _password = s.Column('password', s.String(128), nullable=True)

    @hybrid_property
    def password(self):
        """User's password
        """
        return self._password

    @password.setter
    def password(self, password):
        """Setter of :data:`password`.  It automatically hashes raw password.  

        :param password: raw password string.  
        """
        if password is None:
            self._password = None
            return
        if password == '':
            hashed = ''
        else:
            hashed = make_password(password)
        self._password = hashed

    @password.expression
    def password(self):
        return User._password

    def check_password(self, password):
        """Checks password.  

        :param password: raw password string.  
        """
        return self.password == make_password(password)
    
    image = image_attachment('UserImage')
    created_at = s.Column(s.DateTime, nullable=False, default=func.now())

    @property
    def image_url(self):
        return self.image.locate()

class UserImage(Base, Image):
    __tablename__ = 'user_image'
    user_id = s.Column(s.Integer, s.ForeignKey('user.id'), primary_key=True)
    user = relationship('User', primaryjoin='UserImage.user_id==User.id')

    @property
    def object_id(self):
        return self.user_id

class Issue(Base):
    __tablename__ = 'issue'
    __with__ = ('writer', )

    id = s.Column(s.Integer, primary_key=True)
    title = s.Column(s.String(255), nullable=False)
    description = s.Column(s.Text, nullable=False)
    start_date = s.Column(s.Date, nullable=False, default=func.now())
    end_date = s.Column(s.Date, nullable=True, default=None)
    created_at = s.Column(s.DateTime, nullable=False, default=func.now())

class Photo(Base):
    __tablename__ = 'photo'
    __with__ = ('image_url', 'writer', 'likes_count', 'comments_count')

    id = s.Column(s.Integer, primary_key=True)
    content = s.Column(s.Text, nullable=False)

    writer_id = s.Column(s.Integer, s.ForeignKey('user.id', ondelete='CASCADE'))
    writer = relationship('User', primaryjoin=('Photo.writer_id==User.id'))

    issue_id = s.Column(s.Integer, s.ForeignKey('issue.id', ondelete='CASCADE'))
    issue = relationship('Issue', primaryjoin='Photo.issue_id==Issue.id')

    image = image_attachment('PhotoImage')
    created_at = s.Column(s.DateTime, nullable=False, default=func.now())

    @property
    def image_url(self):
        return self.image.locate()

    @property
    def likes_count(self):
        return Like.query.filter_by(photo=self).count()

    @property
    def comments_count(self):
        return Comment.query.filter_by(photo=self).count()

class PhotoImage(Base, Image):
    __tablename__ = 'photo_image'
    id = s.Column(s.Integer, primary_key=True)
    photo_id = s.Column(s.Integer, s.ForeignKey('photo.id'), primary_key=True)
    photo = relationship('Photo', primaryjoin='PhotoImage.photo_id==Photo.id')

    @property
    def object_id(self):
        return self.photo_id

class Comment(Base):
    __tablename__ = 'comment'
    id = s.Column(s.Integer, primary_key=True)
    writer_id = s.Column(s.Integer, s.ForeignKey('user.id', ondelete='CASCADE'))
    writer = relationship('User', primaryjoin='Comment.writer_id==User.id')

    photo_id = s.Column(s.Integer, s.ForeignKey('photo.id', ondelete='CASCADE'))
    photo = relationship('Photo', primaryjoin='Comment.photo_id==Photo.id')

    content = s.Column(s.Text, nullable=False)
    created_at = s.Column(s.DateTime, nullable=False, default=func.now())

class Like(Base):
    __tablename__ = 'like'
    id = s.Column(s.Integer, primary_key=True)
    user_id = s.Column(s.Integer, s.ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', primaryjoin='Like.user_id==User.id')

    photo_id = s.Column(s.Integer, s.ForeignKey('photo.id', ondelete='CASCADE'))
    photo = relationship('Photo', primaryjoin='Like.photo_id==Photo.id') 

session_factory = sessionmaker(query_cls=Query)
Session = scoped_session(session_factory)

# Query Property
Base.query = Session.query_property()

def create_tables():
    Base.metadata.create_all()

def drop_tables():
    Base.metadata.drop_all()
