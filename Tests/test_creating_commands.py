from Handlers.creating_commands import create_memo, get_all_created_memos, get_content_of_memo_by_id
import pytest
from Models.models import Memo, User
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


def test_get_all_created_memos(memos, user):
    words = [memos[0].title, memos[1].title, str(memos[0].sent), str(memos[1].sent)]
    assert does_table_contain_all_words(words, get_all_created_memos(user))


def test_improper_get_content_of_memo_by_id(session, second_user, memos):
    assert get_content_of_memo_by_id(second_user, memos[0].id) == "You don't own memo with this id."
    assert get_content_of_memo_by_id(second_user, 100) == "You don't own memo with this id."


def test_proper_get_content_of_memo_by_id(user, session):
    memo = session.query(Memo).filter(Memo.creator_id == user.id, Memo.id == 1).first()
    words = [memo.title, memo.content, 'Sent to:', '[1]']
    assert does_table_contain_all_words(words, get_content_of_memo_by_id(user, 1))
