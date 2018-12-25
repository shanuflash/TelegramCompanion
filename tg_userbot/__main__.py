import asyncio
import importlib
import time

import requests
from telethon import events

from tg_userbot import LOGGER, client
from tg_userbot.modules import MODULES

from . import proxy
from ._version import __version__

for module_name in MODULES:
    imported_module = importlib.import_module("tg_userbot.modules." + module_name)

if proxy:
    LOGGER.info("Connecting to Telegram over proxy: {}:{}".format(proxy[1], proxy[2]))
    LOGGER.info("Use .ping in any chat to see if your userbot has connected.")
else:
    LOGGER.info("Your userbot is running. Type .ping in any chat to test it")

if __name__ == "__main__":

    async def start():
        await client.start()
        await client.get_me()
        await client.run_until_disconnected()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
