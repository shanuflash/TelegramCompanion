import asyncio
import os
import time

import asyncssh
from telethon import events

from tg_userbot import (ENABLE_SSH, SSH_HOSTNAME, SSH_KEY, SSH_PASSPHRASE,
                        SSH_PASSWORD, SSH_PORT, SSH_USERNAME, client)
from tg_userbot.utils.decorators import log_exception


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.term (.+)"))
@log_exception
async def terminal(e):

    cmd = e.pattern_match.group(1)

    await e.edit("`Connecting..`")

    start_time = time.time() + 10
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**Output:**\n"

    if cmd in ("ls", "cat"):
        stdout, stderr = await process.communicate()

        if len(OUTPUT) > 4096:
            await e.reply(f"{OUTPUT}\n__Process killed:__ `Messasge too long`")
            return

        await e.edit(f"{OUTPUT}`{stdout.decode()}`")
        return

    while process:
        if time.time() > start_time:
            await e.edit(f"{OUTPUT}\n__Process killed__: `Time limit reached`")
            break

        stdout = await process.stdout.readline()

        if not stdout:
            _, stderr = await process.communicate()
            if stderr.decode():
                OUTPUT += f"`{stderr.decode()}`"
                await e.edit(OUTPUT)
                break

        if stdout:
            OUTPUT += f"`{stdout.decode()}`"

        if len(OUTPUT) > 4096:
            await e.reply(f"{OUTPUT}\n__Process killed:__ `Messasge too long`")
            break
        try:
            await e.edit(OUTPUT)
        except Exception:
            break


@client.on(
    events.NewMessage(outgoing=True,
                      func=lambda x: ENABLE_SSH,
                      pattern="^\.rterm (.+)")
)
@log_exception
async def ssh_terminal(e):
    cmd = e.pattern_match.group(1)
    OUTPUT = f"**Query:**\n`{cmd}`\n\n**Output:**\n"
    await e.edit("`Connecting..`")

    async with asyncssh.connect(
        str(SSH_HOSTNAME),
        port=int(SSH_PORT),
        username=str(SSH_USERNAME),
        password=str(SSH_PASSWORD),
        passphrase=str(SSH_PASSPHRASE),
        client_keys=SSH_KEY,
        known_hosts=None,
    ) as conn:

        start_time = time.time() + 10
        async with conn.create_process(cmd) as process:
            if cmd in ("ls", "cat"):
                stdout, stderr = await process.communicate()
                if not stdout:
                    await e.edit(f"{OUTPUT}`{stderr}`")
                    return
                if len(OUTPUT) > 4096:
                    await e.reply("__Process killed:__ `Messasge too long`")
                    return
                await e.edit(f"{OUTPUT}`{stdout}`")
                return

            while True:
                if time.time() > start_time:
                    break

                stdout = await process.stdout.readline()

                if not stdout:
                    _, stderr = await process.communicate()
                    if stderr:
                        OUTPUT += f"`{stderr}`"
                        await e.edit(OUTPUT)
                        break

                if stdout:
                    OUTPUT += f"`{stdout}`"

                if len(OUTPUT) > 4096:
                    await e.reply("__Process killed:__ `Messasge too long`")
                    break
                try:
                    await e.edit(OUTPUT)
                except Exception:
                    break


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.upload (.+)"))
@log_exception
async def upload_file(e):
    to_upload = e.pattern_match.group(1)
    chat = await e.get_chat()

    if os.path.exists(to_upload):
        try:
            await client.send_file(chat.id, file=to_upload)
            await e.delete()
        except Exception:
            await e.edit(f"__Upload Failed__: {to_upload}")
    else:
        await e.edit(f"__File Not Found__: `{to_upload}`")


@client.on(events.NewMessage(outgoing=True, pattern=r"^\.rupload (.+)"))
@log_exception
async def ssh_upload_file(e):
    to_upload = e.pattern_match.group(1)
    chat = await e.get_chat()
    await e.edit("`Connecting...`")

    async with asyncssh.connect(
            str(SSH_HOSTNAME),
            port=int(SSH_PORT),
            username=str(SSH_USERNAME),
            password=str(SSH_PASSWORD),
            passphrase=str(SSH_PASSPHRASE),
            client_keys=SSH_KEY,
            known_hosts=None) as conn:

        async with conn.create_process(f"test -f {to_upload} && echo 1") as process:
            stdout, _ = await process.communicate()
            if stdout:
                async with conn.start_sftp_client() as ftp:
                    await e.edit("`Downloading...`")
                    await ftp.get(to_upload, to_upload)
                    await e.edit("`Uploading...`")
                    try:
                        await client.send_file(chat.id, file=to_upload)
                    except Exception as exc:
                        await e.edit(f"__Upload Failed__: {to_upload}")
                os.remove(to_upload)
                await e.delete()
            else:
                await e.edit(f"__File Not Found__: `{to_upload}`")
