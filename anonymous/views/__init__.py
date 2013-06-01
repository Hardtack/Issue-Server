from user_view import user_blueprint
from photo_view import photo_blueprint
from issue_view import issue_blueprint

def register_views(app):
    app.register_blueprint(user_blueprint)
    app.register_blueprint(photo_blueprint)
    app.register_blueprint(issue_blueprint)
