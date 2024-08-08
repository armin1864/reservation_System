import csv
from PyInquirer import prompt
from rich import print
from rich.console import Console
from rich.table import Table
from rich import box
import time
import os


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# this to vars will use for save logged-in user's reserve and show her/him its own reserves
logged_user_phoneNumber = ""
logged_user_fullName = ""


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


# method for write user Information into file
def add_info_to_file(name, number, username, password):
    with open("information.txt", "a") as infoFile:
        new_info = "\n" + name + "," + number + "," + username + "," + password
        infoFile.write(new_info)


# gets a username and return full name and number ( they will be used for save reserved times in files)
def find_user_info(username):
    global logged_user_fullName, logged_user_phoneNumber
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username:
                logged_user_fullName = line[0]
                logged_user_phoneNumber = line[1]


# checks if specific date and time exist in free times or not , if exist return false , and if isn't return true
def free_times_check(new_date, new_time):
    with open("freeTimes.txt", "r") as freeTimes:
        csv_reader = csv.reader(freeTimes)
        for line in csv_reader:
            if line[0] == new_date and line[1] == new_time:
                return False
    return True


# checks if specific date and time exist in reserved times or not , if exist return false , and if isn't return true
def reserved_times_check(new_date, new_time):
    with open("reservedTimes.txt", "r") as reservedTimes:
        csv_reader = csv.reader(reservedTimes)
        for line in csv_reader:
            if line[1] == new_date and line[2] == new_time:
                return False
    return True


# show reserved times in table
def admin_view_reserves():
    clear_terminal()
    reserved_times_tabel = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    reserved_times_tabel.add_column("Phone Number", justify="center", style="grey78")
    reserved_times_tabel.add_column("Date", justify="center", style="yellow2")
    reserved_times_tabel.add_column("Time", justify="center", style="green1")
    reserved_times_tabel.add_column("Fee", justify="center", style="orchid1")
    with open("reservedTimes.txt", "r") as reserves:
        csv_reader = csv.reader(reserves)
        next(csv_reader)
        for line in csv_reader:
            reserved_times_tabel.add_row(line[0], line[1], line[2], line[3])
    console = Console()
    console.print(reserved_times_tabel)
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': '  ',
            'choices': [
                '<- back',
            ]
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == '<- back':
        admin_main_page()


# gets new date time and price from admin and if wasn't already exist , add them into free times
def admin_add_reserve():
    console = Console()
    console.rule("[bold italic yellow1]    Add time for Reserve   ")
    new_date = console.input("[italic violet] Enter new reservation date (dd/mm/yyyy) : ")
    new_time = console.input("[italic violet] Enter new reservation hour (hh:mm) : ")
    new_price = console.input("[italic violet] Enter new reservation price : ")
    submiting = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'are you sure you want to add this date and time ? ',
            'choices': [
                'Yes',
                'No'
            ]
        }
    ]
    answer = prompt(submiting)
    choiced = answer['option']
    if choiced == 'No':
        admin_main_page()
    else:
        if free_times_check(new_date, new_time) and reserved_times_check(new_date, new_time):
            with open("freeTimes.txt", "a") as freeTimes:
                freeTimes.write(new_date + "," + new_time + "," + new_price + "\n")
            print("[bold green]New reserve time add successfully... redirecting...")
            time.sleep(3)
            admin_main_page()
        else:
            print("[bold red]this date and time already exist. try another one")
            admin_add_reserve()


# this method will execute when admin logged in
def admin_main_page():
    clear_terminal()
    admin_home_page = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    admin_home_page.add_column(f"WELCOME ADMIN", justify="center", style="magenta3")
    admin_home_page.add_row("Choose one of the options below")
    console = Console()
    console.print(admin_home_page)
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'Please choose an option:',
            'choices': [
                'Add reserve time',
                'View reserves',
                'Exit',
            ]
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == 'Add reserve time':
        clear_terminal()
        admin_add_reserve()
    elif choice == 'View reserves':
        admin_view_reserves()
    elif choice == 'Exit':
        print("Exiting...")


