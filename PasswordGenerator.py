#  GitHub: https://github.com/beh185
#  Telegram: https://T.me/dr_xz
#  e-mail: Behii@tutanota.com
#  ____________________________________________

# ======== # import built-in modules # ======== #
from os import name, system, path, rename, remove
from secrets import choice
from shutil import move
from time import sleep
from datetime import datetime
from urllib.request import urlretrieve
from urllib.error import URLError
import json
import string

# ======== # Rename Project To Its Original name # ======== #
if ("PasswordGenerator.py" not in __file__):
    if name == "nt":
        CurrentlyFileName : str = __file__.split("\\")[-1]
    else:
        CurrentlyFileName : str = __file__.split("/")[-1]
    rename(CurrentlyFileName, "PasswordGenerator.py")

# ======== # import external modules # ======== #
try:
    from colorama import Fore, init
    import pyfiglet
    from tqdm import tqdm
    from zxcvbn import zxcvbn
except ImportError:
    print('Make sure that you are connected to internet!')
    sleep(3)
    system(f'pip install -r {__file__.replace("PasswordGenerator.py", "requirements.txt")}')
    exit('> Run the program again!')
print(Fore.CYAN + "Please wait ..." + Fore.RESET)

init()

# ======== # functions # ======== #
def __clear_screen__() -> None:
    if (name == 'nt'):
        system('cls')
    else:
        system('clear')


# for adding characters to this list
char_list: list[str] = list()

def numbers() -> None:
    global char_list
    char_list.extend(string.digits)

def lowercase() -> None:
    global char_list
    char_list.extend(string.ascii_lowercase)

def uppercase() -> None:
    global char_list
    char_list.extend(string.ascii_uppercase)
    
def symbols() -> None:
    characters: list[str] = ['!', '@', '#', '$', '%', '^', '&', '*', '=']
    global char_list
    char_list.extend(characters)

def Ambiguous() -> None:
    characters: list[str] = ['{', '}', '[', ']', '(', ')', '/', '\\', "'", '"', '~' ',', ';', ':', '.', '<', '>']
    global char_list
    char_list.extend(characters)

# If passwords.txt exist adding number at end of it 
file_name : str = 'passwords.txt'
def __rename_if_file_exist__() -> None:
    file_name_number = 1
    while path.exists(f'passwords{str(file_name_number)}.txt'):
        file_name_number += 1
    global file_name
    file_name = f'passwords{str(file_name_number)}.txt'

def __exists_checker__(FilePath) -> None:
    if not path.exists(FilePath):
        exit(
            Fore.RED + f'"{FilePath}" is not exists. Enter file name correctly !' + Fore.RESET)


# ======== # Install Pyfiglet ANSI Shadow Font # ======== #
if name == 'nt':
    pyfiglet_path: str = pyfiglet.__file__.replace('__init__.py', 'fonts\\')
else:
    pyfiglet_path: str = pyfiglet.__file__.replace('__init__.py', 'fonts/')
if not path.exists(pyfiglet_path + 'ANSI Shadow.flf'):
        try:
            move(__file__.replace('PasswordGenerator.py', 'ANSI Shadow.flf'), pyfiglet_path + 'ANSI Shadow.flf')
        except FileNotFoundError:
            print(Fore.RED + __file__.replace('PasswordGenerator.py', 'ANSI Shadow.flf') + ' Was Not Found!\n' + Fore.RESET)
            print(Fore.YELLOW + 'Downloading the required font!' + Fore.RESET)
            try:
                urlretrieve(
                "https://github.com/xero/figlet-fonts/raw/master/ANSI%20Shadow.flf", 'ANSI Shadow.flf')
                move('ANSI Shadow.flf', pyfiglet_path + 'ANSI Shadow.flf')
            except URLError:
                exit(Fore.RED + "Couldn't connect to server.\nCheck your internet connection and try again" + Fore.RESET)

__clear_screen__()

