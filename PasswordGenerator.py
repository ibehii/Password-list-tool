#  ____       _
# | __ )  ___| |__  _ __   __ _ _ __ ___
# |  _ \ / _ \ '_ \| '_ \ / _` | '_ ` _  \
# | |_) |  __/ | | | | | | (_| | | | | | |
# |____/ \___|_| |_|_| |_|\__,_|_| |_| |_|

#  GitHub: https://github.com/beh185
#  Telegram: https://T.me/dr_xz
#  e-mail: BehnamH.dev@gmail.com
#  ____________________________________________

#import part
from os import name, system, path
from colorama import Fore, init
from random import choice, randint
from pathlib import Path
from shutil import move
import urllib.request
import pyfiglet

init()

# functions
# clear screen


def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


# for adding characters to this list (in forward this change to list)
passwords_list = ''


def symbols():
    characters = '!@#$%^&*='
    global passwords_list
    passwords_list = passwords_list + characters


def numbers():
    characters = '1234567890'
    global passwords_list
    passwords_list = passwords_list + characters


def lowercase():
    characters = 'abcdefghijklmnopqrstuvwxyz'
    global passwords_list
    passwords_list = passwords_list + characters


def uppercase():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    global passwords_list
    passwords_list = passwords_list + characters


def Ambiguous():
    characters = '{}[]()/\\\'"`~,;:.<>'
    global passwords_list
    passwords_list = passwords_list + characters

# making functions to if passwords.txt exist adding number at end of it


def rename_if_file_exists(file_name_number):
    file_name_number = file_name_number
    while path.exists('passwords{number}.txt'.format(number=str(file_name_number))):
        file_name_number += 1
    global file_name
    file_name = 'passwords{number}.txt'.format(
        number=str(file_name_number))


def exists_checker(the_path):
    if not path.exists(the_path):
        raise FileExistsError(
            Fore.RED + f'"{the_path}" is not exists. Enter file name correctly !' + Fore.RESET)


# check if user install pyfiglet ANSI Shadow font
pyfiglet_path = pyfiglet.__file__.replace('__init__.py', 'fonts/')
if not path.exists(pyfiglet_path + 'ANSI Shadow.flf'):
    download_permistion = input(
        Fore.RED + 'require font for this script is not installed. Do you want to download it ? [Y/n] ')
    if download_permistion == 'y' or download_permistion == 'Y' or download_permistion == 'yes' or download_permistion == 'Yes' or download_permistion == 'YES' or download_permistion == 'yEs' or download_permistion == 'yeS' or download_permistion == 'yES' or download_permistion == '':
        print(Fore.GREEN + 'Downloading ... ' + Fore.RESET)
        urllib.request.urlretrieve(
            "https://github.com/xero/figlet-fonts/raw/master/ANSI%20Shadow.flf", 'ANSI Shadow.flf')

        move('ANSI Shadow.flf', pyfiglet_path+'ANSI Shadow.flf')
    else:
        exit('This font is require for run this script. please install it first.')

clear_screen()
# first menu
print(Fore.YELLOW + pyfiglet.figlet_format('Password tool', font='ANSI Shadow') + Fore.GREEN +
      '''[1] - Just one password  
[2] - Generate multiple passwords
[3] - sort password list
[4] - delete duplicate password in password list
[5] - add password lists together\n''' + Fore.RESET)

first_menu_choice = int(
    input(Fore.MAGENTA + '⹃ Enter number of your choice -> ' + Fore.RESET))

clear_screen()

