import pytest
from tri.struct import FrozenStruct

from tri.named_struct import NamedStruct, NamedStructField, named_struct, NamedFrozenStruct, named_frozen_struct


def test_init():
    assert list(named_struct('foo')().keys()) == ['foo']
    assert sorted(named_struct(['foo', 'bar'])().keys()) == ['bar', 'foo']
    assert sorted(named_struct('foo, bar')().keys()) == ['bar', 'foo']
    assert named_struct('foo, bar')().__class__.__name__ == 'NamedStruct'

    assert sorted(named_struct('foo, bar', 'SomeName')().keys()) == ['bar', 'foo']
    assert named_struct('foo, bar', 'SomeName')().__class__.__name__ == 'SomeName'


def test_access():
    MyNamedStruct = named_struct('foo', "MyNamedStruct")
    s = MyNamedStruct()
    assert s.foo is None

    s.foo = 17
    assert s.foo == 17
    assert s['foo'] == 17


def test_read_constraints():
    MyNamedStruct = named_struct('foo', "MyNamedStruct")
    s = MyNamedStruct()
    with pytest.raises(AttributeError):
        # noinspection PyStatementEffect
        s.bar


def test_write_constraints():
    MyNamedStruct = named_struct('foo', "MyNamedStruct")
    s = MyNamedStruct()
    with pytest.raises(AttributeError):
        # noinspection PyStatementEffect
        s.bar = 17

    with pytest.raises(KeyError) as e:
        s['bar']
    assert "KeyError: 'bar'" in str(e)


def test_constructor():
    MyNamedStruct = named_struct('foo, bar')
    s = MyNamedStruct(bar=42, foo=17)
    assert s == dict(foo=17, bar=42)


def test_constructor_failure():

    class MyNamedStruct(named_struct('foo, bar')):
        pass

    with pytest.raises(TypeError) as e:
        MyNamedStruct(1, 2, 3)  # Too many args
    assert "MyNamedStruct() takes at most 2 arguments (3 given)" in str(e)

    with pytest.raises(TypeError) as e:
        MyNamedStruct(1, foo=2)  # Conflicting value for foo
    assert "MyNamedStruct() got multiple values for keyword argument 'foo'" in str(e)

    with pytest.raises(TypeError) as e:
        MyNamedStruct(foo=17, bar=42, boink=25)  # Constraint violation
    assert "MyNamedStruct() got an unexpected keyword argument 'boink'" in str(e)


def test_position_arg_constructor():
    MyNamedStruct = named_struct('foo, bar')
    s = MyNamedStruct(17, 42)
    assert s == dict(foo=17, bar=42)


def test_repr():
    assert repr(named_struct("foo, bar")(foo=17, bar=42)) == "NamedStruct(bar=42, foo=17)"
    assert repr(named_struct("foo, bar", "SomeNamedStruct")(foo=17, bar=42)) == "SomeNamedStruct(bar=42, foo=17)"


def test_subclass():

    class MyNamedStruct(named_struct(['foo', 'bar'])):
        pass

    s = MyNamedStruct(foo=17)
    assert repr(s) == 'MyNamedStruct(bar=None, foo=17)'


def test_declarative_style():

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField()
        bar = NamedStructField()

    assert MyNamedStruct(17, 42) == dict(foo=17, bar=42)


def test_declarative_style_inheritance():

    class MyNamedStructBase(NamedStruct):
        foo = NamedStructField()

    class MyNamedStruct(MyNamedStructBase):
        bar = NamedStructField()

    assert MyNamedStruct(17, 42) == dict(foo=17, bar=42)


def test_default_value():

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField()
        bar = NamedStructField()
        baz = NamedStructField(default='default')

    assert MyNamedStruct(17) == dict(foo=17, bar=None, baz='default')


def test_default_factory():

    class MyNamedStruct(NamedStruct):
        foo = NamedStructField(default_factory=list)

    assert MyNamedStruct().foo == []


def test_freeze():
    MyNamedStruct = named_struct('foo, bar')
    s = MyNamedStruct(foo=17)
    s.bar = 42
    assert FrozenStruct(s) == FrozenStruct(foo=17, bar=42)


def test_inheritance_with_marker_class():
    class MyType(NamedStruct):
        pass

    class MySubType(MyType):
        foo = NamedStructField()

    x = MySubType(foo=1)

    assert x.foo == 1


def test_named_frozen_struct():

    class F(NamedFrozenStruct):
        foo = NamedStructField()
        bar = NamedStructField(default='bar')

    f = F('foo')

    assert {'foo': 'foo', 'bar': 'bar'} == f

    assert f.foo == 'foo'

    with pytest.raises(TypeError):
        f.foo = 'fook'  # Read-only

    g = named_frozen_struct('foo, bar')(1, 2)
    assert g == dict(foo=1, bar=2)
    with pytest.raises(TypeError):
        g.foo = 17


def test_named_struct_subclass_with_constructor():
    class F(NamedStruct):
        foo = NamedStructField()

        def __init__(self, **kwargs):
            super(F, self).__init__(**kwargs)

    assert 17 == F(foo=17).foo


def test_named_struct_subclass_with_constructor_override_before_super():
    class F(NamedStruct):
        foo = NamedStructField()

        def __init__(self, **kwargs):
            self.foo = 17
            super(F, self).__init__(**kwargs)

    assert 17 == F().foo


def test_named_struct_subclass_with_constructor_override_before_super_with_explicit():
    class F(NamedStruct):
        foo = NamedStructField()

        def __init__(self, **kwargs):
            self.foo = 17
            super(F, self).__init__(**kwargs)

    assert 42 == F(foo=42).foo


def test_named_struct_subclass_with_constructor_override_after_super():
    class F(NamedStruct):
        foo = NamedStructField()

        def __init__(self, **kwargs):
            super(F, self).__init__(**kwargs)
            self.foo = 17

    assert 17 == F(foo=42).foo
