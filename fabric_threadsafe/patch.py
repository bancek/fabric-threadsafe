import os
import threading
from functools import wraps
from UserDict import UserDict

state = threading.local()

class DictProxy(UserDict, object):
    def __init__(self, getter, dict=None, **kwargs):
        object.__setattr__(self, 'getter', getter)
        
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)
        
    @property
    def data(self):
        return self.getter()

class _AttributeDictProxy(DictProxy):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value

def synchronize(lock, func):
    @wraps(func)
    def decorated(*args, **kw):
        lock.acquire()
        try:
            return func(*args, **kw)
        finally:
            lock.release()
    return decorated

def fix_terminal():
    '''Multi-threaded fabric breaks terminal's echo'''
    os.system("stty -raw echo")

# monkeypatch
def patch_fabric():
    if getattr(patch_fabric, 'patched', False):
        return False

    patch_fabric.patched = True

    import sys
    import atexit
    from fabric import state as fstate
    from fabric.thread_handling import ThreadHandler

    default_env = fstate.env

    def get_state_env(state=state, default_env=default_env):
        if not hasattr(state, 'env'):
            state.env = default_env.copy()
        return state.env

    fstate.env = _AttributeDictProxy(get_state_env)

    default_channel_lock = threading.Lock()

    fstate.default_channel = synchronize(default_channel_lock,
                                         fstate.default_channel)

    def transfer_state(func):
        def inner(old_state):
            @wraps(func)
            def decorated(*args, **kwargs):
                state.__dict__.update(old_state)
                return func(*args, **kwargs)
            
            return decorated
        
        return inner(state.__dict__)

    def th_init_patcher(func):
        @wraps(func)
        def decorated(self, name, callable, *args, **kwargs):
            callable = transfer_state(callable)
            return func(self, name, callable, *args, **kwargs)
        return decorated

    ThreadHandler.__init__ = th_init_patcher(ThreadHandler.__init__)
    
    for m, v in sys.modules.items():
        if (v and (m.startswith('fabric.') or m == 'fabric')
                and m not in ('fabric.state', 'fabric.utils')):
            reload(v)

    atexit.register(fix_terminal)

    return True
# /monkeypatch
