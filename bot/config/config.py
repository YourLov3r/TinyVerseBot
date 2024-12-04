from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    PLAY_INTRO: bool = True
    INITIAL_START_DELAY_SECONDS: list[int] = [10, 240]  # in seconds

    USE_REF: bool = True
    REF_ID: str = "galaxy-0005d76d760001b8ba230005eb9f2e"


settings = Settings()  # type: ignore
