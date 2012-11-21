Fabric thread-safe
==================

This module will monkeypatch fabric to use DictProxy for fabric.api.env to use
thread local storage.

Installation
------------

::
    
    pip install fabric_threadsafe

Usage
=====

Import `patch` function from `fabric_threadsafe` and call it before any other Fabric imports.

::

    from fabric_threadsafe import patch
    patch()

    from fabric.api import env, run, cd

Testing
=======

Use nose framework for testing.

::

    pip install nose
    nosetests