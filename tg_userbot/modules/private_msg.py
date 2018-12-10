from tg_userbot import client
from telethon import events
from telethon.tl.functions.contacts import BlockRequest
from tg_userbot import BLOCK_PM

@client.on(events.NewMessage(incoming=True))
async def pm_ban(e):
    if BLOCK_PM:
        if e.is_private and not (await e.get_sender()).bot:
            await e.delete()
            await client(BlockRequest(e.chat_id))


