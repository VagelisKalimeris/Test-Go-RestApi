import pytest
from assertpy import assert_that

from framework.response_util import readable_json


class TestUserTodoCRUD:
    """
    @pytest.mark.xfail(reason='Not sure if its a bug or not implemented, but would expect this to work!')
    User & to do creation and deletion are tested by global fixture.

    Retrieves to do on user route, & verifies:
        - To do exists
        - To do data are the expected
    Retrieves all user todos & verifies:
        - To do exists
        - To do data are same
    Updates user to do & verifies:
        - Expected response data
    Retrieves updated user to do & verifies:
        - To do exists
        - To do data are updated
    """
    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would expect this to work!')
    def test_get_user_todo(self, go_rest_client, valid_user_id, valid_todo, valid_todo_id):
        # GET to do on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/todos/{valid_todo_id}')

        # Verify GET user response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_todo)

    def test_user_todo_is_vended_in_user_unfiltered_todos(self, go_rest_client, valid_user_id, valid_todo):
        # GET all user todos
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/todos/')

        # Verify user todos contains to do
        assert_that(get_resp, readable_json(get_resp))\
            .contains(valid_todo)

    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would expect this to work!')
    def test_user_todo_update(self, go_rest_client, valid_user_id, valid_todo_id):
        update_info = {'title': 'Summer vacation cancelled!'}

        # Update to do on user route
        patch_resp = go_rest_client.patch(f'/users/{valid_user_id}/todos{valid_todo_id}', update_info)

        # Verify update response data
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_title('Summer vacation cancelled!')

    @pytest.mark.xfail(reason='Not sure if its a BUG or not implemented, but would expect this to work!')
    def test_get_user_todo_after_update(self, go_rest_client, valid_user_id, valid_todo_id):
        # GET to do on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/todos/{valid_todo_id}')

        # Verify user to do response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_title('Summer vacation cancelled!')
