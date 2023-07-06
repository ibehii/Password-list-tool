#  ____       _
# | __ )  ___| |__  _ __   __ _ _ __ ___
# |  _ \ / _ \ '_ \| '_ \ / _` | '_ ` _  \
# | |_) |  __/ | | | | | | (_| | | | | | |
# |____/ \___|_| |_|_| |_|\__,_|_| |_| |_|

#  GitHub: https://github.com/beh185
#  Telegram: https://T.me/dr_xz
#  e-mail: Behii@tutanota.com
#  ____________________________________________

#import part
from os import name, system, path
from random import choice
from shutil import move
from time import sleep
from datetime import datetime
from urllib.request import urlretrieve
import json
try:
    from colorama import Fore, init
    import pyfiglet
    
except ImportError:
    print('Make sure that you are connected to internet!')
    sleep(3)
    system('pip install colorama')
    system('pip install pyfiglet')
    exit('> Run the program again!')
print(Fore.CYAN + "Please wait ..." + Fore.RESET)

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
    while path.exists(f'passwords{str(file_name_number)}.txt'):
        file_name_number += 1
    global file_name
    file_name = f'passwords{str(file_name_number)}.txt'


def exists_checker(the_path):
    if not path.exists(the_path):
        exit(
            Fore.RED + f'"{the_path}" is not exists. Enter file name correctly !' + Fore.RESET)


# check if user install pyfiglet ANSI Shadow font
if name == 'nt':
    pyfiglet_path = pyfiglet.__file__.replace('__init__.py', 'fonts\\')
else:
    pyfiglet_path = pyfiglet.__file__.replace('__init__.py', 'fonts/')
if not path.exists(pyfiglet_path + 'ANSI Shadow.flf'):
    download_permission = input(
        Fore.RED + '- Require font for this script is not installed. Do you want to download it ? [Y/n] ')
    if download_permission.lower() == 'y' or download_permission.lower() == 'yes' or download_permission == '':
        print(Fore.GREEN + 'Downloading ... ' + Fore.RESET)
        urlretrieve(
            "https://github.com/xero/figlet-fonts/raw/master/ANSI%20Shadow.flf", 'ANSI Shadow.flf')
        
        move('ANSI Shadow.flf', pyfiglet_path+'ANSI Shadow.flf')
    else:
        exit('This font is require for run this script. please install it first.')

clear_screen()
# first menu
print(Fore.YELLOW + pyfiglet.figlet_format('Password tool', font='ANSI Shadow') + Fore.GREEN +
      '''[1] - Just one password  
[2] - Generate password list
[3] - Sort password list
[4] - Delete duplicate password in password list
[5] - Merge password lists\n''' + Fore.RESET)
try:
    first_menu_choice = int(
        input(Fore.MAGENTA + '⹃ Enter number of your choice -> ' + Fore.RESET))
except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
except ValueError:
    exit(Fore.RED + 'Error ! Pay attention that your answer must be a number between 1-5.' + Fore.RESET)
    

clear_screen()

