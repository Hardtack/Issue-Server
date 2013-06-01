import models as m
import datetime
from json import JSONEncoder
from contrib.utils import timestamp
from contrib.typeconverter import Converter
from flask.ext.negotiation import Render
from flask.ext.negotiation.renderers import JSONRenderer

class ConvertEncoder(JSONEncoder):
    def default(self, obj):
        return converter.convert(obj)

converter = Converter((list, dict, int, float, str, unicode))
convert_encoder = ConvertEncoder(converter)
render = Render(renderers=(JSONRenderer(encoder=convert_encoder),))

@converter.handle(m.Base)
def convert_model(model):
    d = {
        '__type__':'model.' + model.__class__.__name__,
    }
    for column in model.__table__.columns:
        attr = column.name
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

