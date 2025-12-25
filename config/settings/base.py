from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).parent.parent.parent / ".env"

class Settings(BaseSettings):
    CAPTION: str
    SECRET_KEY: str
    DEBUG: bool = False

    TOKEN_ALGORITHM: str = "HS256"
    AUTH_SESSION_EXPIRES_SECONDS: int = 3600

    CRONTAB_PATH: Path = Path("/etc/crontab")
    CRON_SCRIPTS_DIR: Path = Path("/etc/cronjobs")

    # ZPool command timeout settings (in seconds)
    # Configurable timeouts for different zpool operations
    ZPOOL_TIMEOUTS: dict[str, int] = {
        'default': 30,          # Default timeout for basic operations
        'list': 30,             # zpool list operations
        'status': 30,           # zpool status operations
        'iostat': 45,           # zpool iostat operations (with sampling)
        'scrub': 30,            # Starting/stopping scrub operations
        'import': 120,          # zpool import operations
        'export': 120,          # zpool export operations
        'create': 180,          # zpool create operations
        'destroy': 120,         # zpool destroy operations
        'history': 60,          # zpool history operations
        'events': 30,           # zpool events operations
        'properties': 30,       # zpool get/set property operations
    }

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="allow")
