from httpx import get, post
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
