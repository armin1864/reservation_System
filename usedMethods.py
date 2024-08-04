from rich import print
from PyInquirer import prompt
import os


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def menu():
    questions = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'Please choose an option:',
            'choices': [
                'available times for reservation',
                'my reserved times',
                'change information',
                'Log out'
            ]
        }
    ]

    answers = prompt(questions)
    choice = answers['option']

    if choice == 'available times for reservation':
        print('[reverse]You selected Option 1. [/]')
        print("[blue bold italic] choose one of times")
    elif choice == 'my reserved times':
        print('You selected Option 2.')
    elif choice == 'change information':
        print('You selected Option 3.')
    elif choice == 'Log out':
        print('Exiting...')
        return

    # Call main again to keep the menu running
    menu()
