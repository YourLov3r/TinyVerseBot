import re
from abc import ABC, abstractmethod
from typing import Dict

import aiohttp

from bot.config.app_config import app_settings
from bot.utils.logger import user_logger


class SafetyManagerInterface(ABC):
    @abstractmethod
    async def check_safety(self, session: aiohttp.ClientSession) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def get_current_tverse_version(self) -> str | None:
        raise NotImplementedError


class SafetyManager(SafetyManagerInterface):
    def __init__(self):
        self._headers = self._create_headers()
        self._known_tverse_version = app_settings.KNOWN_VERSION

    def _create_headers(self) -> Dict[str, Dict[str, str]]:
        base_headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": app_settings.urls.BASE_APP_DOMAIN,
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "",
            "X-Requested-With": "org.telegram.messenger.web",
        }

        def create_headers(additional_headers=None) -> Dict[str, str]:
            headers = base_headers.copy()
            if additional_headers:
                headers.update(additional_headers)
            return headers

        return {
            "appjs": create_headers(),
        }

    async def check_safety(self, session: aiohttp.ClientSession) -> bool:
        current_tverse_version = await self._get_current_version(session)
        if not current_tverse_version:
            user_logger.critical(
                "Safety Manager | It's not safety to run the script, cause we couldn't get the current version of tverse."
            )
            return False

        if current_tverse_version != self._known_tverse_version:
            user_logger.critical(
                f"Safety Manager | It's not safety to run script, cause TinyVerse version is not {self._known_tverse_version} but {current_tverse_version}"
            )
            return False

        self._current_tverse_version = current_tverse_version
        return True

    async def _get_current_version(self, session: aiohttp.ClientSession) -> str | None:
        response = await session.get(
            app_settings.urls.BASE_APP_DOMAIN + app_settings.urls.APPJS_ENDPOINT,
            headers=self._headers["appjs"],
        )
        response.raise_for_status()
        response_text = await response.text()

        match = re.search(r'version:"(\d+(\.\d+)*)"', response_text)
        if not match:
            return None

        version = match.group(1)
        return version

    @property
    def get_current_tverse_version(self) -> str | None:
        if not hasattr(self, "_current_tverse_version"):
            return None
        return self._current_tverse_version
