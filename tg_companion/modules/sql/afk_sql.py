import threading

from sqlalchemy import Boolean, Column, UnicodeText

from tg_companion.modules.sql import BASE, SESSION


class AFK(BASE):
    __tablename__ = "afk"
    is_afk = Column(Boolean, primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, reason="", is_afk=True):
        self.reason = reason
        self.is_afk = is_afk


AFK.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_STATUS = {}


def is_afk():
    return "is_afk" in AFK_STATUS


def check_afk():
    if "is_afk" in AFK_STATUS:
        return True, AFK_STATUS["is_afk"]


def set_afk(reason=""):
    cursor = SESSION.query(AFK).first()
    if not cursor:
        cursor = AFK(reason, True)
    else:
        cursor.is_afk = True
        cursor.reason = reason

    AFK_STATUS["is_afk"] = reason
    SESSION.add(cursor)
    SESSION.commit()


def rm_afk():
    cursor = SESSION.query(AFK).first()
    if cursor:
        if "is_afk" in AFK_STATUS:
            del AFK_STATUS["is_afk"]
            SESSION.delete(cursor)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def __load_afk_state():
    global AFK_STATUS
    try:
        cursor = SESSION.query(AFK).first()
        if cursor:
            AFK_STATUS["is_afk"] = cursor.reason
    finally:
        SESSION.close()


__load_afk_state()
