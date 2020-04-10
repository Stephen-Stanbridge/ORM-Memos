import sys
from prettytable import PrettyTable
from prompt_toolkit import prompt
from termcolor import colored
from Models.models import User, Memo, SentMemo
from SQL.setup_db import Session
session = Session()


def create_memo(user: User) -> str:
    print("After finishing writing your memo press CTRL+D")
    title = input("Title: ")
    print("Content of memo:")
    content = sys.stdin.readlines()
    content = ''.join(content)
    if len(title) < 3 or len(content) < 10:
        return "Title length must be greater than 3 and content greater than 10."
    elif len(title) > 255:
        return "Title length can't be greater than 255."
    new_memo = Memo(title=title, content=content, creator_id=user.id)
    session.add(new_memo)
    session.commit()
    return "Memo with id {} created successfully.".format(new_memo.id)


def get_all_created_memos(user: User) -> str:
    query = session.query(Memo).filter(Memo.creator_id == user.id)
    printed_result = PrettyTable()
    printed_result.field_names = ["ID", "TITLE", "SENT"]
    for memo in query.all():
        printed_result.add_row([memo.id, memo.title, memo.sent])
    return printed_result


def get_content_of_memo_by_id(user: User, memo_id: int) -> str:
    memo = session.query(Memo).filter(Memo.creator_id == user.id, Memo.id == memo_id).first()
    if memo is None:
        return "You don't own memo with this id."
    result = 'TITLE:\n{}\nCONTENT:\n{}\n'.format(memo.title, memo.content)
    if memo.sent:
        receiver_id_list = [sent_memo.receiver_id for sent_memo in memo.sent_memo]
        result += "Sent to:\n{}".format(receiver_id_list)
    return result
