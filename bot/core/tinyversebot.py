import asyncio
import random
import re
import traceback
from datetime import datetime
from typing import Dict, NoReturn

import aiohttp
from aiohttp_socks import ProxyConnector
from pyrogram.client import Client

from bot.config.app_config import app_settings
from bot.config.config import settings
from bot.core.services.safety_manager import SafetyManager, SafetyManagerInterface
from bot.core.tg_mini_app_auth import TelegramMiniAppAuth
from bot.utils.logger import dev_logger, user_logger


class TinyVerseBot:
    RETRY_ITERATION_DELAY = 10 * 60  # 10 minutes
    RETRY_DELAY = 5  # 5 seconds

    def __init__(
        self,
        telegram_client: Client,
        user_agent: str,
        proxy: str | None,
        safety_manager: SafetyManagerInterface,
    ) -> None:
        self.telegram_client: Client = telegram_client
        self.session_name: str = telegram_client.name
        self.user_agent: str = user_agent
        self.proxy: str | None = proxy
        self._headers = self._create_headers()
        self.safety_manager = safety_manager

    def _create_headers(self) -> Dict[str, Dict[str, str]]:
        base_headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": app_settings.urls.BASE_APP_DOMAIN,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "",
            "X-Requested-With": "XMLHttpRequest",
        }

        def create_headers(additional_headers=None) -> Dict[str, str]:
            headers = base_headers.copy()
            if additional_headers:
                headers.update(additional_headers)
            return headers

        return {
            "tinyverse": create_headers(
                {
                    "Origin": app_settings.urls.BASE_APP_DOMAIN,
                    "X-Application-Version": "0.6.30",
                }
            ),
        }

    async def run(self) -> NoReturn:
        chromium_version = re.search(r"Chrome/([\d.]+)", self.user_agent)
        if not chromium_version:
            raise Exception("Chromium version not found in user agent.")
        self.chromium_version = chromium_version.group(1)

        sec_ch_ua = f'"Chromium";v="{chromium_version}", "Android WebView";v="{chromium_version}", "Not-A.Brand";v="99"'
        sec_ch_ua_mobile = "?1"
        sec_ch_ua_platform = '"Android"'

        for header in self._headers.values():
            header["User-Agent"] = self.user_agent
            header["Sec-Ch-Ua"] = sec_ch_ua
            header["Sec-Ch-Ua-Mobile"] = sec_ch_ua_mobile
            header["Sec-Ch-Ua-Platform"] = sec_ch_ua_platform

        self.proxy = self.proxy

        while True:
            try:
                proxy_connector = (
                    ProxyConnector().from_url(self.proxy) if self.proxy else None
                )
                async with aiohttp.ClientSession(
                    connector=proxy_connector, timeout=aiohttp.ClientTimeout(10)
                ) as session:
                    if self.proxy:
                        await self._proxy_checker(session, self.proxy)

                    next_iteration_sleep_time = await self._perform_tinyverse_actions(
                        session, self.telegram_client
                    )

                if not next_iteration_sleep_time:
                    minutes_to_sleep = random.randint(
                        settings.ITERATION_SLEEP_MINUTES[0],
                        settings.ITERATION_SLEEP_MINUTES[1],
                    )
                    sleep_time = minutes_to_sleep * 60
                    user_logger.info(
                        f"{self.session_name} | Sleeping for: {minutes_to_sleep // 60} hours and {minutes_to_sleep % 60} minutes"
                    )
                    await asyncio.sleep(sleep_time)
                else:
                    minutes_to_sleep = int((next_iteration_sleep_time % 3600) // 60)
                    seconds_to_sleep = int(next_iteration_sleep_time % 60)
                    user_logger.info(
                        f"{self.session_name} | Sleeping for: {minutes_to_sleep % 60} minutes and {seconds_to_sleep} seconds"
                    )
                    await asyncio.sleep(next_iteration_sleep_time)
            except Exception as error:
                handle_error(self.session_name, error)
                user_logger.info(
                    f"{self.session_name} | Retrying in {self.RETRY_ITERATION_DELAY} seconds"
                )
                await asyncio.sleep(self.RETRY_ITERATION_DELAY)

    async def _proxy_checker(self, session: aiohttp.ClientSession, proxy: str):
        try:
            response = await session.get(
                "https://ipinfo.io/json",
                timeout=aiohttp.ClientTimeout(10),
                ssl=settings.ENABLE_SSL,
            )
            response.raise_for_status()
            response_json = await response.json()
            ip = response_json.get("ip", "Not Found")
            country = response_json.get("country", "Not Found")

            user_logger.info(
                f"{self.session_name} | Proxy connected | IP: {ip} | Country: {country}"
            )
        except Exception:
            raise Exception(f"{self.session_name} | Proxy error | {proxy}")

    async def _perform_tinyverse_actions(
        self, session: aiohttp.ClientSession, client: Client
    ):
        if settings.SLEEP_AT_NIGHT:
            await self._handle_night_sleep()

        tg_mini_app_auth = TelegramMiniAppAuth(self.telegram_client, proxy=self.proxy)
        tg_auth_app_data = await tg_mini_app_auth.get_telegram_web_data(
            "tverse", "tverse", settings.REF_ID if settings.USE_REF else None
        )

        self._init_data = tg_auth_app_data["init_data"]

        if not await self.safety_manager.check_safety(session):
            raise Exception(f"{self.session_name} | Safety check failed")

        await self._login(session)

    async def _login(self, session: aiohttp.ClientSession):
        form_data = {"bot_id": 7631205793, "data": self._init_data}
        response = await session.post(
            app_settings.urls.BASE_API_DOMAIN + app_settings.urls.AUTH_ENDPOINT,
            data=form_data,
            headers=self._headers["tinyverse"],
        )
        response.raise_for_status()

        response_json = await response.json()
        self._user_info = response_json.get("response", {})
        self._user_session = response_json.get("response", {}).get("session")

        if not self._user_session:
            raise Exception(f"{self.session_name} | Failed to get user session")

        user_logger.info(
            f"{self.session_name} | Successfully logged in | Dust amount: {self._user_info.get("dust")}"
        )

    async def _handle_night_sleep(self) -> None:
        current_hour = datetime.now().hour
        start_night_time = random.randint(
            settings.NIGHT_START_HOURS[0], settings.NIGHT_START_HOURS[1]
        )
        end_night_time = random.randint(
            settings.NIGHT_END_HOURS[0], settings.NIGHT_END_HOURS[1]
        )

        is_night_time = (
            (start_night_time <= current_hour <= 23)
            or (0 <= current_hour <= end_night_time)
            if start_night_time > end_night_time
            else (start_night_time <= current_hour <= end_night_time)
        )

        if is_night_time:
            random_minutes_to_sleep_time = random.randint(
                settings.ADDITIONAL_NIGHT_SLEEP_MINUTES[0],
                settings.ADDITIONAL_NIGHT_SLEEP_MINUTES[1],
            )

            sleep_time_in_hours = None

            if start_night_time <= current_hour <= 23:
                sleep_time_in_hours = 24 - current_hour + end_night_time
            elif 0 <= current_hour <= end_night_time:
                sleep_time_in_hours = end_night_time - current_hour
            else:
                return

            user_logger.info(
                f"{self.session_name} | It's night time. Sleeping for: {int(sleep_time_in_hours)} hours and {random_minutes_to_sleep_time} minutes"
            )

            await asyncio.sleep(
                (sleep_time_in_hours * 60 * 60) + (random_minutes_to_sleep_time * 60)
            )


def handle_error(session_name, error: Exception) -> None:
    user_logger.error(
        f"{error.__str__() if error else 'TinyVerseBot | Something went wrong'}"
    )
    dev_logger.error(f"{session_name} | {traceback.format_exc()}")


async def run_bot(
    telegram_client: Client,
    user_agent: str,
    proxy: str | None,
    start_delay: int,
) -> None:
    try:
        safety_manager = SafetyManager()
        bot = TinyVerseBot(
            telegram_client=telegram_client,
            user_agent=user_agent,
            proxy=proxy,
            safety_manager=safety_manager,
        )
        user_logger.info(f"{telegram_client.name} | Starting in {start_delay} seconds")
        await asyncio.sleep(start_delay)
        await bot.run()
    except Exception as error:
        handle_error(telegram_client.name, error)
    finally:
        if telegram_client.is_connected:
            await telegram_client.disconnect()

        user_logger.info(f"{telegram_client.name} | Stopped")
