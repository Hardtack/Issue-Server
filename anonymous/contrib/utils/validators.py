""":mod:`utils.validators`
==========================

Some validators.
"""
import re
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]'
    r'|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?'
    r'\.)+[A-Z]{2,6}\.?$)'
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)'
    r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE
)
username_re = re.compile(r'^[a-z0-9_\.-]{4,30}$', re.IGNORECASE)
disallowed_names = set(['new', 'delete', 'update'])

def validate_email(email):
    """Validates email.  
    """
    return email_re.match(email) is not None

def validate_username(username):
    """Validates username.  
    """
    if username in disallowed_names:
        return False
    return username_re.match(username) is not None
