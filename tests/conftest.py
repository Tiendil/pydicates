
import pytest

from pydicates import Boolean


@pytest.fixture(scope="session")
def context():
    return Boolean()
