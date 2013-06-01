""":mod:`utils`
===============

Utilities.  
"""
import os
import time
import collections
import rfc822
import cStringIO
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from datetime import datetime
from random import uniform
from wsgiref.handlers import format_date_time
 
def is_iterable(v):
    """Check whether `v` is iterable or not.
    """
    try:
        iter(v)
        return True
    except:
        return False

def is_list_like(v):
    """Check whether `v` is list-like object or not.  
    """
    return not isinstance(v, basestring) and isinstance(v, collections.Sequence)

def match_one(target, operand, *args):
    """Returns :const:`True` if more than one of operands are same with
    `target`.  
    """
    operands = (operand,) + args
    return target in operands

def truncate(string, length, tail='...'):
    """Truncates `string` if it is longer than `length`, and mark
    with `tail`.  
    """
    if len(string) <= length:
        return string
    else:
        return string[:length - len(tail)] + tail

def timestamp(dt):
    """Returns datetime value of `dt`.  
    """
    return time.mktime(dt.timetuple())

def repr_rfc1123(dt):
    """Returns RFC 1123 represented datetime string.  
    """
    return format_date_time(timestamp(dt))

def repr_rfc822(dt):
    """Returns RFC 822 represented datetime string.  
    """
    return rfc822.formatdate(dt)

def str_to_bool(s, default=None):
    """Changes str to bool by checking content of `s`.  

    :param s: original str.
    :param default: default value that is returned when cannot change str to 
        bool.  
    """
    if not isinstance(s, basestring):
        return default
    s = s.lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        return default

def has_keys(d, keys):
    """Check whether `d` has all keys in `keys` or not.  
    """
    for key in keys:
        if not d.has_key(key):
            return False
    return True

def random_time(time1, time2):
    """Create :class:`datetime.datetime` object randomly in between time1 and
    time2.  
    """
    t1 = timestamp(time1)
    t2 = timestamp(time2)
    if t1 > t2:
        t1, t2 = t2, t1
    random_timestamp = uniform(t1, t2)
    return datetime.fromtimestamp(random_timestamp)

def is_integer(s):
    """Check whether `s` is integer string or not.  
    """
    return all(ord('0') <= ord(c) <= ord('9') for c in s)

def is_ascii(s):
    """Check whether `s` is ascii string or not.  
    """
    return all(0 <= ord(c) < 128 for c in s)

def is_eng_alphabet(c):
    """Check whether `c` is english alphabet charater.  
    """
    return ord('a') <= ord(c) <= ord('z') and ord('A') <= ord(c) <= ord('Z')

def is_eng_string(s):
    """Check whether `s` is english string or not.  
    """
    return all(is_eng_string(c) for c in s)

def is_number(s):
    """Check whether `s` is number string or not.  
    """
    return all(ord('0') <= ord(c) <= ord('9') for c in s)

@contextmanager
def StringIO(*args, **kwargs):
    io = cStringIO.StringIO(*args, **kwargs)
    try:
        yield io
    finally:
        io.close()

class DictMixin(collections.Mapping):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def keys(self, key, value):
        pass

    def __contains__(self, item):
        return self.has_key(item)

    def __iter__(self):
        return self.iterkeys()

    def __len__(self):
        return len(self.keys())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def has_key(self, key):
        return  key in self.keys()

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ([k, self[k]] for k in self.keys())

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self[k] for k in self.iterkeys())

    def values(self):
        return list(self.itervalues)

class MutableDictMixin(collections.MutableMapping):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def keys(self, key, value):
        pass

    def __contains__(self, item):
        return self.has_key(item)

    def __iter__(self):
        return self.iterkeys()

    def __len__(self):
        return len(self.keys())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def has_key(self, key):
        return key in self.keys()

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ([k, self[k]] for k in self.keys())

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self[k] for k in self.iterkeys())

    def values(self):
        return list(self.itervalues)

    def clear(self):
        for key in self:
            del self[key]

    def pop(self, key):
        value = self[key]
        del self[key]
        return value

    def popitem(self):
        if len(self) == 0:
            raise KeyError('popitem(): dictionary is empty')
        k = self.keys()[-1]
        v = self.pop(k)
        return k, v

    def setdefault(self, key, value=None):
        if not key in self.iterkeys():
            self[key] = value
            return value

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' %
                len(args))
        if len(args) == 1:
            dct = args[0]
            self.update(**dct)
        else:
            for k in kwargs:
                self[k] = kwargs[k]

default_encoding = 'utf8'
def safe_unicode(s):
    if isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return s.decode(default_encoding)
    else:
        return unicode(s)

def notnull(*args):
    for arg in args:
        if not arg is None:
            return arg
    return None

def homedir():
    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif os.name == 'posix':
        home = os.path.expanduser("~/")
    elif os.name == 'nt':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
        else:
            home = os.environ['HOMEPATH']
    return home

def obj2dict(obj):
    """Converts object to dictionary simply
    """
    d = {}
    for name in dir(obj):
        if not name.startswith('_'):
            try:
                d[name] = getattr(obj, name)
            except AttributeError:
                pass
    return d
