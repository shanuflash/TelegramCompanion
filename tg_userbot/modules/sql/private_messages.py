from sqlalchemy import Column, Integer

from . import BASE, SESSION


class PM(BASE):
    __tablename__ = "private_messages"
    chat_id = Column(Integer, primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


PM.__table__.create(checkfirst=True)


def private_in_db(chat_id):
    return SESSION.query(PM).get(chat_id)


def private_add(chat_id):
    if not private_in_db(chat_id):
        chat = PM(chat_id)

        SESSION.add(chat)
        SESSION.commit()
