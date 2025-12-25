from config.settings.base import Settings as BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "dummy"
    DEBUG: bool = True
