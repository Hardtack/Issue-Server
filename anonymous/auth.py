import models as m
from functools import wraps
from flask import session, g, Blueprint, abort, request
from render import render

def authenticate(username, password):
    user = m.User.query.filter_by(username=username).first()
    if user is None and not user.check_password(password):
        return None
    return user

def login(user):
    session['user_id'] = user.id

def logout(user):
    if session.has_key('user_id'):
        del session['user_id']

def get_login_user():
    user_id = session.get('user_id', None)
    if user_id:
        return m.User.query.filter_by(id=user_id).first()
    auth = request.authorization
    if auth:
        return authenticate(auth.username, auth.password)
    return None

def login_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        if getattr(g, 'user', None) is None:
            abort(401)
        return fn(*args, **kwargs)
    return decorator

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login_view():
    username = request.form['username']
    password = request.form['password']
    user = authenticate(username, password)
    if user is None:
        abort(400)
    login(user)
    return render(user, status=200)

@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout_view():
    logout(g.user)
    return render('Done', status=200)

@auth_blueprint.route('/me')
@login_required
def me_view():
    return render(g.user)
