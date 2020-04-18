from Handlers.sending_commands import make_checks, send_memo, send_memo_to_all
from ConfigClasses.classes import SendMemo
import pytest
from Models.models import SentMemo, Memo, User


def test_make_checks(user, second_user, memos, inbox):
    config = SendMemo()
    config.user, config.memo_id, config.receiver = second_user, memos[0].id, user.id
    assert make_checks(config) == (False, "MemoError")
    config.user, config.receiver = user, 100
    assert make_checks(config) == (False, "UserError")
    config.receiver = user.id
    assert not make_checks(config)
    config.receiver = second_user.id
    assert make_checks(config)


def test_send_memo(user, second_user, session):
    config = SendMemo()
    memo_to_send = session.query(Memo).filter(Memo.creator_id == user.id).first()
    config.user, config.memo_id, config.receiver = user, memo_to_send.id, second_user.id
    before = len(session.query(SentMemo).filter(SentMemo.receiver_id == second_user.id,
                                                SentMemo.memo_id == memo_to_send.id).all())
    memo_to_send.sent = False
    session.commit()
    send_memo(config)
    assert memo_to_send.sent
    assert len(session.query(SentMemo).filter(SentMemo.receiver_id == second_user.id,
                                              SentMemo.memo_id == memo_to_send.id).all()) == before + 1


def test_send_memo_to_all(user, second_user, session):
    new_user = User(username="Third_user", password="password")
    session.add(new_user)
    session.commit()
    before = len(session.query(SentMemo).filter(SentMemo.memo_id == 1).all())
    send_memo_to_all(user, 1)
    assert len(session.query(SentMemo).filter(SentMemo.memo_id == 1).all()) == before + 2
    assert session.query(SentMemo).filter(SentMemo.receiver_id == second_user.id).first() is not None
    assert session.query(SentMemo).filter(SentMemo.receiver_id == new_user.id).first() is not None
