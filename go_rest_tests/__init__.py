from assertpy import add_extension

from framework.assertpy_extensions import extract_key

# Make custom extension available to all tests
add_extension(extract_key)
