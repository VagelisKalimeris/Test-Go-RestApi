from httpx import get, post, put, patch, delete
from assertpy import assert_that

from framework.response_util import readable_json


class TestClient:
    """
    Test client base class.
    Abstracts repetitive boilerplate code form tests.
    """
    def __init__(self):
        self.service_base_url = None
        self.token = None
        self.auth = None

    def get(self, path: str, status_code: int = 200):
        # Do call
        get_resp = get(self.service_base_url + path, headers=self.auth)

        # Verify expected status code
        assert_that(get_resp, readable_json(get_resp.json())).has_status_code(status_code)

        # Extract response body
        return get_resp.json()

    def post(self, path: str, body, status_code: int = 201):
        # Do call
        post_resp = post(self.service_base_url + path, headers=self.auth, data=body)

        # Verify expected status code
        assert_that(post_resp, readable_json(post_resp.json())).has_status_code(status_code)

        # Extract response body
        return post_resp.json()

    def put(self, path: str, body, status_code: int = 200):
        # Do call
        put_resp = put(self.service_base_url + path, headers=self.auth, data=body)

        # Verify expected status code
        assert_that(put_resp, readable_json(put_resp.json())).has_status_code(status_code)

        # Extract response body
        return put_resp.json()

    def patch(self, path: str, body, status_code: int = 200):
        # Do call
        patch_resp = patch(self.service_base_url + path, headers=self.auth, data=body)

        # Verify expected status code
        assert_that(patch_resp, readable_json(patch_resp.json())).has_status_code(status_code)

        # Extract response body
        return patch_resp.json()

    def delete(self, path: str, status_code: int = 204):
        # Do call
        delete_resp = delete(self.service_base_url + path, headers=self.auth)

        # Verify expected status code
        assert_that(delete_resp).has_status_code(status_code)
