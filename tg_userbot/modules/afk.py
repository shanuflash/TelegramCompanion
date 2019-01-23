from telethon import events

from tg_userbot.modules.sql import afk_sql as sql
from tg_userbot import client
from tg_userbot.utils.decorators import log_exception

@client.on(events.NewMessage(outgoing=True, pattern="^\.afk?(.+)"))
@log_exception
async def afk(e):
    reason = e.pattern_match.group(1)
    if len(reason) <= 2:
        reason = ""

    sql.set_afk(reason)
    await e.edit("`I will be afk for a while. I'll be back later`")


@client.on(events.NewMessage(outgoing=True))
@log_exception
async def no_afk(e):
    chat = await e.get_chat()
    if ".afk" not in e.text:
        remove_afk = sql.rm_afk()
        if remove_afk:
            await client.send_message(chat.id, "`I'm no longer afk`")


@client.on(events.NewMessage(incoming=True))
@log_exception
async def reply_afk(e):
    chat = await e.get_chat()
    if e.mentioned or e.is_private:
        if sql.is_afk():
            valid, reason = sql.check_afk()
            if valid:
                if not reason:
                    REPLY = "`I'm afk so please wait for me to reply`"
                else:
                    REPLY = f"I'm afk because of: \n`{reason}`"
                await client.send_message(chat.id, REPLY, reply_to=e.id)
