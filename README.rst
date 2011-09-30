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

Import fabric_threadsafe.patch before any other Fabric imports.

::
    
    import fabric_threadsafe.patch
    
    from fabric.api import env, run, cd

Testing
=======

Use nose framework for testing.
