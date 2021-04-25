

from .predicates import Context


# TODO: add types annotations

class BooleanMixin:

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


class ComparisonMixin:

    def _lt(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) <
                self(predicate.args[1], *argv, **kwargs))

    def _le(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) <=
                self(predicate.args[1], *argv, **kwargs))

    def _eq(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) ==
                self(predicate.args[1], *argv, **kwargs))

    def _ne(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) !=
                self(predicate.args[1], *argv, **kwargs))

    def _gt(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) >
                self(predicate.args[1], *argv, **kwargs))

    def _ge(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) >=
                self(predicate.args[1], *argv, **kwargs))


class MathMixin:

    def _add(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) +
                self(predicate.args[1], *argv, **kwargs))

    def _sub(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) -
                self(predicate.args[1], *argv, **kwargs))

    def _mul(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) *
                self(predicate.args[1], *argv, **kwargs))

    def _matmul(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) @
                self(predicate.args[1], *argv, **kwargs))

    def _truediv(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) /
                self(predicate.args[1], *argv, **kwargs))

    def _floordiv(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) //
                self(predicate.args[1], *argv, **kwargs))

    def _mod(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) %
                self(predicate.args[1], *argv, **kwargs))

    def _divmod(self, predicate, *argv, **kwargs):
        return divmod(self(predicate.args[0], *argv, **kwargs),
                      self(predicate.args[1], *argv, **kwargs))

    def _pow(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) **
                self(predicate.args[1], *argv, **kwargs))

    def _lshift(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) <<
                self(predicate.args[1], *argv, **kwargs))

    def _rshift(self, predicate, *argv, **kwargs):
        return (self(predicate.args[0], *argv, **kwargs) >>
                self(predicate.args[1], *argv, **kwargs))

    def _neg(self, predicate, *argv, **kwargs):
        return -self(predicate.args[0], *argv, **kwargs)

    def _pos(self, predicate, *argv, **kwargs):
        return +self(predicate.args[0], *argv, **kwargs)


class Boolean(BooleanMixin, MathMixin, Context):
    __slots__ = ()

    def __init__(self, prefix: str = 'boolean'):
        super().__init__(prefix=prefix)
