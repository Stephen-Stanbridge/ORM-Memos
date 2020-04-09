from SQL.setup_db import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    def __repr__(self):
        return "<User(id={}, username={})>".format(self.id, self.username)


class Memo(Base):
    __tablename__ = 'memos'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(String)
    sent = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Memo(id={}, title={}, content={}, sent={}, creator_id={})>".format(self.id, self.title, self.content,
                                                                                  self.sent, self.creator_id)


class SentMemo(Base):
    __tablename__ = 'sent_memos'

    id = Column(Integer, primary_key=True)
    memo_id = Column(Integer, ForeignKey('memos.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<SentMemo(id={}, memo_id={}, receiver_id={})>".format(self.id, self.memo_id, self.receiver_id)
