
import pytest

from pydicates import Predicate, UnknownOperation, Boolean


@pytest.fixture(scope="module")
def context():
    return Boolean()


def test_unknown_context_operation(context):
    p = Predicate(operation='unknown')

    with pytest.raises(UnknownOperation):
        context(p, ())
