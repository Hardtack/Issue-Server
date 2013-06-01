from flask import g, request
from meetytools.content_negotiation.renderers import (TemplateRenderer,
    JSONRenderer)
from jinja2.ext import Extension, loopcontrols
from jinja2 import nodes, Markup

# Jinja2 setting
class _CsrfTokenExtension(Extension):
    tags = set(['csrf_token'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        return nodes.Output([self.call_method('_render')]).set_lineno(lineno)
    def _render(self):
        return Markup('')

_JINJA_EXTENTIONS=(_CsrfTokenExtension, loopcontrols)

class ContentNegotiationMiddleware(object):
    def __init__(self, app=None, default_renderers=None):
        self.app = app
        if default_renderers is None:
            default_renderers = (TemplateRenderer, JSONRenderer)
        self.default_renderers = default_renderers
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app, default_renderers=None):
        if default_renderers is None:
            default_renderers = self.default_renderers

        for ext in _JINJA_EXTENTIONS:
            app.jinja_env.add_extension(ext)

        @app.before_request
        def before_request():
            g.renderers = map(lambda x:x(), default_renderers)
            g.with_arg = request.args.get('with', None)
