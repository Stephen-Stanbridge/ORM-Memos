from typing import Union, re as re_type
import re
from prettytable import PrettyTable
from SQL.setup_db import Session
from Models.models import User
session = Session()


def get_list_of_all_users() -> PrettyTable:
    all_users = session.query(User).all()
    list_of_users = PrettyTable()
    list_of_users.field_names = ['USERNAME', 'ID']
    for user in all_users:
        list_of_users.add_row([user.username.capitalize(), user.id])
    return list_of_users


def username_from_id(user_id: int) -> Union[PrettyTable, str]:
    username = session.query(User.username).filter(User.id == user_id).first()
    if username is None:
        return "No user with this id."
    result = PrettyTable()
    result.field_names = ['USERNAME', 'ID']
    result.add_row([username[0], user_id])
    return result


def id_from_username(username: str) -> Union[PrettyTable, str]:
    user_id = session.query(User.id).filter(User.username == username.capitalize()).first()
    if user_id is None:
        return "User with this username doesn't exist."
    result = PrettyTable()
    result.field_names = ['USERNAME', 'ID']
    result.add_row([username.capitalize(), user_id[0]])
    return result


def get_username_or_id(regex: re_type.Match) -> str:
    if re.match(r'\d+', regex.group(2)):
        return username_from_id(regex.group(2))
    else:
        return id_from_username(regex.group(2))
