from Handlers.sending_commands import make_checks
from ConfigClasses.classes import SendMemo
import pytest


def test_make_checks(user, second_user, memos, inbox):
    config = SendMemo()
    config.user, config.memo_id, config.receiver = second_user, memos[0].id, user.id
    assert make_checks(config) == (False, "MemoError")
    config.user, config.receiver = user, 100
    assert make_checks(config) == (False, "UserError")
    config.receiver = user.id
    assert not make_checks(config)
