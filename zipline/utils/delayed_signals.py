from functools import wraps
from signal    import signal

class delayed_signals(object):
    """
    Utility to temporary intercept one or more signals while a function or code
    block is executed, restore their signal handlers at the end of execution,
    and invoke them if the signals were in fact received during execution.

    Can be used either as a decorator or a context manager.

    Pass in an iterable of signals to intercept.
    """

    def handler(self, signum, frame=None):
        self.got.append([self.trapped.index(signum), frame])

    def __init__(self, signals):
        self.trapped = signals
        self.orig_handlers = []
        self.got = []

    def __enter__(self):
        for sig in self.trapped:
            self.orig_handlers.append(signal(sig, self.handler))

    def __exit__(self, time, value, traceback):
        for i in xrange(len(self.trapped)):
            signal(self.trapped[i], self.orig_handlers[i])
        for intercepted in self.got:
            i = intercepted[0]
            signum = self.trapped[i]
            frame = intercepted[1]
            self.orig_handlers[i](signum, frame)

    def __call__(self, fn):
        @wraps(fn)
        def call_fn(*args, **kwargs):
            with self:
                outval = fn(*args, **kwargs)
            return outval
        return call_fn
