from assertpy import assert_that

from framework.response_util import readable_json


class TestAllResourcesCRUD:
    """
    User creation and deletion are tested by global fixtures.

    Retrieves resource & verifies:
        - Resource exists
        - Resource data are same
    Retrieves unfiltered resources & verifies:
        - Resource exists
        - Resource data are same
    Updates resource's info & verifies:
        - Expected response data
    Retrieves updated post & verifies:
        - Resource exists
        - Resource data are updated
    """
    def test_get_resource_by_id(self, go_rest_client, resource_path, resource_data, resource_id):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/{resource_path}/{resource_id}')

        # Verify GET response data is same as original
        assert_that(get_resp, readable_json(get_resp))\
            .is_equal_to(resource_data)

    def test_new_resource_is_vended_in_unfiltered_response(self, go_rest_client, resource_path, resource_data):
        # Retrieve unfiltered resources
        get_resp = go_rest_client.get(f'/{resource_path}/')

        # Verify new resource data is vended in GET unfiltered resources response
        assert_that(get_resp, readable_json(get_resp))\
            .contains(resource_data)

    def test_resource_update(self, go_rest_client, resource_path, resource_id, update_info):
        # Update new resource
        patch_resp = go_rest_client.patch(f'/{resource_path}/{resource_id}', update_info)

        # Verify resource was updated successfully
        assert_that(patch_resp, readable_json(patch_resp)) \
            .contains_entry(update_info)

    def test_retrieve_resource_after_update(self, go_rest_client, resource_path, valid_user_id, update_info):
        # Retrieve resource by id
        get_resp = go_rest_client.get(f'/{resource_path}/{valid_user_id}')

        # Verify GET response data is updated
        assert_that(get_resp, readable_json(get_resp))\
            .contains_entry(update_info)
