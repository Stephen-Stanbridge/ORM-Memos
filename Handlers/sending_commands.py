from SQL.setup_db import Session
import ConfigClasses.classes as config_class
from Models.models import User, SentMemo, Memo
from typing import Union, Tuple
session = Session()


def does_user_exist(receiver_id: int) -> Union[bool, Tuple]:
    query = session.query(User).filter(User.id == receiver_id).first()
    if query is None:
        return False, "No user with id {}.".format(receiver_id)
    return True


def make_checks(config: config_class.SendMemo) -> Union[bool, Tuple[bool, str]]:
    memo_id, user, receiver_id = config.memo_id, config.user, config.receiver
    memo_belongs_to_user = session.query(Memo).filter(Memo.id == memo_id, Memo.creator_id == user.id).first()
    if memo_belongs_to_user is None:
        return False, "You don't own memo with this id."
    memo_was_already_sent_to_user = session.query(SentMemo).filter(SentMemo.memo_id == memo_id,
                                                                   SentMemo.receiver_id == receiver_id).first()
    if memo_was_already_sent_to_user is not None:
        return False
    return True


def send_memo(config: config_class.SendMemo) -> None:
    memo_id, receiver_id = config.memo_id, config.receiver
    memo_to_send = SentMemo(memo_id=memo_id, receiver_id=receiver_id)
    session.add(memo_to_send)
    session.commit()
    set_to_sent = session.query(Memo).filter(Memo.id == memo_id).first()
    if not set_to_sent.sent:
        set_to_sent.sent = True
        session.commit()


def send_memo_to_all(user: User, memo_id: int) -> None:
    query = session.query(User.id).filter(User.id != user.id).all()
    all_users = [user_id[0] for user_id in query]
    config = config_class.SendMemo()
    config.memo_id, config.user = memo_id, user
    for receiver in all_users:
        config.receiver = receiver
        checks = make_checks(config)
        if isinstance(checks, tuple):
            print(checks[1])
            break
        elif checks:
            send_memo(config)
        else:
            continue
    print("Finished.")


def send_memo_to_users(config: config_class.SendMemo) -> None:
    memo_id, user, receivers = config.memo_id, config.user, config.receiver
    if user.id in receivers:
        receivers.remove(user_id)
    for receiver in receivers:
        config.receiver = receiver
        checks = make_checks(config)
        is_user = does_user_exist(receiver)
        if isinstance(is_user, tuple):
            print(is_user[1])
            continue
        elif isinstance(checks, tuple):
            print(checks[1])
            break
        elif checks:
            send_memo(config)
        else:
            continue
    print("Finished.")
