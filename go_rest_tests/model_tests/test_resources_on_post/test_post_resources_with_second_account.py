import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import Post


class TestPostResourcesWithSecUser:
    """
    Creates a 2nd post.
    Retrieves 2nd post's comments & verifies:
        - 1st post's comment is not vended
    Deletes 2nd user.
    """
    @pytest.fixture(scope='session')
    def valid_post_2_id(self, go_rest_client, valid_user_id):
        valid_post = Post(valid_user_id, 'My winter holidays!', 'I will have a cold time.')

        # Create 2nd post
        post_resp = go_rest_client.post('/posts', valid_post.__dict__)

        # Provide 2nd post to later tests
        new_post_id = assert_that(post_resp, readable_json(post_resp)) \
            .extract_key('id') \
            .val

        yield new_post_id

    def test_post_comment_is_not_vended_in_different_posts_comments(self, go_rest_client, valid_post_2_id,
                                                                    valid_comment):
        # GET 2nd post's comments
        get_resp = go_rest_client.get(f'/posts/{valid_post_2_id}/comments/')

        # Verify 1st post's comment is not vended in 2nd post's comments
        assert_that(get_resp, readable_json(get_resp))\
            .does_not_contain(valid_comment)
