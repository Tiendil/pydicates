
import pytest

from hypothesis import given
from hypothesis import strategies as h_st

from pydicates import Predicate, Boolean


class P(Predicate):

    def __init__(self, index: int):
        super().__init__(args=(index,))

    def boolean(self, context: Boolean, data: dict, **kwargs):
        return data[self.args[0]]


def bool_vector(number: int):
    arguments = [h_st.booleans() for i in range(number)]
    return h_st.tuples(*arguments)


@pytest.fixture(scope="session")
def context():
    return Boolean()


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
