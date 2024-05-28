import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus


@pytest.mark.parametrize('valid_user', [
    User('user@random.com', UserGender.male.value, 'John Doe', UserStatus.active.value)
])
def test_create_new_valid_user(go_rest_client, valid_user):
    """
    Creates user & verifies:
        - Operation success
        - Expected response data
    Retrieves created user & verifies:
        - User exists
        - User data are same
    """
    new_user_dict = valid_user.__dict__

    # POST new user
    post_resp = go_rest_client.post('/users', new_user_dict)

    # Verify user creation & POST response data is same as original and retrieve new user id
    new_user_id = assert_that(post_resp, readable_json(post_resp))\
        .is_equal_to(new_user_dict, ignore='id')\
        .extract_key('id')\
        .val

    # GET new user
    get_resp = go_rest_client.get(f'/users/{new_user_id}')

    # Verify GET response data is same as original
    assert_that(get_resp, readable_json(get_resp))\
        .is_equal_to(new_user_dict, ignore='id')\
        .has_id(new_user_id)


@pytest.mark.parametrize('invalid_user', [
    User('invalid@random.com', 'invalid gender option', 'John Doe', UserStatus.active.value),
    User('invalid@random.com', UserGender.male.value, 'John Doe', 'invalid status option'),
    User('invalid@random.com', UserGender.male.value, 'John Doe', ''),
    User('', UserGender.male.value, 'John Doe', UserStatus.active.value),
    User('existing@random.com', UserGender.male.value, 'John Doe', UserStatus.active.value)
])
def test_create_new_invalid_user(go_rest_client, invalid_user):
    """
    Verifies user creation fails with:
        - Invalid gender
        - Invalid status
        - Missing status
        - Missing email
        - Existing user email
    """
    new_user_dict = invalid_user.__dict__

    # POST new user with existing user email and verify 422 code
    go_rest_client.post('/users', new_user_dict, status_code=422)
