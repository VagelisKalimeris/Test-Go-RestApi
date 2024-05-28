from go_rest_tests.test_data.models import User, UserGender, UserStatus

valid_user = User('a@random.com', UserGender.male.value, 'John Doe', UserStatus.active.value)