# ======== # Starting Menu # ======== #
print(Fore.YELLOW + pyfiglet.figlet_format('Password tool', font='ANSI Shadow') + Fore.GREEN +
      f'''{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '1' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Just one password  
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '2'}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Generate password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '3' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Sort password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '4' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Delete duplicate password in password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '5' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Merge password lists
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '6' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Check a password strength\n''' + Fore.RESET)
try:
    first_menu_choice = int(
        input(Fore.MAGENTA + '⹃ Enter number of your choice -> ' + Fore.RESET))
except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
except ValueError:
    exit(Fore.RED + 'Error ! Pay attention that your answer must be a number between 1-5.' + Fore.RESET)

__clear_screen__()

# ======== # One Password # ======== #
if(first_menu_choice == 1):

# ======== # second menu for "just one password" # ======== #
    print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow') +
          f'{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "1"}{Fore.LIGHTYELLOW_EX + "]" + Fore.YELLOW} - Show previous passwords\n{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "2"}{Fore.LIGHTYELLOW_EX + "]" + Fore.YELLOW} - Generate password')
    try:
        second_menu_choice = int(input(Fore.GREEN + '\n⹃ Enter number of the part that you need -> ' + Fore.RESET)) 
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except ValueError:
            exit(Fore.RED + 'Error! Pay attention that your answer must be 1 or 2.')
    except:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

