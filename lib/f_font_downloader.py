#  GitHub: https://github.com/ibehii
#  Telegram: https://T.me/BZHNAM
#  e-mail: Behii@tutanota.com
#  ____________________________________________

# ======== # Import Part # ======== #
from requests import get, exceptions
from shutil import move
from colorama import Fore
from pathlib import Path
import pyfiglet

# ======== # Path of folder that script is on it # ======== #
current_directory_path: Path = Path(__file__).resolve().parent

# ======== # Path of pyfiglet font file # ======== #
pyfiglet_path: Path = Path(pyfiglet.__file__.replace('__init__.py', 'fonts')) / 'ANSI Shadow.flf'

# ======== # Download required font for figlet # ======== #
def figlet_font_downloader() -> None:
    try:
        move(current_directory_path / 'ANSI Shadow.flf', pyfiglet_path.resolve())
    except FileNotFoundError:
        print(Fore.RED + str(current_directory_path.joinpath('ANSI Shadow.flf').resolve()) +  ' Was Not Found!\n' + Fore.RESET)
        print(Fore.YELLOW + 'Downloading the required font!' + Fore.RESET)
        
        # ======== # Download the font # ======== #
        try:
            fontContent: bytes = get("https://github.com/xero/figlet-fonts/raw/master/ANSI%20Shadow.flf").content
            with pyfiglet_path as pyf:
                pyf.write_bytes(fontContent)
        except (exceptions.ConnectionError, exceptions.Timeout):
            exit(Fore.RED + "Couldn't connect to server.\nCheck your internet connection and try again" + Fore.RESET)
