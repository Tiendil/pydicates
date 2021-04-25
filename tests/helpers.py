

from hypothesis import strategies as h_st

from pydicates import Predicate, Boolean


class P(Predicate):

    def __init__(self, index: int):
        super().__init__(args=(index,))

    def boolean(self, context: Boolean, data: tuple[bool, ...], **kwargs):
        return data[self.args[0]]


def bool_vector(number: int):
    arguments = [h_st.booleans() for i in range(number)]
    return h_st.tuples(*arguments)
