
from hypothesis import given, assume

from pydicates import Context, MATH

from .helpers import P, simple_predicate, int_vector, number_vector


context = Context()
context.bulk_register(MATH)
context.register('simple_predicate', simple_predicate)


@given(inputs=number_vector(1))
def test_neg(inputs):
    assert context(-P(0), inputs) == -inputs[0]
    assert context(--P(0), inputs) == --inputs[0]  # pylint: disable=E0107
    assert context(--P(0), inputs) == inputs[0]  # pylint: disable=E0107
    assert context(---P(0), inputs) == -inputs[0]  # pylint: disable=E0107


@given(inputs=number_vector(2))
def test_pos(inputs):
    assert context(+P(0), inputs) == +inputs[0]
    assert context(++P(0), inputs) == ++inputs[0]  # pylint: disable=E0107
    assert context(+++P(0), inputs) == inputs[0]  # pylint: disable=E0107


@given(inputs=number_vector(2))
def test_add(inputs):
    def test(a, b):
        return a + b

    assert context(P(0) + P(1), inputs) == test(*inputs)
    assert context(P(0) + inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] + P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_sub(inputs):
    def test(a, b):
        return a - b

    assert context(P(0) - P(1), inputs) == test(*inputs)
    assert context(P(0) - inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] - P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_mul(inputs):
    def test(a, b):
        return a * b

    assert context(P(0) * P(1), inputs) == test(*inputs)
    assert context(P(0) * inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] * P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_matmul(inputs):

    class FakeMatrix:

        def __init__(self, value):
            self.value = value

        def __matmul__(self, other):
            if self.__class__ is not other.__class__:
                return NotImplemented

            return FakeMatrix(self.value + other.value)

        def __eq__(self, other):
            return self.value == other.value

    inputs = [FakeMatrix(value) for value in inputs]

    def test(a, b):
        return a @ b

    assert context(P(0) @ P(1), inputs) == test(*inputs)
    assert context(P(0) @ inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] @ P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_truediv(inputs):

    assume(inputs[1] != 0)

    def test(a, b):
        return a / b

    assert context(P(0) / P(1), inputs) == test(*inputs)
    assert context(P(0) / inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] / P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_floordiv(inputs):

    assume(inputs[1] != 0)

    def test(a, b):
        return a // b

    assert context(P(0) // P(1), inputs) == test(*inputs)
    assert context(P(0) // inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] // P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_mod(inputs):

    assume(inputs[1] != 0)

    def test(a, b):
        return a % b

    assert context(P(0) % P(1), inputs) == test(*inputs)
    assert context(P(0) % inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] % P(1), inputs) == test(*inputs)


@given(inputs=number_vector(2))
def test_divmod(inputs):

    assume(inputs[1] != 0)

    def test(a, b):
        return divmod(a, b)

    assert context(divmod(P(0), P(1)), inputs) == test(*inputs)
    assert context(divmod(P(0), inputs[1]), inputs) == test(*inputs)
    assert context(divmod(inputs[0], P(1)), inputs) == test(*inputs)


@given(inputs=number_vector(2, min_value=-100, max_value=100))
def test_pow(inputs):

    assume(all(a <= -1 or a >= 1 for a in inputs))
    assume(inputs[1] >= 0 or inputs[0] > 0)

    def test(a, b):
        return a ** b

    assert context(P(0) ** P(1), inputs) == test(*inputs)
    assert context(P(0) ** inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] ** P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2, min_value=-100, max_value=100))
def test_lshift(inputs):

    assume(inputs[1] >= 0)

    def test(a, b):
        return a << b

    assert context(P(0) << P(1), inputs) == test(*inputs)
    assert context(P(0) << inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] << P(1), inputs) == test(*inputs)


@given(inputs=int_vector(2, min_value=-100, max_value=100))
def test_rshift(inputs):
    assume(inputs[1] >= 0)

    def test(a, b):
        return a >> b

    assert context(P(0) >> P(1), inputs) == test(*inputs)
    assert context(P(0) >> inputs[1], inputs) == test(*inputs)
    assert context(inputs[0] >> P(1), inputs) == test(*inputs)


@given(inputs=number_vector(6))
def test_chain(inputs):
    assume(inputs[1] != 0)
    assume(inputs[3] != 0)

    def test(a, b, c, d, e, f):
        return a % b + c / d - e - f

    assert context(P(0) % P(1) + P(2) / P(3) - P(4) - P(5), inputs) == test(*inputs)
    assert context(P(0) % inputs[1] + inputs[2] / P(3) - P(4) - P(5), inputs) == test(*inputs)
