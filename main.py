import csv
from usedMethods import clear_terminal
from PyInquirer import prompt
from rich import print
from rich.console import Console
from rich.table import Table
from rich import box

logged_user_phoneNumber = ""
logged_user_fullName = ""


# this method searches for username and password of users
def user_login(username, password):
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username and line[3] == password:
                return True
        return False


# this method checks if new username exist in file or not
def check_username_validity(username):
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username:
                return False
        return True


# this method checks if new phone number exist in file or not
def check_number_validity(number):
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[1] == number:
                return False
        return True


def add_info_to_file(name, number, username, password):
    with open("information.txt", "a") as infoFile:
        new_info = "\n" + name + "," + number + "," + username + "," + password
        infoFile.write(new_info)


def find_user_info(username):
    global logged_user_fullName, logged_user_phoneNumber
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username:
                logged_user_fullName = line[0]
                logged_user_phoneNumber = line[1]


# this is the method for first list options that user will see when run the code and can choose login / sign up or exit
def first_menu():
    questions = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'Please choose an option:',
            'choices': [
                'Login',
                'Sign up',
                'Exit',
            ]
        }
    ]
    answers = prompt(questions)
    choice = answers['option']

    if choice == 'Login':
        clear_terminal()
        login_page()
    elif choice == 'Sign up':
        clear_terminal()
        signup_page()
    elif choice == 'Exit':
        print('Exiting...')
        return


# this method will execute when admin logged in
def admin_main_page():
    pass


# this method will execute when user logged in
def user_main_page():
    pass


# gets user inputs for sign up and return them
def signup_page_inputs():
    console = Console()
    console.rule("[bold italic royal_blue1]    Sign up    ")
    print("[italic bold turquoise2] Please enter your information")
    fields = [
        {
            'type': 'input',
            'name': 'Name',
            'message': 'Full Name : '
        },
        {
            'type': 'input',
            'name': 'PhoneNumber',
            'message': 'Phone Number : '
        },
        {
            'type': 'input',
            'name': 'Username',
            'message': 'Username : '
        },
        {
            'type': 'password',
            'name': 'Password',
            'message': 'Password : '
        }
    ]
    user_inputs = prompt(fields)
    return user_inputs


# checks the inputs validity and if was ok save them in file and return to log in
def signup_page():
    user_inputs = signup_page_inputs()
    while not check_username_validity(user_inputs["Username"]):
        print("[bold red] Username invalid. try again[/]")
        user_inputs = signup_page_inputs()
    while not check_number_validity(user_inputs["PhoneNumber"]):
        print("[bold red] Phone Number invalid. try again[/]")
        user_inputs = signup_page_inputs()
    print("[bold green1]sign up complete... Please Login now[/]")
    add_info_to_file(user_inputs['Name'], user_inputs['PhoneNumber'], user_inputs['Username'], user_inputs['Password'])
    login_page()


# this method will execute when user choose login from first menu
def login_page():
    console = Console()
    console.rule("[bold italic royal_blue1]    Login    ")
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
        admin_main_page()
    else:
        is_user = user_login(user_inputs["username"], user_inputs["password"])
        if is_user:
            user_main_page()
            find_user_info(user_inputs["username"])
        else:
            # add options here
            print("not found")


def main():
    clear_terminal()
    # making the header for when user runs the code
    first_page = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    first_page.add_column("WELCOME TO RESERVATION SYSTEM", justify="center", style="magenta3")
    first_page.add_row("Choose one of the options below")
    console = Console()
    console.print(first_page)
    first_menu()


if __name__ == "__main__":
    main()
