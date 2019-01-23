# Tg-UserBot

> Tg-UserBot is simple userbot for Telegram to make your time spent on telegram more enjoyable.

## Table of Contents

- [Instalation](#Instalation)
- [Setup](#Setup)
- [Features](#Features)
- [Contribuiting](#Contribuiting)
- [Suport](#Support)


## Instalation

- Install python3.7 and python3.7-dev. python3.6 and python3-dev works too:

```
sudo apt install python3.7 python3.7-dev
```

![Python Installation](/src/python.gif?raw=true)


- Clone the repo:

```
git clone https://github.com/nitanmarcel/Tg-UserBot
```

- Install the requirements using pip3

```
pip3 install -r requirements.txt
```

![Requirements Installation](/src/requirements.gif?raw=true)

---

# Setup

#### Before starting the bot you have to configure it.
> - Create a config.env file. Follow the example from sample.config.env.
> - Write the next lines in the config
> - You can always display the congiguration help with `python3 -m tg_userbot --config`

#### The available config values are:

> - `APP_ID` = Your telegram app id from https://my.telegram.org/apps
>
> - `APP_HASH` = Your telegram app hash from https://my.telegram.org/apps
>
> - `SESSION_NAME` = Custom session name. Leave empty to use the default session name
>
> - `STATS` = Set to False if you want to disable stats gathering",
>
> - `STATS_TIMER` = Set the stats refresh time
>
> - `FORCE_SMS` = Set true to get the security code though SMS
>
> - `DB_URI` = Your postgress database url. Leave empty to disable the modules that use it
>
> - `BLOCK_PM` = Set to True if you want to block new PMs. New PMs will be deleted and user blocked
>
> - `NOPM_SPAM` = Set to True if you want to block users that are spamming your PMs.
>
> - `PROXY_TYPE` = Your proxy type HTTP/SOCKS4/SOCKS5. Leave empty to disable proxy.
>
> - `HOST` = The host of the used proxy.
>
> - `PORT` = The port of the used proxy.
>
> - `USERNAME` = The username of the used proxy. (If any)
>
> - `PASSWORD` = The password of the used proxy. (If any)
>
> - `ENABLE_SSH` = Set True if you want to execute or upload from a ssh server"
>
> - `SSH_HOSTNAME` = SSH: (optional) The hostname or address to connect to.
>
> - `SSH_PORT` = SSH: (optional) The port number to connect to.
>
> - `SSH_USERNAME` = SSH: (optional) Username to authenticate as on the server.
>
> - `SSH_PASSWORD` = SSH: (optional) The password to use for client password authentication
>
> - `SSH_PASSPHRASE` = SSH: (optional) The passphrase for your ssh connection.
>
> - `SSH_KEY` =  SSH: (optional) The private key which will be used to authenticate this client"


---
# Features

> Tg_UserBot brings some small improvments to any Telegram Client
>
> You can some features using a command. Others are enabled from the config file and they work in background
>
#### Available commands are:

> - `.afk` `<optional-reason>` - Sets you as afk and tells everyone that you are away by sending them a message when they mention your username, sends you a PM or replies to your message. Send a message to any chat to dismiss your afk state
>
> -  `.ppic` - Reply to a photo/document to set it as your profile photo
>
> - `.pbio` `<bio>` - Change your about message by sending `.pbio` followed by the bio you want to set.
>
> - `.puname` `<username>` - Change your username by sending `.puname` followed by the username you want to set.
>
> - `.pname` `<name>` - Change your name by sending `.pname` followed by the username you want to set. Use `\n` to separate your first and last name
>
> - You can use `.cpic`, `.cpio`, `.cuname`, `.cname` to do the same for your chats
>
> - `.ping` - Test your userbot response time
>
> - `.stats` - Get your telegram stats. Works only if stats are not disabled from the config file
>
> - `.info` `<optional-username>` - Send it as a message to get your info, reply to one or use the command followed by a username to get user info
>
> - `.github` `<github-username>` - Get the info and repositories of any github user
>
> - `.term` `<command>` - Execute bash commands
>
> - `.rterm` `<command>` - Execute bash commands on a ssh server
>
> - `.upload` `<command>` - Upload files
>
> - `.rupload` `<command>` - Upload files from a ssh server
>
> - `$<language>` `<code>` - Execute code in any programming language using rextester.com api
   - Available languages are:

   > `ada`, `asm`, `bash`, `brainfuck`, `c`, `c#`, `c++`, `c_clang`, `c_gcc`, `clang`, `clang++`, `clangplusplus`, `clisp`, `common_lisp`, `cplusplus`, `cplusplus_clang`, `cplusplus_gcc`, `cpp`, `cpp_clang`, `cpp_gcc`, `csharp`, `d`, `elixir`, `erlang`, `f#`, `fortran`, `fpc`, `fsharp`, `g++`, `gcc`, `go`, `golang`, `haskell`, `java`, `javascript`, `js`, `kotlin`, `lisp`, `lua`, `msvc`, `mysql`, `nasm`, `node`, `objc`, `objective_c`, `ocaml`, `oracle`, `pas`, `pascal`, `perl`, `php`, `postgresql`, `prolog`, `py2`, `py3`, `python`, `python2`, `python3`, `r`, `ruby`, `scala`, `scheme`, `sql_server`, `swift`, `tcl`, `v8`, `vb`, `vb.net`, `vc++`, `visual_basic_dotnet`, `visual_c`, `visual_cplusplus`, `visual_cpp`

## Contribuiting

### To Do

## Support

### To Do
