from user_view import user_blueprint

def register_views(app):
    app.register_blueprint(user_blueprint)