# one password
if(first_menu_choice == 1):
    # second menu for "just one password"
    print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow') + Fore.GREEN + '''[1] - Include Symbols ( e.g. !@#$%^&* )
[2] - Include Numbers ( e.g. 12345 )
[3] - Include Lowercase Characters ( e.g. abcdefgh )
[4] - Include Uppercase Characters ( e.g. ABCDEFGH )
[5] - Include Ambiguous Characters( e.g. { } [ ] ( ) / \ ' " ` ~ , ; : . < > )
''' + Fore.RESET)
    second_menu_choice = input(
        Fore.MAGENTA + ' ⹃ Enter number of your choices. e.g : 1 2 5 -> ' + Fore.RESET)
    # check if user Enter their choice correctly
    second_menu_choice = list(second_menu_choice)
    if '1' in second_menu_choice:
        if second_menu_choice.count('1') != 1:
            exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

    if '2' in second_menu_choice:
        if second_menu_choice.count('2') != 1:
            exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

    if '3' in second_menu_choice:
        if second_menu_choice.count('3') != 1:
            exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

    if '4' in second_menu_choice:
        if second_menu_choice.count('4') != 1:
            exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

    if '5' in second_menu_choice:
        if second_menu_choice.count('5') != 1:
            exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

        list_for_check_superfluous = list(
            '!@#$%^&*=67890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]()/\'"`~,;:.<>')
        for i in list_for_check_superfluous:
            if i in second_menu_choice:
                exit(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)

    # make passwords_list complete
    if ('1' in second_menu_choice):
        symbols()
    if ('2' in second_menu_choice):
        numbers()
    if('3' in second_menu_choice):
        lowercase()
    if('4' in second_menu_choice):
        uppercase()
    if('5' in second_menu_choice):
        Ambiguous()

    # changing to list to use choice meted
    passwords_list = list(passwords_list)

    clear_screen()
    #third menu
    print(Fore.YELLOW + pyfiglet.figlet_format('passwords',
          font='ANSI Shadow') + Fore.RESET)
    password_length = int(
        input(Fore.BLUE + '⹃ Enter password length -> ' + Fore.RESET))

    # the password
    generated_password = ''

    # Generating password
    for _ in range(password_length):
        letter = choice(passwords_list)
        generated_password = generated_password + letter
    print(Fore.BLUE + 'Your password is : ' + generated_password + Fore.RESET)

# multiple passwords
elif (first_menu_choice == 2):
    # second menu for "multiple passwords"
    print(Fore.YELLOW + pyfiglet.figlet_format('multiple password', font='ANSI Shadow') + Fore.GREEN + '''[1] - Include Symbols ( e.g. !@#$%^&* )
[2] - Include Numbers ( e.g. 12345 )
[3] - Include Lowercase Characters ( e.g. abcdefgh )
[4] - Include Uppercase Characters ( e.g. ABCDEFGH )
[5] - Include Ambiguous Characters( e.g. { } [ ] ( ) / \ ' " ` ~ , ; : . < > )
''' + Fore.RESET)
    second_menu_choice = input(
        Fore.MAGENTA + ' ⹃ Enter number of your choice. e.g : 1 2 5 -> ' + Fore.RESET)

    # check if user Enter their choice correctly
    second_menu_choice = list(second_menu_choice)
    if '1' in second_menu_choice:
        if second_menu_choice.count('1') != 1:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()
    if '2' in second_menu_choice:
        if second_menu_choice.count('2') != 1:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()

    if '3' in second_menu_choice:
        if second_menu_choice.count('3') != 1:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()

    if '4' in second_menu_choice:
        if second_menu_choice.count('4') != 1:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()
    if '5' in second_menu_choice:
        if second_menu_choice.count('5') != 1:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()
    list_for_check_superfluous = list(
        '!@#$%^&*=67890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]()/\'"`~,;:.<>')

    for i in list_for_check_superfluous:
        if i in second_menu_choice:
            print(Fore.RED + 'Please, Enter number from menu correctly and separate them with space (e.g : 1 2 5)' + Fore.RESET)
            exit()
    # make passwords_list complete
    if ('1' in second_menu_choice):
        symbols()
    if ('2' in second_menu_choice):
        numbers()
    if('3' in second_menu_choice):
        lowercase()
    if('4' in second_menu_choice):
        uppercase()
    if('5' in second_menu_choice):
        Ambiguous()

    # changing to list to use choice meted
    passwords_list = list(passwords_list)

    clear_screen()
    #third menu
    print(Fore.YELLOW + pyfiglet.figlet_format('password',
          font='ANSI Shadow') + Fore.RESET)
    password_number = int(
        input(Fore.BLUE + 'Enter how many passwords do you want to generate -> '))
    password_length = int(
        input(Fore.BLUE + '⹃ Enter password length -> ' + Fore.RESET))
    print(Fore.BLUE + 'On it ... ' + Fore.RESET)
    # the password
    generated_passwords = []
    temp_generated_password = ''
    # first 'for' is for number of password that must generate
    for _ in range(password_number):
        # second 'for' is for length of password that must generate
        for _1 in range(password_length):
            temp_generated_password += choice(passwords_list)
        generated_passwords.append(temp_generated_password)
        temp_generated_password = ''
    # this variable is related to rename_if_file_exists functions and the value of this variable is name of the file
    file_name = 'passwords.txt'
    if path.exists('passwords.txt'):
        rename_if_file_exists(1)

    # add generated passwords to file
    with open(file_name, 'w') as fn:
        the_passwords = '\n'.join(generated_passwords)
        fn.write(the_passwords)
        fn.close()
    print(Fore.YELLOW + '\nYour file save as : ' + file_name + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)

# sort password list
elif first_menu_choice == 3:
    print(Fore.YELLOW + pyfiglet.figlet_format('sort password',
          font='ANSI Shadow') + Fore.RESET)
    file_name = input(
        Fore.MAGENTA + '⹃ Enter name of your password list [It\'s better to enter complete path of it] -> ' + Fore.RESET)
    exists_checker(file_name)
    print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
    fn = open(file_name, 'r')
    sorted_fn = fn.readlines()

    for item in sorted_fn:
        if '\n' not in item and item != '':
            sorted_fn.remove(item)
            sorted_fn.append(item+'\n')
    # sort list
    sorted_fn.sort()

    # make list to string
    sorted_fn = ''.join(sorted_fn)
    # add it to file
    fn = open(file_name, 'w')
    fn.write(sorted_fn)
    fn.close()
    print(Fore.GREEN + '\n- Your password list is sorted' + Fore.RESET)


# delete duplicate
elif first_menu_choice == 4:
    # make menu
    print(Fore.YELLOW + pyfiglet.figlet_format('duplicate remover',
          font='ANSI Shadow') + Fore.RESET)
    which_meted = int(input(
        Fore.GREEN + '[1] - stable meted [slow]\n[2] - unstable meted [fast]\n\n- Please, enter number of your choice -> ' + Fore.RESET))
    file_name = input(
        Fore.MAGENTA + '\n⹃ Enter name of your password list [It\'s better to enter complete path of it] -> ' + Fore.RESET)
    # check if the file exists | this functions defined in line 68
    exists_checker(file_name)
    if which_meted == 1:
        fn = open(file_name, 'r')
        the_file_content = fn.readlines()
        # adding '\n' to last item till all of item have '\n'
        last_fn_item = the_file_content.pop()
        last_fn_item = str(last_fn_item) + '\n'
        the_file_content.append(last_fn_item)
        # notice user if their system can handle the file
        if len(the_file_content) > 1500000:
            print(
                Fore.RED + '\nThe file is large ! It\'s may take long time. It\'s better to use strong system.')
            system_permistion = input(
                Fore.GREEN + 'Do you want to continue ? [y/N] ' + Fore.RESET)
            if system_permistion == 'y' or system_permistion == 'Y' or system_permistion == 'yes' or system_permistion == 'Yes' or system_permistion == 'YES' or system_permistion == 'yEs' or system_permistion == 'yeS' or system_permistion == 'yES':
                print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)

                # removing duplicate in list
                for i in the_file_content:
                    count_i = the_file_content.count(i)
                    if the_file_content.count(i) != 1:
                        for k in range(count_i-1):
                            the_file_content.remove(i)
            else:
                exit(Fore.LIGHTRED_EX + '\nExiting ... ' + Fore.RESET)

    elif which_meted == 2:
        print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
        fn = open(file_name, "r")
        the_file_content = fn.readlines()
        # make it set because set don't keep 2 same thing on itself
        the_file_content = set(the_file_content)
        the_file_content = list(the_file_content)
        the_file_content = "".join(the_file_content)
        fn = open(file_name, "w")
        fn.write(the_file_content)
        fn.close()
        print("The duplicate passwords are now deleted")
    else:
        exit(Fore.RED + "Please enter name of the file correctly" + Fore.RESET)
    # make the list string and put it into file
    fn_str = ''.join(the_file_content)
    fn_w = open(file_name, 'w')
    fn_w.write(fn_str)
    fn_w.close()
    print(Fore.YELLOW + '\nYour file save as : ' + file_name + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)

# adding password list together
elif first_menu_choice == 5:
    print(Fore.YELLOW + pyfiglet.figlet_format('extend password',
          font='ANSI Shadow') + "𝒍𝒊𝒔𝒕" + Fore.RESET)

    # getting all file name from user
    all_password_list_name = []
    all_password_list_content = []
    file_name = input(
        Fore.MAGENTA + '\n- Enter your file name -> ' + Fore.RESET)
    all_password_list_name.append(file_name)
    # getting name of the file from user
    status = True
    input_number = 2
    while status == True:
        file_name = input(
            Fore.MAGENTA + f'{input_number} - Enter your file name -> ' + Fore.RESET)
        all_password_list_name.append(file_name)
        user_request = input(
            Fore.YELLOW + '\nDo you have anymore password list ? [Y/n] ' + Fore.RESET)
        if user_request == 'y' or user_request == 'Y' or user_request == 'yes' or user_request == 'Yes' or user_request == 'YES' or user_request == 'yEs' or user_request == 'yeS' or user_request == 'yES' or user_request == '':
            clear_screen()
            print(Fore.YELLOW + pyfiglet.figlet_format('extend password',
                  font='ANSI Shadow') + "𝒍𝒊𝒔𝒕" + Fore.RESET)
            input_number += 1
        else:
            status == False
            break
    print(Fore.BLUE + 'On it ... ' + Fore.RESET)
    # check if all of the name are exists
    for i in all_password_list_name:
        exists_checker(i)
    # open all file and adding them to one list.
    for file_name in all_password_list_name:
        password_list = open(file_name, 'r')
        password_list = password_list.readlines()
        all_password_list_content.extend(password_list)
    # adding '\n' to all of the item because some of them have and some of them not and in removing duplicate we go to problem
    for item in all_password_list_content:
        if '\n' not in item and item != '':
            all_password_list_content.remove(item)
            all_password_list_content.append(item+'\n')
    # set file name
    file_name = 'passwords.txt'
    if path.exists('passwords.txt'):
        rename_if_file_exists(1)
    password_list = open(file_name, 'w')
    all_password_list_content = ''.join(all_password_list_content)
    password_list.write(all_password_list_content)

    print(Fore.YELLOW + 'Your file save as : ' + file_name + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)
else:
    print(Fore.RED + 'Please, Enter number correctly !' + Fore.RESET)
