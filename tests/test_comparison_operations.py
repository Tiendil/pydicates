
import pytest

from hypothesis import given

from pydicates import Context, COMPARISONS, UnknownOperation

from .helpers import P, simple_predicate, int_vector

###########################################
# We can not chain redefined comparisons
# a < b < c is equal to (a < b) and (b < c)
#
# Full tests for __lt__
# Simple test for other operators
###########################################


context = Context()
context.bulk_register(COMPARISONS)
context.register('simple_predicate', simple_predicate)


@given(inputs=int_vector(2))
def test_lt(inputs):
    def test(a, b):
        return a < b

    assert context(P(0) < P(1), inputs) == test(*inputs)
    assert context(P(0) < inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] < P(1), inputs) == test(*inputs)


@given(inputs=int_vector(3))
def test_chain_lt(inputs):
    # pylint: disable=W0613
    def test(a, b, c):
        # "a < b < c" translates to "(a < b) and (b < c)"
        # which translates to "b < c", because (a < b) is Predicate and always True (?)
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
def test_le(inputs):
    def test(a, b):
        return a <= b

    assert context(P(0) <= P(1), inputs) == test(*inputs)
    assert context(P(0) <= inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] <= P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_eq(inputs):
    def test(a, b):
        return a == b

    assert context(P(0) == P(1), inputs) == test(*inputs)
    assert context(P(0) == inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] == P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_ne(inputs):
    def test(a, b):
        return a != b

    assert context(P(0) != P(1), inputs) == test(*inputs)
    assert context(P(0) != inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] != P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_gt(inputs):
    def test(a, b):
        return a > b

    assert context(P(0) > P(1), inputs) == test(*inputs)
    assert context(P(0) > inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] > P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2))
def test_ge(inputs):
    def test(a, b):
        return a >= b

    assert context(P(0) >= P(1), inputs) == test(*inputs)
    assert context(P(0) >= inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] >= P(1), inputs) == test(*inputs)
