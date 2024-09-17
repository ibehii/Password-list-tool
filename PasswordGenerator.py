#  GitHub: https://github.com/ibehii
#  Telegram: https://T.me/dr_xz
#  e-mail: Behii@tutanota.com
#  ____________________________________________

# ======== # import built-in modules # ======== #
from os import name
from secrets import choice
from time import sleep
from datetime import datetime
from pathlib import Path
from subprocess import run
import sqlite3

from lib import figlet_font_downloader
from lib import characters
from lib import initializer

current_path: Path = Path(__file__).parent.resolve()
# ======== # import external modules # ======== #
try:
    from colorama import Fore, init, just_fix_windows_console
    import pyfiglet
    from tqdm import tqdm
    from zxcvbn import zxcvbn
    from prettytable import PrettyTable, DOUBLE_BORDER
except ImportError as error:
    exit(f'A required library is missing! {error}. Try using `pip install <library>`')

init()
just_fix_windows_console()
initializer()

# ======== # functions # ======== #
_clear_screen = lambda: run('cls') if name == 'nt' else run('clear')

# ======== # Install Pyfiglet ANSI Shadow Font # ======== #
if not (Path(pyfiglet.__file__).parent.resolve() / 'fonts'  / 'ANSI Shadow.flf').exists():
    figlet_font_downloader()
    
# ======== # If passwords.txt exist adding number at end of it # ======== #
file_name : str = 'passwords.txt'
def _rename_if_file_exist() -> None:
    file_name_number = 1
    while current_path.joinpath(f'passwords{str(file_name_number)}.txt').exists():
        file_name_number += 1
    global file_name
    file_name = f'passwords{str(file_name_number)}.txt'

_clear_screen()

# ======== # Starting Menu # ======== #
print(Fore.YELLOW + pyfiglet.figlet_format('Password tool', font='ANSI Shadow') + Fore.GREEN +
      f'''{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '1' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Generate a password for login  
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '2'}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Generate password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '3' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Sort password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '4' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Delete duplicate password in password list
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '5' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Merge password lists
{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '6' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Check a password strength\n''' + Fore.RESET)
try:
    first_menu_choice = int(
        input(Fore.MAGENTA + '⹃ Pick a number -> ' + Fore.RESET))
except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
except ValueError:
    exit(Fore.RED + 'Error ! Pay attention that your answer must be a number' + Fore.RESET)

_clear_screen()

