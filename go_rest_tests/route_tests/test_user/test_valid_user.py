from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import UserStatus


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
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/users/{valid_user_id}')

        # Verify GET response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_user)

    def test_new_user_is_vended_in_unfiltered_users(self, go_rest_client, valid_user):
        # Verify new resource data is vended in GET unfiltered resources response
        get_res = go_rest_client.get_paginated_result_contains_entry('/users/', valid_user)

        assert_that(get_res, readable_json(get_res))\
            .is_true()

    def test_new_user_update(self, go_rest_client, valid_user_id):
        update_info = {'status': UserStatus.inactive.value}

        # Update new resource
        patch_resp = go_rest_client.patch(f'/users/{valid_user_id}', update_info)

        # Verify resource was updated successfully
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_status(UserStatus.inactive.value)

    def test_get_new_user_after_update(self, go_rest_client, valid_user_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/users/{valid_user_id}')

        # Verify GET response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_status(UserStatus.inactive.value)
