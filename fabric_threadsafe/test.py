import os
import sys
import threading

import nose

def setup_patch():
    from fabric_threadsafe import patch
    assert patch.patch_fabric()

def cleanup():
    from fabric_threadsafe import patch
    reload(patch)

    for m, v in sys.modules.items():
        if m.startswith('fabric.') or m in ('fabric',):
            del sys.modules[m]

@nose.with_setup(setup_patch, cleanup)
def test_dict_proxy():
    from fabric.api import env

    env.host_string = 'myhost'

    # test dict proxy
    assert env['host_string'] == 'myhost'

    # test attribute dict proxy
    assert env.host_string == 'myhost'

@nose.with_setup(setup_patch, cleanup)
def test_state_transfer():
    from fabric.thread_handling import ThreadHandler
    from fabric.api import env

    def state_transfer(x, y):
        assert x == 1
        assert y == 2
        assert env.host_string == 'myhost'

    th = ThreadHandler('footest', state_transfer, [1], {'y': 2})
    th.thread.join()

@nose.with_setup(setup_patch, cleanup)
def test_fresh_state():
    from fabric.api import env

    def env_default(x, y):
        assert x == 1
        assert y == 2
        assert env.host_string == None

    t = threading.Thread(None, env_default, args=[1], kwargs={'y': 2})
    t.start()
    t.join()

@nose.with_setup(setup_patch, cleanup)
def test_output():
    from fabric.api import hide

    with hide('running', 'stdout'):
        pass

@nose.with_setup(setup_patch, cleanup)
def test_ssh_run():
    from fabric.api import env, run

    if os.environ.get('TEST_SSH_HOST', None):
        env.host_string = os.environ['TEST_SSH_HOST']

        run('sleep 2; true')

        original_env = dict(**env)

        def test_ssh_run():
            env.update(original_env)
            run('sleep 2; true')

        threads = []

        for i in range(5):
            t = threading.Thread(None, test_ssh_run)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
