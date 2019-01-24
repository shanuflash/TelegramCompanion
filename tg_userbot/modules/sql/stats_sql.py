import time

import progressbar
from sqlalchemy import Column, Integer, UnicodeText
from telethon import utils
from telethon.tl.functions.channels import GetFullChannelRequest

from tg_userbot import LOGGER, RUN_STATS, STATS_TIMER, client
from tg_userbot.modules.sql import BASE, SESSION
from tg_userbot.utils.decorators import timer, log_exception


class STATS(BASE):
    __tablename__ = "stats"
    updatetime = Column(UnicodeText, primary_key=True)
    totaldialogs = Column(Integer, default=0)
    usercount = Column(Integer, default=0)
    channelcount = Column(Integer, default=0)
    supcount = Column(Integer, default=0)
    convertedgroups = Column(Integer, default=0)
    numchannel = Column(Integer, default=0)
    numuser = Column(Integer, default=0)
    numdeleted = Column(Integer, default=0)
    numbot = Column(Integer, default=0)
    numchat = Column(Integer, default=0)
    numsuper = Column(Integer, default=0)

    def __init__(
        self,
        updatetime,
        totaldialogs,
        usercount,
        channelcount,
        supcount,
        convertedgroups,
        numchannel,
        numuser,
        numdeleted,
        numbot,
        numchat,
        numsuper,
    ):
        self.updatetime = updatetime
        self.totaldialogs = totaldialogs
        self.usercount = usercount
        self.channelcount = channelcount
        self.supcount = supcount
        self.convertedgroups = convertedgroups
        self.numchannel = numchannel
        self.numuser = numuser
        self.numdeleted = numdeleted
        self.numbot = numbot
        self.numchat = numchat
        self.numsuper = numsuper


class GroupsInfo(BASE):
    __tablename__ = "groups_info"
    supergroupid = Column(Integer, primary_key=True)
    oldgroupid = Column(Integer)

    def __init__(self, supergroupid, oldgroupid):
        self.supergroupid = supergroupid
        self.oldgroupid = oldgroupid


STATS.__table__.create(checkfirst=True)
GroupsInfo.__table__.create(checkfirst=True)



def get_stats():
    cursor = SESSION.query(STATS).first()
    try:
        if cursor:
            return (
                cursor.updatetime,
                cursor.totaldialogs,
                cursor.usercount,
                cursor.channelcount,
                cursor.supcount,
                cursor.convertedgroups,
                cursor.numchannel,
                cursor.numuser,
                cursor.numdeleted,
                cursor.numbot,
                cursor.numchat,
                cursor.numsuper,
            )
        else:
            return False
    finally:
        SESSION.close()


FirstRun = True


