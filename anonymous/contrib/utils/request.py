""":mod:`utils.request`
=======================

Simple utils for flask request.  
"""
from flask import request, abort
from functools import wraps

class Rename(object):
    """Rename GET parameter's name.

    :param origin: original name of GET parameter
    :param to: new name of `origin`

    You can use it like::  

       from meetytools.utils import get_params, Rename

       @app.route('/some_view')
       @get_params(Rename('with', 'with_arg'), 'search')
       def some_view(with_arg, search):
           return 'with : %s, search : %s'%(with_arg, search)
    """
    def __init__(self, origin, to):
        self.origin = origin
        self.to = to

def get_params(*params):
    """Binds GET paramter with view's parameter.  

    :param params: names of parameters.  

    Types of each item in params - :class:`str` or :class:`unicode` to just
    name, :class:`tuple` to (name, default_value), :class:`Rename` to
    renaming.  
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            d = {}
            for param in params:
                if isinstance(param, tuple):
                    name, default = param[0], param[1]
                else:
                    name, default = param, None
                if isinstance(name, Rename):
                    d[name.to] = request.args.get(name.origin, default)
                else:
                    d[name] = request.args.get(name, default)
            d.update(kwargs)
            return fn(*args, **d)
        return wrapper
    return decorator

def perm(statement, code=403):
    """Checks permission.  

    Asserts by statement.  if assertion failed, call :func:`flask.abort` with
    `code`

    :param statement: assertion statement
    :param code: http status code
    """
    if not statement:
        abort(code)
