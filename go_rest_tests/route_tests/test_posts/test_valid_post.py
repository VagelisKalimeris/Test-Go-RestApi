from assertpy import assert_that

from framework.response_util import readable_json


class TestPostCRUD:
    """
    Post creation and deletion are tested by global fixture.

    Retrieves valid post & verifies:
        - Post exists
        - Post data are same
    Retrieves all posts & verifies:
        - Post exists
        - Post data are same
    Updates post's info & verifies:
        - Expected response data
    Retrieves updated post & verifies:
        - Post exists
        - Post data are updated
    """
    def test_get_new_post_by_id(self, go_rest_client, valid_post, valid_post_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}')

        # Verify GET response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_post)

    def test_new_post_is_vended_in_unfiltered_users(self, go_rest_client, valid_post):
        # Verify new resource data is vended in GET unfiltered resources response
        get_res = go_rest_client.get_paginated_result_contains_entry('/posts/', valid_post)

        assert_that(get_res, readable_json(get_res))\
            .is_true()

    def test_post_update(self, go_rest_client, valid_post_id):
        update_info = {'title': 'Summer vacation cancelled!'}

        # Update new resource
        patch_resp = go_rest_client.patch(f'/posts/{valid_post_id}', update_info)

        # Verify resource was updated successfully
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_title('Summer vacation cancelled!')

    def test_retrieve_post_after_update(self, go_rest_client, valid_post_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}')

        # Verify GET response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_title('Summer vacation cancelled!')
