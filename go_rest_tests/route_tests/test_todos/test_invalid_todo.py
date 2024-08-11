import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import Todo, TodoStatus


class TestTodoInvalidCRUD:
    """
    Verifies to do creation FAILS with:
        - Invalid user id
        - Invalid status
        - Missing due on
        - Empty title
    Verifies invalid to do email:
        - Does not end up in all todos response
    Verifies non-existing to do:
        - Cannot be updated
        - Cannot be deleted
    Verifies existing to do:
        - Cannot be updated with invalid post id
    """
    def test_invalid_user_id_todo_creation(self, go_rest_client):
        invalid_todo = Todo(9999999, 'Plan vacations', '2024-06-01T00:00:00.000+05:30',
                            TodoStatus.pending.value)

        # POST to do with invalid user id and verify 422 code
        go_rest_client.post('/todos', invalid_todo.__dict__, status_code=422)

    def test_invalid_status_todo_creation(self, go_rest_client, valid_user_id):
        invalid_todo = Todo(valid_user_id, 'Plan vacations',
                            '2024-06-01T00:00:00.000+05:30', 'Invalid status')

        # POST to do with invalid status and verify 422 code
        go_rest_client.post('/todos', invalid_todo.__dict__, status_code=422)

    @pytest.mark.xfail(reason='This actually looks like a BUG. Todos get created with a {"due_on": null} field. '
                              'This should FAIL with 422 returned!')
    def test_missing_due_on_todo_creation(self, go_rest_client, valid_user_id):
        invalid_todo = {'user_id': valid_user_id, 'title': 'This should not be here!',
                        'status': TodoStatus.pending.value}

        # POST to do with missing due on and verify 422 code
        go_rest_client.post('/todos', invalid_todo, status_code=422)

    def test_empty_title_todo_creation(self, go_rest_client, valid_user_id):
        invalid_todo = Todo(valid_user_id, '', '2024-06-01T00:00:00.000+05:30', TodoStatus.pending.value)

        # POST to do with empty title and verify 422 code
        go_rest_client.post('/todos', invalid_todo.__dict__, status_code=422)

    def test_invalid_todo_not_in_unfiltered_todos(self, go_rest_client):
        # Verify all todos do not contain invalid data
        get_res = go_rest_client.get_paginated_result_does_not_contain_value('/todos/', 'title', 'Plan vacations')

        assert_that(get_res, readable_json(get_res))\
            .is_true()

    def test_non_existing_todo_update(self, go_rest_client):
        update_info = {'status': TodoStatus.completed.value}

        # Verify non-existing to do cannot be updated
        go_rest_client.patch('/todos/9999999', update_info, 404)

    def test_non_existing_todo_deletion(self, go_rest_client):
        # Verify non-existing to do cannot be deleted
        go_rest_client.delete('/todos/9999999', 404)

    def test_existing_todo_invalid_update(self, go_rest_client, valid_todo_id):
        update_info = {'user_id': 9999999}

        # Verify existing to do cannot be updated with invalid user id
        go_rest_client.patch(f'/todos/{valid_todo_id}', update_info, 422)
