""":mod:`utils.url`
===================

Provides many utils related to URL
"""
import urllib

"""Almost same as :func:`urllib.unquote` but replaces '+' with ' '.
"""
unquote = (lambda s:urllib.unquote(s.replace('+', ' ')))

def urldecode(s):
    """Decodes url encoded string into dictionary.  
    """
    if s.strip() == '':
        return {}
    d = {}
    for parse in s.split('&'):
        if not '=' in parse:
            break;
        k, v = parse.split('=', 1)
        k = unquote(k)
        v = unquote(v)
        d[k] = v
    return d

def sorted_urlencode(data):
    """Almost same as :func:`urllib.urlencode` but sorts key-value pair by
    key.  
    """
    key_value_pairs = []
    for key in sorted(data.keys()):
        value = data[key]
        if not isinstance(value, basestring):
            value = str(value)
        key = urllib.quote(key)
        value = urllib.quote(value)
        key_value_pair = '='.join([key, value])
        key_value_pairs.append(key_value_pair)
    return '&'.join(key_value_pairs)

def get_param_string(url):
    """Extract GET parameters' part from `url` if exist.  
    """
    s = url
    if '#' in url:
        s = url.split('#', 1)[0]
    if not '?' in s:
        return ''
    s = s.split('?', 1)[-1]
    return s

