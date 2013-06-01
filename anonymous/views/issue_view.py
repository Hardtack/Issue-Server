import datetime
from .. import models as m
from ..render import render
from sqlalchemy import and_
from flask import Blueprint
from flask.ext.router import Router
from flask.ext.negotiation import provides


issue_blueprint = Blueprint('issue', __name__)
view_router = Router(issue_blueprint, 'view')

@view_router('/issue/', methods=['GET'])
@provides('application/json')
def view(issue_id):
    render(m.Issue.query.all())

@view_router('/issue/<int:issue_id>', methods=['GET'])
@provides('application/json')
def read_view(issue_id):
    return render(
        m.Issue.query.filter_by(id=issue_id).first_or_404()
    )

@issue_blueprint.route('/issue/current', methods=['GET'])
@provides('application/json')
def current_view():
    today = datetime.date.today()
    return render(
        m.Issue.query.filter(
            and_(
                m.Issue.start_date <= today,
                m.Issue.end_date >= today
            )
        ).first_or_404()
    )
