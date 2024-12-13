from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    PLAY_INTRO: bool = True
    INITIAL_START_DELAY_SECONDS: list[int] = [10, 240]  # in seconds
    ITERATION_SLEEP_MINUTES: list[int] = [60, 120]  # in minutes
    ENABLE_SSL: bool = True

    SLEEP_AT_NIGHT: bool = True
    NIGHT_START_HOURS: list[int] = [0, 2]  # 24 hour format in your timezone
    NIGHT_END_HOURS: list[int] = [6, 8]  # 24 hour format in your timezone
    ADDITIONAL_NIGHT_SLEEP_MINUTES: list[int] = [2, 45]  # in minutes

    USE_REF: bool = True
    REF_ID: str = "galaxy-0005d76d760001b8ba230005eb9f2e"

    CHECK_BOT_STATE: bool = True
    CLAIM_DUST: bool = True
    ADD_STARS: bool = True


settings = Settings()  # type: ignore
