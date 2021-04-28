
from hypothesis import given

from pydicates import Context, BOOLEANS

from .helpers import P, simple_predicate, bool_vector


context = Context()
context.bulk_register(BOOLEANS)
context.register('simple_predicate', simple_predicate)


@given(inputs=bool_vector(1))
def test_not(inputs):
    assert context(P(0), inputs) == inputs[0]
    assert context(~P(0), inputs) == (not inputs[0])


@given(inputs=bool_vector(2))
def test_and(inputs):
    def test(a, b):
        return a and b

    assert context(P(0) & P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_and(inputs):
    def test(a, b, c):
        return a and b and c

    assert context(P(0) & P(1) & P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_or(inputs):
    def test(a, b):
        return a or b

    assert context(P(0) | P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_or(inputs):
    def test(a, b, c):
        return a or b or c

    assert context(P(0) | P(1) | P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(2))
def test_xor(inputs):
    def test(a, b):
        return a ^ b

    assert context(P(0) ^ P(1), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_complex_xor(inputs):
    def test(a, b, c):
        return a ^ b ^ c

    assert context(P(0) ^ P(1) ^ P(2), inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_complex(inputs):
    def test(a, b, c, d):
        return a and b or c ^ d

    assert context(P(0) & P(1) | P(2) ^ P(3), inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_parentheses(inputs):
    def test(a, b, c, d):
        return a and ((b or c) ^ d)

    assert context(P(0) & ((P(1) | P(2)) ^ P(3)), inputs) == test(*inputs)


@given(inputs=bool_vector(3))
def test_identity(inputs):
    def test(a, b, c):
        return a and b and c

    assert context(inputs[0] & P(1) & P(2), inputs) == test(*inputs)
    assert context(P(0) & inputs[1] & P(2), inputs) == test(*inputs)
    assert context(P(0) & P(1) & inputs[2], inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_inplace_change(inputs):
    def test(a, b, c, d):
        return ((a and b) or c) ^ d

    predicate = True

    predicate &= P(0)
    predicate &= P(1)
    predicate |= inputs[2]
    predicate ^= P(3)

    assert context(predicate, inputs) == test(*inputs)


@given(inputs=bool_vector(4))
def test_complex_inplace_change(inputs):
    def test(a, b, c, d):
        return (a and b) or (c ^ d)

    predicate = True

    predicate &= P(0)
    predicate &= P(1)
    predicate |= P(2) ^ P(3)

    assert context(predicate, inputs) == test(*inputs)
