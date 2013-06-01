""":mod:`utils.module`
======================

Provides many utils related to modeule
"""
import importlib
from . import is_list_like

def _ismoduleinstance(obj,cls):
    if isinstance(cls,type):
        return isinstance(obj,cls)
    components = cls.split('.')
    if len(components) > 1:
        try:
            m_name='.'.join(components[:-1])
            module = importlib.import_module(m_name)
            c = getattr(module, components[-1])
            return isinstance(obj,c)
        except Exception:
            return False

    else:
        return isinstance(obj,eval(components[0]))

def ismoduleinstance(obj, cls):
    """same as isinstance but `cls` can be dotted name of module.

    >>> ismoduleinstance(obj, 'wtforms.Form'
    """
    if is_list_like(cls):
        for c in cls:
            if _ismoduleinstance(obj,c):
                return True
    else:
        return _ismoduleinstance(obj,cls)
