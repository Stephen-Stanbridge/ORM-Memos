from Handlers.commands import *
from Models.models import User
from Handlers.creating_commands import create_memo
import re


regex_for_getting_memos = r"""memo get ?(\d*)"""
regex_for_sending_memos = r"""memo send ((all)|((\d+,)+\d+|\d+)) (\d+)"""
regex_for_getting_inbox = r"""inbox get ?(\d*)"""
regex_for_deleting_memos_from_inbox = r"""inbox delete ((\d+,)+\d+|\d+|all)"""
regex_for_users = r"""(users get) ?(\d+|\w+)*"""
regex_for_account_management = r"""user (delete|password)( (\S+) (\S+))?"""


def execute(command: str, user: User):
    if command == "help":
        app_help()
    elif command == "info":
        print(user)
    elif command == "exit":
        exit()
    elif command == "memo":
        memo_help()
    elif command == "memo create":
        print(create_memo(user))
    elif re.match(regex_for_getting_memos, command):
        regex = re.match(regex_for_getting_memos, command)
        handle_getting_memos(regex, user)
    elif re.match(regex_for_sending_memos, command):
        regex = re.match(regex_for_sending_memos, command)
        handle_sending_memos(regex, user)
    elif command == "inbox":
        inbox_help()
    elif re.match(regex_for_getting_inbox, command):
        regex = re.match(regex_for_getting_inbox, command)
        handle_inbox(regex, user)
    elif re.match(regex_for_deleting_memos_from_inbox, command):
        regex = re.match(regex_for_deleting_memos_from_inbox, command)
        handle_deleting_from_inbox(regex, user)
    elif command == "users":
        users_help()
    elif re.match(regex_for_users, command):
        regex = re.match(regex_for_users, command)
        handle_users(regex, user)
    elif command == "user":
        account_help()
    elif re.match(regex_for_account_management, command):
        regex = re.match(regex_for_account_management, command)
        handle_user_management(regex, user)
    else:
        print("Unrecognized command. Type 'help for help.")
