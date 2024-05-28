from json import dumps


def readable_json(resp):
    """
    Makes json responses humanly readable, for improved assertpy error reporting.
    """
    return dumps(resp, indent=4)
