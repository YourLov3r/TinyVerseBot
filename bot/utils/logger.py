import logging
import logging.handlers
import sys
import time

import colorlog

logging.Formatter.converter = time.localtime

logger = logging.getLogger("user_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

file_handler_user = logging.handlers.RotatingFileHandler(
    "logs/user_logs.log",
    mode="a",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler_user.setLevel(logging.INFO)

user_console_formatter = colorlog.ColoredFormatter(
    "%(bold_white)s%(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | %(bold_white)s%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    style="%",
)

user_file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler.setFormatter(user_console_formatter)
file_handler_user.setFormatter(user_file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler_user)

dev_logger = logging.getLogger("dev_logger")
dev_logger.setLevel(logging.DEBUG)

file_handler_dev = logging.handlers.RotatingFileHandler(
    "logs/dev_logs.log",
    mode="a",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler_dev.setLevel(logging.DEBUG)

dev_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s | Line %(lineno)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler_dev.setFormatter(dev_formatter)

dev_logger.addHandler(file_handler_dev)
