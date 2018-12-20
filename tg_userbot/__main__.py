import asyncio
import importlib
import time

import requests
from telethon import TelegramClient, events, sync

from tg_userbot import LOGGER, client
from tg_userbot.modules import MODULES

for module_name in MODULES:
    imported_module = importlib.import_module("tg_userbot.modules." + module_name)

LOGGER.info("Your userbot is running. Type .ping in any chat to test it")


@client.on(events.NewMessage(outgoing=True, pattern="^.ping"))
async def ping(e):
    start_time = time.time()
    requests.get("https://api.telegram.org")
    end_time = time.time()
    ping_time = float(end_time - start_time) * 1000
    await e.edit(f"Ping time was: {ping_time}ms")


if __name__ == "__main__":

    async def start():
        await client.start()
        await client.get_me()
        await client.run_until_disconnected()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
