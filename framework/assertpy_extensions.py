from assertpy.assertpy import AssertionBuilder
from assertpy import assert_that, add_extension


def extract_key(self, key: str) -> AssertionBuilder:
    """
    Extracts given key from assertion object.
    Reports if key is missing.
    """
    # Verify given json key exists
    assert_that(self.val).contains_key(key)

    # Retrieve json key
    self.val = self.val[key]

    return self


# Make custom extension available to all tests
add_extension(extract_key)
