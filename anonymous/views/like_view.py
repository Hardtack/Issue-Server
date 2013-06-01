from .. import models as m
from ..auth import login_required
from ..render import render
from flask import Blueprint, g
from flask.ext.router import Router
from flask.ext.negotiation import provides

like_blueprint = Blueprint('like', __name__)
view_router = Router(like_blueprint, 'view')

@view_router('/photo/<int:photo_id>/like/', methods=['GET'])
@provides('application/json')
def view(photo_id):
    return render(
        m.Like.query.fiter_by(
            photo=m.Photo.query.filter_by(id=photo_id).first_or_404()
        ).all()
    )

@view_router('/like/<int:like_id>', methods=['GET'])
@provides('application/json')
def read_view(like_id):
    return render(
        m.Like.query.filter_by(id=like_id).first_or_404()
    )

@view_router('/photo/<int:photo_id>/like/', methods=['POST'])
@provides('application/json')
@login_required
def create_view(photo_id):
    photo = m.Photo.query.filter_by(id=photo_id).first_or_404()
    like = m.Like(user=g.user, photo=photo)
    g.session.add(like)
    g.session.commit()
    return render(like, status=201)

@view_router('/like/<int:like_id>', methods=['DELETE'])
@provides('application/json')
def delete_view(like_id):
    like = m.Like.query.filter_by(id=like_id).first_or_404()
    g.session.delete(like)
    g.session.commit()
    return render(None, status=204)

