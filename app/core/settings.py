from dotenv import load_dotenv
from pathlib import Path

from pydantic import BaseModel, PostgresDsn, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR =Path(__file__).parent.parent

load_dotenv()


class FrontSettings(BaseModel):
    url: str
    templates_dir: Path = BASE_DIR / 'templates'
    secret_key: str

class AuthJWT(BaseModel):
    algorithm: str = 'RS256'
    access_token_lifetime_seconds: int = 3600
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'

class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

class RedisSettings(BaseModel):
    redis_host: str
    redis_port: int
    redis_db: int

    @property
    def redis_url(self):
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}'

class EmailSettings(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='APP__',
        env_nested_delimiter='__',
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore',
        populate_by_name=True
    )
    db: DbSettings
    email: EmailSettings 
    redis: RedisSettings 
    front: FrontSettings
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()