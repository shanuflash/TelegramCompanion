import os
import re
import time

import platform
import requests
import telethon
import zipfile
import io
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

from tg_userbot import client
from tg_userbot.modules.rextester.api import CompilerError, Rextester
from tg_userbot.utils.decorators import log_exception
from tg_userbot.modules.sql import stats_sql as sql
from telethon.tl.types import User
from .._version import __version__


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.ping"))
@log_exception
async def ping(e):
    start_time = time.time()
    requests.get("https://api.telegram.org")
    end_time = time.time()
    ping_time = float(end_time - start_time) * 1000
    await e.edit(f"Ping time was: {ping_time}ms")


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.version"))
@log_exception
async def version(e):
    bot_version = __version__.public()
    python_version = platform.python_version()
    telethon_version = telethon.__version__

    await e.edit(f"__Bot Version__ = `{bot_version}`\n\n__Python Version__ = `{python_version}`\n\n__Telethon Version__ = {telethon_version}")


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.info"))
@log_exception
async def user_info(e):
    message = e.message
    user = await e.get_sender()
    chat = await e.get_chat()

    if e.reply_to_msg_id:
        message = await e.get_reply_message()
        user = await message.get_sender()

    if len(e.text.split()) > 1:
        user = e.text.split()[1]
        try:
            user = await client.get_entity(user)
        except Exception as exc:
            await e.reply(str(exc))
            return

        if not isinstance(user, User):
            await e.reply(f"`{user}` is not a User")
            return

    full_user = await client(GetFullUserRequest(user.id))
    firstName = full_user.user.first_name
    lastName = full_user.user.last_name
    username = full_user.user.username
    user_id = full_user.user.id
    common_chats = full_user.common_chats_count

    REPLY = "**User Info:**\n"

    REPLY += f"\nFirst Name: {firstName}"

    if lastName:
        REPLY += f"\nLast Name: {lastName}"
    if username:
        REPLY += f"\nUsername: @{username}"
    REPLY += f"\nPermanent user link: [link](tg://user?id={user_id})"
    if full_user.about:
        REPLY += f"\n\n**About User:**\n{full_user.about}"
    if not full_user.user.is_self:
        REPLY += f"\n\nYou have `{common_chats}` chats in common with this user"

    await client.send_message(
        chat.id, REPLY, reply_to=message.id, link_preview=True, file=full_user.profile_photo
    )


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.stats"))
@log_exception
async def show_stats(e):
    stats = sql.get_stats()
    if stats:
        updatetime, totaldialogs, usercount, channelcount, supcount, convertedgroups, numchannel, numuser, numdeleted, numbot, numchat, numsuper = (
            stats
        )

        if convertedgroups != 0:
            if convertedgroups != numsuper:
                convertedgroups = convertedgroups
            else:
                convertedgroups = "all"
        else:
            convertedgroups = ""

        REPLY = f"""

    **\nMESSAGES COUNTS:**
    Normal groups and chats: `{usercount}`
    Channels: `{channelcount}`
    Supergroups: `{supcount}`
    TOTAL MESSAGES: `{totaldialogs}`

    **\nCHAT COUNTS:**
    Number of Channels: `{numchannel}`
    Number of Supergroups: `{numsuper}` from where `{convertedgroups}` of them converted from normal groups.
    Number of Normal groups: `{numchat}`
    Number of Private conversations: `{numuser}` from where `{numdeleted}` are now Deleted Accounts.
    Number of Bot conversations:  `{numbot}`
    Last Update Time :  `{updatetime} `
    """

        await e.edit(REPLY)
    else:
        await e.edit("`Stats are unavailable `.")


@client.on(events.NewMessage(outgoing=True, pattern=r"^\$"))
@log_exception
async def rextestercli(e):
    stdin = ""
    message = e.text
    chat = await e.get_chat()

    if len(message.split()) > 1:
        regex = re.search(
            r"^\$([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$",
            message,
            re.IGNORECASE,
        )
        language = regex.group(1)
        code = regex.group(2)
        stdin = regex.group(3)

        try:
            regexter = Rextester(language, code, stdin)
        except CompilerError as exc:
            await e.edit(str(exc))
            return

        output = ""
        output += f"**Language:**\n```{language}```"
        output += f"\n\n**Source:** \n```{code}```"

        if regexter.result:
            output += f"\n\n**Result:** \n```{regexter.result}```"

        if regexter.warnings:
            output += f"\n\n**Warnings:** \n```{regexter.warnings}```\n"

        if regexter.errors:
            output += f"\n\n**Errors:** \n'```{regexter.errors}```"

        if len(regexter.result) > 4096:
            with io.BytesIO(str.encode(regexter.result)) as out_file:
                out_file.name = "result.txt"
                await client.send_file(chat.id, file = out_file)
                await e.edit(code)
            return

        await e.edit(output)


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.sendlog"))
@log_exception
async def send_logs(e):

    if os.path.exists("logs/"):

        files_in_dir = os.listdir("logs/")
        chat = await e.get_chat()

        if len(files_in_dir) == 1:
            print(files_in_dir[0])
            await client.send_file(chat.id, file=f"logs/{files_in_dir[0]}", allow_cache=False)
            await e.delete()
            return

        elif len(files_in_dir) > 1:
            with io.BytesIO() as memzip:
                with zipfile.ZipFile(memzip, mode="w") as zf:
                    for logfile in files_in_dir:
                        zf.write(f"logs/{logfile}")
                memzip.seek(0)
                memzip.name = "Logs.zip"
                await client.send_file(chat.id, file=memzip, allow_cache=False)
                await e.delete()
    else:
        await e.edit("There are no logs to send")
