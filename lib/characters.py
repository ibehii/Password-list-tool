#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  e-mail: Behii@tutanota.com
#  ____________________________________________

import string

def numbers() -> list[str]:
    """Return numeric characters 0-9."""
    return list(string.digits)

def lowercase() -> list[str]:
    """Return lowercase ASCII letters a-z."""
    return list(string.ascii_lowercase)

def uppercase() -> list[str]:
    """Return uppercase ASCII letters A-Z."""
    return list(string.ascii_uppercase)

def symbols() -> list[str]:
    """Return common symbol characters."""
    return ['!', '@', '#', '$', '%', '^', '&', '*', '=', '+', '-', '_']

def Ambiguous() -> list[str]:
    """Return ambiguous/bracket punctuation characters."""
    return ['{', '}', '[', ']', '(', ')', '/', '\\', "'", '"', '~', ',', ';', ':', '.', '<', '>']

def all_characters() -> list[str]:
    """Return all standard password characters combined."""
    return numbers() + lowercase() + uppercase() + symbols() + Ambiguous()