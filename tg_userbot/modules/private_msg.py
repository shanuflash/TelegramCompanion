from telethon import events
from telethon.tl.functions.contacts import BlockRequest

from tg_userbot import BLOCK_PM, NOPM_SPAM, client
from tg_userbot.modules.sql import pm_sql as sql

PM_WARNS = {}


@client.on(events.NewMessage(incoming=True))
async def pm_ban(e):
    chat = await e.get_chat()
    if BLOCK_PM is True:
        if e.is_private and not (await e.get_sender()).bot:
            await e.delete()
            await client(BlockRequest(chat.id))


@client.on(events.NewMessage(incoming=True, outgoing=True))
async def await_permission(e):
    global PM_WARNS
    if NOPM_SPAM is True and e.is_private:
        chat = await e.get_chat()
        chat = chat.id
        if e.out:
            sql.private_add(chat.id)
            try:
                del PM_WARNS[chat.id]
            except KeyError:
                pass

        elif not sql.private_in_db(chat.id) and PM_WARNS[chat.id != 4]:
            await client.send_message(
                chat.id,
                message="`Hi! This user will answer to your message soon. Please wait for his response and don't spam his PM. Thanks`",
            )
            if chat.id not in PM_WARNS:
                PM_WARNS.update({chat.id: 1})
            else:
                PM_WARNS[chat.id] += 1
                print(PM_WARNS)
            if PM_WARNS[chat.id] == 4:
                await client.send_message(
                    chat.id,
                    message="You are spamming this user. I will ban you until he decides to unban you. Thanks ",
                )
                await client(BlockRequest(chat.id))
