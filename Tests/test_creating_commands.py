from Handlers.creating_commands import create_memo, get_all_created_memos
import pytest
from Models.models import Memo
import io
import re
from conftest import does_table_contain_all_words


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


def test_get_all_created_memos(user, session):
    memos = [Memo(title="Title2", content="this is content2", sent=True, creator_id=user.id),
             Memo(title="Title3", content="this is content3", sent=False, creator_id=user.id)]
    session.bulk_save_objects(memos)
    session.commit()
    words = ['Title2', 'Title3', 'True', 'False']
    assert does_table_contain_all_words(words, get_all_created_memos(user))
