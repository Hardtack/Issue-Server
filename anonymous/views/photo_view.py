from .. import models as m
from ..auth import login_required
from ..render import render
from flask import Blueprint, g, request, current_app as app
from flask.ext.router import Router
from flask.ext.negotiation import provides
from sqlalchemy_imageattach.context import store_context

photo_blueprint = Blueprint('photo', __name__)
view_router = Router(photo_blueprint, 'view')

@view_router('/issue/<int:issue_id>/photo/', methods=['GET'])
@provides('application/json')
def view(issue_id):
    issue = m.Issue.query.filter_by(id=issue_id).first_or_404()
    photos = m.Photo.query.filter_by(
        issue_id=issue.id
    ).order_by(m.Photo.created_at).all()
    return render(photos)

@view_router('/photo/<int:photo_id>', methods=['GET'])
@provides('application/json')
def read_view(photo_id):
    return render(
        m.Photo.query.filter_by(id=photo_id).first_or_404()
    )

@view_router('/issue/<int:issue_id>/photo/', methods=['POST'])
@provides('application/json')
@login_required
def create_view(issue_id):
    issue = m.Issue.query.filter_by(id=issue_id).first_or_404()
    image = request.files['image']
    content = request.form['content']
    photo = m.Photo(writer=g.user, content=content, issue=issue)
    with store_context(app.store):
        photo.image.from_file(image)
    return render(photo, status=201)

@view_router('/photo/<int:photo_id>', methods=['DELETE'])
@provides('application/json')
def delete_view(photo_id):
    photo = m.Photo.query.filter_by(id=photo_id).first_or_404()
    g.session.delete(photo)
    g.session.commit()
    return render(None, status=204)

