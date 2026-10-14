#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  ____________________________________________
"""Rich-powered terminal user interface and interactive menus."""

from __future__ import annotations

import getpass
import os
import re
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text
from zxcvbn import zxcvbn

from lib.f_font_downloader import render_figlet_banner
from lib.generators import (
    TargetProfile,
    generate_cupp_wordlist,
    generate_mask_passwords,
    generate_passphrase,
    generate_single_password,
    get_character_pool,
    stream_passwords_to_file,
)
from lib.pwned import check_single_password_breached, check_wordlist_pwned
from lib.vault import (
    InvalidMasterPasswordError,
    PasswordVault,
    VaultError,
    VaultNotInitializedError,
    copy_password_to_clipboard,
)
from lib.wordlist_tools import (
    count_lines,
    external_sort,
    filter_wordlist,
    merge_wordlists,
    mutate_wordlist,
    split_wordlist,
    streaming_deduplicate,
)

console = Console()


def clear_screen() -> None:
    """Clear terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(subtitle: str = "") -> None:
    """Display the application banner."""
    rendered_art = render_figlet_banner("Password Tool")
    styled_title = Text(rendered_art, style="bold cyan")
    console.print(styled_title)
    console.print("[dim]GitHub: https://github.com/ibehii | Telegram: https://t.me/dr_xz[/dim]\n")
    if subtitle:
        console.print(Panel(f"[bold yellow]{subtitle}[/bold yellow]", border_style="cyan", expand=False))


def display_strength_analysis(password: str) -> None:
    """Analyze and display password strength using zxcvbn with correct spellings and formatting."""
    score_labels: dict[int, tuple[str, str]] = {
        0: ("Very weak", "bold red"),
        1: ("Weak", "bold red"),
        2: ("Normal", "bold yellow"),
        3: ("Good", "bold blue"),
        4: ("Strong", "bold green"),
    }

    analysis_result = zxcvbn(password)
    score_value: int = analysis_result["score"]
    label_text, label_style = score_labels.get(score_value, ("Unknown", "white"))

    crack_time: str = analysis_result["crack_times_display"].get(
        "offline_fast_hashing_1e10_per_second", "N/A"
    )
    warning_text: str = analysis_result["feedback"].get("warning", "")
    suggestions_list: list[str] = analysis_result["feedback"].get("suggestions", [])

    strength_table = Table(show_header=False, box=None, padding=(0, 1))
    strength_table.add_column("Key", style="bold white")
    strength_table.add_column("Value")

    strength_table.add_row("Password Rating:", f"[{label_style}]{label_text}[/{label_style}]")
    strength_table.add_row("Est. Crack Time:", f"[{label_style}]{crack_time}[/{label_style}] (10B hashes/sec)")
    if warning_text:
        strength_table.add_row("Warning:", f"[yellow]{warning_text}[/yellow]")
    if suggestions_list:
        strength_table.add_row("Suggestions:", "\n".join(f"• {item}" for item in suggestions_list))

    console.print(Panel(strength_table, title="[bold cyan]Strength Analysis[/bold cyan]", border_style="cyan"))


def get_unique_filename(base_name: str = "passwords.txt", directory: Optional[Path] = None) -> Path:
    """Determine a non-colliding file path by appending numbers if needed."""
    work_dir = directory or Path.cwd()
    candidate_path = work_dir / base_name
    if not candidate_path.exists():
        return candidate_path

    file_stem = candidate_path.stem
    file_ext = candidate_path.suffix
    file_number = 1
    while (work_dir / f"{file_stem}_{file_number}{file_ext}").exists():
        file_number += 1

    return work_dir / f"{file_stem}_{file_number}{file_ext}"


def pause_for_user() -> None:
    """Prompt user to press enter to return to the menu."""
    console.print()
    Prompt.ask("[dim]Press Enter to return to main menu[/dim]", default="")


# =========================================================================
# Submenu Handlers
# =========================================================================

def handle_generate_single_password(vault: PasswordVault) -> None:
    """Interactive workflow for generating a single login password."""
    clear_screen()
    print_banner("Generate Login Password")

    include_symbols = Confirm.ask("Include Symbols? (e.g. !@#$%^&*)", default=True)
    include_numbers = Confirm.ask("Include Numbers? (0-9)", default=True)
    include_lower = Confirm.ask("Include Lowercase letters? (a-z)", default=True)
    include_upper = Confirm.ask("Include Uppercase letters? (A-Z)", default=True)
    include_ambiguous = Confirm.ask("Include Ambiguous characters? ({ } [ ] ( ) / \\ ~ ; : . < >)", default=False)

    char_pool = get_character_pool(
        include_symbols=include_symbols,
        include_numbers=include_numbers,
        include_lower=include_lower,
        include_upper=include_upper,
        include_ambiguous=include_ambiguous,
    )
    if not char_pool:
        console.print("[bold red]Error: No character sets selected![/bold red]")
        pause_for_user()
        return

    password_length = IntPrompt.ask("Enter password length", default=20)
    generated_pass = generate_single_password(length=password_length, char_pool=char_pool)

    console.print()
    console.print(Panel(f"[bold green]{generated_pass}[/bold green]", title="Generated Password", border_style="green"))

    display_strength_analysis(generated_pass)

    if Confirm.ask("Copy password to clipboard? (auto-clears in 30s)", default=True):
        if copy_password_to_clipboard(generated_pass, auto_clear_seconds=30):
            console.print("[green]✔ Copied to clipboard! (will auto-clear in 30 seconds)[/green]")
        else:
            console.print("[yellow]Clipboard operation not supported in current environment.[/yellow]")

    if Confirm.ask("Save this password to your encrypted vault?", default=False):
        handle_save_to_vault(vault, generated_pass)

    pause_for_user()


def handle_generate_passphrase() -> None:
    """Generate memorable Diceware passphrase."""
    clear_screen()
    print_banner("Diceware Passphrase Generator")

    word_count = IntPrompt.ask("Number of words", default=4)
    separator_choice = Prompt.ask("Separator character (e.g. -, _, space, .)", default="-")
    capitalize_words = Confirm.ask("Capitalize each word?", default=True)
    include_number = Confirm.ask("Include random numbers at the end?", default=True)
    include_symbol = Confirm.ask("Include random symbol at the end?", default=False)

    passphrase = generate_passphrase(
        word_count=word_count,
        separator=separator_choice,
        capitalize=capitalize_words,
        include_number=include_number,
        include_symbol=include_symbol,
    )

    console.print()
    console.print(Panel(f"[bold cyan]{passphrase}[/bold cyan]", title="Generated Passphrase", border_style="cyan"))
    display_strength_analysis(passphrase)

    if Confirm.ask("Copy passphrase to clipboard?", default=True):
        if copy_password_to_clipboard(passphrase, auto_clear_seconds=30):
            console.print("[green]✔ Copied to clipboard![/green]")
        else:
            console.print("[yellow]Clipboard unavailable.[/yellow]")

    pause_for_user()


def handle_generate_mask_list() -> None:
    """Generate passwords based on Hashcat mask syntax."""
    clear_screen()
    print_banner("Pattern / Mask Wordlist Generator")

    console.print("[bold yellow]Mask placeholders:[/bold yellow]")
    console.print("  [cyan]?l[/cyan] = Lowercase (a-z)     [cyan]?u[/cyan] = Uppercase (A-Z)")
    console.print("  [cyan]?d[/cyan] = Digits (0-9)        [cyan]?s[/cyan] = Symbols (!@#$...)")
    console.print("  [cyan]?a[/cyan] = All printable       [cyan]?h[/cyan] = Hex lower (0-9a-f)")
    console.print("  [dim]Example: Secret?d?d?d! produces Secret000! to Secret999![/dim]\n")

    mask_expression = Prompt.ask("Enter mask expression", default="Pass?d?d?d!")
    destination_str = Prompt.ask("Destination file path", default="mask_passwords.txt")
    destination_path = Path(destination_str).resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    console.print("[yellow]Generating combinations...[/yellow]")
    total_generated = 0
    with open(destination_path, "w", encoding="utf-8", buffering=64 * 1024) as out_file:
        for candidate_pass in generate_mask_passwords(mask_expression):
            out_file.write(f"{candidate_pass}\n")
            total_generated += 1

    console.print(f"[bold green]✔ Done! Generated {total_generated:,} passwords at {destination_path}[/bold green]")
    pause_for_user()


def handle_generate_cupp_list() -> None:
    """Generate targeted wordlist from profile data (CUPP style)."""
    clear_screen()
    print_banner("Targeted Profile Wordlist Generator (CUPP Style)")

    console.print("[dim]Fill in target information (press Enter to skip any field):[/dim]\n")
    first_name = Prompt.ask("Target's first name", default="")
    last_name = Prompt.ask("Target's last name", default="")
    nickname = Prompt.ask("Target's nickname", default="")
    birthdate = Prompt.ask("Target's birthdate (YYYY-MM-DD or DDMMYYYY or YYYY)", default="")
    mother_name = Prompt.ask("Mother's name", default="")
    mother_birthdate = Prompt.ask("Mother's birthdate", default="")
    father_name = Prompt.ask("Father's name", default="")
    father_birthdate = Prompt.ask("Father's birthdate", default="")
    partner_name = Prompt.ask("Partner's name", default="")
    partner_nickname = Prompt.ask("Partner's nickname", default="")
    partner_birthdate = Prompt.ask("Partner's birthdate", default="")
    child_name = Prompt.ask("Child's name", default="")
    child_birthdate = Prompt.ask("Child's birthdate", default="")
    pet_name = Prompt.ask("Pet's name", default="")
    company = Prompt.ask("Company / School / Org name", default="")
    name_abbr_raw = Prompt.ask("Name abbreviation(s) / initials (e.g. AS, admin)", default="")
    keywords_raw = Prompt.ask("Extra keywords (comma-separated)", default="")
    special_years_raw = Prompt.ask("Special years (comma-separated)", default="")

    keywords_list = [keyword.strip() for keyword in keywords_raw.split(",") if keyword.strip()]
    special_years_list = [year_item.strip() for year_item in special_years_raw.split(",") if year_item.strip()]
    abbreviations_list = [
        item_token.strip()
        for item_token in re.split(r"[,;\s]+", name_abbr_raw)
        if item_token.strip()
    ]

    profile = TargetProfile(
        first_name=first_name,
        last_name=last_name,
        nickname=nickname,
        birthdate=birthdate,
        partner_name=partner_name,
        partner_nickname=partner_nickname,
        partner_birthdate=partner_birthdate,
        child_name=child_name,
        child_birthdate=child_birthdate,
        pet_name=pet_name,
        company=company,
        mother_name=mother_name,
        father_name=father_name,
        mother_birthdate=mother_birthdate,
        father_birthdate=father_birthdate,
        name_abbr=name_abbr_raw,
        name_abbreviations=abbreviations_list,
        keywords=keywords_list,
        special_years=special_years_list,
    )

    destination_str = Prompt.ask("Output file path", default=f"{first_name or 'target'}_wordlist.txt")
    destination_path = Path(destination_str).resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    console.print("[yellow]Generating targeted permutations...[/yellow]")
    count_generated = 0
    with open(destination_path, "w", encoding="utf-8", buffering=64 * 1024) as out_file:
        for candidate_pass in generate_cupp_wordlist(profile):
            out_file.write(f"{candidate_pass}\n")
            count_generated += 1

    console.print(f"[bold green]✔ Successfully created targeted wordlist with {count_generated:,} words at {destination_path}[/bold green]")
    pause_for_user()


def handle_generate_bulk_list() -> None:
    """Stream bulk randomly generated passwords directly to file."""
    clear_screen()
    print_banner("Bulk Password List Generator")

    include_symbols = Confirm.ask("Include Symbols?", default=True)
    include_numbers = Confirm.ask("Include Numbers?", default=True)
    include_lower = Confirm.ask("Include Lowercase characters?", default=True)
    include_upper = Confirm.ask("Include Uppercase characters?", default=True)
    include_ambiguous = Confirm.ask("Include Ambiguous characters?", default=False)

    char_pool = get_character_pool(
        include_symbols=include_symbols,
        include_numbers=include_numbers,
        include_lower=include_lower,
        include_upper=include_upper,
        include_ambiguous=include_ambiguous,
    )
    if not char_pool:
        console.print("[bold red]Error: No character types selected![/bold red]")
        pause_for_user()
        return

    password_count = IntPrompt.ask("How many passwords to generate?", default=10_000)
    password_length = IntPrompt.ask("Length of each password?", default=16)

    default_file = get_unique_filename("passwords.txt")
    target_path_str = Prompt.ask("Save path", default=str(default_file))
    target_path = Path(target_path_str).resolve()

    console.print(f"[yellow]Streaming {password_count:,} passwords directly to disk...[/yellow]")
    stream_passwords_to_file(target_path, count=password_count, length=password_length, char_pool=char_pool)

    console.print(f"[bold green]✔ Finished! Saved to {target_path}[/bold green]")
    pause_for_user()


def handle_sort_list() -> None:
    """Sort massive password list using external merge sort."""
    clear_screen()
    print_banner("Sort Password List (External Merge Sort)")

    file_path_str = Prompt.ask("Enter path of the password list to sort")
    file_path = Path(file_path_str).resolve()
    if not file_path.is_file():
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        pause_for_user()
        return

    reverse_order = Confirm.ask("Sort in reverse order?", default=False)
    in_place = Confirm.ask("Sort in-place (overwrite original file)?", default=True)

    destination_path = file_path if in_place else Path(Prompt.ask("Output file path", default=str(file_path.with_name(f"sorted_{file_path.name}")))).resolve()

    console.print("[yellow]Running streaming external merge sort (zero memory overhead)...[/yellow]")
    external_sort(input_path=file_path, output_path=destination_path, reverse=reverse_order)

    console.print(f"[bold green]✔ Successfully sorted! Result saved to {destination_path}[/bold green]")
    pause_for_user()


def handle_deduplicate_list() -> None:
    """Deduplicate password list using streaming external deduplication."""
    clear_screen()
    print_banner("Deduplicate Password List")

    file_path_str = Prompt.ask("Enter path of the password list to deduplicate")
    file_path = Path(file_path_str).resolve()
    if not file_path.is_file():
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        pause_for_user()
        return

    in_place = Confirm.ask("Deduplicate in-place?", default=True)
    destination_path = file_path if in_place else Path(Prompt.ask("Output file path", default=str(file_path.with_name(f"deduped_{file_path.name}")))).resolve()

    console.print("[yellow]Deduplicating via streaming pipeline...[/yellow]")
    total_read, total_unique = streaming_deduplicate(input_path=file_path, output_path=destination_path, sort_first=True)

    duplicates_removed = total_read - total_unique
    console.print(f"[bold green]✔ Complete! Read {total_read:,} lines, removed {duplicates_removed:,} duplicates, saved {total_unique:,} unique entries.[/bold green]")
    pause_for_user()


def handle_merge_lists() -> None:
    """Merge multiple wordlists into one using streaming."""
    clear_screen()
    print_banner("Merge Password Lists")

    file_list: list[Path] = []
    index_counter = 1
    while True:
        path_str = Prompt.ask(f"Enter path for file #{index_counter} (or press Enter to finish)", default="")
        if not path_str.strip():
            if file_list:
                break
            console.print("[red]Please enter at least one file path.[/red]")
            continue

        resolved = Path(path_str).resolve()
        if not resolved.is_file():
            console.print(f"[red]File does not exist: {resolved}[/red]")
            continue

        file_list.append(resolved)
        index_counter += 1

    destination_str = Prompt.ask("Enter output merged file path", default="merged_passwords.txt")
    destination_path = Path(destination_str).resolve()
    dedupe_choice = Confirm.ask("Remove duplicate entries during merge?", default=True)

    console.print("[yellow]Streaming merge in progress...[/yellow]")
    lines_written = merge_wordlists(input_paths=file_list, output_path=destination_path, deduplicate=dedupe_choice)

    console.print(f"[bold green]✔ Merged {len(file_list)} files into {destination_path} ({lines_written:,} lines).[/bold green]")
    pause_for_user()


def handle_filter_list() -> None:
    """Filter massive wordlist by criteria."""
    clear_screen()
    print_banner("Filter Password List")

    file_path_str = Prompt.ask("Enter source password list path")
    file_path = Path(file_path_str).resolve()
    if not file_path.is_file():
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        pause_for_user()
        return

    destination_str = Prompt.ask("Output file path", default=str(file_path.with_name(f"filtered_{file_path.name}")))
    destination_path = Path(destination_str).resolve()

    min_len = IntPrompt.ask("Minimum length (0 to ignore)", default=8)
    max_len = IntPrompt.ask("Maximum length (0 to ignore)", default=64)
    req_lower = Confirm.ask("Must contain lowercase letter?", default=False)
    req_upper = Confirm.ask("Must contain uppercase letter?", default=False)
    req_digit = Confirm.ask("Must contain numeric digit?", default=False)
    req_symbol = Confirm.ask("Must contain special symbol?", default=False)
    regex_input = Prompt.ask("Optional regex pattern (press Enter to skip)", default="")

    console.print("[yellow]Filtering stream...[/yellow]")
    total_scanned, total_matched = filter_wordlist(
        input_path=file_path,
        output_path=destination_path,
        min_length=min_len,
        max_length=max_len,
        require_lower=req_lower,
        require_upper=req_upper,
        require_digit=req_digit,
        require_symbol=req_symbol,
        regex_pattern=regex_input.strip() or None,
    )

    console.print(f"[bold green]✔ Scanned {total_scanned:,} lines, matched {total_matched:,} lines. Saved to {destination_path}[/bold green]")
    pause_for_user()


def handle_mutate_list() -> None:
    """Mutate words with leetspeak, case changes, and affixes."""
    clear_screen()
    print_banner("Wordlist Mutation & Leetspeak Engine")

    file_path_str = Prompt.ask("Enter source wordlist path")
    file_path = Path(file_path_str).resolve()
    if not file_path.is_file():
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        pause_for_user()
        return

    destination_str = Prompt.ask("Output file path", default=str(file_path.with_name(f"mutated_{file_path.name}")))
    destination_path = Path(destination_str).resolve()

    include_leet = Confirm.ask("Include Leetspeak transformations? (e.g. a->@, e->3)", default=True)
    case_var = Confirm.ask("Include Case transformations? (lower, UPPER, Capital)", default=True)

    console.print("[yellow]Mutating words into destination file...[/yellow]")
    words_in, mutations_out = mutate_wordlist(
        input_path=file_path,
        output_path=destination_path,
        include_leet=include_leet,
        case_variations=case_var,
    )

    console.print(f"[bold green]✔ Mutated {words_in:,} input words into {mutations_out:,} passwords at {destination_path}[/bold green]")
    pause_for_user()


def handle_split_and_count() -> None:
    """Split large file and count lines efficiently."""
    clear_screen()
    print_banner("Large File Splitter & Fast Line Counter")

    file_path_str = Prompt.ask("Enter file path")
    file_path = Path(file_path_str).resolve()
    if not file_path.is_file():
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        pause_for_user()
        return

    console.print("[yellow]Calculating line count via fast buffered binary scanner...[/yellow]")
    total_lines = count_lines(file_path)
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    console.print(f"[cyan]File Size:[/cyan] {file_size_mb:.2f} MB")
    console.print(f"[cyan]Total Lines:[/cyan] [bold green]{total_lines:,}[/bold green]")

    if Confirm.ask("Do you want to split this file into smaller chunks?", default=False):
        lines_per_chunk = IntPrompt.ask("Lines per chunk", default=500_000)
        output_dir_str = Prompt.ask("Output directory for chunks", default=str(file_path.parent / f"{file_path.stem}_chunks"))
        output_dir = Path(output_dir_str).resolve()

        console.print(f"[yellow]Splitting into chunks of {lines_per_chunk:,} lines...[/yellow]")
        created_chunks = split_wordlist(input_path=file_path, output_dir=output_dir, lines_per_chunk=lines_per_chunk)
        console.print(f"[bold green]✔ Created {len(created_chunks)} chunk files in {output_dir}[/bold green]")

    pause_for_user()


def handle_pwned_checker() -> None:
    """Check password or wordlist against Have I Been Pwned API."""
    clear_screen()
    print_banner("Have I Been Pwned (HIBP) Breach Checker")

    console.print("[dim]Uses SHA-1 k-anonymity: your password is NEVER sent over the internet.[/dim]\n")
    sub_choice = Prompt.ask("Choose mode: [1] Check single password, [2] Scan wordlist", choices=["1", "2"], default="1")

    if sub_choice == "1":
        candidate_pass = Prompt.ask("Enter password to check", password=True)
        is_breached, breach_count = check_single_password_breached(candidate_pass)
        if is_breached:
            console.print(Panel(
                f"[bold red]⚠ COMPROMISED![/bold red]\nThis password appeared in [bold red]{breach_count:,}[/bold red] data breaches!",
                border_style="red"
            ))
        else:
            console.print(Panel(
                "[bold green]✔ CLEAN![/bold green]\nThis password was NOT found in known data breaches.",
                border_style="green"
            ))
    else:
        file_path_str = Prompt.ask("Enter wordlist file path")
        file_path = Path(file_path_str).resolve()
        if not file_path.is_file():
            console.print(f"[bold red]File not found: {file_path}[/bold red]")
            pause_for_user()
            return

        destination_str = Prompt.ask("Output file for compromised entries", default="pwned_matches.txt")
        destination_path = Path(destination_str).resolve()
        max_scan = IntPrompt.ask("Max passwords to check (0 for all)", default=50)

        console.print("[yellow]Scanning against HIBP k-anonymity API with rate-limiting...[/yellow]")
        total_checked, total_breached = check_wordlist_pwned(
            wordlist_path=file_path,
            output_compromised_path=destination_path,
            max_check_count=max_scan,
        )
        console.print(f"[bold green]✔ Checked {total_checked:,} passwords. Found {total_breached:,} compromised entries saved at {destination_path}[/bold green]")

    pause_for_user()


def handle_strength_menu() -> None:
    """Analyze strength of an arbitrary password."""
    clear_screen()
    print_banner("Password Strength Checker")

    user_pass = Prompt.ask("Enter password to analyze")
    display_strength_analysis(user_pass)
    pause_for_user()


# =========================================================================
# Vault Submenu Handlers
# =========================================================================

def unlock_or_init_vault(vault: PasswordVault) -> bool:
    """Ensure vault is unlocked, prompting for master password."""
    if vault.is_unlocked:
        return True

    if vault.is_legacy_unencrypted():
        console.print("[bold yellow]Detected legacy unencrypted password database![/bold yellow]")
        console.print("To protect your passwords with AES-256 encryption, set a master password:")
        master_pass = Prompt.ask("Choose Master Password", password=True)
        migrated = vault.migrate_legacy(master_pass)
        console.print(f"[bold green]✔ Migrated {migrated} passwords to encrypted vault![/bold green]")
        return True

    if not vault.is_initialized():
        console.print("[bold cyan]Welcome! Initialize your encrypted vault.[/bold cyan]")
        master_pass_one = Prompt.ask("Set Master Password", password=True)
        master_pass_two = Prompt.ask("Confirm Master Password", password=True)
        if master_pass_one != master_pass_two:
            console.print("[bold red]Passwords do not match![/bold red]")
            return False
        vault.initialize_vault(master_pass_one)
        console.print("[bold green]✔ Vault successfully initialized![/bold green]")
        return True

    attempts = 3
    while attempts > 0:
        entered_pass = Prompt.ask("Enter Master Password", password=True)
        try:
            vault.unlock(entered_pass)
            console.print("[bold green]✔ Vault unlocked![/bold green]")
            return True
        except InvalidMasterPasswordError:
            attempts -= 1
            console.print(f"[bold red]Incorrect master password! {attempts} attempts left.[/bold red]")
        except VaultError as error_msg:
            console.print(f"[bold red]Vault error: {error_msg}[/bold red]")
            return False

    return False


def handle_save_to_vault(vault: PasswordVault, password_text: str) -> None:
    """Save a password into the encrypted vault."""
    if not unlock_or_init_vault(vault):
        return

    service_name = Prompt.ask("Service / Site name (e.g. GitHub, Email)", default="General")
    reminder_note = Prompt.ask("Reminder / Note (optional)", default="")
    entry_id = vault.add_entry(service=service_name, password_text=password_text, reminder=reminder_note)
    console.print(f"[bold green]✔ Saved to vault with ID #{entry_id}![/bold green]")


def handle_vault_menu(vault: PasswordVault) -> None:
    """Encrypted vault management menu."""
    clear_screen()
    print_banner("Encrypted Password Vault (AES-256)")

    if not unlock_or_init_vault(vault):
        pause_for_user()
        return

    while True:
        clear_screen()
        print_banner("Encrypted Password Vault (AES-256)")

        console.print("[bold yellow][1][/bold yellow] - List & search saved passwords")
        console.print("[bold yellow][2][/bold yellow] - Add new password entry")
        console.print("[bold yellow][3][/bold yellow] - Delete password entry")
        console.print("[bold yellow][4][/bold yellow] - Export vault (JSON/CSV backup)")
        console.print("[bold yellow][5][/bold yellow] - Import vault (restore from JSON/CSV)")
        console.print("[bold yellow][6][/bold yellow] - Lock vault and return\n")

        vault_choice = Prompt.ask("Pick an option", choices=["1", "2", "3", "4", "5", "6"], default="1")

        if vault_choice == "1":
            filter_query = Prompt.ask("Search term (press Enter to show all)", default="")
            entries = vault.get_entries(search_query=filter_query)
            if not entries:
                console.print("[yellow]No matching password entries found.[/yellow]")
            else:
                table = Table(title="Vault Passwords", border_style="cyan")
                table.add_column("ID", style="dim", justify="right")
                table.add_column("Service", style="bold cyan")
                table.add_column("Password", style="bold green")
                table.add_column("Date Added", style="dim")
                table.add_column("Reminder / Note", style="italic yellow")

                for record in entries:
                    table.add_row(
                        str(record["id"]),
                        record["service"],
                        record["password"],
                        record["date"],
                        record["reminder"],
                    )
                console.print(table)

                copy_id_str = Prompt.ask("Enter ID to copy to clipboard (or press Enter to skip)", default="")
                if copy_id_str.isdigit():
                    selected_id = int(copy_id_str)
                    match_entry = next((entry_item for entry_item in entries if entry_item["id"] == selected_id), None)
                    if match_entry:
                        copy_password_to_clipboard(match_entry["password"], auto_clear_seconds=30)
                        console.print("[green]✔ Copied to clipboard! (will auto-clear in 30s)[/green]")
            pause_for_user()

        elif vault_choice == "2":
            service_name = Prompt.ask("Service / Account", default="General")
            password_text = Prompt.ask("Password")
            reminder_text = Prompt.ask("Reminder / Note", default="")
            new_id = vault.add_entry(service=service_name, password_text=password_text, reminder=reminder_text)
            console.print(f"[bold green]✔ Added entry #{new_id}![/bold green]")
            pause_for_user()

        elif vault_choice == "3":
            del_id_str = Prompt.ask("Enter ID of entry to delete")
            if del_id_str.isdigit():
                if Confirm.ask(f"Are you sure you want to delete entry #{del_id_str}?", default=False):
                    if vault.delete_entry(int(del_id_str)):
                        console.print("[bold green]✔ Deleted![/bold green]")
                    else:
                        console.print("[red]Entry not found.[/red]")
            pause_for_user()

        elif vault_choice == "4":
            export_format = Prompt.ask("Format (json or csv)", choices=["json", "csv"], default="json")
            plaintext_choice = Confirm.ask("Export plaintext passwords? (Warning: file will contain unencrypted passwords)", default=False)
            default_export = f"vault_export.{export_format}"
            export_path_str = Prompt.ask("Export file path", default=default_export)
            exported_count = vault.export_entries(
                export_path=Path(export_path_str),
                export_format=export_format,
                plaintext=plaintext_choice,
            )
            console.print(f"[bold green]✔ Exported {exported_count} records to {export_path_str}![/bold green]")
            pause_for_user()

        elif vault_choice == "5":
            import_path_str = Prompt.ask("Enter backup file path to import (JSON or CSV)")
            import_path = Path(import_path_str).resolve()
            if not import_path.is_file():
                console.print(f"[bold red]File not found: {import_path}[/bold red]")
            else:
                try:
                    imported_count = vault.import_entries(import_path)
                    console.print(f"[bold green]✔ Successfully imported {imported_count} records![/bold green]")
                except Exception as import_error:
                    console.print(f"[bold red]Import error: {import_error}[/bold red]")
            pause_for_user()

        elif vault_choice == "6":
            vault.lock()
            break


def handle_about_us() -> None:
    """Display information about Password List Tool, mission, and author contact."""
    clear_screen()
    print_banner("About Password List Tool")

    about_table = Table(show_header=False, box=None, padding=(0, 2))
    about_table.add_column("Key", style="bold cyan")
    about_table.add_column("Value")

    about_table.add_row("Project Name:", "[bold white]Password List Tool[/bold white] (v3.2.1)")
    about_table.add_row("Mission:", "Zero-OOM, streaming wordlist engine, targeted generation & local encrypted vault.")
    about_table.add_row("Developer:", "[bold green]Behnam[/bold green]")
    about_table.add_row("GitHub:", "[link=https://github.com/ibehii]https://github.com/ibehii[/link]")
    about_table.add_row("Telegram:", "[link=https://t.me/dr_xz]https://t.me/dr_xz[/link]")
    about_table.add_row("Contact Email:", "Behii@tutanota.com")
    about_table.add_row("License:", "MIT Open Source License")

    console.print(Panel(about_table, title="[bold green]About Us & Project Mission[/bold green]", border_style="green"))

    summary_text = (
        "[dim]Engineered for cybersecurity researchers, sysadmins, and privacy advocates.\n"
        "Features streaming external merge sort, constant memory footprint on 50GB+ files,\n"
        "AES-256 encrypted SQLite vault, and SHA-1 k-anonymity breach detection.[/dim]"
    )
    console.print(Panel(summary_text, border_style="cyan"))
    pause_for_user()


# =========================================================================
# Main Interactive Loop
# =========================================================================

def run_interactive_menu() -> None:
    """Launch the main interactive Rich terminal menu."""
    vault = PasswordVault()

    while True:
        try:
            clear_screen()
            print_banner("Ultimate High-Performance Password & Wordlist Engine")

            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Number", style="bold yellow", justify="right")
            menu_table.add_column("Description", style="bold white")

            menu_table.add_row("[1]", "Generate single password (customizable, strength, clipboard)")
            menu_table.add_row("[2]", "Generate bulk password list (streaming, memory-safe)")
            menu_table.add_row("[3]", "Generate Diceware passphrase (memorable multi-word)")
            menu_table.add_row("[4]", "Generate Pattern / Mask list (Hashcat-style ?l?u?d?s)")
            menu_table.add_row("[5]", "Targeted profile wordlist generator (CUPP-style)")
            menu_table.add_row("[6]", "Sort password list (streaming external merge sort)")
            menu_table.add_row("[7]", "Delete duplicate passwords (streaming deduplication)")
            menu_table.add_row("[8]", "Merge password lists (streaming multi-file combiner)")
            menu_table.add_row("[9]", "Filter password list (by length, charset, regex)")
            menu_table.add_row("[10]", "Mutate & Leetspeak engine (rules, casing, leet, affixes)")
            menu_table.add_row("[11]", "Large file splitter & line counter (constant RAM)")
            menu_table.add_row("[12]", "Have I Been Pwned check (SHA-1 k-anonymity API)")
            menu_table.add_row("[13]", "Encrypted Password Vault (.passwords.db, AES-256)")
            menu_table.add_row("[14]", "Check password strength & crack time (zxcvbn)")
            menu_table.add_row("[15]", "About Us & Project Info (developer, mission, contacts)")
            menu_table.add_row("[0]", "Exit")

            console.print(Panel(menu_table, title="[bold green]Main Menu[/bold green]", border_style="green"))

            choice = Prompt.ask(
                "[bold magenta]Pick an option[/bold magenta]",
                choices=[str(val) for val in range(16)],
                default="1",
            )

            if choice == "1":
                handle_generate_single_password(vault)
            elif choice == "2":
                handle_generate_bulk_list()
            elif choice == "3":
                handle_generate_passphrase()
            elif choice == "4":
                handle_generate_mask_list()
            elif choice == "5":
                handle_generate_cupp_list()
            elif choice == "6":
                handle_sort_list()
            elif choice == "7":
                handle_deduplicate_list()
            elif choice == "8":
                handle_merge_lists()
            elif choice == "9":
                handle_filter_list()
            elif choice == "10":
                handle_mutate_list()
            elif choice == "11":
                handle_split_and_count()
            elif choice == "12":
                handle_pwned_checker()
            elif choice == "13":
                handle_vault_menu(vault)
            elif choice == "14":
                handle_strength_menu()
            elif choice == "15":
                handle_about_us()
            elif choice == "0":
                console.print("[cyan]Goodbye![/cyan]")
                break

        except KeyboardInterrupt:
            console.print("\n[bold red]Operation canceled by user.[/bold red]")
            break
        except Exception as error_unhandled:
            console.print(f"\n[bold red]An unexpected error occurred: {error_unhandled}[/bold red]")
            pause_for_user()

