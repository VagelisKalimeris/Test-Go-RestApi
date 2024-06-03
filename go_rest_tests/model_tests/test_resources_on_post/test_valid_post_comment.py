import pytest
from assertpy import assert_that

from framework.response_util import readable_json


class TestCommentCommentCRUD:
    """
    Comment & post creation and deletion are tested by global fixture.

    Retrieves comment on post route, & verifies:
        - Comment exists
        - Comment data are the expected
    Retrieves all post comments & verifies:
        - Comment exists
        - Comment data are same
    Updates post comment & verifies:
        - Expected response data
    Retrieves updated post comment & verifies:
        - Comment exists
        - Comment data are updated
    """
    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would have expected this to work!')
    def test_get_post_comment(self, go_rest_client, valid_post_id, valid_comment, valid_comment_id):
        # GET comment on post route
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}/comments/{valid_comment_id}')

        # Verify GET post response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_comment)

    def test_post_comment_is_vended_in_post_unfiltered_comments(self, go_rest_client, valid_post_id, valid_comment):
        # GET all post comments
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}/comments/')

        # Verify post comments contains comment
        assert_that(get_resp, readable_json(get_resp))\
            .contains(valid_comment)

    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would have expected this to work!')
    def test_post_comment_update(self, go_rest_client, valid_post_id, valid_comment_id):
        update_info = {'body': 'I HATE this post!!!'}

        # Update comment on post route
        patch_resp = go_rest_client.patch(f'/posts/{valid_post_id}/comments{valid_comment_id}', update_info)

        # Verify update response data
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_body('I HATE this post!!!')

    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would have expected this to work!')
    def test_get_post_comment_after_update(self, go_rest_client, valid_post_id, valid_comment_id):
        # GET comment on post route
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}/comments/{valid_comment_id}')

        # Verify post comment response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_body('I HATE this post!!!')
