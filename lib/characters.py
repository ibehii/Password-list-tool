#  GitHub: https://github.com/ibehii
#  Telegram: https://T.me/dr_xz
#  e-mail: Behii@tutanota.com
#  ____________________________________________

# ======== # import built-in modules # ======== #
import string

def numbers() -> list:
    global char_list
    return(list(string.digits))

def lowercase() -> list:
    global char_list
    return(list(string.ascii_lowercase))

def uppercase() -> list:
    global char_list
    return(list(string.ascii_uppercase))
    
def symbols() -> list:
    characters: list[str] = ['!', '@', '#', '$', '%', '^', '&', '*', '=']
    global char_list
    return(characters)

def Ambiguous() -> list:
    characters: list[str] = ['{', '}', '[', ']', '(', ')', '/', '\\', "'", '"', '~' ',', ';', ':', '.', '<', '>']
    global char_list
    return(characters)