import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import Comment


class TestCommentInvalidCRUD:
    """
    Verifies comment creation FAILS with:
        - Invalid email
        - Invalid post id
        - Missing name
        - Empty body
    Verifies invalid comment email:
        - Does not end up in all comments response
    Verifies non-existing comment:
        - Cannot be updated
        - Cannot be deleted
    Verifies existing comment:
        - Cannot be updated with invalid post id
    """
    def test_invalid_email_comment_creation(self, go_rest_client, valid_post_id):
        invalid_comment = Comment(valid_post_id, 'John Doe', 'invalid email', 'This post is awesome!')

        # POST comment with invalid email and verify 422 code
        go_rest_client.post('/comments', invalid_comment.__dict__, status_code=422)

    def test_invalid_post_id_comment_creation(self, go_rest_client):
        invalid_comment = Comment(9999999, 'John Doe', 'valid@email.com',
                                  'This post is awesome!')

        # POST comment with invalid post id and verify 422 code
        go_rest_client.post('/comments', invalid_comment.__dict__, status_code=422)

    @pytest.mark.xfail(reason='This actually looks like a BUG. Comments get created with missing fields eg '
                              '\'name\' or \'email\'. This should FAIL with error returned!')
    def test_missing_name_comment_creation(self, go_rest_client, valid_post_id):
        invalid_comment = {'post_id': valid_post_id, 'email': 'valid@email.com', 'body': 'This post is awesome!'}

        # POST comment with missing name and verify 422 code
        go_rest_client.post('/comments', invalid_comment, status_code=422)

    def test_empty_body_comment_creation(self, go_rest_client, valid_post_id):
        invalid_comment = Comment(valid_post_id, 'John Doe', 'invalid email', '')

        # POST comment with empty body and verify 422 code
        go_rest_client.post('/comments', invalid_comment.__dict__, status_code=422)

    def test_invalid_comment_not_in_unfiltered_comments(self, go_rest_client):
        # GET all comments
        get_resp = go_rest_client.get('/comments/')

        # Verify GET all comments response does not contain invalid account data
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('email')\
            .does_not_contain('valid@email.com')

    def test_non_existing_comment_update(self, go_rest_client):
        update_info = {'email': 'valid@email.com'}

        # Verify non-existing comment cannot be updated
        go_rest_client.patch(f'/comments/{9999999}', update_info, 404)

    def test_non_existing_comment_deletion(self, go_rest_client):
        # Verify non-existing comment cannot be deleted
        go_rest_client.delete(f'/comments/{9999999}', 404)

    @pytest.mark.xfail(reason='This actually looks like a BUG. Attempting to update the post id internally fails, '
                              'but API returns 200 OK! We should be getting ERROR response since a comment\'s  '
                              'post id cannot be altered!')
    def test_existing_comment_invalid_update(self, go_rest_client, valid_comment_id):
        update_info = {'post': 9999999}

        # Verify existing comment cannot be updated with invalid post id
        go_rest_client.patch(f'/comments/{valid_comment_id}', update_info, 422)
