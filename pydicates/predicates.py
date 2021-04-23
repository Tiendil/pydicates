
from collections.abc import Iterable, Mapping

# candidates to redefine:
# __getitem__
# __contains__
# __call__
# __getattr__

# Do not redefine __bool__ (?) — it is used by python conditions


BINARY_OPERATIONS = {'__add__': 'add',
                     '__sub__': 'sub',
                     '__mul__': 'mul',
                     '__matmul__': 'matmul',
                     '__truediv__': 'truediv',
                     '__floordiv__': 'floordiv',
                     '__mod__': 'mod',
                     '__divmod__': 'divmod',
                     '__pow__': 'pow',
                     '__lshift__': 'lshift',
                     '__rshift__': 'rshift',
                     '__and__': 'and',
                     '__xor__': 'xor',
                     '__or__': 'or'}


BINARY_R_OPERATIONS = {f'__r{name[2:]}': op for name, op in BINARY_R_OPERATIONS.items()}

BINARY_I_OPERATIONS = {f'__i{name[2:]}': op for name, op in BINARY_R_OPERATIONS.items()}

UNARY_OPERATIONS = {'__neg__': 'neg',
                    '__pos__': 'pos',
                    '__invert__': 'invert'}

COMPARISON_OPERATIONS = {'__lt__': 'lt',
                         '__le__': 'le',
                         '__eq__': 'eq',
                         '__ne__': 'ne',
                         '__gt__': 'gt',
                         '__ge__': 'ge'}


def normalize_predicate(value: typing.Any) -> 'Predicate':
    if isinstance(value, Predicate):
        return value

    return Predicate('identity', arguments=(value,))


def unary_op(name):

    def method(self):
        return Predicate(name, args=(self,))

    return method


def binary_op(name):

    def method(self, other):
        return Predicate(name, args=(self, normalize_predicate(other)))

    return method


def binary_r_op(name):

    def method(self, other):
        return Predicate(name, args=(normalize_predicate(other), self))

    return method


def binary_i_op(name):

    def method(self, other):
        left = copy.copy(self)
        other = normalize_predicate(other)

        self.operation = name
        self.args = tuple(left, other)

        return self

    return method


class Meta(type):

    def __new__(mcls, name, bases, attrs):  # noqa: disable=C901

        if name.startswith('None'):
            return None

        for name, op in BINARY_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_op(op)

        for name, op in BINARY_R_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_r_op(op)

        for name, op in BINARY_I_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_i_op(op)

        for name, op in UNARY_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = unary_op(op)

        for name, op in COMPARISON_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_op(op)

        return super(Meta, mcls).__new__(mcls, name, bases, attrs)


class Predicate(metaclass=Meta):
    __slots__ = ('operation', 'args', 'kwargs')

    def __init__(self, operation: str, args: Iterable = (), kwargs: Mapping = None):

        if kwargs is None:
            kwargs = {}

        self.operation = operation
        self.args = tuple(arguments)
        self.kwargs = kwargs

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class Context:
    __slots__ = ('prefix',)

    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, predicate: Predicate, *argv, **kwargs):
        callback = f'{self.orefix}{predicate.operation}'

        if hasattr(self, callback):
            return getattr(self, callback)(*argv, **kwargs)

        if hasattr(predicate, callback):
            return getattr(predicate, callback)(self, *argv, **kwargs)

        # TODO: invoke __call__ instead? To allow callbacks as predicates

        # TODO: custom exception
        raise Exception(f'Unknown operation {predicate.operation}')


class Boolean(Context):
    __slots__ = ()

    def __init__(self, prefix: str = 'bool_'):
        super().__init__(prefix=prefix)


    # TODO: I think prefixes is not required
    def bool_and(self):
        pass

    def bool_xor(self):
        pass

    def bool_or(self):
        pass

    def bool_invert(self):
        pass
