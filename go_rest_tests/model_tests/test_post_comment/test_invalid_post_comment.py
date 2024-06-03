import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import Comment


class TestPostCommentInvalidCRUD:
    """
    Verifies comment creation on post route FAILS with:
        - Invalid email
        - Invalid post id
        - Missing name
        - Empty body
    Verifies invalid comment email:
        - Does not end up in post route comments response
    Verifies non-existing comment:
        - Cannot be updated on post route
        - Cannot be deleted on post route
    Verifies existing comment:
        - Cannot be updated with invalid post id on post route
    """
    def test_invalid_email_comment_creation_on_post_route(self, go_rest_client, valid_post_id):
        invalid_comment = {'name': 'John Doe', 'email': 'invalid email', 'body': 'This post is awesome!'}

        # POST comment with invalid email and verify 422 code on post route
        go_rest_client.post(f'/posts/{valid_post_id}/comments', invalid_comment, status_code=422)

    def test_invalid_post_id_comment_creation_on_post_route(self, go_rest_client, valid_post_id):
        invalid_comment = {'name': 'John Doe', 'email': 'valid@email.com', 'body': 'This post is awesome!'}

        # POST comment with invalid post id and verify 422 code on post route
        go_rest_client.post(f'/posts/9999999/comments', invalid_comment, status_code=422)

    def test_missing_name_comment_creation_on_post_route(self, go_rest_client, valid_post_id):
        invalid_comment = {'email': 'valid@email.com', 'body': 'This post is awesome!'}

        # POST comment with missing name and verify 422 code on post route
        go_rest_client.post(f'/posts/{valid_post_id}/comments', invalid_comment, status_code=422)

    def test_empty_body_comment_creation_on_post_route(self, go_rest_client, valid_post_id):
        invalid_comment = {'name': 'John Doe', 'email': 'valid@email.com', 'body': ''}

        # POST comment with empty body and verify 422 code on post route
        go_rest_client.post(f'/posts/{valid_post_id}/comments', invalid_comment, status_code=422)

    def test_invalid_comment_not_in_unfiltered_comments_on_post_route(self, go_rest_client, valid_post_id):
        # GET all comments on post route
        get_resp = go_rest_client.get(f'/posts/{valid_post_id}/comments/')

        # Verify GET all comments response does not contain invalid data on post route
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('email')\
            .does_not_contain('valid@email.com')

    @pytest.mark.xfail(reason='Attempting to update email fails with 404 which is expected. Problem here is response '
                              'is not json decode-able which is inconsistent with general routes behaviour!')
    def test_non_existing_comment_update_on_post_route(self, go_rest_client, valid_post_id):
        update_info = {'email': 'valid@email.com'}

        # Verify non-existing comment cannot be updated on post route
        go_rest_client.patch(f'/posts/{valid_post_id}/comments/9999999', update_info, 404)

    def test_non_existing_comment_deletion_on_post_route(self, go_rest_client, valid_post_id):
        # Verify non-existing comment cannot be deleted on post route
        go_rest_client.delete(f'/posts/{valid_post_id}/comments/9999999', 404)

    @pytest.mark.xfail(reason='Attempting to update post id fails with 404. We should be getting 403 Forbidden, or 422 '
                              'since a posts\'s user id cannot be altered! Also response is not json decode-able which '
                              'is inconsistent with general routes behaviour!')
    def test_existing_comment_invalid_update_on_post_route(self, go_rest_client, valid_post_id, valid_comment_id):
        update_info = {'post': 9999999}

        # Verify existing comment cannot be updated with invalid post id on post route
        go_rest_client.patch(f'/posts/{valid_post_id}/comments/{valid_comment_id}', update_info, 422)
