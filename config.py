from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "secret_keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "secret_keys" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    COMMENTS_DB_HOST: str
    COMMENTS_DB_PORT: int
    COMMENTS_DB_USER: str
    COMMENTS_DB_PASS: str
    COMMENTS_DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return (f"postgresql+asyncpg://{self.COMMENTS_DB_USER}:"
                f"{self.COMMENTS_DB_PASS}@"
                f"{self.COMMENTS_DB_HOST}:"
                f"{self.COMMENTS_DB_PORT}/"
                f"{self.COMMENTS_DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
