from flask import g, request, current_app
from flask.ext.babel import Babel
from meetytools import texter
from meetytools.utils import str_to_bool

class FlaskBabelText(texter.Text):
    def __init__(self, *args, **kwargs):
        super(FlaskBabelText, self).__init__(*args, **kwargs)

    @property
    def default_locale(self):
        try:
            return str(current_app.babel.default_locale)
        except (RuntimeError, AttributeError):
            return self._default_locale

    @default_locale.setter
    def default_locale(self, default_locale):
        self._default_locale = default_locale

class FlaskBabelTexter(texter.Texter):
    def text(self, f):
        return FlaskBabelText(self.locale, f)

class BabelMiddleware(object):
    def __init__(self, app=None, environ_key='beaker.session'):
        self.app = app
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        babel = Babel(app)
        app.babel = babel
        @babel.localeselector
        def get_locale():
            locale = getattr(g, 'locale', None)
            if not locale is None:
                return locale
            ignore_user_locale = str_to_bool(
                request.headers.get('x-meety-ignore-user-locale', 'false'),
                False
            )
            if not ignore_user_locale:
                user = getattr(g, 'user', None)
                if user is not None:
                    return user.locale
            locale = request.accept_languages.best_match(['en', 'ko'])
            return locale

        @babel.timezoneselector
        def get_timezone():
            pass
