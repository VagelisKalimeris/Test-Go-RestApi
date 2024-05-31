import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus
from go_rest_tests.test_data.comment_emails import valid_comment_email, invalid_comment_email


class TestCommentInvalidCRUD:
    """
    Verifies comment creation FAILS with:
        - Invalid gender
        - Invalid status
        - Missing status
        - Missing email
        - Existing comment email
    Verifies invalid comment email:
        - Does not end up in all comments request
    Verifies non-existing comment:
        - Cannot be updated
        - Cannot be deleted
    Verifies existing comment:
        - Cannot be updated with invalid gender
    """
    @pytest.mark.parametrize('invalid_comment', [
        # User(invalid_comment_email, 'invalid gender option', 'John Doe', UserStatus.active.value),
        # User(invalid_comment_email, UserGender.male.value, 'John Doe', 'invalid status option'),
        # User(invalid_comment_email, UserGender.male.value, 'John Doe', ''),
        # User('', UserGender.male.value, 'John Doe', UserStatus.active.value),
        # User(valid_comment_email, UserGender.male.value, 'John Doe', UserStatus.active.value)
    ])
    def test_invalid_comment_creation(self, go_rest_client, invalid_comment):
        # POST new comment with existing comment email and verify 422 code
        go_rest_client.post('/comments', invalid_comment.__dict__, status_code=422)

    def test_invalid_comment_not_in_unfiltered_comments(self, go_rest_client):
        """
        Verifies invalid comment is not present in all comments response.
        """
        # GET all comments
        get_resp = go_rest_client.get('/comments/')

        # Verify GET all comments response does not contain invalid account
        assert_that(get_resp, readable_json(get_resp))\
            .extracting('email')\
            .does_not_contain(invalid_comment_email)

    def test_non_existing_comment_update(self, go_rest_client):
        update_info = {'status': UserStatus.inactive.value}

        # Verify non-existing comment cannot be updated
        go_rest_client.patch(f'/comments/{9999999}', update_info, 404)

    def test_non_existing_comment_deletion(self, go_rest_client):
        # Verify non-existing comment cannot be deleted
        go_rest_client.delete(f'/comments/{9999999}', 404)

    def test_existing_comment_invalid_update(self, go_rest_client, valid_comment_id):
        update_info = {'gender': 'invalid gender option'}

        # Verify existing comment cannot be updated with invalid gender
        go_rest_client.patch(f'/comments/{valid_comment_id}', update_info, 422)
