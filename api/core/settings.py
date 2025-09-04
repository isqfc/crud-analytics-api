from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    APP & Database Settings
    DATABASE_URL: database location
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    ACESS_TOKEN_EXPIRE_TIME: int
