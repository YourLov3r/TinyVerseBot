import asyncio
import sys

from bot.utils.logger import logger
from bot.utils.launcher import process


async def main():
    await process()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped")
        sys.exit()
