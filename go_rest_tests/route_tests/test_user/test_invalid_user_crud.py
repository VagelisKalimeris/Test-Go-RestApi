import pytest
from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus


@pytest.mark.parametrize('invalid_user', [
    User('invalid@random.com', 'invalid gender option', 'John Doe', UserStatus.active.value),
    User('invalid@random.com', UserGender.male.value, 'John Doe', 'invalid status option'),
    User('invalid@random.com', UserGender.male.value, 'John Doe', ''),
    User('', UserGender.male.value, 'John Doe', UserStatus.active.value),
    User('existing@random.com', UserGender.male.value, 'John Doe', UserStatus.active.value)
])
def test_create_new_invalid_user(go_rest_client, invalid_user):
    """
    Verifies user creation fails with:
        - Invalid gender
        - Invalid status
        - Missing status
        - Missing email
        - Existing user email
    """
    new_user_dict = invalid_user.__dict__

    # POST new user with existing user email and verify 422 code
    go_rest_client.post('/users', new_user_dict, status_code=422)



