import pytest
from assertpy import assert_that

from framework.response_util import readable_json


class TestUserPostInvalidCRUD:
    """
    Verifies post creation on user route FAILS with:
        - Invalid user
        - Missing body
        - Empty title
    Verifies invalid post:
        - Is not vended in user route posts response
    Verifies non-existing post:
        - Cannot be updated on user route
        - Cannot be deleted on user route
    Verifies existing post user id:
        - Cannot be updated with invalid user id on user route
    """
    def test_invalid_user_post_creation_on_user_route(self, go_rest_client):
        invalid_post = {'title': 'I liked this game!', 'body': 'My friends liked it too'}

        # POST a post with invalid user id on user route and verify 422 code
        go_rest_client.post('/users/9999999/posts', invalid_post, status_code=422)

    def test_missing_body_post_creation_on_user_route(self, go_rest_client, valid_user_id):
        invalid_post = {'title': 'I liked this game!'}

        # POST a post with missing title on user route and verify 422 code
        go_rest_client.post(f'/users/{valid_user_id}/posts', invalid_post, status_code=422)

    def test_empty_title_post_creation_on_user_route(self, go_rest_client, valid_user_id):
        invalid_post = {'title': '', 'body': 'My friends liked it too'}

        # POST a post with empty title on user route and verify 422 code
        go_rest_client.post(f'/users/{valid_user_id}/posts', invalid_post, status_code=422)

    def test_invalid_post_not_in_user_posts(self, go_rest_client, valid_user_id):
        # GET all posts on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/posts')

        # Verify GET all posts on user route response does not contain invalid  data
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('body')\
            .does_not_contain('My friends liked it too')

    @pytest.mark.xfail(reason='Attempting to update the id fails with 404 which is expected. Problem here is response '
                              'is not json decode-able which is inconsistent with general routes behaviour!')
    def test_non_existing_post_update_on_user_route(self, go_rest_client, valid_user_id):
        update_info = {'body': 'My friends liked it too'}

        # Verify non-existing post cannot be updated on user route
        go_rest_client.patch(f'/users/{valid_user_id}/posts/9999999', update_info, 404)

    def test_non_existing_post_deletion_on_user_route(self, go_rest_client, valid_user_id):
        # Verify non-existing post cannot be deleted on user route
        go_rest_client.delete(f'/users/{valid_user_id}/posts/9999999', 404)

    @pytest.mark.xfail(reason='Attempting to update the id fails with 404. Getting 403 Forbidden, or 422 seems more '
                              'appropriate here, since a posts\'s user id should not be mutable!')
    def test_existing_post_invalid_update_on_user_route(self, go_rest_client, valid_post_id, valid_user_id):
        update_info = {'id': 9999999}

        # Verify existing post cannot be updated with invalid user id on user route
        go_rest_client.patch(f'/users/{valid_user_id}/posts/{valid_post_id}', update_info, 422)
