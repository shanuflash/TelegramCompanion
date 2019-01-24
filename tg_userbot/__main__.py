import asyncio
import importlib

from tg_userbot import LOGGER, FORCE_SMS, client
from tg_userbot.modules import MODULES
from tg_userbot.modules.sql.stats_sql import GetStats

from . import proxy

for module_name in MODULES:
    imported_module = importlib.import_module("tg_userbot.modules." + module_name)

if proxy:
    LOGGER.info(f"Connecting to Telegram over proxy: {proxy[1]}:{proxy[2]}")
    LOGGER.info("Use .ping in any chat to see if your userbot has connected.")
else:
    LOGGER.info("Your userbot is running. Type .ping in any chat to test it")


if __name__ == "__main__":

    async def RunClient():
        await client.start(force_sms=FORCE_SMS)
        await client.get_me()
        await client.run_until_disconnected()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(RunClient())
