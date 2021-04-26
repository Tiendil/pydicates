
import pytest

from hypothesis import given

from .helpers import P, bool_vector

from pydicates import BooleanMixin, Context


class ContextForTests(BooleanMixin, Context):
    pass


@pytest.fixture(scope="module")
def context():
    return ContextForTests()


@given(inputs=bool_vector(1))
def test_not(context, inputs):
    assert context(P(0), inputs) == inputs[0]
    assert context(~P(0), inputs) == (not inputs[0])


@given(inputs=bool_vector(2))
def test_and(context, inputs):
    def test(a, b):
        return a and b

    assert context(P(0) & P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_and(context, inputs):
    def test(a, b, c):
        return a and b and c

    assert context(P(0) & P(1) & P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_or(context, inputs):
    def test(a, b):
        return a or b

    assert context(P(0) | P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_or(context, inputs):
    def test(a, b, c):
        return a or b or c

    assert context(P(0) | P(1) | P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_xor(context, inputs):
    def test(a, b):
        return a ^ b

    assert context(P(0) ^ P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_xor(context, inputs):
    def test(a, b, c):
        return a ^ b ^ c

    assert context(P(0) ^ P(1) ^ P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_complex(context, inputs):
    def test(a, b, c, d):
        return a and b or c ^ d

    assert context(P(0) & P(1) | P(2) ^ P(3), inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_parentheses(context, inputs):
    def test(a, b, c, d):
        return a and ((b or c) ^ d)

    assert context(P(0) & ((P(1) | P(2)) ^ P(3)), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_identity(context, inputs):
    def test(a, b, c):
        return a and b and c

    assert context(inputs[0] & P(1) & P(2), inputs) == test(*inputs)
    assert context(P(0) & inputs[1] & P(2), inputs) == test(*inputs)
    assert context(P(0) & P(1) & inputs[2], inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_inplace_change(context, inputs):
    def test(a, b, c, d):
        return ((a and b) or c) ^ d

    p = True

    p &= P(0)
    p &= P(1)
    p |= inputs[2]
    p ^= P(3)

    assert context(p, inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_complex_inplace_change(context, inputs):
    def test(a, b, c, d):
        return (a and b) or (c ^ d)

    p = True

    p &= P(0)
    p &= P(1)
    p |= P(2) ^ P(3)

    assert context(p, inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_inplace_change_with_predicate_replace(inputs):

    # do not define all default methods
    context = Context()

    def test(a, b):
        return a and b

    p = P(0)
    p &= P(1)

    # Must not failed due predicate moving in binary_i_op
    assert context(p, inputs) == test(*inputs)
