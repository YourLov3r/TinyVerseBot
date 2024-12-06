import asyncio
import sys

from bot.utils.logger import user_logger
from bot.utils.launcher import process


async def main():
    await process()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        user_logger.warning("Bot stopped")
        sys.exit()
