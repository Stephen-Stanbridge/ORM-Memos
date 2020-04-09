from SQL.setup_db import Session
from Models.models import User
from termcolor import colored
from typing import Union
import hashlib
session = Session()


def hash_password(password: str) -> str:
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password


def login_or_register(username: str, password: str) -> Union[User, None]:
    query = session.query(User).filter(User.username == username)
    does_exist = False if query.count() == 0 else True
    if does_exist:
        user = query.one()
        if user.password == hash_password(password):
            return user
        print("Wrong password.")
        return None
    new_user = User(username=username, password=hash_password(password))
    session.add(new_user)
    session.commit()
    return new_user
