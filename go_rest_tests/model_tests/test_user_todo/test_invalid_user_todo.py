import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import Todo, TodoStatus


class TestUserTodoInvalidCRUD:
    """
    Verifies to do creation on user route FAILS with:
        - Invalid user
        - Invalid status
        - Missing due on
        - Empty title
    Verifies invalid to do email:
        - Does not end up in user route todos response
    Verifies non-existing to do:
        - Cannot be updated on user route
        - Cannot be deleted on user route
    Verifies existing to do:
        - Cannot be updated with invalid post id on user route
    """
    def test_invalid_user_id_todo_creation_on_user_route(self, go_rest_client):
        invalid_todo = {'title': 'Plan vacations', 'due_on': '2024-06-01T00:00:00.000+05:30',
                        'status': TodoStatus.pending.value}

        # POST to do with invalid user id on user route and verify 422 code
        go_rest_client.post('/users/9999999/todos', invalid_todo, status_code=422)

    def test_invalid_status_todo_creation_on_user_route(self, go_rest_client, valid_user_id):
        invalid_todo = {'title': 'Plan vacations', 'due_on': '2024-06-01T00:00:00.000+05:30',
                        'status': 'Invalid status'}

        # POST to do with invalid status on user route and verify 422 code
        go_rest_client.post(f'/users/{valid_user_id}/todos', invalid_todo, status_code=422)

    @pytest.mark.xfail(reason='This actually looks like a BUG. Todos get created with a {"due_on": null} field. '
                              'This should FAIL with error returned!')
    def test_missing_due_on_todo_creation_on_user_route(self, go_rest_client, valid_user_id):
        invalid_todo = {'title': 'This should not be here!', 'status': TodoStatus.pending.value}

        # POST to do with missing due on, on user route and verify 422 code
        go_rest_client.post(f'/users/{valid_user_id}/todos', invalid_todo, status_code=422)

    def test_empty_title_todo_creation_on_user_route(self, go_rest_client, valid_user_id):
        invalid_todo = {'title': '', 'due_on': '2024-06-01T00:00:00.000+05:30', 'status': TodoStatus.pending.value}

        # POST to do with empty title on user route and verify 422 code
        go_rest_client.post(f'/users/{valid_user_id}/todos', invalid_todo, status_code=422)

    def test_invalid_todo_not_in_unfiltered_todos_on_user_route(self, go_rest_client, valid_user_id):
        # GET all todos on user route
        get_resp = go_rest_client.get(f'/users/{valid_user_id}/todos/')

        # Verify GET all todos response does not contain invalid data on user route
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('title')\
            .does_not_contain('Plan vacations')

    @pytest.mark.xfail(reason='Attempting to update status fails with 404 which is expected. Problem here is response '
                              'is not json decode-able which is inconsistent with general routes behaviour!')
    def test_non_existing_todo_update_on_user_route(self, go_rest_client, valid_user_id):
        update_info = {'status': TodoStatus.completed.value}

        # Verify non-existing to do cannot be updated on user route
        go_rest_client.patch(f'/users/{valid_user_id}/todos/9999999', update_info, 404)

    def test_non_existing_todo_deletion_on_user_route(self, go_rest_client, valid_user_id):
        # Verify non-existing to do cannot be deleted on user route
        go_rest_client.delete(f'/users/{valid_user_id}/todos/9999999', 404)

    @pytest.mark.xfail(reason='Attempting to update user id fails with 404. We should be getting 403 Forbidden, '
                              'since a todo\'s user id cannot be altered!')
    def test_existing_todo_invalid_update_on_user_route(self, go_rest_client, valid_user_id, valid_todo_id):
        update_info = {'user_id': 9999999}

        # Verify existing to do cannot be updated with invalid user id on user route
        go_rest_client.patch(f'/users/{valid_user_id}/todos/{valid_todo_id}', update_info, 422)
