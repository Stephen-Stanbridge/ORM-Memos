from prettytable import PrettyTable
from Models.models import User, SentMemo, Memo
from SQL.setup_db import Session
from typing import Union
session = Session()


def does_user_have_memo_in_inbox(user_id: int, memo_id: int) -> bool:
    is_memo_in_inbox = session.query(SentMemo).filter(SentMemo.receiver_id == user_id,
                                                      SentMemo.memo_id == memo_id).first()
    if is_memo_in_inbox is None:
        return False
    return True


def get_all_received_memos(user: User) -> PrettyTable:
    received_memos = session.query(SentMemo).filter(SentMemo.receiver_id == user.id).all()
    result = PrettyTable()
    result.field_names = ["MEMO ID", "TITLE", "CONTENT", "AUTHOR"]
    for received_memo in received_memos:
        received_memo = received_memo.memo_details
        author = session.query(User.username).filter(User.id == received_memo.creator_id).first()[0]
        result.add_row([received_memo.id, received_memo.title, received_memo.content, author])
    return result


def get_received_memo_by_id(user: User, memo_id: int) -> Union[PrettyTable, str]:
    if not does_user_have_memo_in_inbox(user.id, memo_id):
        return "You don't have memo with this id in your inbox"
    result = PrettyTable()
    result.field_names = ["MEMO ID", "TITLE", "CONTENT", "AUTHOR"]
    memo = session.query(Memo).filter(Memo.id == memo_id).first()
    author = session.query(User.username).filter(User.id == memo.creator_id).first()[0]
    result.add_row([memo.id, memo.title, memo.content, author])
    return result


def delete_all_memos_from_inbox(user: User) -> None:
    session.query(SentMemo).filter(SentMemo.receiver_id == user.id).delete()
    session.commit()
    print("Finished")


def delete_memo_from_inbox_by_id(user: User, memo_ids: set) -> None:
    memos_to_delete = memo_ids
    for memo_id in memos_to_delete:
        if not does_user_have_memo_in_inbox(user.id, memo_id):
            print("You don't have memo with id {} in your inbox. Ommited.".format(memo_id))
            continue
        session.query(SentMemo).filter(SentMemo.memo_id == memo_id).delete()
        session.commit()
    print("Finished")
