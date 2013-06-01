""":mod:`utils.serializer`
==========================

Provides many utils related to serialization.  
"""
import json
import numbers
import collections
from speaklater import is_lazy_string
from datetime import datetime
from module import ismoduleinstance
from . import is_iterable, is_list_like, timestamp, safe_unicode as u

_user_model_map = {}

def register_serializer(type, serializer):
    _user_model_map[type] = serializer

def register_sqlalchemy_model(model):
    register_serializer(model, _serialize_model)

class NotSerializable(Exception):
    """Be raised when not serializable.
    """
    pass

def _serialize_addtional(obj, additional_attrs=(), ignore_error=False):
    """Serialize attributes needed additionally.
    """
    d = {}
    dict_like = isinstance(additional_attrs, collections.Mapping)
    for attr in additional_attrs:
        try:
            additional_deep = ()
            if dict_like:
                deep = additional_attrs[attr]
                if isinstance(deep, basestring):
                    additional_deep=(deep, )
                elif is_iterable(deep):
                    additional_deep = deep
            d[attr] = serialize(getattr(obj, attr), additional_deep,
                ignore_error)
        except AttributeError:
            pass
        except Exception:
            if not ignore_error:
                raise
    return d

def _serialize_file_storage(file_storage, additional_attrs, ignore_error):
    """Serialize :class:`wtforms.Form`
    """
    d = {
        '__type__':'file_storage',
        'filename':file_storage.filename,
    }
    d.update(_serialize_addtional(file_storage, additional_attrs, ignore_error))
    return d

def _serialize_date(date, additional_attrs, ignore_error):
    """Serialize date.  
    """
    d = {
        '__type__':'date',
        'timestamp':timestamp(date),
    }
    d.update(_serialize_addtional(date, additional_attrs, ignore_error))
    return d

def _serialize_model(model, additional_attrs=(), ignore_error=False):
    """Serialize model
    """
    d = {
        '__type__':'model.' + model.__class__.__name__,
    }
    serialize_ex = getattr(model, '__serialize_ex__', ())
    serialize_with = getattr(model, '__serialize_with__', ())
    if isinstance(additional_attrs, collections.Mapping):
        d = {}
        for attr in [x for x in serialize_with if x not in serialize_ex]:
            d[attr] = None
        additional_attrs.update(d)
    elif is_list_like(additional_attrs):
        additional_attrs = tuple(additional_attrs)
        additional_attrs += tuple(
            x for x in serialize_with if x not in serialize_ex
        )
    else:
        additional_attrs = serialize_with

    for column in model.__table__.columns:
        try:
            attr = column.name
            if attr in serialize_ex:
                continue
            value = getattr(model, attr)
            d[attr]=serialize(value)
        except Exception:
            if not ignore_error:
                raise
    d.update(_serialize_addtional(model, additional_attrs, ignore_error))
    return d

def serialize(obj, additional_attrs=(), ignore_error=False):
    """Converts some kinds of object to serilized object. (In fact, it does 
    not serialize object, but converts to generally serializable object.)
    """
    if obj is None:
        return None
    elif isinstance(obj, tuple(_user_model_map.keys())):
        for type in _user_model_map.iterkeys():
            if isinstance(obj, type):
                return _user_model_map[type](obj, additional_attrs,
                    ignore_error)
    elif callable(getattr(obj, 'serialize', None)):
        d = obj.serialize()
        d.update(_serialize_addtional(obj, additional_attrs, ignore_error))
        return d
    elif ismoduleinstance(obj, 'werkzeug.FileStorage'): # Werkzeug filestorage
        return _serialize_file_storage(obj, additional_attrs, ignore_error)
    elif isinstance(obj, datetime):
        return _serialize_date(obj, additional_attrs, ignore_error)
    elif isinstance(obj, tuple):
        return tuple(map(lambda x:serialize(x, additional_attrs, ignore_error),
            obj))
    elif isinstance(obj, (numbers.Number, basestring)):
        return obj
    elif is_lazy_string(obj):
        return u(obj)
    elif isinstance(obj, collections.Mapping):
        d={}
        for k, v in dict(obj).iteritems():
            d[k] = serialize(v, additional_attrs, ignore_error)
        return d
    elif is_list_like(obj):
        return [serialize(x, additional_attrs, ignore_error) for x in obj]
    else:
        raise NotSerializable(repr(obj))

def is_serialized(obj):
    """Check whether `obj` is generally serilized object or not.
    """
    _serialized_types = (type(None), numbers.Number, basestring)
    if isinstance(obj, _serialized_types):
        return True
    elif isinstance(obj, dict):
        for k, v in obj.iteritems():
            if not (is_serialized(k) and is_serialized(v)):
                return False
        return True
    elif isinstance(obj, (list, tuple, set)):
        for i in obj:
            if not is_serialized(i):
                return False
        return True
    else:
        return False

def jsonify(obj, additional_attrs=()):
    """Shortener of `json.dumps(serialize(obj, additional_attrs))`.  
    """
    return json.dumps(serialize(obj, additional_attrs))