# if user wants to change password this method runs and change users password in file
def user_change_password():
    console = Console()
    password = console.input("[italic violet] Enter new password : ")
    re_enter_password = console.input("[italic violet] re-enter new password : ")
    if password == re_enter_password:
        global logged_user_phoneNumber
        new_info = ""
        with open("information.txt", "r") as infoFile:
            csv_reader = csv.reader(infoFile)
            for line in csv_reader:
                if line[1] != logged_user_phoneNumber:
                    new_info += ','.join(line) + "\n"
                elif line[1] == logged_user_phoneNumber:
                    new_info += line[0] + "," + line[1] + "," + line[2] + "," + password + "\n"
        with open("information.txt", "w") as newInfoFile:
            newInfoFile.write(new_info)
        print("[bold green]password changed successfully. redirecting... ")
        time.sleep(3)
        user_main_page()
    else:
        console.print("[bold red] passwords dont match try again")
        user_change_password()


# if user wants to change username , this gets a new username and if it valid , change the username in file
def user_change_username():
    console = Console()
    new_username = console.input("[italic violet] Enter new Username : ")
    submiting = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'are you sure you want to change username ? ',
            'choices': [
                'Yes',
                'No'
            ]
        }
    ]
    answer = prompt(submiting)
    choiced = answer['option']
    if choiced == 'No':
        user_main_page()
    elif choiced == 'Yes':
        if check_username_validity(new_username):
            global logged_user_phoneNumber
            new_info = ""
            with open("information.txt", "r") as infoFile:
                csv_reader = csv.reader(infoFile)
                for line in csv_reader:
                    if line[1] != logged_user_phoneNumber:
                        new_info += ','.join(line) + "\n"
                    elif line[1] == logged_user_phoneNumber:
                        new_info += line[0] + "," + line[1] + "," + new_username + "," + line[3] + "\n"
            with open("information.txt", "w") as newInfoFile:
                newInfoFile.write(new_info)
            print("[bold green]username changed successfully. redirecting... ")
            time.sleep(3)
            user_main_page()
        else:
            print('[bold red]this username is invalid . try another')
            user_change_username()


# give user options for change username or password
def user_change_info():
    clear_terminal()
    console = Console()
    console.rule("[bold italic yellow1]    Change information   ")
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'which info you want to change ? ',
            'choices': ['Username', 'Password', '<- back']
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == 'Username':
        user_change_username()
    elif choice == 'Password':
        user_change_password()
    else:
        user_main_page()


# add a new time for reserve into free times file
def add_time_to_free_times(new_time):
    with open("freeTimes.txt", "a") as freeTimes:
        freeTimes.write("\n" + new_time)


# execute when user wants to cancel a reserve ; delete time from reserves and add it again to free times
def user_cancel_reserve():
    global logged_user_phoneNumber
    user_times = []
    with open("reservedTimes.txt", "r") as timesFile:
        csv_reader = csv.reader(timesFile)
        next(csv_reader)
        for line in csv_reader:
            if line[0] == logged_user_phoneNumber:
                user_times.append(line[1] + "," + line[2] + "," + line[3])
    user_times.append("<- back")
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'which time you want to cancel ? ',
            'choices': user_times
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == "<- back":
        user_main_page()
    else:
        print("your choice is : ", choice)
        submiting = [
            {
                'type': 'list',
                'name': 'option',
                'message': 'are you sure about canceling this time ? ',
                'choices': [
                    'Yes',
                    'No'
                ]
            }
        ]
        answer = prompt(submiting)
        choiced = answer['option']
        if choiced == 'No':
            time.sleep(3)
            user_reserved_times()
        elif choiced == 'Yes':
            with open("reservedTimes.txt", "r") as freeTimes:
                lines = freeTimes.readlines()
            with open("reservedTimes.txt", "w") as freeTimes:
                for line in lines:
                    if line.strip("\n") != choice:
                        freeTimes.write(line)
            add_time_to_free_times(choice)
            print("Reserve Canceled.  redirecting...")
            time.sleep(3)
            user_main_page()


# shows users reserved times and give her/him option for cancel a reserve
def user_reserved_times():
    clear_terminal()
    global logged_user_phoneNumber
    my_times_tabel = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    my_times_tabel.add_column("Date", justify="center", style="yellow2")
    my_times_tabel.add_column("Time", justify="center", style="green1")
    my_times_tabel.add_column("Fee", justify="center", style="orchid1")
    with open("reservedTimes.txt", "r") as reserves:
        csv_reader = csv.reader(reserves)
        for line in csv_reader:
            if line[0] == logged_user_phoneNumber:
                my_times_tabel.add_row(line[1], line[2], line[3])
    console = Console()
    console.print(my_times_tabel)
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': '  ',
            'choices': [
                'cancel a reserve',
                '<- back',
            ]
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == 'cancel a reserve':
        user_cancel_reserve()
    elif choice == '<- back':
        user_main_page()


