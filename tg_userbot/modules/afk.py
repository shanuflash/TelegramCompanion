from telethon import events

from tg_userbot.modules.sql import afk_sql as sql

from .. import client


@client.on(events.NewMessage(outgoing=True, pattern="^\.afk?(.+)"))
async def afk(e):
    reason = e.pattern_match.group(1)
    if len(reason) <= 2:
        reason = ""

    sql.set_afk(reason)
    await e.edit("`I will be afk for a while. I'll be back later`")


@client.on(events.NewMessage(outgoing=True))
async def no_afk(e):
    if ".afk" not in e.text:
        remove_afk = sql.rm_afk()
        if remove_afk:
            await client.send_message(e.chat_id, "`I'm no longer afk`")


@client.on(events.NewMessage(incoming=True))
async def reply_afk(e):
    if e.mentioned:
        if sql.is_afk():
            valid, reason = sql.check_afk()
            if valid:
                if not reason:
                    REPLY = "`I'm afk so please wait for me to reply`"
                else:
                    REPLY = "I'm afk because of: \n`{}``".format(reason)
                await client.send_message(e.chat_id, REPLY, reply_to=e.id)
