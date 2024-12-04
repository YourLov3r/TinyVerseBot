import argparse

from bot.config.config import settings
from bot.core.registrator import register_sessions
from bot.utils.banner_animation import print_banner_animation
from bot.utils.logger import logger

options = """
1. Register session

"""


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    if settings.PLAY_INTRO:
        print_banner_animation()

    action = parser.parse_args().action

    if not action:
        print(options)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
                print(options)
            elif action not in ["1"]:
                logger.warning("Action must be 1")
                print(options)
            else:
                action = int(action)
                break

    if action == 1:
        while True:
            await register_sessions()

            answer = input("Do you want to register another session? [Y/n]: ")

            if not answer or answer.lower() == "y" or answer.lower() == "yes":
                continue

            break
