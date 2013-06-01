from .. import models as m
from ..render import render
from flask import Blueprint, g, request, abort
from flask.ext.router import Router
from flask.ext.negotiation import provides
from sqlalchemy import or_

user_blueprint = Blueprint('user', __name__)
view_router = Router(user_blueprint, 'view')

@view_router('/user/', methods=['GET'])
@provides('application/json')
def index_view():
    return render(m.User.query.all())

@view_router('/user/<user_id>', methods=['GET'])
@provides('application/json')
def read_view(user_id):
    return render(m.User.query.filter(
        or_(
            m.User.id==user_id,
            m.User.username==user_id.lower()
        )
    ).first_or_404())

@view_router('/user/', methods=['POST'])
@provides('application/json')
def create_view():
    username = request.form['username']
    password = request.form['password']
    if not m.User.query.filter_by(username=username).first() is None:
        abort(400)
    user = m.User(username=username, password=password)
    g.session.add(user)
    g.session.commit()
    return render(user)

@view_router('/user/<user_id>', methods=['DELETE'])
@provides('application/json')
def delete_view(user_id):
    user = m.User.query.filter(
        or_(
            m.User.id==user_id,
            m.User.username==user_id.lower()
        )
    ).first_or_404()
    g.session.delete(user)
    g.session.commit()
    return render(None, status=204)
