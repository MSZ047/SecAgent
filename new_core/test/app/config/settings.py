import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    minimax_group_id: str = ""
    minimax_api_key: str = ""
    # lancedb_path: str = "./data/lancedb"
    wiki_path: str = "./llmWiki/experiences"
    # pinchtab_host: str = "http://localhost:9867"
    model_config = SettingsConfigDict(env_file =".env",env_file_encoding="utf-8")
settings = Settings()