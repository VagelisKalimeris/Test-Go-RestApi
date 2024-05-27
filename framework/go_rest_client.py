from os import environ

from dotenv import load_dotenv

from framework.http_client import TestClient
from go_rest_tests.config import GO_REST_BASE_URL


class GoRestTestClient(TestClient):
    """
    Test client child class, for Go Rest API testing.
    """
    def __init__(self):
        super().__init__()
        # Define service url for current api
        self.service_base_url = GO_REST_BASE_URL

        # Retrieve secret test api token for current api
        load_dotenv()
        self.token = environ['GO_REST_TEST_KEY']

        # Setup authorization for current api
        self.auth = {
            'Authorization': f'Bearer {self.token}'
        }
