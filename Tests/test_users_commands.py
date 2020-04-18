from conftest import does_table_contain_all_words
from Handlers.users_commands import get_list_of_all_users, username_from_id, id_from_username


def test_get_list_of_all_users(user, second_user):
    words = [user.username, second_user.username, str(user.id), str(second_user.id)]
    assert does_table_contain_all_words(words, get_list_of_all_users())
