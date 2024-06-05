from random import randint


def gen_rand_email(name_len: int = 8) -> str:
    """Generates a new email consisting of given length."""
    char_selection = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    new_name = ''
    for digit in range(name_len):
        rand_ind = randint(0, len(char_selection) - 1)
        new_name += str(char_selection[rand_ind])

    return f'{new_name}@random.com'
