import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import Post


class TestPostInvalidCRUD:
    """
    Verifies post creation FAILS with:
        - Invalid user
        - Missing body
        - Empty title
    Verifies invalid post:
        - Is not vended in user's posts response
    Verifies non-existing post:
        - Cannot be updated
        - Cannot be deleted
    Verifies existing post user id:
        - Cannot be updated with invalid user id
    """
    def test_invalid_user_id_post_creation(self, go_rest_client):
        invalid_post = Post(9999999, 'I liked this game!', 'My friends liked it too')

        # POST a post with invalid user id and verify 422 code
        go_rest_client.post('/posts', invalid_post.__dict__, status_code=422)

    def test_missing_body_post_creation(self, go_rest_client, valid_user_id):
        invalid_post = {'user_id': valid_user_id, 'title': 'I liked this game!'}

        # POST a post with missing title and verify 422 code
        go_rest_client.post('/posts', invalid_post, status_code=422)

    def test_empty_title_post_creation(self, go_rest_client, valid_user_id):
        invalid_post = Post(valid_user_id, '', 'My friends liked it too')

        # POST a post with empty title and verify 422 code
        go_rest_client.post('/posts', invalid_post.__dict__, status_code=422)

    def test_invalid_post_not_in_user_posts(self, go_rest_client, valid_user_id):
        # GET all posts
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/posts')

        # Verify GET all posts response does not contain invalid  data
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('body')\
            .does_not_contain('My friends liked it too')

    def test_non_existing_post_update(self, go_rest_client):
        update_info = {'body': 'My friends liked it too'}

        # Verify non-existing post cannot be updated
        go_rest_client.patch(f'/posts/{9999999}', update_info, 404)

    def test_non_existing_post_deletion(self, go_rest_client):
        # Verify non-existing post cannot be deleted
        go_rest_client.delete(f'/posts/{9999999}', 404)

    @pytest.mark.xfail(reason='This actually looks like a BUG. Attempting to update the id internally fails, '
                              'but API returns 200 OK! We should be getting 403 Forbidden, since a posts\'s  '
                              'user id cannot be altered!')
    def test_existing_post_invalid_update(self, go_rest_client, valid_post_id):
        update_info = {'id': 9999999}

        # Verify existing post cannot be updated with invalid user id
        go_rest_client.patch(f'/posts/{valid_post_id}', update_info, 422)
