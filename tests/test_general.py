
import pytest

from pydicates import Predicate, UnknownOperation


def test_unknown_context_operation(context):
    p = Predicate(operation='unknown')

    with pytest.raises(UnknownOperation):
        context(p, ())