# ======== # login password # ======== #
if(first_menu_choice == 1):

    # ======== # sub menu for "login password" # ======== #
    print(Fore.YELLOW + pyfiglet.figlet_format('login password', font='ANSI Shadow') +
          f'{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "1"}{Fore.LIGHTYELLOW_EX + "]" + Fore.YELLOW} - Show previous passwords\n{Fore.LIGHTYELLOW_EX + "["}{Fore.LIGHTGREEN_EX + "2"}{Fore.LIGHTYELLOW_EX + "]" + Fore.YELLOW} - Generate password')
    try:
        sub_menu = int(input(Fore.GREEN + '\n⹃ Pick a number -> ' + Fore.RESET)) 
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except ValueError:
            exit(Fore.RED + 'Error! Pay attention that your answer must be 1 or 2.')
    except Exception:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

    # ======== # Show previous passwords # ======== #
    if (sub_menu == 1):
        _clear_screen()
        print(Fore.YELLOW + pyfiglet.figlet_format('login password', font='ANSI Shadow'))
        try:
            PasswordReminder: str = input(
                Fore.MAGENTA + ' ⹃ Enter a reminder for filter result.\nPress enter to display all password -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        
        try:
            # ====== # Confecting to database that stored passwords # ====== #
            connection: sqlite3.Connection = sqlite3.connect(current_path / 'lib' / 'db' /'.passwords.db')
            cursor: sqlite3.Cursor = connection.cursor()
            cursor.execute("SELECT * FROM password")
            all_data: list[tuple] = cursor.fetchall()
            
            # ==== # checking that there is at list one password in database # ==== #
            if not all_data:
                exit(Fore.RED + 'Error! No password found in database.' + Fore.RESET) 
                
            # ====== #Creating table  # ====== #
            table = PrettyTable()
            table.field_names = ['The password', 'Creation date', 'Reminder']
            table.set_style(DOUBLE_BORDER)
                
            for data in all_data:
                passwords, date, reminder =  data
                if PasswordReminder and PasswordReminder in reminder:
                    table.add_row([passwords, date, reminder])
                elif not PasswordReminder:
                    table.add_row([passwords, date, reminder])
                    
            else:
                table.get_string()
                
        except FileNotFoundError:
            exit(Fore.RED + 'Error! Database was not found.\nFirst generate some passwords.' + Fore.RESET) 
    
# ======== # Generate a password # ======== #
    elif (sub_menu == 2): 
        _clear_screen()
        print(Fore.YELLOW + pyfiglet.figlet_format('login password', font='ANSI Shadow') + Fore.GREEN + f'''{Fore.LIGHTYELLOW_EX + '['}{Fore.LIGHTGREEN_EX + '1' + Fore.GREEN}{Fore.LIGHTYELLOW_EX + ']' + Fore.GREEN} - Include Symbols ( e.g. !@#$%^&* )
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
        except Exception as error:
            exit(Fore.RED + f'Some things went wrong, Please try again ! {error}' + Fore.RED)

# ======== # check if user Enter their choice correctly# ======== #
        for items in included_obj:
            try:
                int(items)
            except ValueError:
                exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
            if len(items) != 1 or int(items) > 5:
                exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
        
        # ======== # Adding chosen letter to password list # ======== #
        char_list: list = []
        if ('1' in included_obj):
            char_list.extend(characters.symbols())
        if ('2' in included_obj):
            char_list.extend(characters.numbers())
        if('3' in included_obj):
            char_list.extend(characters.lowercase())
        if('4' in included_obj):
            char_list.extend(characters.uppercase())
        if('5' in included_obj):
            char_list.extend(characters.Ambiguous())

        _clear_screen()

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
        except Exception as error:
            print(Fore.RED + f'Some thing went wrong try again! {error}'+ Fore.RESET)
        print(Fore.BLUE + 'Your password is: ' + generated_password + Fore.RESET)
        
        # ======== # Checking Password Strength # ======== #
        PasswordStrength = zxcvbn(generated_password)
        PasswordScore = PasswordStrength['score']
        PasswordCrackTime: str = PasswordStrength['crack_times_display']['offline_fast_hashing_1e10_per_second']
        
        PasswordScores: dict = {"0" :"Very week", "1":"Week", "2":"Normal", "3":"Good", "4":"Strong"}
        
        print(f'\n{Fore.BLUE}The generated password is a {Fore.RED if 0 <= PasswordScore <= 1 else Fore.GREEN + PasswordScores[str(PasswordScore)] + Fore.BLUE} password.' + Fore.RESET)
        print(f'{Fore.BLUE}Estimated time to crack the password is: {Fore.RED if 0 <= PasswordScore <= 1 else Fore.GREEN + PasswordCrackTime}')

        # ======== # Saving generated password # ======== #
        try:
            SavingPasswordPermission: str = input(Fore.GREEN + '\nDo you want to save the password? [Y/n] -> ' + Fore.RESET)
        except KeyboardInterrupt:
            exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
        if(SavingPasswordPermission.lower() in ['yes', 'y', '']):
            PasswordReminder: str = input(Fore.GREEN + '\nSet a reminder for this password -> ' + Fore.RESET)
            # ====== # Confecting to database that stored passwords # ====== #
            connection: sqlite3.Connection = sqlite3.connect(current_path / 'lib' / 'db' / '.passwords.db')
            cursor: sqlite3.Cursor = connection.cursor()
            cursor.execute("INSERT INTO password VALUES (?, ?, ?)", (generated_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), PasswordReminder))
            connection.commit()
            connection.close()
            print(Fore.LIGHTGREEN_EX + 'You can access your password at "Login password -> Show previous passwords" section' + Fore.RESET)

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
    except Exception:
        exit(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)

# ======== # check if user Enter their choice correctly # ======== #
    for items in included_obj:
        try:
            int(items)
        except ValueError:
            exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
        if len(items) != 1 or int(items) > 5:
            exit(Fore.RED + 'Error! Pay attention that your answer must be numbers between 1-5 and separated by spaces')
        # ======== # Adding chosen letter to password list # ======== #
        char_list: list = []
        if ('1' in included_obj):
            char_list.extend(characters.symbols())
        if ('2' in included_obj):
            char_list.extend(characters.numbers())
        if('3' in included_obj):
            char_list.extend(characters.lowercase())
        if('4' in included_obj):
            char_list.extend(characters.uppercase())
        if('5' in included_obj):
            char_list.extend(characters.Ambiguous())
    _clear_screen()
    
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

    while (current_path / file_name).exists():
        _rename_if_file_exist()
        
    try:
        def password_generator() :
            # ====== # Generating The Passwords # ====== #
            # first 'for' is for number of password that must generate
            for _ in tqdm(range(password_number)):
                temp_generated_password: str = ""
                # second 'for' is for length of password that must generate
                for _ in range(password_length):
                    temp_generated_password += choice(char_list)
                yield temp_generated_password + '\n'
        with open(current_path / file_name, 'a+') as file:
            for generated_password in password_generator():
                file.write(generated_password)

        print(Fore.GREEN + '\nThe operation was successful!' + Fore.RESET)
        print(Fore.YELLOW + '\nPassword list save as : ' + str(current_path / file_name) + Fore.RESET)
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except MemoryError:
        exit(Fore.RED + 'There is no available ram left. Try make password list with less passwords' + Fore.RED)

# ======== # sort password list # ======== #
elif (first_menu_choice == 3):
    print(Fore.YELLOW + pyfiglet.figlet_format('sort password',
          font='ANSI Shadow') + Fore.RESET)
    try:
        file_path: Path = Path(input(
            Fore.MAGENTA + '⹃ Enter your password list file path -> ' + Fore.RESET))
    except KeyboardInterrupt:
        exit(Fore.RED + '\nThe operation canceled by user' + Fore.RESET)
    except Exception:
        print(Fore.RED + 'Some things went wrong, Please try again !' + Fore.RED)
        
    if not file_path.exists():
        exit(Fore.RED + str(file_path) + " is not exist" + Fore.RESET)
    print(Fore.YELLOW + '\nOn it ...' + Fore.RESET)
    with open(file_name, 'r') as f:
        sorted_fn : list = f.readlines()
        sorted_fn[-1] += '\n'
# ======== # Sort List # ======== #
        sorted_fn = sorted(sorted_fn)
        f.close()

# ======== # add it to file # ======== #
    with open(current_path / file_name, 'w') as fn:
        fn.writelines(sorted_fn)
        fn.close()
    print(Fore.GREEN + f'\n- Your password list is sorted and saved at {str(current_path / file_name)}' + Fore.RESET)


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
    except Exception:
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
            _clear_screen()
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