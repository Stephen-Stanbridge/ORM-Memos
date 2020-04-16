from Handlers.creating_commands import create_memo
import pytest
from Models.models import Memo
import io


PARAMS = [
    ('T\nAnd this is content', 'Title length must be greater than 3 and content greater than 10.'),
    ('\nAnd this is content', 'Title length must be greater than 3 and content greater than 10.'),
    ('This is title\nshort', 'Title length must be greater than 3 and content greater than 10.'),
    ('This is title\n', 'Title length must be greater than 3 and content greater than 10.'),
    ('{}\nAnd this is content'.format('A' * 300), "Title length can't be greater than 255.")
]


@pytest.mark.parametrize('user_input, result', PARAMS)
def test_unsuccessfull_create_memo(monkeypatch, user, session, user_input, result):
    memos_count = len(session.query(Memo).all())
    monkeypatch.setattr('sys.stdin', io.StringIO(user_input))
    assert create_memo(user) == result
    assert len(session.query(Memo).all()) == memos_count


def test_successfull_create_memo(monkeypatch, user, session):
    memos_count = len(session.query(Memo).all())
    monkeypatch.setattr('sys.stdin', io.StringIO('This is title\nAnd this is content'))
    assert 'memo with id' and 'created successfully' in create_memo(user)
    assert len(session.query(Memo).all()) == memos_count + 1
