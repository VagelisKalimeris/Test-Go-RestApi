from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import TodoStatus


class TestTodoCRUD:
    """
    To do creation and deletion are tested by global fixture.

    Retrieves valid to do & verifies:
        - Post exists
        - Post data are same
    Retrieves all todos & verifies:
        - Post exists
        - Post data are same
    Updates to do's info & verifies:
        - Expected response data
    Retrieves updated to do & verifies:
        - Post exists
        - Post data are updated
    """
    def test_get_new_todo_by_id(self, go_rest_client, valid_todo, valid_todo_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/todos/{valid_todo_id}')

        # Verify GET response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(valid_todo)

    def test_new_todo_is_vended_in_unfiltered_users(self, go_rest_client, valid_todo):
        # Retrieve unfiltered resources
        get_res = go_rest_client.get_paginated_result_contains_entry('/todos/', valid_todo)

        assert_that(get_res, readable_json(get_res))\
            .is_true()

    def test_todo_update(self, go_rest_client, valid_todo_id):
        update_info = {'status': TodoStatus.completed.value}

        # Update new resource
        patch_resp = go_rest_client.patch(f'/todos/{valid_todo_id}', update_info)

        # Verify resource was updated successfully
        assert_that(patch_resp, readable_json(patch_resp)) \
            .has_status(TodoStatus.completed.value)

    def test_retrieve_todo_after_update(self, go_rest_client, valid_todo_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/todos/{valid_todo_id}')

        # Verify GET response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .has_status(TodoStatus.completed.value)
