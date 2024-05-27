import pytest
from assertpy import add_extension

from framework.go_rest_client import GoRestTestClient
from framework.assertpy_extensions import extract_key


@pytest.fixture(scope='session')
def go_rest_client():
    """
    Provides test client instance to all module tests.
    """
    yield GoRestTestClient()


@pytest.fixture(scope='module', autouse=True)
def custom_extensions():
    """
    Makes custom extensions available to all module tests.
    """
    add_extension(extract_key)