
import typing

from collections.abc import Iterable, Mapping

from . import exceptions

# candidates to redefine:
# __getitem__
# __contains__
# __call__
# __getattr__

# Do not redefine __bool__ (?) — it is used by python conditions

# do not redefine comparison operations since we can not chain them
# a < b < c is equal to (a < b) and (b < c)
# so "and" block predicates spread over comparison groups


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


BINARY_R_OPERATIONS = {f'__r{name[2:]}': op for name, op in BINARY_OPERATIONS.items()}

BINARY_I_OPERATIONS = {f'__i{name[2:]}': op for name, op in BINARY_OPERATIONS.items()}

UNARY_OPERATIONS = {'__neg__': 'neg',
                    '__pos__': 'pos',
                    '__invert__': 'invert'}


def normalize_predicate(value: typing.Any) -> 'Predicate':
    if isinstance(value, Predicate):
        return value

    return Predicate('identity', args=(value,))


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

    def __new__(mcls, class_name, bases, attrs):  # noqa: disable=C901

        if class_name.startswith('None'):
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

        return super(Meta, mcls).__new__(mcls, class_name, bases, attrs)


class Predicate(metaclass=Meta):
    __slots__ = ('operation', 'args', 'kwargs')

    def __init__(self,
                 operation: typing.Optional[str] = None,
                 args: Iterable = (),
                 kwargs: Mapping = None):

        if operation is None:
            operation = self.__class__.__name__.lower()

        if kwargs is None:
            kwargs = {}

        self.operation = operation
        self.args = tuple(args)
        self.kwargs = kwargs

    # TODO: improve __str__ and __repr
    def __str__(self):
        return f'{self.operation}({self.args}, {self.kwargs})'

    def __repr__(self):
        return f'{self.operation}({self.args}, {self.kwargs})'


class Context:
    __slots__ = ('prefix',)

    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, predicate: Predicate, *argv, **kwargs):

        # use Duck Typing for speed and flexibility

        if hasattr(predicate, 'operation'):
            callback = f'_{predicate.operation}'

            if hasattr(self, callback):
                return getattr(self, callback)(predicate, *argv, **kwargs)

        if hasattr(predicate, self.prefix):
            return getattr(predicate, self.prefix)(self, *argv, **kwargs)

        raise exceptions.UnknownOperation(predicate.operation)


class Boolean(Context):
    __slots__ = ()

    def __init__(self, prefix: str = 'boolean'):
        super().__init__(prefix=prefix)

    def _identity(self, predicate, *argv, **kwargs):
        return predicate.args[0]

    def _and(self, predicate, *argv, **kwargs):
        return all(bool(self(arg, *argv, **kwargs)) for arg in predicate.args)

    def _xor(self, predicate, *argv, **kwargs):
        return bool(sum(1
                        for arg in predicate.args
                        if bool(self(arg, *argv, **kwargs))) % 2)

    def _or(self, predicate, *argv, **kwargs):
        return any(bool(self(arg, *argv, **kwargs)) for arg in predicate.args)

    def _invert(self, predicate, *argv, **kwargs):
        return not self(predicate.args[0], *argv, **kwargs)
