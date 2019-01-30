from argparse import ArgumentParser
import socks
import sys
import os
import logging
import dotenv
import re


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

parser = ArgumentParser()
parser.add_argument(
    "--config", help="Display all the config variables", action="store_true"
)

parser.add_argument("--install", help="Install any given plugin. Usage: --install <pluginname> or <user/repo/plugin_name>.")

CONFIG_VALUES = [
    "APP_ID         : Your telegram app id from https://my.telegram.org/apps",
    "APP_HASH       : Your telegram app hash from https://my.telegram.org/apps",
    "DB_URI         : Your postgress database url. Leave empty to disable the modules that use it",
    "DEBUG          : Set True if you want to generate log files from exceptions",
    "STATS_TIMER    : (optional) Update stats every x seconds. Default = 3600 seconds. Set to 0 to disable",
    "BLOCK_PM       : Set to True if you want to block new PMs. New PMs will be deleted and user blocked",
    "NOPM_SPAM      : Set to True if you want to block users that are spamming your PMs.",
    "PROXY_TYPE     : Your proxy type HTTP/SOCKS4/SOCKS5. Leave empty to disable proxy.",
    "HOST           : The host of the used proxy.",
    "PORT           : The port of the used proxy.",
    "USERNAME       : The username of the used proxy. (If any)",
    "PASSWORD       : The password of the used proxy. (If any)",
    "SESSION_NAME   : Custom session name. Leave empty to use the default session name",
    "ENABLE_SSH     : Set True if you want to execute/upload from a ssh server",
    "SSH_HOSTNAME   : SSH: (optional) The hostname or address to connect to.",
    "SSH_PORT       : SSH: (optional) The hostname or address to connect to.",
    "SSH_USERNAME   : SSH: (optional) Username to authenticate as on the server.",
    "SSH_PASSWORD   : SSH: (optional) The password to use for client password authentication",
    "SSH_PASSPHRASE : SSH: (optional) The passphrase for your ssh connection.",
    "SSH_KEY        : SSH: (optional) The private key which will be used to authenticate this client",
]

args = parser.parse_args()

TO_INSTALL = ""
if args.config:
    print("\n".join(CONFIG_VALUES))
    quit(1)
    
if args.install:
    TO_INSTALL = args.install


dotenv.load_dotenv("config.env")

APP_ID = os.environ.get("APP_ID", None)
APP_HASH = os.environ.get("APP_HASH", None)
SESSION_NAME = os.environ.get("SESSION_NAME", "tg_companion")
DB_URI = os.environ.get("DB_URI", None)
DEBUG = os.environ.get("DEBUG", False)

PROXY_TYPE = os.environ.get("PROXY_TYPE", None)
HOST = os.environ.get("HOST", None)
PORT = os.environ.get("PORT", None)
USERNAME = os.environ.get("USERNAME", None)
PASSWORD = os.environ.get("PASSWORD", None)

BLOCK_PM = os.environ.get("BLOCK_PM", False)
NOPM_SPAM = os.environ.get("NOPM_SPAM", False)
STATS_TIMER = int(os.environ.get("STATS_TIMER", 3600))

ENABLE_SSH = os.environ.get('ENABLE_SSH', False)
SSH_HOSTNAME = os.environ.get('SSH_HOSTNAME', '::1')
SSH_PORT = os.environ.get('SSH_PORT', 22)
SSH_USERNAME = os.environ.get('SSH_USERNAME', None)
SSH_PASSWORD = os.environ.get('SSH_PASSWORD', None)
SSH_PASSPHRASE = os.environ.get('SSH_PASSPHRASE', None)
SSH_KEY = os.environ.get('SSH_KEY', None)

proxy = None
proxy_type = None
proxy_addr = HOST
proxy_port = PORT
proxy_username = USERNAME
proxy_password = PASSWORD
if PROXY_TYPE:
    if PROXY_TYPE == "HTTP":
        porxy_type = socks.HTTP
    elif PROXY_TYPE == "SOCKS4":
        proxy_type = socks.SOCKS4
    elif PROXY_TYPE == "SOCKS5":
        proxy_type = socks.SOCKS5
    else:
        proxy_type = None

    proxy = (proxy_type, proxy_addr, int(proxy_port), False)
if USERNAME and PASSWORD:
    proxy = (
        proxy_type,
        proxy_addr,
        proxy_port,
        False,
        proxy_username,
        proxy_password)
