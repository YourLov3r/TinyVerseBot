import asyncio
import sys
from typing import NoReturn

import aiohttp

from bot.utils.logger import user_logger


async def bot_state_checker() -> NoReturn:
    while True:
        async with aiohttp.ClientSession() as session:
            bot_state = await session.get(
                "https://raw.githubusercontent.com/YourLov3r/TinyVerseBot/refs/heads/master/bot_state"
            )
            bot_state.raise_for_status()

            if await bot_state.text() != "running":
                user_logger.critical("Admins have stopped the bot!")
                sys.exit(1)

        await asyncio.sleep(20 * 60)  # 20 minutes


def max_stars_to_add(total_dust: int, current_stars: int) -> int:
    if not total_dust or not current_stars:
        return 0

    max_cost_per_star = (total_dust * 70 + 1) // (current_stars + 1)

    max_total_stars = 100000 - current_stars

    maximum_stars = min(max_cost_per_star, max_total_stars)

    if maximum_stars >= 100:
        return maximum_stars
    else:
        return 0
