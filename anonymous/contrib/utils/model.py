""":mod:`utils.model`
=====================

Provides many utils for :mod:`meetytools.models`
"""
import json
import collections
from flask import request
from . import is_list_like, str_to_bool
from serializer import serialize
from sqlalchemy.orm import Query
from sqlalchemy.sql.operators import ColumnOperators

def get_object_or_404(model_class, pk, session=None):
    """Returns model indentified by `pk`.  If there's no such a model
    abort 404 by :func:`flask.abort`.  
    :returns: found model
    :rtype: `model_class`
    
    Example::
       
       from meetytools.utils.model import get_object_or_404
       from meetytools.model import User

       user = get_object_or_404(User, pk=1) # 1 exists, succeed
       user = get_object_or_404(User, pk=2) # not exists, fail
    """
    from flask import abort, g
    session = session or g.session
    obj = session.query(model_class).filter(model_class.id==pk).first()
    if obj is None:
        abort(404)
    return obj

def get_or_create(model, defaults=None, session=None, **kwargs):
    """Get model with options. If such a model not exists, create model with 
    options.
    :returns: model and boolean value that indicates created bound by tuple
    (model, created)
    :rtype: :class:`tuple`
    Example::
       
       from meetytools.utils.model import get_or_create
       from meetytools.model import SomeModel
    """
    from flask import g
    from sqlalchemy.sql.expression import ClauseElement
    session = session or g.session
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems()
            if not isinstance(v, ClauseElement))
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        return instance, True

def filter_models(q, last_id=None, count=None, model=None, order_by=None, 
    pk_name='id', desc=None):
    """Filters query with `last_id`, count by `count` and order by `order_by`.  
    How to use::

       from meetytools.utils.model import filter_models

    :param last_id: bottom-model's primary key
    :param order_by: ordering keyword or column
    :returns: filtered models
    :rtype: :class:`list`
    """
    last_id = request.args.get('last_id', None) if last_id is None else last_id
    count = request.args.get('count', 15) if count is None else count
    order_by = (request.args.get('order_by', None) if order_by is None else
        order_by)
    desc = request.args.get('desc', False) if desc is None else desc

    if model is None or model == '':
        model = q.column_descriptions[0]['expr']

    if isinstance(desc, basestring):
        desc = str_to_bool(desc, False)
    if desc:
        q.desc = desc

    if isinstance(order_by, basestring):
        li = [x.strip() for x in order_by.split(',')]
    elif isinstance(order_by, ColumnOperators):
        li = [order_by]
    elif not isinstance(order_by, collections.Iterable):
        li = [order_by]
    else:
        li = order_by

    order_bys = []
    for order_by in li:
        if isinstance(order_by, basestring):
            ex = getattr(model, '__serialize_ex__', [])
            if not order_by in ex:
                order_by = getattr(model, order_by, None)
                if not order_by is None:
                    order_bys.append(order_by)
        else:
            order_bys.append(order_by)

    if order_bys:
        if last_id is not None:
            for order_by in order_bys:
                if desc:
                    q = q.filter(order_by < Query(order_by).filter_by(
                        **{pk_name:last_id}).as_scalar())
                else:
                    q = q.filter(order_by > Query(order_by).filter_by(
                        **{pk_name:last_id}).as_scalar())
        if desc:
            q = q.order_by(*[x.desc() for x in order_bys])
        else:
            q = q.order_by(*order_bys)

    if count is not None:
        if count != 'all':
            try:
                count = int(count)
                return q[:count]
            except:
                pass
    return q.all()
     
def serialize_with(obj, with_arg):
    """Serialize object with attributes whose name in `with_arg`.  
    You can serialize object deeply by set `with_arg` json serialized 
    dictionary.  For example::
       
       import json
       from meetytools.utils import notnull
       from meetytools.utils.model import serialize_with

       d = {
           'model2':['model3']
       }
       with_arg = json.dumps(d)
       serialized = serialize_with(model1, d)

       # serialized => '{"model2": {"model3": {"some_attr": "some_value"}, \
       # "some_attr": "some_value"}, "some_attr": "some_value"}'
    """
    try:
        args = json.loads(with_arg)
    except:
        try:
            args = tuple(map(lambda x:x.strip(), with_arg.split(',')))
        except:
            args = ()
    if is_list_like(obj):
        f = (lambda x:serialize(x, additional_attrs=args))
        return map(f, obj)
    else:
        return serialize(obj, additional_attrs=args)
