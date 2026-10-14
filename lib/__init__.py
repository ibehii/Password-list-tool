"""Password Tool library package."""

from lib.characters import Ambiguous, lowercase, numbers, symbols, uppercase
from lib.f_font_downloader import figlet_font_downloader
from lib.generators import (
    TargetProfile,
    generate_cupp_wordlist,
    generate_mask_passwords,
    generate_passphrase,
    generate_single_password,
    stream_passwords_to_file,
)
from lib.initializer import initializer
from lib.pwned import check_single_password_breached, check_wordlist_pwned
from lib.vault import PasswordVault, copy_password_to_clipboard
from lib.wordlist_tools import (
    count_lines,
    external_sort,
    filter_wordlist,
    merge_wordlists,
    mutate_wordlist,
    split_wordlist,
    streaming_deduplicate,
)

__all__: list[str] = [
    "figlet_font_downloader",
    "initializer",
    "Ambiguous",
    "lowercase",
    "numbers",
    "symbols",
    "uppercase",
    "TargetProfile",
    "generate_cupp_wordlist",
    "generate_mask_passwords",
    "generate_passphrase",
    "generate_single_password",
    "stream_passwords_to_file",
    "check_single_password_breached",
    "check_wordlist_pwned",
    "PasswordVault",
    "copy_password_to_clipboard",
    "count_lines",
    "external_sort",
    "filter_wordlist",
    "merge_wordlists",
    "mutate_wordlist",
    "split_wordlist",
    "streaming_deduplicate",
]