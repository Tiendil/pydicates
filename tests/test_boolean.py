
import pytest

from pydicates import Predicate, Boolean


class Check(Predicate):

    def __init__(self, index: int):
        super().__init__()
        self.index = index

    def bool(self, context: Boolean, data: dict, **kwargs):
        return bool(data[self.index])


@pytest.fixture
def context():
    return Boolean()


def test_not(context):
    assert context(Check(0), [True])
    assert context(~Check(0), [False])

    assert not context(Check(0), [False])
    assert not context(~Check(0), [True])


def test_and(context):
    assert context(Check(0) & Check(1), [True, True])
    assert not context(Check(0) & Check(1), [True, False])
    assert not context(Check(0) & Check(1), [False, True])
    assert not context(Check(0) & Check(1), [False, False])


def test_complex_and(context):
    assert context(Check(0) & Check(1) & Check(2), [True, True, True])
    assert not context(Check(0) & Check(1) & Check(2), [True, True, False])
    assert not context(Check(0) & Check(1) & Check(2), [True, False, True])
    assert not context(Check(0) & Check(1) & Check(2), [True, False, False])
    assert not context(Check(0) & Check(1) & Check(2), [False, True, True])
    assert not context(Check(0) & Check(1) & Check(2), [False, True, False])
    assert not context(Check(0) & Check(1) & Check(2), [False, False, True])
    assert not context(Check(0) & Check(1) & Check(2), [False, False, False])

    assert context(Check(0) & Check(1) & ~Check(2), [True, True, False])
    assert context(Check(0) & ~Check(1) & Check(2), [True, False, True])
    assert context(Check(0) & ~Check(1) & ~Check(2), [True, False, False])
    assert context(~Check(0) & Check(1) & Check(2), [False, True, True])
    assert context(~Check(0) & Check(1) & ~Check(2), [False, True, False])
    assert context(~Check(0) & ~Check(1) & Check(2), [False, False, True])
    assert context(~Check(0) & ~Check(1) & ~Check(2), [False, False, False])


def test_or(context):
    assert context(Check(0) | Check(1), [True, True])
    assert context(Check(0) | Check(1), [True, False])
    assert context(Check(0) | Check(1), [False, True])
    assert not context(Check(0) | Check(1), [False, False])


def test_complex_or(context):
    assert context(Check(0) | Check(1) | Check(2), [True, True, True])
    assert context(Check(0) | Check(1) | Check(2), [True, True, False])
    assert context(Check(0) | Check(1) | Check(2), [True, False, True])
    assert context(Check(0) | Check(1) | Check(2), [True, False, False])
    assert context(Check(0) | Check(1) | Check(2), [False, True, True])
    assert context(Check(0) | Check(1) | Check(2), [False, True, False])
    assert context(Check(0) | Check(1) | Check(2), [False, False, True])
    assert not context(Check(0) | Check(1) | Check(2), [False, False, False])


def test_xor(context):
    assert not context(Check(0) ^ Check(1), [True, True])
    assert context(Check(0) ^ Check(1), [True, False])
    assert context(Check(0) ^ Check(1), [False, True])
    assert not context(Check(0) ^ Check(1), [False, False])


def test_complex_xor(context):
    assert context(Check(0) ^ Check(1) ^ Check(2), [True, True, True])
    assert not context(Check(0) ^ Check(1) ^ Check(2), [True, True, False])
    assert not context(Check(0) ^ Check(1) ^ Check(2), [True, False, True])
    assert context(Check(0) ^ Check(1) ^ Check(2), [True, False, False])
    assert not context(Check(0) ^ Check(1) ^ Check(2), [False, True, True])
    assert context(Check(0) ^ Check(1) ^ Check(2), [False, True, False])
    assert context(Check(0) ^ Check(1) ^ Check(2), [False, False, True])
    assert not context(Check(0) ^ Check(1) ^ Check(2), [False, False, False])
