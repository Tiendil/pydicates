
import pytest

from hypothesis import given
from hypothesis import strategies as h_st

from pydicates import Predicate, Boolean


class Check(Predicate):

    def __init__(self, index: int):
        super().__init__()
        self.index = index

    def bool(self, context: Boolean, data: dict, **kwargs):
        return bool(data[self.index])


def bool_vector(number: int):
    arguments = [h_st.booleans() for i in range(number)]
    return h_st.tuples(*arguments)


@pytest.fixture(scope="session")
def context():
    return Boolean()


@given(inputs=bool_vector(1))
def test_not(context, inputs):
    assert context(Check(0), inputs) == inputs[0]
    assert context(~Check(0), inputs) == (not inputs[0])


@given(inputs=bool_vector(2))
def test_and(context, inputs):
    def test(a, b):
        return a and b

    assert context(Check(0) & Check(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_and(context, inputs):
    def test(a, b, c):
        return a and b and c

    assert context(Check(0) & Check(1) & Check(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_or(context, inputs):
    def test(a, b):
        return a or b

    assert context(Check(0) | Check(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_or(context, inputs):
    def test(a, b, c):
        return a or b or c

    assert context(Check(0) | Check(1) | Check(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_xor(context, inputs):
    def test(a, b):
        return a ^ b

    assert context(Check(0) ^ Check(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_xor(context, inputs):
    def test(a, b, c):
        return a ^ b ^ c

    assert context(Check(0) ^ Check(1) ^ Check(2), inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_complex(context, inputs):
    def test(a, b, c, d):
        return a and b or c ^ d

    assert context(Check(0) & Check(1) | Check(2) ^ Check(3), inputs) == test(*inputs)



@given(inputs=bool_vector(4))
def test_parentheses(context, inputs):
    def test(a, b, c, d):
        return a and ((b or c) ^ d)

    assert context(Check(0) & ((Check(1) | Check(2)) ^ Check(3)), inputs) == test(*inputs)
