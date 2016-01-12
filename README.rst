.. image:: https://travis-ci.org/TriOptima/tri.named_struct.svg?branch=master
    :target: https://travis-ci.org/TriOptima/tri.named_struct
.. image:: http://codecov.io/github/TriOptima/tri.named_struct/coverage.svg?branch=master
    :target: http://codecov.io/github/TriOptima/tri.named_struct?branch=master

tri.named_struct
================

tri.named_struct supplies classes that can be used like dictionaries, but with a predefined set of possible key values.

Example
-------

.. code:: python

    from tri.named_struct import NamedStruct

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField()
        bar = NamedStructField()

    m = MyNamedStruct(17, 42)
    assert m['foo'] == 17
    assert m.foo == 17
    assert m == dict(foo=17, bar=42)

    m.not_foo  # Will raise an AttributeError


Default values can be provided:

.. code:: python

    from tri.named_struct import NamedStruct

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField()
        bar = NamedStructField()
        baz = NamedStructField(default='default')

    assert MyNamedStruct(17) == dict(foo=17, bar=None, baz='default')


Default values can alternatively be provided by a factory method:

.. code:: python

    from tri.named_struct import NamedStruct

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField(default_factory=list)

    assert MyNamedStruct().foo == []


There is also a functional way to defined a :code:`NamedStruct` subclass:

.. code:: python

    from tri.named_struct import named_struct

    MyNamedStruct = named_struct('foo, bar')
    m = MyNamedStruct(17, 42)
    assert m.foo == 17
    assert m.bar == 42


Running tests
-------------

You need tox installed then just :code:`make test`.


License
-------

BSD


Documentation
-------------

http://trinamedstruct.readthedocs.org.
