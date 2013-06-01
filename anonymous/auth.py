import models as m
from functools import wraps
from flask import session, g, Blueprint, abort, request
from render import render

def authenticate(username, password):
    user = m.User.filter_by(username=username).first()
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
    return m.User.filter_by(id=user_id).first()

def login_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        if g.user is None:
            abort(401)
        return fn(*args, **kwargs)
    return decorator

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.before_request
def before_request():
    g.user = get_login_user()

@auth_blueprint.route('/login', methods=['POST'])
def login_view():
    username = request.form['username']
    password = request.form['username']
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
