
import pytest

from pydicates import Predicate, UnknownOperation, common


def test_unknown_context_operation():
    predicate = Predicate(operation='unknown', data=())

    with pytest.raises(UnknownOperation):
        common(predicate, ())
