from tg_userbot import client
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest


@client.on(events.NewMessage(outgoing=True, pattern="^\.info"))
async def user_info(e):
    user = await e.get_sender()
    if e.reply_to_msg_id:
        message = await e.get_reply_message()
        user = await message.get_sender()

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
        REPLY += "\n\nYou have `{}` chats in common with this user".format(
            common_chats)

    await client.send_message(
        e.chat_id, REPLY, reply_to=e.id, link_preview=True, file=full_user.profile_photo
        )
