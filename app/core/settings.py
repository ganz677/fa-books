from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR =Path(__file__).parent.parent


class AuthJWT(BaseModel):
    algorithm: str = 'RS256' 
    lifetime_seconds: int = 3600
    secret_key: str
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'

class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        env_prefix='APP__',
        case_sensitive=False,
        env_nested_delimiter="__" 
    )
    db: DbSettings
    jwt_token: AuthJWT

settings = Settings()

