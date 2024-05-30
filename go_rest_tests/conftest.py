import pytest
from assertpy import assert_that

from framework.go_rest_client import GoRestTestClient
from framework.response_util import readable_json
from go_rest_tests.test_data.models import User, UserGender, UserStatus, Post, Comment, Todo, TodoStatus
from go_rest_tests.test_data.user_emails import valid_user_email


pytest_plugins = ['framework.assertpy_extensions']


########################################################################################################################
#                                          Resource Creation & Deletion                                                #
########################################################################################################################
@pytest.fixture(scope='session')
def go_rest_client():
    """
    Provides test client instance to all module tests.
    """
    yield GoRestTestClient()


@pytest.fixture(scope='session', autouse=True)
def valid_user(go_rest_client):
    """
    Valid user for all tests to access and use.
    Created before and deleted after each run.

    Creates user & verifies:
        - Expected response data
    Deletes user & verifies:
        - Operation success
    Retrieves deleted user & verifies:
        - Operation failure
    """
    valid_user = User(valid_user_email, UserGender.male.value, 'John Doe', UserStatus.active.value)
    valid_user_dict = valid_user.__dict__

    # POST new user
    post_resp = go_rest_client.post('/users', valid_user_dict)

    # Create valid user & provide to later tests
    new_user_id = assert_that(post_resp, readable_json(post_resp)) \
        .is_equal_to(valid_user.__dict__, ignore='id') \
        .extract_key('id') \
        .val

    valid_user_dict['id'] = new_user_id

    yield valid_user_dict

    # DELETE new user
    go_rest_client.delete(f'/users/{new_user_id}')

    # GET deleted user by id & verify is absent
    go_rest_client.get(f'/users/{new_user_id}', 404)


@pytest.fixture(scope='session')
def valid_user_id(valid_user):
    """
    Abstracts repetitive user id retrieval.
    """
    return valid_user['id']


########################################################################################################################
@pytest.fixture(scope='session', autouse=True)
def valid_post(go_rest_client, valid_user_id):
    """
    Valid post for all tests to access and use.
    Created before and deleted after each run.

    Creates post & verifies:
        - Expected response data
    Deletes post & verifies:
        - Operation success
    Retrieves deleted post & verifies:
        - Operation failure
    """
    valid_post = Post(valid_user_id, 'My summer holidays!', 'I will have a great time.')
    valid_post_dict = valid_post.__dict__

    # POST new post
    post_resp = go_rest_client.post('/posts', valid_post_dict)

    # Create valid post & provide to later tests
    new_post_id = assert_that(post_resp, readable_json(post_resp)) \
        .is_equal_to(valid_post.__dict__, ignore='id') \
        .extract_key('id') \
        .val

    valid_post_dict['id'] = new_post_id

    yield valid_post_dict

    # DELETE new post
    go_rest_client.delete(f'/posts/{new_post_id}')

    # GET deleted post by id & verify is absent
    go_rest_client.get(f'/posts/{new_post_id}', 404)


@pytest.fixture(scope='session')
def valid_post_id(valid_post):
    """
    Abstracts repetitive post id retrieval.
    """
    return valid_post['id']


########################################################################################################################
@pytest.fixture(scope='session', autouse=True)
def valid_comment(go_rest_client, valid_post_id):
    """
    Valid comment for all tests to access and use.
    Created before and deleted after each run.

    Creates comment & verifies:
        - Expected response data
    Deletes comment & verifies:
        - Operation success
    Retrieves deleted comment & verifies:
        - Operation failure
    """
    valid_comment = Comment(valid_post_id, 'John Doe', valid_user_email, 'I liked this post.')
    valid_comment_dict = valid_comment.__dict__

    # POST new comment
    comment_resp = go_rest_client.post('/comments', valid_comment_dict)

    # Create valid comment & provide to later tests
    new_comment_id = assert_that(comment_resp, readable_json(comment_resp)) \
        .is_equal_to(valid_comment.__dict__, ignore='id') \
        .extract_key('id') \
        .val

    valid_comment_dict['id'] = new_comment_id

    yield valid_comment_dict

    # DELETE new comment
    go_rest_client.delete(f'/comments/{new_comment_id}')

    # GET deleted comment by id & verify is absent
    go_rest_client.get(f'/comments/{new_comment_id}', 404)


@pytest.fixture(scope='session')
def valid_comment_id(valid_comment):
    """
    Abstracts repetitive comment id retrieval.
    """
    return valid_comment['id']


########################################################################################################################
@pytest.fixture(scope='session', autouse=True)
def valid_todo(go_rest_client, valid_user_id):
    """
    Valid to do for all tests to access and use.
    Created before and deleted after each run.

    Creates to do & verifies:
        - Expected response data
    Deletes to do & verifies:
        - Operation success
    Retrieves deleted to do & verifies:
        - Operation failure
    """
    valid_todo = Todo(valid_user_id, 'Shopping List', '2024-06-08T00:00:00.000+05:30', TodoStatus.pending.value)
    valid_todo_dict = valid_todo.__dict__

    # POST new to do
    todo_resp = go_rest_client.post('/todos', valid_todo_dict)

    # Create valid to do & provide to later tests
    new_todo_id = assert_that(todo_resp, readable_json(todo_resp)) \
        .is_equal_to(valid_todo.__dict__, ignore='id') \
        .extract_key('id') \
        .val

    valid_todo_dict['id'] = new_todo_id

    yield valid_todo_dict

    # DELETE new to do
    go_rest_client.delete(f'/todos/{new_todo_id}')

    # GET deleted to do by id & verify is absent
    go_rest_client.get(f'/todos/{new_todo_id}', 404)


@pytest.fixture(scope='session')
def valid_todo_id(valid_todo):
    """
    Abstracts repetitive to do id retrieval.
    """
    return valid_todo['id']