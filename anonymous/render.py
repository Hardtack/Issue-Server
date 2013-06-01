from json import JSONEncoder
from contrib.typeconverter import Converter
from flask.ext.negotiation import Render
from flask.ext.negotiation.renderers import JSONRenderer

class ConvertEncoder(JSONEncoder):
    def default(self, obj):
        return converter.convert(obj)

converter = Converter((list, dict, int, float, str, unicode))
convert_encoder = ConvertEncoder(converter)
render = Render(renderers=(JSONRenderer(encoder=convert_encoder)))
