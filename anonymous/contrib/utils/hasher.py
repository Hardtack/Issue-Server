""":mod:`utils.hasher`
======================

Provides many hashing utils for :mod:`meety`
"""
import hashlib
import hmac
import binascii

def make_password(raw):
    """Converts raw password to hashed password. 
    Internally, it is shortener of sha1 hashing. 
    You can use it like:

    >>> from meetytools.utils.hasher import make_password
    >>> raw = 'password'
    >>> hashed = make_password(raw)
    >>> print hashed
    some_hashed_string
    """
    sha1 = hashlib.sha1()
    sha1.update(raw)
    return sha1.hexdigest()

def b64_hmac_sha1(raw, key):
    """Generate HMAC-SHA1 encoded value, then encode it to base64.  
    You can use it like:

    >>> from meetytools.utils.hasher import b64_hmac_sha1
    >>> raw = 'some_value'
    >>> key = 'some_key'
    >>> hashed = b64_hmac_sha1(raw, key)
    >>> print hashed
    tVejaILWI9KQKhwnPumNdXpHw8A=
    """
    # Hash
    hashed = hmac.new(key, raw, hashlib.sha1)

    # Convert to base64 string
    return binascii.b2a_base64(hashed.digest()).strip()
