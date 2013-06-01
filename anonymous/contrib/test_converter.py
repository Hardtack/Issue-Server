import pytest
import typeconverter as t

def test_converter():
    converter = t.Converter(str)

    @converter.handle(unicode)
    def convert_unicode(u):
        return u.encode('utf-8')
    
    @converter.handle(list)
    def convert_list(li):
        return ', '.join(map(converter.convert, li))

    @converter.handle(tuple)
    def contert_tuple(tp):
        return '(' + ', '.join(map(converter.convert, tp)) + ')'

    @converter.handle(int, float, long)
    def convert_number(n):
        return 'n' + str(n)
    
    @converter.default
    def convert(obj):
        return str(obj)

    assert isinstance(converter.convert(u'string'), str)
    assert 'a, b, c' == converter.convert(['a', 'b', 'c'])
    assert '(a, b)' == converter.convert(('a', 'b'))
    assert 'n123' == converter.convert(123)
    assert 'n1' == converter.convert(long(1))
    assert '{}' == converter.convert({})
    assert 'n1, n2, n3' == converter.convert([1, 2, 3])

def test_multiple():
    converter = t.Converter(list)
    @converter.handle(tuple, set)
    def convert_iterable(i):
        return list(i)

    s = {1, 2, 3}
    converted = converter.convert(s)
    assert len(s) == len(converted)
    assert isinstance(converted, list)
    for i in s:
        assert i in converted

    with pytest.raises(TypeError):
        converter.convert('str')

def test_chain():
    converter = t.Converter((list, dict, int, basestring))

    class A(object):
        def __init__(self, v):
            self.v = v

    @converter.handle(A)
    def convert_A(a):
        return a.v

    class B(object):
        def __init__(self, v):
            self.v = v

    @converter.handle(B)
    def convert_B(b):
        return A(b.v)

    assert 1 == converter.convert(A(1))
    assert 2 == converter.convert(B(2))
    
    assert '1' == converter.convert(A('1'))
    assert '2' == converter.convert(B('2'))

def test_assert():
    class DeepConverter(t.Converter):
        def assert_type(self, obj):
            super(DeepConverter, self).assert_type(obj)
            if isinstance(obj, list):
                for i in obj:
                    self.assert_type(i)
            elif isinstance(obj, dict):
                for k, v in obj.iter_items():
                    self.assert_type(k)
                    self.assert_type(v)

    converter = DeepConverter((list, dict, basestring))

    @converter.handle(set, tuple)
    def convert_iterable(i):
        return list(i)

    @converter.handle(list)
    def convert_list(li):
        return map(converter.convert, li)

    @converter.handle(dict)
    def convert_dict(d):
        converted = {}
        for k, v in d.iter_items():
            converted[converter.convert(k)] = converter.convert(v)
        return converted
    
    @converter.default
    def convert(obj):
        return str(obj)

    assert [['1', '2', '3'], 'b', 'c'] == converter.convert(
        ({1, 2, 3}, 'b', 'c')
    )
