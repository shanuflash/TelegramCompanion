from ._version import __version__
from telethon import TelegramClient, sync
from argparse import ArgumentParser
import socks
import sys
import os
import logging
import dotenv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

parser = ArgumentParser()
parser.add_argument('--host', help='a valid host')
parser.add_argument('--port', help='a valid port')

args = parser.parse_args()
host = args.host
port = args.port
proxy = None

dotenv.load_dotenv('config.env')

APP_ID = os.environ.get('APP_ID', None)
APP_HASH = os.environ.get('APP_HASH', None)
DB_URI = os.environ.get('DB_URI', None)
BLOCK_PM = os.environ.get('BLOCK_PM', False)

DISABLED = []
if not DB_URI:
    DISABLED.append('notes')

if host and port:
    proxy = (socks.SOCKS5, host, int(port))

version = f'{__version__.major}.{__version__.minor}.{__version__.micro}'

client = TelegramClient('tg_userbot', APP_ID, APP_HASH, proxy=proxy, app_version=version)

