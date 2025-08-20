import os
from enum import Enum
from typing import Self

from pydantic import HttpUrl, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"



class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    app_url: HttpUrl
    headless: bool
    browsers: list[Browser]

    videos_dir: DirectoryPath
    tracing_dir: DirectoryPath

    def get_base_url(self) -> str:
        return f"{self.app_url}"


    @classmethod
    def initialize(cls) -> Self:
        videos_dir = DirectoryPath("./videos")
        tracing_dir = DirectoryPath("./tracing")

        videos_dir.mkdir(exist_ok=True)
        tracing_dir.mkdir(exist_ok=True)

        return Settings(
            videos_dir=videos_dir,
            tracing_dir=tracing_dir
        )


settings = Settings.initialize()