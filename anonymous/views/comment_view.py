from .. import models as m
from ..auth import login_required
from ..render import render
from flask import Blueprint, g, request
from flask.ext.router import Router
from flask.ext.negotiation import provides

comment_blueprint = Blueprint('comment', __name__)
view_router = Router(comment_blueprint, 'view')

@view_router('/photo/<int:photo_id>/comment/', methods=['GET'])
@provides('application/json')
def view(photo_id):
    return render(
        m.Comment.query.fiter_by(
            photo=m.Photo.query.filter_by(id=photo_id).first_or_404()
        ).order_by(m.Comment.created_at).all()
    )

@view_router('/comment/<int:comment_id>', methods=['GET'])
@provides('application/json')
def read_view(comment_id):
    return render(
        m.Comment.query.filter_by(id=comment_id).first_or_404()
    )

@view_router('/photo/<int:photo_id>/comment/', methods=['POST'])
@provides('application/json')
@login_required
def create_view(photo_id):
    photo = m.Photo.query.filter_by(id=photo_id).first_or_404()
    content = request.form['content']
    comment = m.Comment(writer=g.user, photo=photo, content=content)
    g.session.add(comment)
    g.session.commit()
    return render(comment, status=201)

@view_router('/comment/<int:comment_id>', methods=['DELETE'])
@provides('application/json')
def delete_view(comment_id):
    comment = m.Comment.query.filter_by(id=comment_id).first_or_404()
    g.session.delete(comment)
    g.session.commit()
    return render(None, status=204)

