import requests
from telethon import events

from tg_userbot import client

URL = "https://api.github.com/users/"


@client.on(events.NewMessage(outgoing=True, pattern=r"\.github (\w*)"))
async def github(e):

    request = requests.get(URL + e.pattern_match.group(1))

    if request.status_code == 404:
        await e.reply("`" + e.pattern_match.group(1) + " not found`")
        return

    result = request.json()

    url = result.get("html_url", None)
    name = result.get("name", None)
    company = result.get("company", None)
    bio = result.get("bio", None)
    created_at = result.get("created_at", "Not Found")

    REPLY = f"""
    GitHub Info for `{e.pattern_match.group(1)}`

    Username: `{name}`
    Bio: `{bio}`
    URL: `{url}`
    Company: `{company}`
    Created at: `{created_at}`
    """

    request = requests.get(result.get("repos_url", None))
    if request.status_code == 404:
        await e.edit(REPLY)
        return

    result = request.json()
    chat = await e.get_chat()

    REPLY += "\nRepos: \n\n"

    for nr in range(len(result)):
        REPLY += f"  [{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

    await client.send_message(chat.id, message=REPLY, reply_to=e.id, link_preview=False)
