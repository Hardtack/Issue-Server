from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

class BeakerSessionInterface(SessionInterface):
    def __init__(self, environ_key='beaker.session', *args, **kwargs):
        super(BeakerSessionInterface, self).__init__(*args, **kwargs)
        self.environ_key = environ_key

    def open_session(self, app, request):
        return request.environ.get(self.environ_key, None)

    def save_session(self, app, session, response):
        session.save()

class BeakerMiddleware(object):
    def __init__(self, app=None, environ_key='beaker.session'):
        self.app = app
        self.environ_key = environ_key
        if self.app is not None:
            self.init_app(app, environ_key)

    def init_app(self, app, environ_key):
        beaker_config = app.config.get('BEAKER_SESSION', {
            'session.type':'file',
            'session.data_dir':'/tmp/beaker/data',
            'session.lock_dir':'/tmp/beaker/lock',
            'session.url':None,
            'session.cookie_expires':True,
        })
        app.wsgi_app = SessionMiddleware(app.wsgi_app, beaker_config,
            environ_key)
        app.session_interface = BeakerSessionInterface(environ_key)
