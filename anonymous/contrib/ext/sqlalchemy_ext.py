from flask import abort
from sqlalchemy import create_engine as _create_engine, orm

def engine_url(db_info):
    """Makes URL from `db_info`.  
    """
    db_url_li = [db_info['DB']]
    if db_info.get('DRIVER', None):
        db_url_li.append('+%s'%db_info['DRIVER'])
    db_url_li.append('://')
    if db_info.get('USER', None):
        db_url_li.append(db_info['USER'])
        if db_info.get('PASSWORD', None):
            db_url_li.append(':%s'%db_info['PASSWORD'])
        host = db_info.get('HOST', None) or 'localhost'
        db_url_li.append('@%s'%host)
        if db_info.get('PORT', None):
            db_url_li.append(':%s'%db_info['PORT'])
    if db_info.get('NAME', None):
        db_url_li.append('/%s'%db_info['NAME'])
    return ''.join(db_url_li)

def create_engine(db_info, **kwargs):
    """Creates :mod:`sqlalchemy` engine.  
    """
    if isinstance(db_info, basestring):
        db_info = {
            'DB':'sqlite',
            'NAME':db_info,
        }
    db_url = engine_url(db_info)
    if not kwargs.has_key('convert_unicode'):
        kwargs['convert_unicode'] = True
    return _create_engine(db_url, **kwargs)

class Query(orm.Query):
    """Customized query.  
    """
    def get_or_404(self, id):
        """Invokes :meth:`get` and aborts 404 if result is None.  
        """
        rv = self.get(id)
        if rv is None:
            abort(404)
        return rv

    def first_or_404(self):
        """Invokes :meth:`first` and aborts 404 if result is None.  
        """
        rv = self.first()
        if rv is None:
            abort(404)
        return rv
