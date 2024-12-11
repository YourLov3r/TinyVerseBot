import asyncio
import random
import re
import sys
import traceback
from datetime import datetime
from typing import Dict, List, NoReturn

import aiohttp
from aiohttp_socks import ProxyConnector
from pyrogram.client import Client

from bot.config.app_config import app_settings
from bot.config.config import settings
from bot.core.services.safety_manager import SafetyManager, SafetyManagerInterface
from bot.core.tg_mini_app_auth import TelegramMiniAppAuth
from bot.utils.json_manager import JsonManager
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
        self.json_manager = JsonManager()
        if settings.USE_REF:
            self.ref_id = settings.REF_ID.split("-")[1]

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

        def create_headers(
            additional_headers: Dict[str, str] | None = None,
            delete_headers: List[str] | None = None,
        ) -> Dict[str, str]:
            headers = base_headers.copy()
            if additional_headers:
                headers.update(additional_headers)
            if delete_headers:
                for header in delete_headers:
                    headers.pop(header, None)
            return headers

        return {
            "tinyverse": create_headers(
                {
                    "Origin": app_settings.urls.BASE_APP_DOMAIN,
                    "X-Application-Version": "",
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

        for headers_name, headers in self._headers.items():
            headers["User-Agent"] = self.user_agent
            headers["Sec-Ch-Ua"] = sec_ch_ua
            headers["Sec-Ch-Ua-Mobile"] = sec_ch_ua_mobile
            headers["Sec-Ch-Ua-Platform"] = sec_ch_ua_platform

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

        if settings.CHECK_BOT_STATE:
            bot_state = await session.get(
                "https://raw.githubusercontent.com/YourLov3r/TinyVerseBot/refs/heads/master/bot_state"
            )
            bot_state.raise_for_status()

            if await bot_state.text() != "running":
                user_logger.critical("Admins have stopped the bot!")
                sys.exit(1)

        if not await self.safety_manager.check_safety(session):
            user_logger.critical(f"{self.session_name} | Safety check failed")
            sys.exit(1)

        self.current_tverse_version = self.safety_manager.get_current_tverse_version
        if not self.current_tverse_version:
            raise ValueError(f"{self.session_name} | Cannot get current tverse version")

        tg_mini_app_auth = TelegramMiniAppAuth(self.telegram_client, proxy=self.proxy)
        tg_auth_app_data = await tg_mini_app_auth.get_telegram_web_data(
            "tverse", "tverse", settings.REF_ID if settings.USE_REF else None
        )

        self._headers["tinyverse"]["X-Application-Version"] = (
            self.current_tverse_version
        )

        await self._get_config(session)
        await self._get_lang(session)
        await self._get_boost(session)

        self._tverse_session = await self._get_tverse_session()
        if not self._tverse_session:
            await self._login(session, tg_auth_app_data["init_data"])
        else:
            await self._get_info(session)
            user_logger.info(
                f"{self.session_name} | Successfully logged in | Dust amount: {self._user_info.get("dust")}"
            )

        await self._get_galaxy(session)

        is_journey_started = self._user_info.get("galaxy") > 0
        if not is_journey_started:
            await asyncio.sleep(random.uniform(2, 4))
            await self._begin_journey(session)
            await self._get_info(session)
            await self._get_galaxy(session, go_to_home_galaxy=True)

        if is_journey_started:
            await self._get_galaxy(session, go_to_home_galaxy=True)

        if settings.CLAIM_DUST:
            if self._user_info.get("dust_progress") == 1:
                await asyncio.sleep(random.uniform(1, 2))
                await self._collect_dust(session)
                await self._get_info(session)
            else:
                dust_progress = round(self._user_info.get("dust_progress") * 100, 2)
                user_logger.info(
                    f"{self.session_name} | No dust to collect | Current progress: {dust_progress}%"
                )

    async def _login(self, session: aiohttp.ClientSession, init_data: str):
        form_data = {"bot_id": 7631205793, "data": init_data}
        response = await session.post(
            app_settings.urls.BASE_API_DOMAIN + app_settings.urls.AUTH_ENDPOINT,
            data=form_data,
            headers=self._headers["tinyverse"],
        )
        response.raise_for_status()

        response_json = await response.json()
        self._user_info = response_json.get("response", {})
        self._tverse_session = response_json.get("response", {}).get("session")

        if not self._tverse_session:
            raise Exception(f"{self.session_name} | Failed to get user session")

        self.json_manager.update_account(
            session_name=self.session_name,
            tverse_session=self._tverse_session,
        )

        user_logger.info(
            f"{self.session_name} | Successfully logged in | Dust amount: {self._user_info.get("dust")}"
        )

    async def _get_tverse_session(self) -> str | None:
        account_data = self.json_manager.get_account_by_session_name(self.session_name)
        if account_data is not None:
            return account_data.get("tverse_session")
        raise Exception(
            f"{self.session_name} | Can't find session: {self.session_name} in accounts.json"
        )

    async def _get_config(self, session: aiohttp.ClientSession) -> None:
        try:
            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN + app_settings.urls.CONFIG_ENDPOINT,
                data={"env": "app"},
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()

        except Exception:
            raise Exception(f"{self.session_name} | Failed to get config")

    async def _get_lang(self, session: aiohttp.ClientSession) -> None:
        try:
            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN + app_settings.urls.LANG_ENDPOINT,
                data={},
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()

        except Exception:
            raise Exception(f"{self.session_name} | Failed to get lang")

    async def _get_boost(self, session: aiohttp.ClientSession) -> None:
        try:
            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN + app_settings.urls.BOOST_ENDPOINT,
                data={},
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()

        except Exception:
            raise Exception(f"{self.session_name} | Failed to get boosts")

    async def _get_info(self, session: aiohttp.ClientSession) -> None:
        try:
            form_data = {"session": self._tverse_session, "id": "undefined"}
            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN + app_settings.urls.INFO_ENDPOINT,
                data=form_data,
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()
            response_json = await response.json()
            self._user_info = response_json.get("response", {})

        except Exception:
            raise Exception(f"{self.session_name} | Failed to get info")

    async def _get_galaxy(
        self,
        session: aiohttp.ClientSession,
        go_to_home_galaxy: bool = False,
    ) -> None:
        try:
            form_payload = {
                "session": self._tverse_session,
                "member_id": "null",
            }
            if settings.USE_REF and not go_to_home_galaxy:
                form_payload["id"] = self.ref_id

            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN
                + app_settings.urls.GET_GALAXY_PREVIEW_ENDPOINT,
                data=form_payload,
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()

        except Exception:
            raise Exception(
                f"{self.session_name} | Failed to get galaxy"
            )  # failed to get get

    async def _begin_journey(self, session: aiohttp.ClientSession) -> None:
        try:
            form_payload = {
                "session": self._tverse_session,
                "stars": 100,
                "referral": "",
            }
            if settings.USE_REF:
                form_payload["referral"] = settings.REF_ID.split("-")[1]

            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN + app_settings.urls.BEGIN_ENDPOINT,
                data=form_payload,
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()

            user_logger.info(f"{self.session_name} | Journey has begun")
        except Exception:
            raise Exception(f"{self.session_name} | Failed to begin journey")

    async def _collect_dust(self, session: aiohttp.ClientSession) -> None:
        try:
            response = await session.post(
                app_settings.urls.BASE_API_DOMAIN
                + app_settings.urls.COLLECT_DUST_ENDPOINT,
                data={"session": self._tverse_session},
                headers=self._headers["tinyverse"],
            )
            response.raise_for_status()
            response_json = await response.json()

            user_logger.info(
                f"{self.session_name} | Successfully collected {response_json.get("response").get("dust")} dust"
            )

        except Exception:
            raise Exception(f"{self.session_name} | Failed to collect dust")

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
