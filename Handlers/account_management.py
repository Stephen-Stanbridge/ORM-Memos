from SQL.setup_db import Session, engine
from Models.models import User, Memo
from Handlers.inbox_commands import delete_all_memos_from_inbox
from typing import Union
import hashlib
import re
session = Session()


def hash_password(password: str) -> str:
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password


def check_username(username: str) -> bool:
    if re.match(r"^[a-zA-Z_]+$", username):
        return True
    return False


def login_or_register(username: str, password: str) -> Union[User, str]:
    username = username.capitalize()
    user = session.query(User).filter(User.username == username).first()
    if user is not None:
        if user.password == hash_password(password):
            return user
        return "Wrong password."
    if not check_username(username):
        return "Username can only contain letters and _ character."
    new_user = User(username=username, password=hash_password(password))
    session.add(new_user)
    session.commit()
    return new_user


def delete_user(user: User) -> str:
    delete_all_memos_from_inbox(user)
    session.query(Memo).filter(Memo.creator_id == user.id).delete()
    session.query(User).filter(User.id == user.id).delete()
    session.commit()
    return "User, inbox and created memos deleted. Use exit command."


def change_password(old_password: str, new_password: str, user: User) -> str:
    if old_password == new_password:
        return "It's the same password. Not changed."
    is_old_password_correct = session.query(User).filter(User.password == hash_password(old_password)).first()
    if is_old_password_correct is None:
        return "Old password is incorrect."
    user.password = hash_password(new_password)
    session.flush()
    session.commit()
    return "Password changed successfully."
