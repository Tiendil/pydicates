
import pytest

from hypothesis import given

from .helpers import P, int_vector

from pydicates import ComparisonMixin, Context, UnknownOperation

###########################################
# We can not chain redefined comparisons
# a < b < c is equal to (a < b) and (b < c)
#
# Full tests for __lt__
# Simple test for other operators
###########################################


class ContextForTests(ComparisonMixin, Context):
    pass


@pytest.fixture(scope="module")
def context():
    return ContextForTests()


@given(inputs=int_vector(2))
def test_lt(context, inputs):
    def test(a, b):
        return a < b

    assert context(P(0) < P(1), inputs) == test(*inputs)
    assert context(P(0) < inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] < P(1), inputs) == test(*inputs)


@given(inputs=int_vector(3))
def test_chain_lt(context, inputs):
    def test(a, b, c):
        # "a < b < c" translates to "(a < b) and (b < c)"
        # which translates to "b < c"
        return b < c

    assert context(P(0) < P(1) < P(2), inputs) == test(*inputs)
    assert context(P(0) < P(1) < inputs[2], inputs) == test(*inputs)
    assert context(P(0) < inputs[1] < P(2), inputs) == test(*inputs)

    with pytest.raises(UnknownOperation):
        context(P(0) < inputs[1] < inputs[2], inputs)

    assert context(inputs[0] < P(1) < P(2), inputs) == test(*inputs)
    assert context(inputs[0] < P(1) < inputs[2], inputs) == test(*inputs)

    if inputs[0] < inputs[1]:
        assert context(inputs[0] < inputs[1] < P(2), inputs) == test(*inputs)
    else:
        with pytest.raises(UnknownOperation):
            context(inputs[0] < inputs[1] < P(2), inputs)

    with pytest.raises(UnknownOperation):
        context(inputs[0] < inputs[1] < inputs[2], inputs)


@given(inputs=int_vector(2))
def test_le(context, inputs):
    def test(a, b):
        return a <= b

    assert context(P(0) <= P(1), inputs) == test(*inputs)
    assert context(P(0) <= inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] <= P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_eq(context, inputs):
    def test(a, b):
        return a == b

    assert context(P(0) == P(1), inputs) == test(*inputs)
    assert context(P(0) == inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] == P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_ne(context, inputs):
    def test(a, b):
        return a != b

    assert context(P(0) != P(1), inputs) == test(*inputs)
    assert context(P(0) != inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] != P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_gt(context, inputs):
    def test(a, b):
        return a > b

    assert context(P(0) > P(1), inputs) == test(*inputs)
    assert context(P(0) > inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] > P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_ge(context, inputs):
    def test(a, b):
        return a >= b

    assert context(P(0) >= P(1), inputs) == test(*inputs)
    assert context(P(0) >= inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] >= P(1), inputs) == test(*inputs)
