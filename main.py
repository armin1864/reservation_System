import csv
from usedMethods import clear_terminal
from PyInquirer import prompt
from rich import print
from rich.layout import Layout


def user_login(username, password):
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username and line[3] == password:
                return True
        return False


def login_page():
    clear_terminal()

    layout = Layout()
    print(layout)

    admin_username = "4[)m1n$P49[-"
    admin_password = "?4$$4[)JVI1^/"
    fields = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Username : '
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Password : '
        }
    ]
    user_inputs = prompt(fields)
    if user_inputs["username"] == admin_username and user_inputs["password"] == admin_password:
        print("welcome admin !!!")
    else:
        is_user = user_login(user_inputs["username"], user_inputs["password"])
        if is_user:
            print("hello user !!!")
        else:
            print("not found")


def main():
    login_page()


if __name__ == "__main__":
    main()
