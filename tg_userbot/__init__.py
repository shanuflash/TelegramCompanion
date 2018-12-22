from ._version import __version__
from telethon import TelegramClient
from argparse import ArgumentParser
import socks
import sys
import os
import logging
import dotenv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ArgumentParser()
parser.add_argument("--host", help="A valid proxy host")
parser.add_argument("--port", help="A valid proxy port")
parser.add_argument(
    "--config", help="Display all the config variables", action="store_true"
)

args = parser.parse_args()
host = args.host
port = args.port
proxy = None

CONFIG_VALUES = [
    "APP_ID   : Your telegram app id from https://my.telegram.org/apps",
    "APP_HASH : Your telegram app hash from https://my.telegram.org/apps",
    "DB_URI   : Your postgress database url. Leave empty to disable the modules that use it",
    "BLOCK_PM : Set to True if you want to block new PMs. New PMs will be deleted and user blocked",
    "NOPM_SPAM : Set to True if you want to block users that are spamming your PMs.",
]

if args.config:
    print("\n".join(CONFIG_VALUES))
    quit(1)

dotenv.load_dotenv("config.env")

APP_ID = os.environ.get("APP_ID", None)
APP_HASH = os.environ.get("APP_HASH", None)
DB_URI = os.environ.get("DB_URI", None)
BLOCK_PM = os.environ.get("BLOCK_PM", False)
NOPM_SPAM = os.environ.get("NOPM_SPAM", False)

if host and port:
    proxy = (socks.SOCKS5, host, int(port))


client = TelegramClient(
    "tg_userbot", APP_ID, APP_HASH, proxy=proxy, app_version=__version__.public()
)
