from Handlers.inbox_commands import does_user_have_memo_in_inbox, delete_all_memos_from_inbox, delete_memo_from_inbox_by_id
from Models.models import SentMemo
import pytest


def test_does_user_have_memo_in_inbox(user, inbox):
    assert does_user_have_memo_in_inbox(user.id, inbox[0].id)
    assert not does_user_have_memo_in_inbox(user.id, 4)


def test_delete_all_memos_from_inbox(user, inbox, session):
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()) == 3
    delete_all_memos_from_inbox(user)
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()) == 0


def test_delete_one_memo_from_inbox_by_id(user, inbox, session):
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()) == 3
    delete_memo_from_inbox_by_id(user, {1})
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()) == 2
