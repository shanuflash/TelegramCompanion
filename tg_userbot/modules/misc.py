import logging
import re
import time

import requests
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

from tg_userbot import client
from tg_userbot.modules.rextester.api import CompilerError, Rextester
from tg_userbot.modules.sql import stats_sql as sql
from telethon.tl.types import User
from .._version import __version__


@client.on(events.NewMessage(outgoing=True, pattern="^\.ping"))
async def ping(e):
    start_time = time.time()
    requests.get("https://api.telegram.org")
    end_time = time.time()
    ping_time = float(end_time - start_time) * 1000
    await e.edit(f"Ping time was: {ping_time}ms")


@client.on(events.NewMessage(outgoing=True, pattern="^\.version"))
async def version(e):
    await e.edit("Version: `{}`".format(__version__.public()))


@client.on(events.NewMessage(outgoing=True, pattern="^\.info"))
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
            await e.reply('`{}` is not a User'.format(user))
            return

    full_user = await client(GetFullUserRequest(user.id))
    firstName = full_user.user.first_name
    lastName = full_user.user.last_name
    username = full_user.user.username
    user_id = full_user.user.id
    common_chats = full_user.common_chats_count

    REPLY = "**User Info:**\n"

    REPLY += "\nFirst Name: {}".format(firstName)

    if lastName:
        REPLY += "\nLast Name: {}".format(lastName)
    if username:
        REPLY += "\nUsername: @{}".format(username)
    REPLY += "\nPermanent user link: [link](tg://user?id={})".format(user_id)
    if full_user.about:
        REPLY += "\n\n**About User:**\n{}".format(full_user.about)
    if not full_user.user.is_self:
        REPLY += "\n\nYou have `{}` chats in common with this user".format(common_chats)

    await client.send_message(
        chat.id, REPLY, reply_to=message.id, link_preview=True, file=full_user.profile_photo
    )


@client.on(events.NewMessage(outgoing=True, pattern="^\.stats"))
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

        REPLY = """

    **\nMESSAGES COUNTS:**
    Normal groups and chats: `{}`
    Channels: `{}`
    Supergroups: `{}`
    TOTAL MESSAGES: `{}`

    **\nCHAT COUNTS:**
    Number of Channels: `{}`
    Number of Supergroups: `{}` from where `{}` of them converted from normal groups.
    Number of Normal groups: `{}`
    Number of Private conversations: `{}` from where `{}` are now Deleted Accounts.
    Number of Bot conversations:  `{}`
    Last Update Time :  `{} `
        """.format(
            usercount,
            channelcount,
            supcount,
            totaldialogs,
            numchannel,
            numsuper,
            convertedgroups,
            numchat,
            numuser,
            numdeleted,
            numbot,
            updatetime,
        )
        await e.edit(REPLY)
    else:
        await e.edit("`Stats are unavailable `.")


@client.on(events.NewMessage(outgoing=True, pattern="^\$"))
async def rextestercli(e):
    stdin = ""
    message = e.text

    if len(message.split()) > 1:
        regex = re.search(
            "^\$([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$",
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
        output += "**Language:**\n```{}```".format(language)
        output += "\n\n**Source:** \n```{}```".format(code)

        if regexter.result:
            output += "\n\n**Result:** \n```{}```".format(regexter.result)

        if regexter.warnings:
            output += "\n\n**Warnings:** \n```{}```\n".format(regexter.warnings)

        if regexter.errors:
            output += "\n\n**Errors:** \n'```{}```".format(regexter.errors)

        await e.edit(output)
