from assertpy import assert_that

from framework.response_util import readable_json


class TestUserPostCRUD:
    """
    User & post creation and deletion are tested by global fixture.

    Retrieves post on user route, & verifies:
        - Post exists
        - Post data are the expected
    Retrieves all user posts & verifies:
        - Post exists
        - Post data are same
    Updates user post & verifies:
        - Expected response data
    Retrieves updated user post & verifies:
        - Post exists
        - Post data are updated
    """
    def test_get_user_post(self, go_rest_client, valid_user_id, valid_post, valid_post_id):
        # GET post on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/posts/{valid_post_id}')

        # Verify GET user response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_post)

    def test_user_post_is_vended_in_user_unfiltered_posts(self, go_rest_client, valid_user_id, valid_post):
        # GET all user posts
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/posts/')

        # Verify user posts contains post
        assert_that(get_resp, readable_json(get_resp))\
            .contains(valid_post)

    def test_user_post_update(self, go_rest_client, valid_user_id, valid_post_id):
        update_info = {'title': 'Summer vacation cancelled!'}

        # Update post on user route
        patch_resp = go_rest_client.patch(f'/users/{valid_user_id}/posts{valid_post_id}', update_info)

        # Verify update response data
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_title('Summer vacation cancelled!')

    def test_get_user_post_after_update(self, go_rest_client, valid_user_id, valid_post_id):
        # GET post on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/posts/{valid_post_id}')

        # Verify user post response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_title('Summer vacation cancelled!')