# this method gets a time and delete it from free times  ( when a time get reserved )
def delete_time_from_file(reserved_time):
    with open("freeTimes.txt", "r") as freeTimes:
        lines = freeTimes.readlines()
    with open("freeTimes.txt", "w") as freeTimes:
        for line in lines:
            if line.strip("\n") != reserved_time:
                freeTimes.write(line)


# will execute when user wants to reserve a time ; gets a time , add it to reserved times and remove it from free times
def user_reserving_time():
    available_times = []
    with open("freeTimes.txt", "r") as timesFile:
        csv_reader = csv.reader(timesFile)
        next(csv_reader)
        for line in csv_reader:
            available_times.append(",".join(line))
    available_times.append("<- back")
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'which time you want to reserve ? ',
            'choices': available_times
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == "<- back":
        user_main_page()
    else:
        print("your choice is : ", choice)
        submiting = [
            {
                'type': 'list',
                'name': 'option',
                'message': 'are you sure about reserving this time ? ',
                'choices': [
                    'Yes',
                    'No'
                ]
            }
        ]
        answer = prompt(submiting)
        choiced = answer['option']
        if choiced == 'No':
            time.sleep(3)
            user_available_times()
        elif choiced == 'Yes':
            global logged_user_phoneNumber
            with open("reservedTimes.txt", "a") as reserved_times:
                new_line = "\n" + logged_user_phoneNumber + "," + choice
                reserved_times.write(new_line)
            print("[bold green] Time reserved!..")
            delete_time_from_file(choice)
            time.sleep(3)
            user_main_page()


# this method will show the available times to the user if she/he wants to reserve direct him to reserve method
def user_available_times():
    clear_terminal()
    available_times_tabel = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    available_times_tabel.add_column("Date", justify="center", style="yellow2")
    available_times_tabel.add_column("Time", justify="center", style="green1")
    available_times_tabel.add_column("Fee", justify="center", style="orchid1")
    with open("freeTimes.txt", "r") as timesFile:
        csv_reader = csv.reader(timesFile)
        next(csv_reader)
        for line in csv_reader:
            available_times_tabel.add_row(line[0], line[1], line[2])
    console = Console()
    console.print(available_times_tabel)
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': '  ',
            'choices': [
                'reserve time',
                '<- back',
            ]
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == 'reserve time':
        user_reserving_time()
    elif choice == '<- back':
        user_main_page()


# this method will execute when user logged in
def user_main_page():
    clear_terminal()
    global logged_user_fullName
    user_home_page = Table(expand=True, style="cyan", box=box.DOUBLE_EDGE)
    user_home_page.add_column(f"WELCOME {logged_user_fullName}", justify="center", style="magenta3")
    user_home_page.add_row("Choose one of the options below")
    console = Console()
    console.print(user_home_page)
    options = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'Please choose an option:',
            'choices': [
                'available times',
                'my reserved times',
                'change information',
                'Exit',
            ]
        }
    ]
    answers = prompt(options)
    choice = answers['option']
    if choice == 'available times':
        user_available_times()
    elif choice == 'my reserved times':
        user_reserved_times()
    elif choice == 'change information':
        user_change_info()
    elif choice == 'Exit':
        print("Exiting...")


# gets user inputs for sign up and return them
def signup_page_inputs():
    console = Console()
    console.rule("[bold italic yellow1]    Sign up    ")
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


# this method searches for username and password of users
def user_login(username, password):
    with open("information.txt", "r") as infoFile:
        csv_reader = csv.reader(infoFile)
        for line in csv_reader:
            if line[2] == username and line[3] == password:
                return True
        return False


# this method will execute when user choose login from first menu
def login_page():
    console = Console()
    console.rule("[bold italic yellow1]    Login    ")
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
            find_user_info(user_inputs["username"])
            user_main_page()
        else:
            print("[bold red]User not found...try again[/]")
            time.sleep(2)
            main()


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
