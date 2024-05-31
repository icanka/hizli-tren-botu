"""A simple bot for the Discord API."""

import logging


default_settings = {
    "LOG_LEVEL": logging.INFO,
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
    "LOG_FILE": "bot_data/logs/bot.log",
    "LOG_STREAM": True,
}
globals().update(default_settings)

__version__ = "0.0.1"
__author__ = "REMOVED_CARDHOLDER_NAME"
__license__ = "MIT"
