# -*- encoding: utf-8 -*-
import os
import uuid
from datetime import datetime
from utils import (is_iterable, is_list_like, match_one, truncate, timestamp,
    str_to_bool, has_keys, random_time, is_ascii, StringIO, is_integer)
from utils.file import extension, convert, mkdir_if_needed
from utils.http import parse_header
from utils.module import ismoduleinstance
from utils.validators import validate_email
from utils.url import urldecode, get_param_string, sorted_urlencode
from utils.proxy import Proxy
from utils.media_type import MediaType
from utils.config import DictionaryConfig
from utils.hasher import make_password

#Simples
def test_is_iterable():
    assert is_iterable([1, 2, 3])
    assert is_iterable((1, 2, 3))
    assert is_iterable('string')
    assert is_iterable(u'unicode')
    assert is_iterable({'key':'val'})
    def f():
        for i in xrange(3):
            yield i

    assert is_iterable(f())
    assert not is_iterable(123)

def test_is_list_like():
    assert is_list_like([1, 2, 3])
    assert is_list_like((1, 2, 3))
    assert not is_list_like('string')
    assert not is_list_like(u'unicode')
    assert not is_list_like({'key':'val'})

def test_match_one():
    assert match_one(1, 2, 3, 1)
    assert not match_one(1, 2, 3, 4)

def test_truncate():
    s = '12345'
    assert s == truncate(s, 10)
    s = '1234567890'
    assert s == truncate(s, 10)
    s = '12345678901234567890'
    assert '1234567...' == truncate(s, 10)
    assert '1234561234' == truncate(s, 10, '1234')

def test_extension():
    filename = 'some_image.png'
    assert 'png' == extension(filename)

    filename = 'some_tar_ball.tar.gz2'
    assert 'gz2' == extension(filename)
    
    filename = 'no_ext'
    assert extension(filename) is None

def test_convert():
    unsafe_filename='unsaf/e'*37
    result = ('unsaf_e' * 37)[-255:]
    assert result == convert(unsafe_filename)

def test_mkdir_if_needed(tmpdir):
    while True:
        d = os.path.join(str(tmpdir),
            'some_directory_not_exists%s' % uuid.uuid1().hex)
        if not os.path.exists(d):
            break
    mkdir_if_needed(d)
    assert os.path.exists(d)
    
    os.rmdir(d)
    assert not os.path.exists(d)

def test_hash():
    password = 'password'
    hashed = make_password(password)
    assert hashed != password

def test_parse_header():
    header = ' application/json;indent=4'
    key, params = parse_header(header)
    assert key == 'application/json'
    assert params == {'indent':'4'}

    header = 'application/json.vnd."what the hell;indent=4";q=0.8'
    key, params = parse_header(header)
    assert key == 'application/json.vnd."what the hell;indent=4"'
    assert params == {'q':'0.8'}

def test_email_validator():
    assert validate_email('admin@example.com')
    assert validate_email('admin+test@example.com')
    assert not validate_email('example.com')

def test_ismoduleinstance():
    dt = datetime.now()
    assert ismoduleinstance(dt, 'datetime.datetime')
    assert not ismoduleinstance(1, 'datetime.datetime')

def test_timestamp():
    d = datetime.fromtimestamp(0)
    assert timestamp(d) == 0.0

def test_str_to_bool():
    assert str_to_bool('true') == True
    assert str_to_bool('false') == False
    assert str_to_bool('TRUE') == True
    assert str_to_bool('FALSE') == False
    assert str_to_bool('FAIL') is None
    assert str_to_bool('Fail', True) == True
    assert str_to_bool(None, True) == True
    assert str_to_bool('Fail', 'Oh!') == 'Oh!'

def test_has_keys():
    d = {
        'a':1, 
        'b':2, 
        'c':3, 
    }
    assert has_keys(d, ['a', 'b', 'c'])
    assert not has_keys(d, ['a', 'b', 'c', 'd'])

def test_random_time():
    date1 = datetime(1970, 1, 1, 9, 0)
    date2 = datetime.now()
    generated = random_time(date1, date2)
    assert date1 <= generated
    assert date2 >= generated

def test_urldecode():
    s = 'key=value'
    assert {'key':'value'} == urldecode(s)

    s = 'key='
    assert {'key':''} == urldecode(s)

    s = 'key1=value1&key2=value2'
    assert {'key1':'value1', 'key2':'value2'} == urldecode(s)

    s = 'key1=value1&key2='
    assert {'key1':'value1', 'key2':''} == urldecode(s)

    s = 'key1=a+b&key2=a%2Bb'
    assert {'key1':'a b', 'key2':'a+b'} == urldecode(s)

    s = 'key1=%20&key2=%0A'
    assert {'key1':' ', 'key2':'\n'} == urldecode(s)

def test_get_param_string():
    url = 'http://example.com/path'
    assert '' == get_param_string(url)

    url = 'http://example.com/path?key=value'
    assert 'key=value' == get_param_string(url)

    url = 'http://example.com/path?key=value#blah'
    assert 'key=value' == get_param_string(url)

    url = 'http://example.com/path?key=value#blah?trap=value'
    assert 'key=value' == get_param_string(url)

def test_sorted_urlencode():
    d = {
        'b':'v', 
        'a':'v'
    }
    assert 'a=v&b=v' == sorted_urlencode(d)

def test_is_integer():
    assert is_integer('931229')
    assert not is_integer('asd123')
    assert is_integer('0123')

def test_is_ascii():
    assert is_ascii('abcd123')
    assert not is_ascii('가나다')
    assert not is_ascii(u'가나다')

def test_proxy():
    class Duck(object):
        pass

    obj = Duck()
    p = Proxy(lambda:obj)

    obj.item = []
    assert obj.item == p.item

    p = Proxy(lambda:obj, exclude_names=['ex'])
    obj.ex = 1
    p.ex = 2

    assert 1 == obj.ex
    assert 2 == p.ex
    assert obj.item == p.item

def test_media_type():
    application_json_type = MediaType('application/json')
    application_type = MediaType('application/*')
    assert application_json_type in application_type

    json_type = MediaType('*/json')
    assert application_json_type in json_type

    image_type = MediaType('image/*')
    assert not application_json_type in image_type

    assert application_json_type == MediaType('application/json')

def test_config():
    config_str = '''
[Section1]
foo=boy
bar : I'm a %(foo)s

[Section2]
baz=%(new)s value
    '''

    config = DictionaryConfig()
    with StringIO(config_str) as sio:
        config.readfp(sio)

    assert 'boy' == config['Section1']['foo']
    assert "I'm a boy" == config['Section1']['bar']
    
    config['Section2']['new'] = 'some'
    assert 'some' == config['Section2']['new']
    assert 'some value' == config['Section2']['baz']

    del config['Section2']['baz']
    assert ['new'] == config['Section2'].keys()
