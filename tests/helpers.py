

from hypothesis import strategies as h_st

from pydicates import Predicate


# pylint: disable=C0103
def P(index: int):
    return Predicate('simple_predicate', index)


# pylint: disable=C0103, W0613
def simple_predicate(context, data: int, inputs: tuple, **kwargs):
    return inputs[data]


def bool_vector(number: int):
    arguments = [h_st.booleans() for i in range(number)]
    return h_st.tuples(*arguments)


def int_vector(number: int,
               min_value=None,
               max_value=None,):
    arguments = [h_st.integers(min_value=min_value,
                               max_value=max_value) for i in range(number)]
    return h_st.tuples(*arguments)


def number_vector(number: int,
                  min_value=None,
                  max_value=None,
                  allow_nan=False,
                  allow_infinity=False):
    arguments = [h_st.integers(min_value=min_value,
                               max_value=max_value) | h_st.floats(min_value=min_value,
                                                                  max_value=max_value,
                                                                  allow_nan=allow_nan,
                                                                  allow_infinity=allow_infinity)
                 for i in range(number)]
    return h_st.tuples(*arguments)
