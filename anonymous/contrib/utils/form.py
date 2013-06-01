""":mod:`utils.form`
====================

Provides utils for :mod:`wtforms`
"""
def add_error(to, error):
    """Add error to field.  If field.errors is None.  So it set errors to empty 
    class:`tuple`.  You can use it like:
       
    >>> from meetytools.utils.form import add_error
    >>> form = Form()
    >>> print form.field.error
    None
    >>> add_error(form.field, 'Some error')
    >>> print form.field.error
    ['Some error']
    """
    if to.errors is None:
        to.errors = ()
    to.errors += (error,)
