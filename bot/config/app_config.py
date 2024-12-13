from pydantic import BaseModel


class UrlConfig(BaseModel):
    BASE_APP_DOMAIN: str = "https://app.tonverse.app"
    BASE_API_DOMAIN: str = "https://api.tonverse.app"
    APPJS_ENDPOINT: str = "/assets/js/app.js"
    AUTH_ENDPOINT: str = "/auth/telegram"

    CONFIG_ENDPOINT: str = "/config"
    LANG_ENDPOINT: str = "/data/lang"
    BOOST_ENDPOINT: str = "/data/boost"
    INFO_ENDPOINT: str = "/user/info"
    GET_GALAXY_PREVIEW_ENDPOINT: str = "/galaxy/get"
    BEGIN_ENDPOINT: str = "/galaxy/begin"
    COLLECT_DUST_ENDPOINT: str = "/galaxy/collect"
    USER_BOOSTS_ENDPOINT: str = "/user/boosts"
    CREATE_STARS_ENDPOINT: str = "/stars/create"


class AppSettings(BaseModel):
    urls: UrlConfig = UrlConfig()
    KNOWN_VERSION: str = "0.7.18"


app_settings = AppSettings()
