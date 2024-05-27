import pytest

from framework.go_rest_client import GoRestTestClient


@pytest.fixture(scope='session')
def go_rest_client():

    yield GoRestTestClient()
