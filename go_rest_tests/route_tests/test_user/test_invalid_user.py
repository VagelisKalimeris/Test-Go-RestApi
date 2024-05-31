import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.resource_models import User, UserGender, UserStatus
from go_rest_tests.test_data.user_emails import valid_user_email, invalid_user_email


class TestUserInvalidCRUD:
    """
    Verifies user creation fails with:
        - Invalid gender
        - Invalid status
        - Missing status
        - Missing email
        - Existing user email
    Verifies invalid user email:
        - Does not end up in all users response
    Verifies non-existing user:
        - Cannot be updated
        - Cannot be deleted
    Verifies existing user:
        - Cannot be updated with invalid gender
    """
    @pytest.mark.parametrize('invalid_user', [
        User(invalid_user_email, 'invalid gender option', 'John Doe', UserStatus.active.value),
        User(invalid_user_email, UserGender.male.value, 'John Doe', 'invalid status option'),
        User(invalid_user_email, UserGender.male.value, 'John Doe', ''),
        User('', UserGender.male.value, 'John Doe', UserStatus.active.value),
        User(valid_user_email, UserGender.male.value, 'John Doe', UserStatus.active.value)
    ])
    def test_invalid_user_creation(self, go_rest_client, invalid_user):
        # POST invalid user and verify 422 code
        go_rest_client.post('/users', invalid_user.__dict__, status_code=422)

    def test_invalid_user_not_in_unfiltered_users(self, go_rest_client):
        # GET all users
        get_resp = go_rest_client.get('/users/')

        # Verify GET all users response does not contain invalid account
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('email')\
            .does_not_contain(invalid_user_email)

    def test_non_existing_user_update(self, go_rest_client):
        update_info = {'status': UserStatus.inactive.value}

        # Verify non-existing user cannot be updated
        go_rest_client.patch(f'/users/{9999999}', update_info, 404)

    def test_non_existing_user_deletion(self, go_rest_client):
        # Verify non-existing user cannot be deleted
        go_rest_client.delete(f'/users/{9999999}', 404)

    def test_existing_user_invalid_update(self, go_rest_client, valid_user_id):
        update_info = {'gender': 'invalid gender option'}

        # Verify existing user cannot be updated with invalid gender
        go_rest_client.patch(f'/users/{valid_user_id}', update_info, 422)
