import models as m
import datetime
from json import JSONEncoder
from contrib.utils import timestamp
from contrib.typeconverter import Converter
from flask.ext.negotiation import Render
from flask.ext.negotiation.renderers import Renderer

class ConvertEncoder(JSONEncoder):
    def default(self, obj):
        return converter.convert(obj)

class DeepConverter(Converter):
    def assert_type(self, obj):
        super(DeepConverter, self).assert_type(obj)
        if isinstance(obj, list):
            for i in obj:
                self.assert_type(i)
        elif isinstance(obj, dict):
            for k, v in obj.iteritems():
                self.assert_type(k)
                self.assert_type(v)

converter = DeepConverter((list, dict, int, float, str, unicode))
convert_encoder = ConvertEncoder(converter)


class ConvertJSONRenderer(Renderer):
    __media_types__ = ('application/json', )
    def render(self, data, template=None, ctx=None):
        return convert_encoder.encode({'data':data})
render = Render(renderers=(ConvertJSONRenderer(), ))

@converter.handle(m.Base)
def convert_model(model):
    d = {
        '__type__':'model.' + model.__class__.__name__,
    }
    attrs = [x.name for x in model.__table__.columns]
    withs = set(getattr(model, '__with__', ()))
    exs = set(getattr(model, '__ex__', ()))
    attrs |= withs
    attrs -= exs
    for attr in attrs:
        x = object()
        value = getattr(model, attr, x)
        if value is x:
            continue
        d[attr] = converter.convert(value)
    return d

@converter.handle(datetime.datetime)
def convert_datetime(date):
    return {
        '__type__':'datetime',
        'timestamp':timestamp(date),
    }

@converter.handle(dict)
def convert_dict(d):
    converted = {}
    for k, v in d.iteritems():
        converted[converter.convert(k)] = converter.convert(v)
    return converted

@converter.handle(list)
def convert_list(li):
    return map(converter.convert, li)

@converter.default
def convert(obj):
    if callable(getattr(obj, '__default__', None)):
        return obj.__default__()
    raise TypeError('Cannot convert object of ' + str(type(obj)))
