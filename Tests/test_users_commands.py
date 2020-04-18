from conftest import does_table_contain_all_words
from Handlers.users_commands import get_list_of_all_users, username_from_id, id_from_username


def test_get_list_of_all_users(user, second_user):
    words = [user.username, second_user.username, str(user.id), str(second_user.id)]
    assert does_table_contain_all_words(words, get_list_of_all_users())


def test_username_from_id(user):
    words = [user.username]
    assert does_table_contain_all_words(words, username_from_id(user.id))
    assert username_from_id(100) == "No user with this id."


def test_id_from_username(user):
    words = [user.id]
    assert does_table_contain_all_words(words, username_from_id(user.username))
    assert id_from_username('username_does_not_exist') == "User with this username doesn't exist."
