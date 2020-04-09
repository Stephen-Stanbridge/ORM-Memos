import os
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from termcolor import colored
from Services.command_line import execute
from Models.models import User
from Handlers.User import login_or_register
import argparse
from prompt_toolkit.formatted_text import HTML

parser = argparse.ArgumentParser(description="Login to memos' server.")
parser.add_argument('username', type=str, nargs="+", help="Your username")
parser.add_argument('password', type=str, nargs="+", help="Your password")
args = parser.parse_args()

user = login_or_register(args.username[0], args.password[0])


def bottom_toolbar():
    return HTML('<style bg="ansired">Memos server</style>')


if user:
    os.system('clear')
    print("Welcome to your dashboard", colored(user.username.capitalize(), "green"))
    print("Type 'help' for available commands.")
    print("To exit application use 'exit' command.")
    while 1:
        user_input = prompt('--> ', history=FileHistory('.memo_history'), bottom_toolbar=bottom_toolbar())
        execute(user_input, user)
