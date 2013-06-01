""":mod:`utils.file`
====================

Provides many utils for files.  
"""
from werkzeug import secure_filename
import os

def extension(filename):
    """Extract extesion string from filename.  And you can use it like:

    >>> from meetytools.utils.file import extesion
    >>> ext = extesion(filename)
    """
    if filename:
        return filename.rsplit('.',1)[1].lower() if '.' in filename else None
    else:
        return None

def convert(filename):
    """Convert filename to safe for :mod:`meety` application.  
    You can use it like: 

    >>> from meetytools.utils.file import convert
    >>> filename = convert(filename)
    """
    return secure_filename(filename)[-255:]

def mkdir_if_needed(directory):
    """Make directory if it does not exist.  
    
    For example::

       from meetytools.utils.file import mkdir_if_needed

       mkdir_if_needed('/some/dir/exist') # Do nothing

       mkdir_if_needed('/some/dir/dont/exist') # Make directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
