""":mod:`utils.thread`
======================

Provides many utils related to threading.
"""
def synchronized(lock):
    """Synchronization decorator.
    """
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap
