from tri.declarative.declarative import declarative_member, declarative
from tri.struct import Struct


__version__ = '0.1.0'


@declarative_member
class NamedStructField(object):

    def __init__(self, default=None):
        self.default = default
        super(NamedStructField, self).__init__()


def _get_members(named_struct):
    # Fancy getter to not stumble over our own __getitem__ implementation
    return object.__getattribute__(named_struct, '__class__').Meta.members


@declarative(NamedStructField, add_init_kwargs=False)
class NamedStruct(Struct):

    def __init__(self, *args, **kwargs):
        members = _get_members(self)

        if len(args) > len(members):
            raise ValueError("Too many arguments")

        values_by_name = dict(zip(members.keys(), args))
        for kwargs_name, value in kwargs.items():
            if kwargs_name in values_by_name:
                raise ValueError('Field "%s" already given as positional argument' % (kwargs_name, ))
            values_by_name[kwargs_name] = value

        for kwargs_name in values_by_name:
            if kwargs_name not in members:
                raise KeyError(kwargs_name)

        super(NamedStruct, self).__init__(**{name: values_by_name.get(name, field.default) for name, field in members.items()})

    def __getitem__(self, key):
        if key not in _get_members(self):
            raise KeyError(key)
        return super(NamedStruct, self).__getitem__(key)

    def __setitem__(self, key, value):
        if key not in _get_members(self):
            raise KeyError(key)
        super(NamedStruct, self).__setitem__(key, value)

    def __setattr__(self, k, v):
        try:
            self[k] = v
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, k))


def named_struct(field_names, typename="NamedStruct"):

    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split()
    field_names = map(str, field_names)
    typename = str(typename)

    return type(typename, (NamedStruct, ), {field: NamedStructField() for field in field_names})

