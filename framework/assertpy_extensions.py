from assertpy import assert_that


def extract_key(self, key):
    """
    Extracts given key from assertion object.
    Reports if key is missing.
    """
    # Verify given json key exists
    assert_that(self.val).contains_key(key)

    # Retrieve json key
    self.val = self.val[key]

    return self
