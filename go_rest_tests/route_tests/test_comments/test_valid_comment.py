from assertpy import assert_that

from framework.response_util import readable_json


class TestCommentCRUD:
    """
    Comment creation and deletion are tested by global fixture.

    Retrieves valid comment & verifies:
        - Post exists
        - Post data are same
    Retrieves all comments & verifies:
        - Post exists
        - Post data are same
    Updates comment's info & verifies:
        - Expected response data
    Retrieves updated comment & verifies:
        - Post exists
        - Post data are updated
    """
    def test_get_new_comment_by_id(self, go_rest_client, valid_comment, valid_comment_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/comments/{valid_comment_id}')

        # Verify GET response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_comment)

    def test_new_comment_is_vended_in_unfiltered_users(self, go_rest_client, valid_comment):
        # Retrieve unfiltered resources
        get_res = go_rest_client.get_paginated_result_contains_entry('/comments/', valid_comment)

        assert_that(get_res, readable_json(get_res))\
            .is_true()

    def test_comment_update(self, go_rest_client, valid_comment_id):
        update_info = {'body': 'I HATE this post!!!'}

        # Update new resource
        patch_resp = go_rest_client.patch(f'/comments/{valid_comment_id}', update_info)

        # Verify resource was updated successfully
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_body('I HATE this post!!!')

    def test_retrieve_comment_after_update(self, go_rest_client, valid_comment_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/comments/{valid_comment_id}')

        # Verify GET response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_body('I HATE this post!!!')
