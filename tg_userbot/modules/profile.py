import io
import os
import re

from telethon import events
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

from tg_userbot import client
from tg_userbot.utils.decorators import log_exception


@client.on(events.NewMessage(outgoing=True, pattern="^\.ppic"))
@log_exception
async def update_profile_pic(e):
    if e.reply_to_msg_id:
        message = await e.get_reply_message()
        photo = None
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                await e.edit("`DOWNLOADING`")
                photo = await client.download_media(message.photo)

            elif isinstance(message.media, MessageMediaDocument):
                mime_type = message.media.document.mime_type.split("/")
                media_type = mime_type[0]
                media_ext = mime_type[1]

                if media_type == "image":
                    await e.edit("`DOWNLOADING`")
                    photo = await client.download_file(message.media.document)
                    photo = io.BytesIO(photo)
                    photo.name = "image." + media_ext

            else:
                await e.edit("`The type of this media entity is invalid.`")

        if photo:
            await e.edit("`UPLOADING`")
            file = await client.upload_file(photo)
            try:
                await client(UploadProfilePhotoRequest(file))
                await e.edit("`Profile picture changed`")

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await e.edit("`The image is too small`")
                if isinstance(exc, ImageProcessFailedError):
                    await e.edit("`Failure while processing the image`")

            if isinstance(photo, str):
                os.remove(photo)


@client.on(events.NewMessage(outgoing=True, pattern="^\.pbio (.+)"))
@log_exception
async def update_profile_bio(e):
    bio = e.pattern_match.group(1)
    if len(bio) > 70:
        await e.edit("`Your bio is too long.`")
    else:
        await client(UpdateProfileRequest(about=bio))
        await e.edit("`Succesfully changed your bio`")


@client.on(events.NewMessage(outgoing=True, pattern="^\.puname (.+)"))
@log_exception
async def change_profile_username(e):
    username = e.pattern_match.group(1)

    if "@" in username:
        username = username[1:]

    allowed_char = re.match(r"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", username)

    if not allowed_char:
        await e.edit("`Invalid Username`")

    elif len(username) > 30:
        await e.edit("`Your username is too long.`")

    elif len(username) < 5:
        await e.edit("`Your username is too short`")

    else:
        try:
            await client(UpdateUsernameRequest(username))
            await e.edit("`Succesfully changed your username`")

        except UsernameOccupiedError:
            await e.edit(f"`{username} is already taken`")


@client.on(events.NewMessage(outgoing=True, pattern="^\.pname (.+)"))
@log_exception
async def change_profile_name(e):
    name = e.pattern_match.group(1)
    firstName = name.split("\\n", 1)[0]
    lastName = " "

    if "\\n" in name:
        lastName = name.split("\\n", 1)[1]

    await client(UpdateProfileRequest(first_name=firstName, last_name=lastName))
    await e.edit("`Succesfully changed your name`")
