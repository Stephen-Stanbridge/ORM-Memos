from Models.models import User
from typing import Union


class SendMemo:
    user: User
    memo_id: int
    receiver: Union[int, list]
