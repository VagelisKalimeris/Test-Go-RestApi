import pytest
from assertpy import assert_that

from framework.go_rest_client import GoRestTestClient
from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus
from go_rest_tests.test_data.user_emails import valid_user_email


@pytest.fixture(scope='session')
def go_rest_client():
    """
    Provides test client instance to all module tests.
    """
    yield GoRestTestClient()


@pytest.fixture(scope='session', autouse=True)
def valid_user(go_rest_client):
    """
    Valid user for all tests to access and use.
    Created before and deleted after each run.

    Creates user & verifies:
        - Expected response data
    Deletes user & verifies:
        - Operation success
    Retrieves deleted user & verifies:
        - Operation failure
    """
    valid_user = User(valid_user_email, UserGender.male.value, 'John Doe', UserStatus.active.value)
    valid_user_dict = valid_user.__dict__

    # POST new user
    post_resp = go_rest_client.post('/users', valid_user_dict)

    # Create & save valid user for later tests
    new_user_id = assert_that(post_resp, readable_json(post_resp)) \
        .is_equal_to(valid_user.__dict__, ignore='id') \
        .extract_key('id') \
        .val

    valid_user_dict['id'] = new_user_id

    yield valid_user_dict

    # DELETE new user
    go_rest_client.delete(f'/users/{new_user_id}')

    # GET deleted user by id & verify is absent
    go_rest_client.get(f'/users/{new_user_id}', 404)


@pytest.fixture(scope='session')
def valid_user_id(valid_user):
    """
    Abstracts repetitive user id retrieval.
    """
    return valid_user['id']
