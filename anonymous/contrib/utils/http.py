""":mod:`utils.http`
====================

Provides many utils for HTTP
"""
def parse_header(s):
    """Parses parameter header
    """
    params = _parse_header_params(';'+s)
    key = params.pop(0).lower()
    pdict = {}
    for param in params:
        i = param.find('=')
        if i >= 0:
            name = param[:i].strip().lower()
            value = param[i+1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace(r'\\','\\').replace(r'\"','"')
            pdict[name]=value
    return key,pdict

def _parse_header_params(s):
    li = []
    while s[:1] == ';':
        s=s[1:]
        end = s.find(';')
        while end > 0 and s.count('"',0,end) % 2:
            # For quote
            end = s.find(';',end+1)
        end = end if end >= 0 else len(s)
        li.append(s[:end].strip())
        s = s[end:]
    return li