# ======== # Show previous passwords # ======== #
    if (second_menu_choice == 1):
        __clear_screen__()
        print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow'))
        try:
            PasswordName: str = input(
                Fore.MAGENTA + ' ⹃ Enter name of password -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        try:
            with open(__file__.replace('PasswordGenerator.py', 'one_password.json'),'r') as fn:
                password_data: dict = json.load(fn)[PasswordName]
                print(Fore.MAGENTA + f'Your password is: {password_data["password"]}\nTime of creation: {password_data["date"]}' + Fore.RESET)
        except FileNotFoundError:
            exit(Fore.RED + 'Error! Data base didn\'t found.\nFirst generate some passwords and then use this part' + Fore.RESET) 
        except KeyError:
            exit(Fore.RED + "Error! The password's name wasn't correct. Try again. " + Fore.RESET)
    
# ======== # Generate a password # ======== #
    elif (second_menu_choice == 2): 
        __clear_screen__()
        print(Fore.YELLOW + pyfiglet.figlet_format('single password', font='ANSI Shadow') + Fore.GREEN + f'''{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '1' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Symbols ( e.g. !@#$%^&* )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '2'}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Numbers ( e.g. 12345 )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '3' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Lowercase Characters ( e.g. abcdefgh )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '4' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Uppercase Characters ( e.g. ABCDEFGH )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '5' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Ambiguous Characters( e.g. {"{ }"} [ ] ( ) / \\ ' " ~ , ; : . < > )
    ''' + Fore.RESET)
        try:
            included_obj: list[str] = input(
                Fore.MAGENTA + ' ⹃ Enter number of your choices. e.g : 1 2 5 -> ' + Fore.RESET).split()
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

# ======== # check if user Enter their choice correctly# ======== #
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

        __clear_screen__()

# ======== # Third Menu For One Password # ======== #
        print(Fore.YELLOW + pyfiglet.figlet_format('passwords',
            font='ANSI Shadow') + Fore.RESET)
        try:
            password_length = int(
                input(Fore.BLUE + '⹃ Enter password length -> ' + Fore.RESET))
        except ValueError:
            exit(Fore.RED + 'Error! Your answer must be numbers')
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)


        # The password
        generated_password: str = ''

        # ======== # Generating password # ======== #
        try:
            for _ in range(password_length):
                letter: str = choice(char_list)
                generated_password: str = generated_password + letter
        except KeyboardInterrupt:
                exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some thing went wrong try again!'+ Fore.RESET)
        print(Fore.BLUE + 'Your password is: ' + generated_password + Fore.RESET)
        
        # ======== # Checking Password Strength # ======== #
        PasswordStrength = zxcvbn(generated_password)
        PasswordScore = PasswordStrength['score']
        PasswordCrackTime: str = PasswordStrength['crack_times_display']['offline_fast_hashing_1e10_per_second']
        
        if(PasswordScore == 0):
            PasswordScore = Fore.RED + 'Very week' 
            PasswordCrackTime: str = Fore.RED + PasswordCrackTime + Fore.RESET
        elif(PasswordScore == 1):
            PasswordScore = Fore.RED + 'Week' 
            PasswordCrackTime: str = Fore.RED + PasswordCrackTime + Fore.RESET
        elif(PasswordScore == 2):
            PasswordScore = Fore.YELLOW + 'Normal' 
            PasswordCrackTime: str = Fore.YELLOW + PasswordCrackTime + Fore.RESET
        elif(PasswordScore == 3):
            PasswordScore = Fore.CYAN + 'Good' 
            PasswordCrackTime: str = Fore.CYAN + PasswordCrackTime + Fore.RESET
        elif(PasswordScore == 4):
            PasswordScore = Fore.GREEN + 'Strong' 
            PasswordCrackTime: str = Fore.GREEN + PasswordCrackTime + Fore.RESET
        
        print(f'\n{Fore.BLUE}The generated password is a {PasswordScore + Fore.BLUE} password.' + Fore.RESET)
        print(f'{Fore.BLUE}Estimated time to crack the password is: {PasswordCrackTime}')

        # ======== # Saving generated password # ======== #
        try:
            SavingPasswordPermission: str = input(Fore.GREEN + '\nDo you want to save the password? [Y/n] -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        if(SavingPasswordPermission.lower() == 'yes' or SavingPasswordPermission.lower() == 'y' or SavingPasswordPermission == ''):
            PasswordName: str = input(Fore.GREEN + '\nPick a name for you password -> ' + Fore.RESET)     
            try:
                if(path.getsize(__file__.replace('PasswordGenerator.py', 'one_password.json')) == 0):
                    remove(__file__.replace('PasswordGenerator.py', 'one_password.json'))     
            except:
                pass
                      
            if not path.exists(__file__.replace('PasswordGenerator.py', 'one_password.json')):
                with open(__file__.replace('PasswordGenerator.py', 'one_password.json'),'w') as f:
                    password_data = {
                        PasswordName:{'password': generated_password, 
                                      'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                                    }}
                    json.dump(password_data, f, indent=4)
                print(Fore.LIGHTGREEN_EX + 'You can access your password by entering ' + Fore.CYAN + PasswordName + Fore.LIGHTGREEN_EX + 'on Just "one password/Show previous passwords" section' + Fore.RESET)
            else:
                with open(__file__.replace('PasswordGenerator.py', 'one_password.json'),'r') as fn:
                    try:
                        PerviousPass: dict = json.load(fn)
                    except json.decoder.JSONDecodeError:
                        exit(Fore.RED + 'Failed to load the one_password.json file' + Fore.RESET)
                        
                    if(PasswordName in PerviousPass.keys()):
                        try:
                            OverwriteNamePermission: str = input(Fore.RED + 'This name is already exist. Do you want to overwrite it? [y/N] -> ' + Fore.RESET)
                        except KeyboardInterrupt:
                            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
                            
                        if(OverwriteNamePermission.lower() == 'n' or OverwriteNamePermission.lower() == 'no' or OverwriteNamePermission == ''):
                            while PasswordName in PerviousPass.keys():
                                print(Fore.RED + '\nChoose something other than "' + PasswordName + '" that already exist' + Fore.RESET)
                                try:
                                    PasswordName: str = input(Fore.GREEN + 'Pick a name for you password -> ' + Fore.RESET)
                                except KeyboardInterrupt:
                                    exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
                        elif(OverwriteNamePermission.lower() == 'y' or OverwriteNamePermission.lower() == 'yes'):
                            PerviousPass.pop(PasswordName)
                        else:
                            print(Fore.RED + 'Your answer was valid, so we are going to overwrite the password' + Fore.RESET)
                            PerviousPass.pop(PasswordName)
                            
                    password_data = {
                        PasswordName:{'password': generated_password, 
                                      'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                                    }}

                    CurrentlyPass: dict = {**PerviousPass, **password_data}
                    
                    with open(__file__.replace('PasswordGenerator.py', 'one_password.json'), 'w') as f:
                        json.dump(CurrentlyPass, f, indent=4)
                        print(Fore.LIGHTGREEN_EX + 'You can access your password by entering ' + Fore.CYAN + PasswordName + Fore.LIGHTGREEN_EX + 'on Just "one password/Show previous passwords" section' + Fore.RESET)
    else:
        exit(Fore.RED + 'Error! Please enter the number of the part that you need correctly!'+ Fore.RESET)                       

# ======== # Generate password list # ======== #
elif (first_menu_choice == 2):

# ======== # second menu for "multiple passwords" # ======== #
    print(Fore.YELLOW + pyfiglet.figlet_format('Password list', font='ANSI Shadow') + Fore.GREEN + f'''{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '1' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Symbols ( e.g. !@#$%^&* )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '2'}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Numbers ( e.g. 12345 )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '3' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Lowercase Characters ( e.g. abcdefgh )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '4' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Uppercase Characters ( e.g. ABCDEFGH )
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '5' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Ambiguous Characters( e.g. {"{ }"} [ ] ( ) / \\ ' " ~ , ; : . < > )
''' + Fore.RESET)
    try:
        included_obj: list[str] = input(
            Fore.MAGENTA + ' ⹃ Enter number of your choices. e.g : 1 2 5 -> ' + Fore.RESET).split()
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

# ======== # check if user Enter their choice correctly # ======== #
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

    __clear_screen__()
    
# ======== # Third Menu For "multiple passwords" # ======== #
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
        print(Fore.RED + 'Warning! You are going to produce huge amount of passwords this may take a long time and takes resources' + Fore.RESET)
        sleep(3)

    while path.exists(__file__.replace('PasswordGenerator.py', file_name)):
        __rename_if_file_exist__()
    PasswordFilePath: str = __file__.replace('PasswordGenerator.py', file_name)

    try:
# ======== # Generating The Passwords # ======== #
        if(password_number <= 500_000):
            generated_passwords: set = set()
            temp_generated_password: str = str()
            # first 'for' is for number of password that must generate
            for _ in tqdm(range(password_number)):
                # second 'for' is for length of password that must generate
                for _1 in range(password_length):
                    temp_generated_password += choice(char_list)
                generated_passwords.add(temp_generated_password + '\n')
                temp_generated_password = str()

# ======== # add generated passwords to file # ======== #
            with open(PasswordFilePath, 'w') as f:
                f.writelines(generated_passwords)
                f.close()
            print(Fore.BLUE + '\nDeleting duplicate passwords ...' + Fore.RESET)
        else:
            generated_passwords : set = set()
            temp_generated_password: str = str()
            open(PasswordFilePath, 'w')
            for _ in tqdm(range(password_number)):
                # second 'for' is for length of password that must generate
                for _1 in range(password_length):
                    temp_generated_password += choice(char_list)
                generated_passwords.add(temp_generated_password + '\n')
                temp_generated_password: str = str()

# =========== # Adding generated password until now to file for saving resources # =========== #
                if(len(temp_generated_password) == int(password_number / 20)):
                    with open(PasswordFilePath, 'a') as f:
                        f.writelines(generated_passwords)
                        generated_passwords.clear()
            else:
                with open(PasswordFilePath, 'a') as f:
                    f.writelines(generated_passwords)
                    generated_passwords.clear()

        print(Fore.GREEN + '\nThe operation was successful!' + Fore.RESET)
        print(Fore.YELLOW + '\nPassword list save as : ' + PasswordFilePath + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except MemoryError:
        exit(Fore.RED + 'There is no available ram left. Try make password list with less passwords' + Fore.RED)

# ======== # sort password list # ======== #
elif (first_menu_choice == 3):
    print(Fore.YELLOW + pyfiglet.figlet_format('sort password',
          font='ANSI Shadow') + Fore.RESET)
    try:
        file_name = input(
            Fore.MAGENTA + '⹃ Enter your password list file path -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        
    __exists_checker__(file_name)
    print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
    with open(file_name, 'r') as f:
        sorted_fn : list = f.readlines()
        sorted_fn[-1] += '\n'
# ======== # Sort List # ======== #
        sorted_fn.sort()
        f.close()

# ======== # add it to file # ======== #
    with open(file_name, 'w') as fn:
        fn.writelines(sorted_fn)
        fn.close()
    print(Fore.GREEN + '\n- Your password list is sorted' + Fore.RESET)


# ======== # delete duplicate # ======== #
elif (first_menu_choice == 4):

# ======== # Deleting duplicate Menu # ======== #
    print(Fore.YELLOW + pyfiglet.figlet_format('duplicate remover',
          font='ANSI Shadow') + Fore.RESET)
    try:
        try:
            which_method = int(input(
                Fore.GREEN + f'{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "1" + Fore.GREEN}{Fore.LIGHTYELLOW_EX + "]" + Fore.GREEN} - Method 1 [won\'t change the order]\n{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "2"}{Fore.LIGHTYELLOW_EX + "]" + Fore.GREEN} - Method 2 [change the order, but faster]\n\n- Please, enter number of your choice -> ' + Fore.RESET))
        except ValueError:
            exit(Fore.RED + '\nError! Only numbers are acceptable.' + Fore.RESET)
        UserFileName: str = input(
            Fore.MAGENTA + '\n⹃ Enter path of your password list -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        
# ======== # check if the user file actually exist # ======== #
    __exists_checker__(UserFileName)
    print(Fore.YELLOW + 'Starting the operation' + Fore.RESET)
    if (which_method == 1):
        try:
            FileContents: list[str] = open(UserFileName, 'r').readlines()
        except IsADirectoryError:
            exit(Fore.RED + f'{UserFileName} is a directory. Please enter path of a file')
        except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to read the {UserFileName} file' + Fore.RESET)
        if(len(FileContents) == 0):
            exit(Fore.RED + 'The file is empty!' + Fore.RESET )
            
# ======== # The last line doesn't have \n so when it sorted it will connect to another item # ======== #
        FileContents[-1] = FileContents[-1] +'\n'
        FileContents: list[str] = list(dict.fromkeys(FileContents).keys())
        try:
            open(UserFileName, 'w').writelines(FileContents)
        except IsADirectoryError:
            exit(Fore.RED + f'{UserFileName} is a directory. Please enter path of a file')
        except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to write the {UserFileName} file' + Fore.RESET)
        print(Fore.GREEN + "The duplicate passwords are now deleted" + Fore.RESET)

# ======== # Using Fast Mode # ======== #
    elif (which_method == 2): 
        try:
            _FileContents: set[str] = set(open(UserFileName, 'r').readlines())
        except IsADirectoryError:
            exit(Fore.RED + f'{UserFileName} is a directory. Please enter path of a file')
        except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to read the {UserFileName} file' + Fore.RESET)
            
        if(len(_FileContents) == 0):
            exit(Fore.RED + 'The file is empty!' + Fore.RESET )
        try:
            open(UserFileName, 'w').writelines(_FileContents)
        except IsADirectoryError:
            exit(Fore.RED + f'{UserFileName} is a directory. Please enter path of a file')
        except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to write the {UserFileName} file' + Fore.RESET)
        print(Fore.GREEN + "The duplicate passwords are now deleted" + Fore.RESET)
    else:
        exit(Fore.RED + "Please enter the number of the part that you need correctly!" + Fore.RESET)

# ======== # Merge password lists # ======== #
elif (first_menu_choice == 5):
    print(Fore.YELLOW + pyfiglet.figlet_format('Pass list merger',
            font='ANSI Shadow') + Fore.RESET)
    
# ======== # getting all file name from user # ======== #
    FilesContents: list = list() 
    try:
        file_name: str = input(
            Fore.MAGENTA + '\n1 - Enter your file path -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
    __exists_checker__(file_name)
    try:
        FileData: list[str] = open(file_name, 'r').readlines()
    except IsADirectoryError:
            exit(Fore.RED + f'{file_name} is a directory. Please enter path of a file')
    except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to read the {file_name} file' + Fore.RESET)   
    #The last line doesn't have \n so when it sorted it will connect to another item
    FileData[-1] +='\n'
    FilesContents.extend(FileData)

    # getting name of the file from user
    input_number = 2
    while True:
        try:
            file_names: str = input(
                Fore.MAGENTA + f'{input_number} - Enter your file path -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        except:
            print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

        __exists_checker__(file_name)
        try:
            FileData = open(file_name, 'r').readlines()
        except IsADirectoryError:
            exit(Fore.RED + f'{file_name} is a directory. Please enter path of a file')
        except PermissionError:
            exit(Fore.RED + f'We don\'t have permission to read the {file_name} file' + Fore.RESET)   
        
        #The last line doesn't have \n so when it sorted it will connect to another item
        FileData[-1] = FileData[-1] +'\n'

        FilesContents.extend(FileData)
        user_request: str = input(
            Fore.YELLOW + '\nWant to add more password list ? [Y/n] ' + Fore.RESET)
        if user_request.lower() == 'y' or user_request.lower() == 'yes' or user_request == '':
            __clear_screen__()
            print(Fore.YELLOW + pyfiglet.figlet_format('Pass list merger',
                  font='ANSI Shadow') + Fore.RESET)
            input_number += 1
        else:
            break

    print(Fore.BLUE + 'On it ... ' + Fore.RESET)

# ======== # set file name # ======== #
    if path.exists(__file__.replace('PasswordGenerator.py', 'passwords.txt')):
        __rename_if_file_exist__()
    with open(__file__.replace('PasswordGenerator.py', file_name), 'w') as f:
        f.writelines(FilesContents)

    print(Fore.YELLOW + 'Your file save as : ' + __file__.replace('PasswordGenerator.py', file_name) + Fore.RESET)
    print(Fore.GREEN + 'Done !' + Fore.RESET)

# ======== # Check A Password Strength # ======== #
elif(first_menu_choice == 6):
    print(Fore.YELLOW + pyfiglet.figlet_format('Strength checker',
        font='ANSI Shadow') + Fore.RESET)
    try:
        UserPassword: str = input(
            Fore.MAGENTA + '⹃ Enter a password to find out its strength -> ' + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        
    result = zxcvbn(UserPassword)
    
    PasswordScore = result['score']
    PasswordCrackTime: str = result['crack_times_display']['offline_fast_hashing_1e10_per_second']
    warning: str = result['feedback']['warning']
    suggestion: list = result['feedback']['suggestions']

    if(PasswordScore == 0):
        PasswordScore = Fore.RED + 'Very week'  
        PasswordCrackTime: str = Fore.RED + PasswordCrackTime + Fore.RESET
    elif(PasswordScore == 1):
        PasswordScore = Fore.RED + 'Week' 
        PasswordCrackTime: str = Fore.RED + PasswordCrackTime + Fore.RESET
    elif(PasswordScore == 2):
        PasswordScore = Fore.YELLOW + 'Normal' 
        PasswordCrackTime: str = Fore.YELLOW + PasswordCrackTime + Fore.RESET
    elif(PasswordScore == 3):
        PasswordScore = Fore.CYAN + 'Good' 
        PasswordCrackTime: str = Fore.CYAN + PasswordCrackTime + Fore.RESET
    elif(PasswordScore == 4):
        PasswordScore = Fore.GREEN + 'Strong' 
        PasswordCrackTime: str = Fore.GREEN + PasswordCrackTime + Fore.RESET
    
    print(Fore.MAGENTA + f'\n- Your password is a "{PasswordScore + Fore.MAGENTA}" password.' + Fore.RESET)
    print(Fore.MAGENTA + f'- Your password will be cracked approximately in {PasswordCrackTime}')
    if len(warning) != 0:
        print(Fore.RED + 'Warning: ' + warning + Fore.RESET)
    if len(suggestion) != 0:
        print(Fore.RED + 'Suggestion: ' + '\n'.join(suggestion) + Fore.RESET)
        
    
else:
        exit(Fore.RED + 'Error ! Pay attention that your answer must be a number between 1-6.' + Fore.RESET)