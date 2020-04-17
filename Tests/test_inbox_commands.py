from Handlers.inbox_commands import does_user_have_memo_in_inbox


def test_does_user_have_memo_in_inbox(user, inbox):
    assert does_user_have_memo_in_inbox(user.id, inbox[0].id)
    assert not does_user_have_memo_in_inbox(user.id, 4)
