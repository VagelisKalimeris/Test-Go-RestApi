from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import UserStatus


class TestUserCRUD:
    """
    User creation and deletion are tested by global fixture.

    Retrieves valid user & verifies:
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
    """
    def test_get_new_user_by_id(self, go_rest_client, valid_user, valid_user_id):
        # GET new user by id
        get_resp = go_rest_client.get(f'/users/{valid_user_id}')

        # Verify GET user response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_user)

    def test_new_user_is_vended_in_unfiltered_users(self, go_rest_client, valid_user):
        # GET all users
        get_resp = go_rest_client.get('/users/')

        # Verify GET all users response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .contains(valid_user)

    def test_new_user_update(self, go_rest_client, valid_user_id):
        update_info = {'status': UserStatus.inactive.value}

        # PUT new user
        patch_resp = go_rest_client.patch(f'/users/{valid_user_id}', update_info)

        # Verify user update & PUT response data
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_status(UserStatus.inactive.value)

    def test_get_new_user_after_update(self, go_rest_client, valid_user_id):
        # GET new user by id
        get_resp = go_rest_client.get(f'/users/{valid_user_id}')

        # Verify GET user response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_status(UserStatus.inactive.value)
