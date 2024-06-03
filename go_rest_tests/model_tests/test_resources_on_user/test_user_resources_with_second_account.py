import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import UserGender, UserStatus, User


class TestUserResourcesWithSecUser:
    """
    Creates a 2nd user.
    Retrieves 2nd user's posts & verifies:
        - 1st user's post is not vended
    Retrieves 2nd user's todos & verifies:
        - 1st user's to do is not vended
    Deletes 2nd user.
    """
    @pytest.fixture(scope='session')
    def valid_user_2_id(self, go_rest_client):
        valid_user = User('another.user@random.com', UserGender.female.value, 'Jane Doe', UserStatus.active.value)

        # Create 2nd user
        post_resp = go_rest_client.post('/users', valid_user.__dict__)

        # Provide 2nd to later tests
        new_user_id = assert_that(post_resp, readable_json(post_resp)) \
            .extract_key('id') \
            .val

        yield new_user_id

        # DELETE 2nd user
        go_rest_client.delete(f'/users/{new_user_id}')

    def test_user_post_is_not_vended_in_different_users_posts(self, go_rest_client, valid_user_2_id, valid_post):
        # GET 2nd user's posts
        get_resp = go_rest_client.get(f'/users/{valid_user_2_id}/posts/')

        # Verify 1st user's post is not vended in 2nd user's posts
        assert_that(get_resp, readable_json(get_resp))\
            .does_not_contain(valid_post)

    def test_user_todo_is_not_vended_in_different_users_todos(self, go_rest_client, valid_user_2_id, valid_todo):
        # GET 2nd user's todos
        get_resp = go_rest_client.get(f'/users/{valid_user_2_id}/todos/')

        # Verify 1st user's to do is not vended in 2nd user's todos
        assert_that(get_resp, readable_json(get_resp))\
            .does_not_contain(valid_todo)
