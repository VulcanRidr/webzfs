import pam


def authenticate_user(username: str, password: str) -> bool:
    return pam.authenticate(username, password)
