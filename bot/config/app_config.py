from pydantic import BaseModel

class UrlConfig(BaseModel):
    BASE_APP_DOMAIN: str = "https://app.tonverse.app"
    BASE_API_DOMAIN: str = "https://api.tonverse.app"
    APPJS_ENDPOINT: str = "/assets/js/app.js"
    AUTH_ENDPOINT: str = "/auth/telegram"


class AppSettings(BaseModel):
    urls: UrlConfig = UrlConfig()


app_settings = AppSettings()