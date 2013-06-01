""":mod:`typeconverter`
=======================

Converts object into specified type.  
"""
from functools import wraps

class Handler(object):
    def __init__(self, fn, domain):
        super(Handler, self).__init__()
        self.fn = fn
        self.domain = domain
        self.handlable = self.default_handlable

    def default_handlable(self, obj):
        """Default handlability checker.   
        Just check type of instance.  
        """
        for t in self.domain:
            if isinstance(obj, t):
                return True
        return False

    def __call__(self, obj):
        return self.fn(obj)

    def check_handlable(self, fn):
        """Decorator for function that indicates the handler can handle
        object.  
        """
        self.handlable = fn
        return fn

    def can_handle(self, obj):
        return self.handlable(obj)

class Converter(object):
    """Converts object into specified types.  
    """
    def assert_type(self, obj):
        """Asserts if type of `obj` is in range of the converter.  
        """
        for t in self.range:
            if isinstance(obj, t):
                return
        assert False

    def inrange(self, obj):
        """Checks if `obj` is in range of the conveter.  
        """
        try:
            self.assert_type(obj)
        except AssertionError:
            return False
        return True

    def handle(self, *types):
        """Decorator for function that converts type.  
        """
        def decorator(fn):
            handler = Handler(fn, types)
            wraps(fn)(handler)
            self.handlers.append(handler)
            return handler
        return decorator

    def default(self, fn):
        """Decorator that changes default handler.  
        """
        self.default_handler = fn
        return fn

    def convert(self, obj):
        while not self.inrange(obj):
            handled = False
            for handler in self.handlers:
                if handler.can_handle(obj):
                    obj = handler(obj)
                    handled = True
            if not handled:
                return self.default_handler(obj)
        return obj

    def default_handler(self, obj):
        """Default convert handler.  
        It just raises :type:`TypeError`
        """
        raise TypeError('Cannot convert object of ' + str(type(obj)))

    def __init__(self, range):
        super(Converter, self).__init__()
        if isinstance(range, type):
            range = [range]
        self.range = range
        self.handlers = []
