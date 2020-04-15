from Handlers.account_management import hash_password, login_or_register, check_username, delete_user, change_password
from Models.models import User, Memo, SentMemo
import pytest


def test_hash_password():
    assert hash_password('test') == '098f6bcd4621d373cade4e832627b4f6'


USERNAMES = [
    ("Mark", True),
    ("mark", True),
    ("Mark_Smith", True),
    ("420Mark", False),
    ("123", False),
    ("M4rk", False)
]


@pytest.mark.parametrize('username, result', USERNAMES)
def test_check_username(username, result):
    assert check_username(username) == result


def test_wrong_password(user, session):
    assert login_or_register('Testing_user', 'wrong_password') == 'Wrong password.'


def test_wrong_username(session):
    assert login_or_register('User2name', 'password') == 'Username can only contain letters and _ character.'


def test_successfull_registration(session):
    login_or_register('Stephen', 'password')
    assert len(session.query(User).all()) == 1


def test_successfull_login(user, session):
    assert isinstance(login_or_register('Testing_user', 'test'), User)


def test_delete_user(session, user):
    assert len(session.query(Memo).all()) == 1
    assert len(session.query(SentMemo).all()) == 1
    assert len(session.query(User).all()) == 1
    delete_user(user)
    assert len(session.query(User).all()) == 0
    assert len(session.query(Memo).all()) == 0
    assert len(session.query(SentMemo).all()) == 0


def test_change_password_same(user):
    assert change_password('test', 'test', user) == "It's the same password. Not changed."


def test_change_password_wrong_old(user):
    assert change_password('wrong_password', 'new_password', user) == 'Old password is incorrect.'


def test_change_password_corredt(user):
    assert change_password('test', 'new_password', user) == 'Password changed successfully.'
    assert user.password == hash_password('new_password')
