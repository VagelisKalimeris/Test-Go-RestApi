from enum import Enum
from datetime import date


class UserGender(Enum):
    """
    Restricts usage to allowed options.
    We can add any other genders supported.
    """
    male = 'male'
    female = 'female'


class UserStatus(Enum):
    """
    Restricts usage to allowed options.
    """
    active = 'active'
    inactive = 'inactive'


class TodoStatus(Enum):
    """
    Restricts usage to allowed options.
    """
    pending = 'pending'
    completed = 'completed'


class User:
    """
    Go Rest user model.
    """
    def __init__(self, email: str, gender: UserGender, name: str, status: UserStatus):
        self.email = email
        self.gender = gender
        self.name = name
        self.status = status


class Post:
    """
    Go Rest post model.
    """
    def __init__(self, user_id: int, title: str, body: str):
        self.user_id = user_id
        self.title = title
        self.body = body


class Comment:
    """
    Go Rest comment model.
    """
    def __init__(self, post_id: int, name: str, email: str, body: str):
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body


class Todo:
    """
    Go Rest to do model.
    """
    def __init__(self, user_id: int, title: str, due_on: str, status: str):
        self.user_id = user_id
        self.title = title
        self.due_on = due_on
        self.status = status