# one password
if(first_menu_choice == 1):
    # second menu for "just one password"
    print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow') +
          '[1] - Show previous passwords\n[2] - Generate password')
    try:
        second_menu_choice = int(input(Fore.GREEN + '\n⹃ Enter number of the part that you need -> ' + Fore.RESET)) 
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except ValueError:
            exit(Fore.RED + 'Error! Pay attention that your answer must be 1 or 2.')
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
    # Show previous passwords
    if second_menu_choice == 1:
        clear_screen()
        print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow'))
        try:
            password_key: str = input(
                Fore.MAGENTA + ' ⹃ Enter key of password -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        try:
            with open(__file__.replace('PasswordGenerator.py', 'Just_one_password.json'),'r') as fn:
                password_data = json.load(fn)
                print(Fore.MAGENTA + f'''The password is = {Fore.GREEN + password_data[password_key]['password'] + Fore.MAGENTA}
The year it was saved = {Fore.GREEN + str(password_data[password_key]['Year']) + Fore.MAGENTA}
The month it was saved = {Fore.GREEN + str(password_data[password_key]['month']) + Fore.MAGENTA}
The day it was saved = {Fore.GREEN + str(password_data[password_key]['day']) + Fore.MAGENTA}
The time it was saved = {Fore.GREEN + str(password_data[password_key]['hour']) + ':' + str(password_data[password_key]['min']) + Fore.MAGENTA}''' + Fore.RESET)
        except FileNotFoundError:
            exit(Fore.RED + 'Error! Data base didn\'t found.\nFirst generate some passwords and then use this part' + Fore.RESET) 
        except KeyError:
            exit(Fore.RED + "Error! The password's key wasn't correct. Try again. " + Fore.RESET)
    # Generate password
    elif second_menu_choice == 2: 
        clear_screen()
        print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow') + Fore.GREEN + '''[1] - Include Symbols ( e.g. !@#$%^&* )
[2] - Include Numbers ( e.g. 12345 )
[3] - Include Lowercase Characters ( e.g. abcdefgh )
[4] - Include Uppercase Characters ( e.g. ABCDEFGH )
[5] - Include Ambiguous Characters( e.g. { } [ ] ( ) / \ ' " ` ~ , ; : . < > )
    ''' + Fore.RESET)
        try:
            included_obj: str = input(
                Fore.MAGENTA + ' ⹃ Enter number of your choices. e.g : 1 2 5 -> ' + Fore.RESET).split()
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        # check if user Enter their choice correctly
        for items in included_obj:
            try:
                int(items)
            except ValueError:
                exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
            if len(items) != 1 or int(items) > 5:
                exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
        # make passwords_list complete
        if ('1' in included_obj):
            symbols()
        if ('2' in included_obj):
            numbers()
        if('3' in included_obj):
            lowercase()
        if('4' in included_obj):
            uppercase()
        if('5' in included_obj):
            Ambiguous()

        # changing to list to use choice method
        passwords_list = list(passwords_list)

        clear_screen()
        #third menu
        print(Fore.YELLOW + pyfiglet.figlet_format('passwords',
            font='ANSI Shadow') + Fore.RESET)
        try:
            password_length = int(
                input(Fore.BLUE + '⹃ Enter password length -> ' + Fore.RESET))
        except ValueError:
            exit(Fore.RED + 'Error! Your answer must be numbers')
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)


        # the password
        generated_password = ''

        # Generating password
        try:
            for _ in range(password_length):
                letter = choice(passwords_list)
                generated_password = generated_password + letter
        except KeyboardInterrupt:
                exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some thing went wrong try again!'+ Fore.RESET)
        print(Fore.BLUE + 'Your password is : ' + generated_password + Fore.RESET)

        if not path.exists(__file__.replace('PasswordGenerator.py', 'Just_one_password.json')):
            with open(__file__.replace('PasswordGenerator.py', 'Just_one_password.json'),'w') as f:
                password_data = {
                    'password_1':{'password': generated_password, 
                                'Year': datetime.today().year,
                                'month': datetime.now().strftime("%B"),
                                'day':datetime.now().strftime("%d"),
                                'hour':datetime.now().strftime("%H"),
                                'min':datetime.now().strftime("%M")
                                }
                }
                password_data = json.dump(password_data,f ,indent=4)
            print(Fore.LIGHTGREEN_EX + 'Your passwords by key of => ' + Fore.CYAN + 'password_1' + Fore.LIGHTGREEN_EX +
                   '\nUse this key to access the password on Just "one password/Show previous passwords" section' + Fore.RESET)
        else:
            with open(__file__.replace('PasswordGenerator.py', 'Just_one_password.json'),'r') as fn:
                password_data = json.load(fn)
                len_password_data = len(password_data)
                with open(__file__.replace('PasswordGenerator.py', 'Just_one_password.json'),'w') as fn:
                    password_data[f'password_{len_password_data+1}'] = {
                                'password': generated_password, 
                                'Year': datetime.today().year,
                                'month': datetime.now().strftime("%B"),
                                'day':datetime.now().strftime("%d"),
                                'hour':datetime.now().strftime("%H"),
                                'min':datetime.now().strftime("%M")}
                    password_data = json.dump(password_data,fn ,indent=4)
                
                print(Fore.LIGHTGREEN_EX + 'Your passwords by key of => ' + Fore.CYAN + f'password_{len_password_data+1}' + Fore.LIGHTGREEN_EX +
                 '\nUse this key to access the password on "Just one password/Show previous passwords" section' + Fore.RESET)
    else:
        exit(Fore.RED + 'Error! Please enter the number of the part that you need correctly!'+ Fore.RESET)                       
# password list 
elif (first_menu_choice == 2):
    # second menu for "multiple passwords"
    print(Fore.YELLOW + pyfiglet.figlet_format('Password list', font='ANSI Shadow') + Fore.GREEN + '''[1] - Include Symbols ( e.g. !@#$%^&* )
[2] - Include Numbers ( e.g. 12345 )
[3] - Include Lowercase Characters ( e.g. abcdefgh )
[4] - Include Uppercase Characters ( e.g. ABCDEFGH )
[5] - Include Ambiguous Characters( e.g. { } [ ] ( ) / \ ' " ` ~ , ; : . < > )
''' + Fore.RESET)
    try:
        included_obj: str = input(
            Fore.MAGENTA + ' ⹃ Enter number of your choices. e.g : 1 2 5 -> ' + Fore.RESET).split()
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
       # check if user Enter their choice correctly
           # check if user Enter their choice correctly
    for items in included_obj:
        try:
            int(items)
        except ValueError:
            exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
        if len(items) != 1 or int(items) > 5:
            exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
    # add obj that user want to password_list
    if ('1' in included_obj):
        symbols()
    if ('2' in included_obj):
        numbers()
    if('3' in included_obj):
        lowercase()
    if('4' in included_obj):
        uppercase()
    if('5' in included_obj):
        Ambiguous()

    # changing to list to use choice method
    passwords_list = list(passwords_list)

    clear_screen()
    #third menu
    print(Fore.YELLOW + pyfiglet.figlet_format('password',
          font='ANSI Shadow') + Fore.RESET)
    try:
        password_number = int(
            input(Fore.BLUE + 'Enter how many passwords do you want to generate -> '+ Fore.RESET))
        password_length = int(
            input(Fore.BLUE + '⹃ Enter passwords length -> ' + Fore.RESET))
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except ValueError:
        exit(Fore.RED + '\nError! Only numbers are acceptable.' + Fore.RESET)
    if (password_number > 500_000 or password_length > 100):
        print(Fore.RED + 'Warning! You are going to produce huge amount of passwords this may take a long time and takes memory' + Fore.RESET)
        sleep(3)
    print(Fore.BLUE + 'On it ... ' + Fore.RESET)
    try:
        # the password
        generated_passwords = set()
        temp_generated_password = str()
        # first 'for' is for number of password that must generate
        for _ in range(password_number):
            # second 'for' is for length of password that must generate
            for _1 in range(password_length):
                temp_generated_password += choice(passwords_list)
            generated_passwords.add(temp_generated_password)
            temp_generated_password = str()
        # this variable is related to rename_if_file_exists functions and the value of this variable is name of the file
        file_name = 'passwords.txt'
        if path.exists('passwords.txt'):
            rename_if_file_exists(1)

        # add generated passwords to file
        with open(__file__.replace('PasswordGenerator.py', file_name), 'w') as f:
            the_passwords = '\n'.join(generated_passwords)
            f.write(the_passwords)
            f.close()
        print(Fore.GREEN + '\nDone !' + Fore.RESET)
        sleep(0.5)
        print(Fore.BLUE + '\nDeleting duplicate passwords ...' + Fore.RESET)
        sleep(1.5)
        print(Fore.GREEN + '\nThe operation was successful!' + Fore.RESET)
        print(Fore.YELLOW + '\nPassword list save as : ' + __file__.replace('PasswordGenerator.py', file_name) + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except MemoryError:
        exit(Fore.RED + 'There is no available ram left. Try make password list with less passwords' + Fore.RED)

# sort password list
elif first_menu_choice == 3:
    print(Fore.YELLOW + pyfiglet.figlet_format('sort password',
          font='ANSI Shadow') + Fore.RESET)
    try:
        file_name = input(
            Fore.MAGENTA + '⹃ Enter your password list file path -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        
    exists_checker(file_name)
    print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
    with open(file_name, 'r') as f:
        sorted_fn : list = f.readlines()
        #The last line doesn't have \n so when it sorted it will connect to another item
        sorted_fn[-1] = sorted_fn[-1] +'\n'
        # sort list
        sorted_fn.sort()
        f.close()

    # make list to string so can write it in file
    sorted_fn = ''.join(sorted_fn)
    # add it to file
    fn = open(file_name, 'w')
    fn.write(sorted_fn)
    fn.close()
    print(Fore.GREEN + '\n- Your password list is sorted' + Fore.RESET)


# delete duplicate
elif first_menu_choice == 4:
    # menu
    print(Fore.YELLOW + pyfiglet.figlet_format('duplicate remover',
          font='ANSI Shadow') + Fore.RESET)
    try:
        try:
            which_method = int(input(
                Fore.GREEN + '[1] - Slow method [won\'t change the order]\n[2] - Fast method [change the order]\n\n- Please, enter number of your choice -> ' + Fore.RESET))
        except ValueError:
            exit(Fore.RED + '\nError! Only numbers are acceptable.' + Fore.RESET)
        file_name = input(
            Fore.MAGENTA + '\n⹃ Enter path of your password list -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        
    # check if the file exists | this functions defined in line 68
    exists_checker(file_name)
    print(Fore.YELLOW + 'Starting the operation' + Fore.RESET)
    if which_method == 1:
        fn = open(file_name, 'r')
        the_file_content = fn.readlines()
        #The last line doesn't have \n so when it sorted it will connect to another item
        the_file_content[-1] = the_file_content[-1] +'\n'
        # notice user if their system can handle the file
        if len(the_file_content) > 1_000_000:
            print(Fore.RED + 
                'Warning! You are going to produce huge amount of passwords this may take a long time and takes memory' + Fore.RESET)

            system_permission = input(
                Fore.GREEN + 'Do you want to continue ? [y/N] ' + Fore.RESET)
            if system_permission.lower() == 'y' or system_permission.lower() == 'yes':
                print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)

                # removing duplicate in list
                for i in the_file_content:
                    count_i = the_file_content.count(i)
                    if the_file_content.count(i) != 1:
                        for k in range(count_i-1):
                            the_file_content.remove(i)
                print(Fore.GREEN + "The duplicate passwords are now deleted" + Fore.RESET)
                
            else:
                exit(Fore.RED + '\nPermission denied!' + Fore.RESET)
        else:
            # removing duplicate in list
            for i in the_file_content:
                count_i = the_file_content.count(i)
                if the_file_content.count(i) != 1:
                    for k in range(count_i-1):
                        the_file_content.remove(i)
            print(Fore.GREEN + "The duplicate passwords are now deleted" + Fore.RESET)


    elif which_method == 2:
        print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
        fn = open(file_name, "r")
        # make it set because set don't keep 2 same thing on itself
        the_file_content = set(fn.readlines())
        print(Fore.GREEN + "The duplicate passwords are now deleted" + Fore.RESET)
    else:
        exit(Fore.RED + "Please enter the number of the part that you need correctly!" + Fore.RESET)
    # make the list string and put it into file
    the_file_content = "".join(the_file_content)
    fn_w = open(file_name, 'w')
    fn_w.write(the_file_content)
    fn_w.close()
    print(Fore.YELLOW + '\nYour file save as : ' + file_name + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)

# adding password list together
elif first_menu_choice == 5:
    print(Fore.YELLOW + pyfiglet.figlet_format('Pass list merger',
            font='ANSI Shadow') + Fore.RESET)
    # getting all file name from user
    all_password_list_content: list = list() 
    try:
        file_name = input(
            Fore.MAGENTA + '\n1 - Enter your file path -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
    exists_checker(file_name)
    file_name = open(file_name, 'r').readlines()
        
    #The last line doesn't have \n so when it sorted it will connect to another item
    file_name[-1] = file_name[-1] +'\n'
    all_password_list_content.extend(file_name)
    # getting name of the file from user
    input_number = 2
    while True:
        try:
            file_name = input(
                Fore.MAGENTA + f'{input_number} - Enter your file path -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

        exists_checker(file_name)
        file_name = open(file_name, 'r').readlines()
        
        #The last line doesn't have \n so when it sorted it will connect to another item
        file_name[-1] = file_name[-1] +'\n'

        all_password_list_content.extend(file_name)
        user_request = input(
            Fore.YELLOW + '\nWant to add more password list ? [Y/n] ' + Fore.RESET)
        if user_request == 'y' or user_request == 'yes' or user_request == '':
            clear_screen()
            print(Fore.YELLOW + pyfiglet.figlet_format('Pass list merger',
                  font='ANSI Shadow') + Fore.RESET)
            input_number += 1
        else:
            break

    print(Fore.BLUE + 'On it ... ' + Fore.RESET)

    # set file name
    file_name = 'passwords.txt'
    if path.exists('passwords.txt'):
        rename_if_file_exists(1)
    password_list = open(file_name, 'w')
    all_password_list_content_str: str = "".join(all_password_list_content)
    password_list.write(all_password_list_content_str)

    print(Fore.YELLOW + 'Your file save as : ' + file_name + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)
else:
        exit(Fore.RED + 'Error ! Pay attention that your answer must be a number between 1-5.' + Fore.RESET)