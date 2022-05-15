#  ____       _                           
# | __ )  ___| |__  _ __   __ _ _ __ ___  
# |  _ \ / _ \ '_ \| '_ \ / _` | '_ ` _  \ 
# | |_) |  __/ | | | | | | (_| | | | | | |
# |____/ \___|_| |_|_| |_|\__,_|_| |_| |_|

#  Github: https://github.com/beh185
#  Telegram: https://T.me/dr_xz
#  e-mail: BehnamH.dev@gmail.com
#  ____________________________________________

#import part
from os import system ; from sys import platform 
from colorama import Fore
from random import choice

#menu
print(Fore.GREEN , '''____       _                           
| __ )  ___| |__  _ __   __ _ _ __ ___  
|  _ \ / _ \ '_ \| '_ \ / _` | '_ ` _  \ 
| |_) |  __/ | | | | | | (_| | | | | | |
|____/ \___|_| |_|_| |_|\__,_|_| |_| |_|

[1] - Generaiting with number 
[2] - Generaiting with letter
[3] - Genetating with number and letter 
[4] - Sort password list
''' , Fore.RESET)
user_request = int(input(Fore.YELLOW + '⹃ Enter number of your choice -> '+ Fore.RESET))

# clear screen

if (platform == "Windwos".lower()): 
    system('cls') 
elif (platform == "Linux".lower()): 
    system('clear') 
else: 
    try: 
        system('clear') 
    except: 
        pass 


print(Fore.MAGENTA + ''' ____                                     _ 
|  _ \ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |
|  __/ (_| \__ \__ \\\ V  V / (_) | | | (_| |
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|       
 ''' + Fore.RESET)

# Generaiting with number
if (user_request == 1):
    def Generaiting_numbers():
        # Quantifying 
        numbers = ['1','2','3','4','5','6','7','8','9','0']
        generated_passsword_list = []
        generated_passsword = choice(numbers)

        number_password = int(input(Fore.YELLOW + 'How many passwords do i have to generate ? ' + Fore.RESET))
        len_password = int(input(Fore.YELLOW + 'How many number must passwords have ? ' + Fore.RESET))
        # this `for` is about number of password that must generated 
        for t in range (number_password):
            # this `for` is about number of passowrd's letter that must generated
            for i in range(len_password - 1):
                temp_number = choice(numbers)
                generated_passsword = generated_passsword + temp_number
            if(generated_passsword in generated_passsword_list):
                number_password = number_password + 1
            else:
                generated_passsword_list.append(generated_passsword)
                generated_passsword = choice(numbers)

        # Add generated password to file 
        file = open('passwords.txt', 'w')
        generated_passswords = '\n'.join(generated_passsword_list)
        file.write(generated_passswords)
        file.close()
        print(Fore.GREEN + 'Done !'+ Fore.RESET)
        again = str(input('You want to make numbers again? [yes:no] : '))

        if again == 'yes'.lower(): 
            Generaiting_numbers() 
        else:
            pass

    Generaiting_numbers() 
    
    
# Generaiting with letters
elif (user_request == 2):
    def tolls(): 

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        generated_passsword_list = []
        generated_passsword = choice(letters)
        
        number_password = int(input(Fore.YELLOW + 'How many passwords do i have to generate ? ' + Fore.RESET))
        len_password = int(input(Fore.YELLOW + 'How many letter must passwords have ? ' + Fore.RESET))

        # this `for` is about number of password that must generated
        for t in range(number_password):
            # this `for` is about number of passowrd's letter that must generated
            for i in range(len_password - 1):
                temp_letter = choice(letters)
                generated_passsword = generated_passsword + temp_letter
            if(generated_passsword in generated_passsword_list):
                number_password = number_password + 1
            else:
                generated_passsword_list.append(generated_passsword)
                generated_passsword = choice(letters)

        file = open('passwords.txt', 'w')
        generated_passswords = '\n'.join(generated_passsword_list)
        file.write(generated_passswords)
        file.close()
        print(Fore.GREEN + 'Done !' + Fore.RESET)
        
        again = str(input('You want to make numbers again? [yes:no] : '))

        if again == "yes".lower(): 
            tolls()
        else:
            pass
    tolls() 


# generating with number and letter
elif(user_request == 3):
    def sery(): 
        numbers_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        generated_passsword_list = []
        generated_passsword = choice(numbers_letters)

        number_password = int(input(Fore.YELLOW + 'How many passwords do i have to generate ? ' + Fore.RESET))
        len_password = int(input(Fore.YELLOW + 'How many letter must passwords have ? ' + Fore.RESET))

        for t in range (number_password):
            for i in range(len_password - 1):
                temp_letter_number = choice(numbers_letters)
                generated_passsword = generated_passsword + temp_letter_number
            if(generated_passsword in generated_passsword_list):
                number_password = number_password + 1
            else:
                generated_passsword_list.append(generated_passsword)
                generated_passsword = choice(numbers_letters)
        
        file = open('passwords.txt', 'w')
        generated_passswords = '\n'.join(generated_passsword_list)
        file.write(generated_passswords)
        file.close()
        print(Fore.GREEN + 'Done !' + Fore.RESET)
        again = str(input('You want to make numbers again? [yes:no] : '))

        if again == "yes".lower(): 
            sery()
        else:
            pass
    sery() 

# sort password list
elif(user_request == 4):

    def fris():
        file_name = input(Fore.YELLOW + 'Please, enter name of file (example : passwords.txt)→ ' + Fore.RESET)
        file = open(file_name, 'r')
        file_content = list(file.read())
        file.close()
        temp_password = ''
        password_list = []

        for i in file_content:
            if i != '\n':
                temp_password = temp_password + i
            else:
                password_list.append(temp_password)
                temp_password = ''
        password_list.sort()
        str_password = '\n'.join(password_list)

        file = open(file_name, 'w')
        file.write(str_password)
        file.close()
        print(Fore.GREEN + 'Done !' + Fore.RESET)

        again = str(input('You want to make numbers again? [yes:no] : '))

        if again == "yes".lower(): 
            fris()
        else:
            pass
    fris()

else:
    print(Fore.RED + 'Something went wrong please try again !')
