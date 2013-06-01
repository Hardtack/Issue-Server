""":mod:`utils.proxy`
=====================

Proxy object with getter
"""
class Proxy(object):
    """Object that proxying object with object getter function.  
    You can use it like: 

    >>> from meetytools.utils.proxy import Proxy
    >>> obj = 1
    >>> getter = lambda:obj
    >>> proxy = Proxy(getter)
    >>> print proxy
    1

    """
    __slots__ = ["_obj", "__weakref__"]
    def __init__(self, obj, exclude_names=None):
        object.__setattr__(self, '_obj', obj)
        object.__setattr__(self, '_exclude_names', exclude_names or [])
    
    #
    # proxying (special cases)
    #
    def __getattribute__(self, name):
        _exclude_names = object.__getattribute__(self, '_exclude_names')
        if name in _exclude_names:
            return super(Proxy, self).__getattribute__(name)
        else:
            return getattr(object.__getattribute__(self, "_obj")(), name)
    def __delattr__(self, name):
        _exclude_names = object.__getattribute__(self, '_exclude_names')
        if name in _exclude_names:
            super(Proxy, self).__delattr__(name)
        else:
            delattr(object.__getattribute__(self, "_obj")(), name)
    def __setattr__(self, name, value):
        _exclude_names = object.__getattribute__(self, '_exclude_names')
        if name in _exclude_names:
            super(Proxy, self).__setattr__(name, value)
        else:
            setattr(object.__getattribute__(self, "_obj")(), name, value)
    
    def __nonzero__(self):
        return bool(object.__getattribute__(self, "_obj")())
    def __str__(self):
        return str(object.__getattribute__(self, "_obj")())
    def __repr__(self):
        return repr(object.__getattribute__(self, "_obj")())
    
    #
    # factories
    #
    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__', 
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__', 
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', 
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__', 
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__',
        '__irshift__', '__isub__', '__iter__', '__itruediv__', '__ixor__',
        '__le__', '__len__', '__long__', '__lshift__', '__lt__', '__mod__',
        '__mul__', '__ne__', '__neg__', '__oct__', '__or__', '__pos__',
        '__pow__', '__radd__', '__rand__', '__rdiv__', '__rdivmod__',
        '__reduce__', '__reduce_ex__', '__repr__', '__reversed__',
        '__rfloorfiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__',
        '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__',
        '__rxor__', '__setitem__', '__setslice__', '__sub__', '__truediv__',
        '__xor__', 'next',
    ]
    
    @classmethod
    def _create_class_proxy(cls, theclass):
        """creates a proxy for the given class"""
        
        def make_method(name):
            def method(self, *args, **kw):
                _exclude_names = object.__getattribute__(self,
                    '_exclude_names')
                if name in _exclude_names:
                    return getattr(self, name)(*args, **kw)
                else:
                    return getattr(
                        object.__getattribute__(self, "_obj")(), name
                    )(*args, **kw)
            return method
        
        namespace = {}
        for name in cls._special_names:
            if hasattr(theclass, name):
                namespace[name] = make_method(name)
        return type(
            "%s(%s)" % (cls.__name__, theclass.__name__), (cls,), namespace
        )
    
    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an 
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(
                obj.__class__
            )
        ins = object.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins
