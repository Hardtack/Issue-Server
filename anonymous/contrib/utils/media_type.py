from http import parse_header

class MediaType(object):
    """Abstracted media type class.  
    """
    def __init__(self, raw):
        raw = raw or ''
        self.raw = raw
        self.media_type, self.params = parse_header(raw)
        self.main_type, sep, self.sub_type = self.media_type.partition('/')

    def __contains__(self, other):
        for k, v in self.params.iteritems():
            if k != 'q' and other.params.get(k, None) != v:
                return False
        if self.main_type == '*' and self.sub_type == '*':
            return True
        if self.sub_type == '*' and self.main_type == other.main_type:
            return True
        if self.main_type == '*' and self.sub_type == other.sub_type:
            return True
        return self == other

    def __eq__(self, other):
        return (self.main_type == other.main_type and self.sub_type ==
            other.sub_type)

    def __repr__(self):
        return '<media type:' + str(self) + '>'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'; '.join(
            [u'%s/%s' % (self.main_type, self.sub_type)] +
            [u'%s=%s' % (k, v) for k, v in self.params.iteritems()]
        )
