from sqlalchemy import create_engine
from Models.models import Base, User, Memo, SentMemo
from SQL.setup_db import engine, Session
import pytest
import re
from prettytable import PrettyTable


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


def does_table_contain_all_words(words: list, table: PrettyTable) -> bool:
    table = table.get_html_string()
    table = re.split(r'<td>|</td>', table)
    return all(word in table for word in words)
