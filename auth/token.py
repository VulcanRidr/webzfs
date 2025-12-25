from datetime import datetime, timedelta

from jose import JWTError, jwt

from config.settings import settings


class InvalidToken(BaseException):
    pass


def create_token(username: str) -> str:
    exp = datetime.utcnow() + timedelta(seconds=settings.AUTH_SESSION_EXPIRES_SECONDS)
    token = jwt.encode(
        {"username": username, "exp": exp},
        key=settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )
    return token


def get_username_from_token(token: str) -> str:
    try:
        claims = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
        )
        return claims["username"]
    except (JWTError, KeyError):
        raise InvalidToken
