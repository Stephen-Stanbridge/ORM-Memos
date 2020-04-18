from sqlalchemy import create_engine
from Models.models import Base, User, Memo, SentMemo
from SQL.setup_db import engine, Session
import pytest
import re
from prettytable import PrettyTable
from typing import Union


@pytest.fixture
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close_all()


@pytest.fixture
def user(session):
    user = User(username="Testing_user", password="098f6bcd4621d373cade4e832627b4f6")
    session.add(user)
    session.commit()
    memo = Memo(title="Title", content="this is content", sent=True, creator_id=user.id)
    session.add(memo)
    session.commit()
    inbox_memo = SentMemo(memo_id=memo.id, receiver_id=user.id)
    session.add(inbox_memo)
    session.commit()
    yield user


@pytest.fixture
def second_user(session):
    second_user = User(username="Second_user", password="password")
    session.add(second_user)
    session.commit()
    yield second_user


@pytest.fixture
def memos(session, user):
    memo1 = Memo(title="Title2", content="this is content2", sent=True, creator_id=user.id)
    memo2 = Memo(title="Title3", content="this is content3", sent=False, creator_id=user.id)
    session.add(memo1)
    session.add(memo2)
    session.commit()
    yield [memo1, memo2]


@pytest.fixture
def inbox(session, user, memos):
    memos[1].sent = True
    sent_memo1 = SentMemo(memo_id=memos[0].id, receiver_id=user.id)
    sent_memo2 = SentMemo(memo_id=memos[1].id, receiver_id=user.id)
    session.add(sent_memo1)
    session.add(sent_memo2)
    session.commit()
    yield [sent_memo1, sent_memo2]


def does_table_contain_all_words(words: list, table: Union[PrettyTable, str]) -> bool:
    if isinstance(table, str):
        table = re.split(r'\n', table)
        return all(word in table for word in words)
    table = table.get_html_string()
    table = re.split(r'<td>|</td>', table)
    return all(word in table for word in words)
