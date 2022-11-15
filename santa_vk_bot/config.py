from typing import Optional
from pydantic import BaseSettings


class BotSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    vk_bot_token: str
    vk_api_version: str
    vk_group_id: int
    vk_service_token: Optional[str]
    creator_id: Optional[int]
    error_receiver_id: Optional[int]

    class Config:
        env_file = ".env"


settings = BotSettings()
