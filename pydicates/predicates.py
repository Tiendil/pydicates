
import copy
import typing

from collections.abc import Iterable, Mapping

from . import exceptions

# candidates to redefine:
# __getitem__
# __contains__
# __call__
# __getattr__


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

# Do not redefine conversions __bool__, __complex__, __float__, __int__
# since Python implicity check returned types
# and produce errors like: TypeError: __complex__ returned non-complex (type Predicate)


# we can not chain redefined comparisons
# "a < b < c" is equal to "(a < b) and (b < c)"
# which translates to "b < c", becouse (a < b) is Predicate and always True (?)
# so, predicates can not spread over comparison chains
COMPARISON_OPERATIONS = {'__lt__': 'lt',
                         '__le__': 'le',
                         '__eq__': 'eq',
                         '__ne__': 'ne',
                         '__gt__': 'gt',
                         '__ge__': 'ge'}


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

        # ensure that current predicate will safe its class and attributes
        left = copy.copy(self)

        other = normalize_predicate(other)

        # that redifinition should be correct,
        # since operation — is standard operation and should be supported by Context class
        self.operation = name
        self.args = (left, other)
        self.kwargs = {}

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

        for name, op in COMPARISON_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_op(op)

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

    def __init__(self, prefix: typing.Optional[str] = None):
        if prefix is None:
            prefix = self.__class__.__name__

        self.prefix = prefix

    def __call__(self, predicate: Predicate, *argv, **kwargs):

        # use Duck Typing for speed and flexibility

        # check if context define logic for predicate
        if hasattr(predicate, 'operation'):
            callback = f'_{predicate.operation}'

            if hasattr(self, callback):
                return getattr(self, callback)(predicate, *argv, **kwargs)

        # check if predicate define logic for context
        if hasattr(predicate, self.prefix):
            return getattr(predicate, self.prefix)(self, *argv, **kwargs)

        # check if predicate define common logic
        if callable(predicate):
            return predicate(self, *argv, **kwargs)

        raise exceptions.UnknownOperation(self, predicate)

    def _identity(self, predicate, *argv, **kwargs):
        return predicate.args[0]