@timer(STATS_TIMER, run=RUN_STATS)
@log_exception
async def GetStats():
    global FirstRun

    TotalDialogs = 0
    UserCount = 0
    ChannelCount = 0
    SupCount = 0
    ConvertedGroupsIDs = []
    NewGroupsIDs = []
    NumChannel = 0
    NumUser = 0
    NumDeleted = 0
    NumBot = 0
    NumChat = 0
    NumSuper = 0
    UserId = None

    if FirstRun:
        LOGGER.info(
            "Gathering Stats. You'll be able to use this app during this process without problems"
        )
        LOGGER.info("You can disable this in the config.env file")
        if not get_stats():
            LOGGER.info(
                "Because this is your first time running this, the .stats command won't work until this process isn't over"
            )
    else:
        LOGGER.info("Updating Stats.")

    UpdateTime = time.strftime("%c")
    CachedSupergroups = []

    OldGroupsList = []
    try:
        cursor = SESSION.query(GroupsInfo).first()
        if cursor:
            OldGroupsList.append(cursor.oldgroupid)
            for old in OldGroupsList:
                CachedSupergroups.append(old)
    finally:
        SESSION.close()

    UserId = await client.get_me()
    UserId = UserId.id

    dialogs = await client.get_dialogs(limit=None)

    for dialog in dialogs:
        await client.get_input_entity(dialog)
        if dialog.is_group:
            NumChat = NumChat + 1
        if dialog.is_user:
            if dialog.entity.bot:
                NumBot = NumBot + 1
            elif not dialog.entity.deleted:
                NumUser = NumUser + 1
            else:
                NumDeleted = NumDeleted + 1
        if dialog.is_channel:
            if dialog.is_group:
                NumSuper = NumSuper + 1
            else:
                NumChannel = NumChannel + 1

    completed = 0
    bar = progressbar.ProgressBar(max_value=NumSuper, widget=None, poll_interval=1)
    bar.update(completed)

    for dialog in dialogs:
        if dialog.is_channel:
            if dialog.is_group:
                ID1 = utils.get_peer_id(utils.get_input_peer(dialog, allow_self=False))
                strid = str(ID1).replace("-100", "")
                ID = int(strid)
                if ID not in CachedSupergroups:
                    gotChatFull = await client(
                        GetFullChannelRequest(await client.get_input_entity(ID1))
                    )
                    cursor = SESSION.query(GroupsInfo).first()
                    if not cursor:
                        cursor = GroupsInfo(
                            gotChatFull.full_chat.id,
                            gotChatFull.full_chat.migrated_from_chat_id,
                        )
                    else:
                        cursor.supergroupid = gotChatFull.full_chat.id
                        cursor.oldgroupid = gotChatFull.full_chat.migrated_from_chat_id

                completed = completed + 1
                bar.update(completed)
    try:
        SESSION.add(cursor)
        SESSION.commit()
    except Exception:
        pass

    LookIds = []

    for dialog in dialogs:
        ID = None
        try:
            ID = await utils.get_peer(dialog, allow_self=False)
        except Exception:
            ID = UserId
            if dialog.is_channel:
                strid = str(ID).replace("-100", "")
                ID = int(strid)
            elif dialog.is_group:
                strid = str(ID).replace("-", "")
                ID = int(strid)
                LookIds.append(ID)

    for dialog in dialogs:
        if dialog.is_channel:
            if dialog.entity.megagroup == True:
                ID1 = utils.get_peer_id(utils.get_input_peer(dialog, allow_self=False))
                strid = str(ID1).replace("-100", "")
                ID = int(strid)
                try:
                    superGroupIDs = SESSION.query(GroupsInfo).first()
                    superGroupList = []
                    oldGroupList = []
                    if superGroupIDs:
                        superGroupList.append(superGroupIDs.supergroupid)
                        oldGroupList.append(superGroupIDs.oldgroupid)
                        for new in superGroupList:
                            NewGroupsIDs.append(new)
                        for old in oldGroupList:
                            ConvertedGroupsIDs.append(old)
                finally:
                    SESSION.close()

    bar.finish()
    LOGGER.info("Counting your chats:")

    for dialog in dialogs:
        ID = None
        try:
            ID = utils.get_peer_id(utils.get_input_peer(dialog, allow_self=False))
        except Exception:
            ID = UserId
        if dialog.is_channel:
            strid = str(ID).replace("-100", "")
            ID = int(strid)
        if dialog.is_group:
            strid = str(ID).replace("-", "")
            ID = int(strid)
        if ID not in ConvertedGroupsIDs:
            count = await client.get_messages(await client.get_input_entity(dialog))
            if dialog.is_channel:
                if dialog.entity.megagroup == True:
                    SupCount = SupCount + count.total
                else:
                    ChannelCount = ChannelCount + count.total
            elif dialog.is_group or dialog.is_user:
                UserCount = UserCount + count.total
        if ID in NewGroupsIDs:
            if ID in LookIds and ID not in ConvertedGroupsIDs:
                index = NewGroupsIDs.index(ID)
                OldChatCount = await client.get_messages(
                    await client.get_input_entity(
                        int("-" + str(ConvertedGroupsIDs[index]))
                    )
                )
                UserCount = UserCount + OldChatCount

    TotalDialogs = UserCount + ChannelCount + SupCount
    ConvertedCount = len(NewGroupsIDs)
    NumChat = NumChat - ConvertedCount

    cursor = SESSION.query(STATS).first()
    if not cursor:
        cursor = STATS(
            UpdateTime,
            TotalDialogs,
            UserCount,
            ChannelCount,
            SupCount,
            ConvertedCount,
            NumChannel,
            NumUser,
            NumDeleted,
            NumBot,
            NumChat,
            NumSuper,
        )
    else:
        cursor.updatetime = UpdateTime
        cursor.totaldialogs = TotalDialogs
        cursor.usercount = UserCount
        cursor.channelcount = ChannelCount
        cursor.supcount = SupCount
        cursor.convertedgroups = ConvertedCount
        cursor.numchannel = NumChannel
        cursor.numuser = NumUser
        cursor.numdeleted = NumDeleted
        cursor.numbot = NumBot
        cursor.numchat = NumChat
        cursor.numsuper = NumSuper

    SESSION.merge(cursor)
    SESSION.commit()

    FirstRun = False

    LOGGER.info("DONE!! Stats updated. Get them using .stats!")
    LOGGER.info(f"The stats will be updated every {STATS_TIMER}s")
