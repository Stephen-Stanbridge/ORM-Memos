import ConfigClasses.classes as config_class
from typing import re as re_type
import re
from Handlers.creating_commands import get_all_created_memos, get_content_of_memo_by_id
from Handlers.inbox_commands import get_all_received_memos, get_received_memo_by_id, delete_all_memos_from_inbox, \
    delete_memo_from_inbox_by_id
from Handlers.sending_commands import send_memo_to_all, send_memo_to_users
from Handlers.users_commands import get_list_of_all_users, get_username_or_id
from Handlers.User import delete_user, change_password
from Models.models import User


app_help_message = """
help - List of commands
exit - Exit dashboard
info - Your info
memo - List of available commands for created and sent memos administration
inbox - List of available commands for received memos administration
users - List of available commands for getting information about users
user - List of available commands for account management
"""

memo_help_message = """
memo create - Create memo
memo get - Get all created memos and their status
memo get [id] - Get particular created memo with content
memo send [user_id]/[user_ids]/all [memo_id] - send memo to all users or with particular id(s) (use format [id],[id]...)
"""

inbox_help_message = """
inbox get - Get all received memos
inbox get [memo_id] - get particular received memo
inbox delete [memo_id]/[memo_ids]/all - delete all memos from your inbox or with particular id(s) (use format [id],[id]...)
"""

users_help_message = """
users get - Get list of all users
users get [id]/[username] - Get info about user with specific id or username
"""

account_help_message = """
user password [old_password] [new_password] - Change your password
user delete - Delete your account 
"""


def app_help():
    print(app_help_message)


def memo_help():
    print(memo_help_message)


def inbox_help():
    print(inbox_help_message)


def users_help():
    print(users_help_message)


def account_help():
    print(account_help_message)


def handle_getting_memos(regex: re_type.Match, user: User) -> None:
    if not regex.group(1):
        print(get_all_created_memos(user))
    else:
        print(get_content_of_memo_by_id(user, regex.group(1)))


def handle_sending_memos(regex: re_type.Match, user: User) -> None:
    memo_id = int(regex.group(5))
    if regex.group(2):
        send_memo_to_all(user, memo_id)
    else:
        receivers = set(regex.group(3).split(','))
        receivers = [id for id in receivers]
        config = config_class.SendMemo()
        config.user = user
        config.receiver = receivers
        config.memo_id = memo_id
        send_memo_to_users(config)


def handle_inbox(regex: re_type.Match, user: User) -> None:
    if not regex.group(1):
        print(get_all_received_memos(user))
    else:
        print(get_received_memo_by_id(user, regex.group(1)))


def handle_deleting_from_inbox(regex: re_type.Match, user: User) -> None:
    memo_ids = regex.group(1)
    if memo_ids == "all":
        delete_all_memos_from_inbox(user)
    else:
        memo_ids = set(memo_ids.split(','))
        delete_memo_from_inbox_by_id(user, memo_ids)


def handle_users(regex: re_type.Match) -> None:
    if not regex.group(2):
        print(get_list_of_all_users())
    else:
        print(get_username_or_id(regex))


def handle_user_management(regex: re_type.Match, user: User) -> None:
    action = regex.group(1)
    if action == "delete":
        print(delete_user(user))
    elif regex.group(4):
        old_password = regex.group(3)
        new_password = regex.group(4)
        print(change_password(old_password, new_password, user))
