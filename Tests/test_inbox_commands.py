from Handlers.inbox_commands import does_user_have_memo_in_inbox, delete_all_memos_from_inbox, \
    delete_memo_from_inbox_by_id, get_received_memo_by_id, get_all_received_memos
from Models.models import SentMemo, User
import pytest
from conftest import does_table_contain_all_words


def test_does_user_have_memo_in_inbox(user, inbox):
    assert does_user_have_memo_in_inbox(user.id, inbox[0].id)
    assert not does_user_have_memo_in_inbox(user.id, 4)


def test_delete_all_memos_from_inbox(user, inbox, session):
    delete_all_memos_from_inbox(user)
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()) == 0


def test_delete_one_memo_from_inbox_by_id(user, inbox, session):
    before = len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all())
    delete_memo_from_inbox_by_id(user, {1})
    assert before - 1 == len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all())


def test_delete_few_memo_from_inbox_by_id(user, inbox, session):
    before = len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all())
    delete_memo_from_inbox_by_id(user, {inbox[0].memo_id, inbox[1].memo_id})
    assert before - 2 == len(session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all())


def test_delete_memo_from_inbox_by_id_when_memo_does_not_exist(capsys, user, session):
    delete_memo_from_inbox_by_id(user, {1, 2})
    out, err = capsys.readouterr()
    assert "You don't have memo with id 2 in your inbox. Ommited." in out
    assert session.query(SentMemo).filter(SentMemo.memo_id == 1, SentMemo.receiver_id == user.id).first() is None


def test_delete_memo_from_inbox_by_id_when_memo_belongs_to_another_user(capsys, user, second_user, session):
    delete_memo_from_inbox_by_id(second_user, {1})
    out, err = capsys.readouterr()
    assert "You don't have memo with id 1 in your inbox. Ommited." in out
    assert len(session.query(SentMemo).filter(SentMemo.memo_id == 1, SentMemo.receiver_id == 1).all()) == 1


def test_improper_get_received_memo_by_id(second_user, inbox):
    assert get_received_memo_by_id(second_user, inbox[0].memo_id) == "You don't have memo with this id in your inbox."
    assert get_received_memo_by_id(second_user, 10) == "You don't have memo with this id in your inbox."


def test_get_received_memo_by_id(user, inbox, session):
    memo = inbox[0].memo_details
    words = [str(memo.id), memo.title, memo.content, user.username]
    assert does_table_contain_all_words(words, get_received_memo_by_id(user, memo.id))


def test_get_all_received_memos(user, inbox):
    memo1 = inbox[0].memo_details
    memo2 = inbox[1].memo_details
    words = [str(memo1.id), memo1.title, memo1.content, user.username, str(memo2.id), memo2.title, memo2.content]
    assert does_table_contain_all_words(words, get_all_received_memos(user))
