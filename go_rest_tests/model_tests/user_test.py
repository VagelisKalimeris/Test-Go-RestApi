from assertpy import assert_that

from framework.response_util import readable_json
from go_rest_tests.test_data.users import user_1


def test_create_new_user(go_rest_client):
    # POST new user
    post_resp = go_rest_client.post('/users', user_1.__dict__)

    # Verify user creation & POST response data is same as original
    new_user_id = assert_that(post_resp, readable_json(post_resp))\
        .is_equal_to(user_1.__dict__, ignore='id')\
        .extract_key('id')\
        .val

    # GET new user
    get_resp = go_rest_client.get(f'/users/{new_user_id}')

    # Verify GET response data is same as original
    assert_that(get_resp, readable_json(get_resp))\
        .is_equal_to(user_1.__dict__, ignore='id')\
        .has_id(new_user_id)
