from typing import List

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict



class BotSettings(BaseModel):
    token: SecretStr
    required_chats: List[int]
    chat_link: str
    admin_ids: List[int]


class Settings(BaseSettings):
    database_url: SecretStr
    log_level: str = "DEBUG"

    bot: BotSettings
    
    
    model_config = SettingsConfigDict(
        env_file='.secrets.toml',
        env_file_encoding="utf-8",
        env_prefix="ENV_",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()

