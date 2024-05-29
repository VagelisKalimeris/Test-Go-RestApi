import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus


@pytest.mark.parametrize('valid_user', [
    User('kergddovy@random.com', UserGender.male.value, 'John Doe', UserStatus.active.value)
])
class TestUserCRUD:
    """
    Creates user & verifies:
        - Expected response data
    Retrieves created user & verifies:
        - User exists
        - User data are same
    Retrieves all users & verifies:
        - User exists
        - User data are same
    Updates user's info & verifies:
        - Expected response data
    Retrieves updated user & verifies:
        - User exists
        - User data are updated
    Deletes user & verifies:
        - Operation success
    Retrieves deleted user & verifies:
        - Operation failure
    """
    @pytest.fixture(scope='function')
    def new_user_dict(self, valid_user):
        return valid_user.__dict__

    def test_create_new_user(self, go_rest_client, new_user_dict):
        # POST new user
        post_resp = go_rest_client.post('/users', new_user_dict)

        # Verify user creation & POST response data is same as original and retrieve new user id
        new_user_id = assert_that(post_resp, readable_json(post_resp))\
            .is_equal_to(new_user_dict, ignore='id')\
            .extract_key('id')\
            .val

        # Save new user id for later tests
        pytest.new_user_id = new_user_id

    def test_get_new_user_by_id(self, go_rest_client, new_user_dict):
        # GET new user by id
        get_resp = go_rest_client.get(f'/users/{pytest.new_user_id}')

        # Verify GET user response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(new_user_dict, ignore='id')\
            .has_id(pytest.new_user_id)

    def test_new_user_is_vended_in_unfiltered_users(self, go_rest_client, new_user_dict):
        # GET new user by id
        get_resp = go_rest_client.get('/users/')

        new_user_dict['id'] = pytest.new_user_id

        # Verify GET all users response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .contains(new_user_dict)

    def test_new_user_update(self, go_rest_client, new_user_dict):
        update_info = {'status': UserStatus.inactive.value}

        # PUT new user
        patch_resp = go_rest_client.patch(f'/users/{pytest.new_user_id}', update_info)

        # Verify user update & PUT response data
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_status(UserStatus.inactive.value)

    def test_get_new_user_after_update(self, go_rest_client, new_user_dict):
        # GET new user by id
        get_resp = go_rest_client.get(f'/users/{pytest.new_user_id}')

        # Verify GET user response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_status(UserStatus.inactive.value)

    def test_delete_new_user(self, go_rest_client, new_user_dict):
        # DELETE new user
        go_rest_client.delete(f'/users/{pytest.new_user_id}')

    def test_get_new_user_after_deletion(self, go_rest_client, new_user_dict):
        # GET deleted user by id
        go_rest_client.get(f'/users/{pytest.new_user_id}', 404)
