"""Command-line interface (CLI) parser and subcommands dispatcher."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

from lib.generators import (
    TargetProfile,
    generate_cupp_wordlist,
    generate_mask_passwords,
    generate_passphrase,
    generate_passwords_stream,
    generate_single_password,
    get_character_pool,
    stream_passwords_to_file,
)
from lib.pwned import check_single_password_breached, check_wordlist_pwned
from lib.ui import display_strength_analysis, run_interactive_menu
from lib.wordlist_tools import (
    count_lines,
    external_sort,
    filter_wordlist,
    merge_wordlists,
    mutate_wordlist,
    split_wordlist,
    streaming_deduplicate,
)

cli_console = Console()


def create_argument_parser() -> argparse.ArgumentParser:
    """Build and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="PasswordGenerator",
        description="High-performance password generator, wordlist toolkit, and secure vault.",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch interactive Rich terminal menu (default when no command specified).",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate single or bulk passwords")
    gen_parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate")
    gen_parser.add_argument("-l", "--length", type=int, default=16, help="Password length")
    gen_parser.add_argument("-o", "--output", type=str, default="", help="Output file path (prints to stdout if omitted)")
    gen_parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    gen_parser.add_argument("--no-numbers", action="store_true", help="Exclude digits")
    gen_parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase")
    gen_parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase")
    gen_parser.add_argument("--ambiguous", action="store_true", help="Include ambiguous characters")

    # Command: passphrase
    passphrase_parser = subparsers.add_parser("passphrase", help="Generate Diceware passphrases")
    passphrase_parser.add_argument("-w", "--words", type=int, default=4, help="Number of words")
    passphrase_parser.add_argument("-s", "--separator", type=str, default="-", help="Word separator")
    passphrase_parser.add_argument("--no-capitalize", action="store_true", help="Do not capitalize words")
    passphrase_parser.add_argument("--no-number", action="store_true", help="Do not append number")
    passphrase_parser.add_argument("--symbol", action="store_true", help="Append random symbol")

    # Command: mask
    mask_parser = subparsers.add_parser("mask", help="Generate passwords from Hashcat-style mask")
    mask_parser.add_argument("pattern", type=str, help="Mask pattern (e.g. Pass?d?d?d!)")
    mask_parser.add_argument("-o", "--output", type=str, default="", help="Output file path")

    # Command: cupp
    cupp_parser = subparsers.add_parser("cupp", help="Generate targeted profile wordlist (CUPP style)")
    cupp_parser.add_argument("--first-name", type=str, default="", help="Target first name")
    cupp_parser.add_argument("--last-name", type=str, default="", help="Target last name")
    cupp_parser.add_argument("--nickname", type=str, default="", help="Target nickname")
    cupp_parser.add_argument("--birthdate", type=str, default="", help="Target birthdate")
    cupp_parser.add_argument("--mother", "--mother-name", dest="mother_name", type=str, default="", help="Mother's name")
    cupp_parser.add_argument("--father", "--father-name", dest="father_name", type=str, default="", help="Father's name")
    cupp_parser.add_argument("--mother-birthdate", dest="mother_birthdate", type=str, default="", help="Mother's birthdate")
    cupp_parser.add_argument("--father-birthdate", dest="father_birthdate", type=str, default="", help="Father's birthdate")
    cupp_parser.add_argument("--partner", "--partner-name", dest="partner", type=str, default="", help="Partner name")
    cupp_parser.add_argument("--partner-nickname", dest="partner_nickname", type=str, default="", help="Partner nickname")
    cupp_parser.add_argument("--partner-birthdate", dest="partner_birthdate", type=str, default="", help="Partner birthdate")
    cupp_parser.add_argument("--child", "--child-name", dest="child", type=str, default="", help="Child name")
    cupp_parser.add_argument("--child-birthdate", dest="child_birthdate", type=str, default="", help="Child birthdate")
    cupp_parser.add_argument("--pet", "--pet-name", dest="pet", type=str, default="", help="Pet name")
    cupp_parser.add_argument("--company", type=str, default="", help="Company or school name")
    cupp_parser.add_argument("--name-abbr", "--abbr", dest="name_abbr", type=str, default="", help="Name abbreviation(s) or initials")
    cupp_parser.add_argument("--keywords", type=str, nargs="*", default=[], help="Additional keywords")
    cupp_parser.add_argument("--years", type=str, nargs="*", default=[], help="Special years")
    cupp_parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")

    # Command: sort
    sort_parser = subparsers.add_parser("sort", help="Sort wordlist using streaming external merge sort")
    sort_parser.add_argument("file", type=str, help="Input file path")
    sort_parser.add_argument("-o", "--output", type=str, default="", help="Output file path (default: in-place)")
    sort_parser.add_argument("-r", "--reverse", action="store_true", help="Sort in reverse order")

    # Command: dedupe
    dedupe_parser = subparsers.add_parser("dedupe", help="Deduplicate wordlist using streaming pipeline")
    dedupe_parser.add_argument("file", type=str, help="Input file path")
    dedupe_parser.add_argument("-o", "--output", type=str, default="", help="Output file path (default: in-place)")

    # Command: merge
    merge_parser = subparsers.add_parser("merge", help="Merge multiple wordlists via streaming")
    merge_parser.add_argument("files", type=str, nargs="+", help="Input files to merge")
    merge_parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    merge_parser.add_argument("--dedupe", action="store_true", help="Deduplicate merged results")

    # Command: filter
    filter_parser = subparsers.add_parser("filter", help="Filter wordlist by criteria")
    filter_parser.add_argument("file", type=str, help="Input file path")
    filter_parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    filter_parser.add_argument("--min", type=int, default=0, help="Minimum password length")
    filter_parser.add_argument("--max", type=int, default=0, help="Maximum password length")
    filter_parser.add_argument("--require-lower", action="store_true", help="Require lowercase character")
    filter_parser.add_argument("--require-upper", action="store_true", help="Require uppercase character")
    filter_parser.add_argument("--require-digit", action="store_true", help="Require numeric digit")
    filter_parser.add_argument("--require-symbol", action="store_true", help="Require special symbol")
    filter_parser.add_argument("--regex", type=str, default="", help="Regex pattern to match")

    # Command: mutate
    mutate_parser = subparsers.add_parser("mutate", help="Mutate wordlist with leetspeak and rules")
    mutate_parser.add_argument("file", type=str, help="Input file path")
    mutate_parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    mutate_parser.add_argument("--no-leet", action="store_true", help="Disable leetspeak transformations")
    mutate_parser.add_argument("--no-case", action="store_true", help="Disable case variations")

    # Command: split
    split_parser = subparsers.add_parser("split", help="Split large wordlist into chunks")
    split_parser.add_argument("file", type=str, help="Input file path")
    split_parser.add_argument("-o", "--output-dir", type=str, required=True, help="Output directory")
    split_parser.add_argument("-l", "--lines", type=int, default=1_000_000, help="Lines per chunk")

    # Command: count
    count_parser = subparsers.add_parser("count", help="Count lines in large file quickly")
    count_parser.add_argument("file", type=str, help="File path to count")

    # Command: pwned
    pwned_parser = subparsers.add_parser("pwned", help="Check password against HIBP breach database")
    pwned_parser.add_argument("password", type=str, help="Password to check")

    # Command: strength
    strength_parser = subparsers.add_parser("strength", help="Analyze password strength using zxcvbn")
    strength_parser.add_argument("password", type=str, help="Password to analyze")

    return parser


def handle_cli_execution(arguments: list[str]) -> int:
    """Parse command line arguments and execute the appropriate handler."""
    parser = create_argument_parser()

    if not arguments or (len(arguments) == 1 and arguments[0] in ("-i", "--interactive")):
        run_interactive_menu()
        return 0

    parsed_args = parser.parse_args(arguments)

    if parsed_args.interactive or not parsed_args.command:
        run_interactive_menu()
        return 0

    command_name = parsed_args.command

    if command_name == "generate":
        char_pool = get_character_pool(
            include_symbols=not parsed_args.no_symbols,
            include_numbers=not parsed_args.no_numbers,
            include_lower=not parsed_args.no_lower,
            include_upper=not parsed_args.no_upper,
            include_ambiguous=parsed_args.ambiguous,
        )
        if parsed_args.count == 1 and not parsed_args.output:
            generated = generate_single_password(length=parsed_args.length, char_pool=char_pool)
            cli_console.print(generated)
        elif parsed_args.output:
            stream_passwords_to_file(
                output_path=Path(parsed_args.output),
                count=parsed_args.count,
                length=parsed_args.length,
                char_pool=char_pool,
            )
            cli_console.print(f"[green]Successfully generated {parsed_args.count:,} passwords to {parsed_args.output}[/green]")
        else:
            for password_item in generate_passwords_stream(count=parsed_args.count, length=parsed_args.length, char_pool=char_pool):
                sys.stdout.write(f"{password_item}\n")

    elif command_name == "passphrase":
        passphrase_result = generate_passphrase(
            word_count=parsed_args.words,
            separator=parsed_args.separator,
            capitalize=not parsed_args.no_capitalize,
            include_number=not parsed_args.no_number,
            include_symbol=parsed_args.symbol,
        )
        cli_console.print(passphrase_result)

    elif command_name == "mask":
        if parsed_args.output:
            out_path = Path(parsed_args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as out_stream:
                for candidate_pass in generate_mask_passwords(parsed_args.pattern):
                    out_stream.write(f"{candidate_pass}\n")
            cli_console.print(f"[green]Mask passwords saved to {parsed_args.output}[/green]")
        else:
            for candidate_pass in generate_mask_passwords(parsed_args.pattern):
                sys.stdout.write(f"{candidate_pass}\n")

    elif command_name == "cupp":
        abbr_list: list[str] = []
        if parsed_args.name_abbr:
            for item_token in re.split(r"[,;\s]+", parsed_args.name_abbr):
                clean_abbr = item_token.strip()
                if clean_abbr:
                    abbr_list.append(clean_abbr)

        profile = TargetProfile(
            first_name=parsed_args.first_name,
            last_name=parsed_args.last_name,
            nickname=parsed_args.nickname,
            birthdate=parsed_args.birthdate,
            partner_name=parsed_args.partner,
            partner_nickname=parsed_args.partner_nickname,
            partner_birthdate=parsed_args.partner_birthdate,
            child_name=parsed_args.child,
            child_birthdate=parsed_args.child_birthdate,
            pet_name=parsed_args.pet,
            company=parsed_args.company,
            mother_name=parsed_args.mother_name,
            father_name=parsed_args.father_name,
            mother_birthdate=parsed_args.mother_birthdate,
            father_birthdate=parsed_args.father_birthdate,
            name_abbr=parsed_args.name_abbr,
            name_abbreviations=abbr_list,
            keywords=parsed_args.keywords,
            special_years=parsed_args.years,
        )
        out_path = Path(parsed_args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        count_written = 0
        with open(out_path, "w", encoding="utf-8") as out_stream:
            for candidate_word in generate_cupp_wordlist(profile):
                out_stream.write(f"{candidate_word}\n")
                count_written += 1
        cli_console.print(f"[green]Generated {count_written:,} CUPP passwords to {parsed_args.output}[/green]")

    elif command_name == "sort":
        input_target = Path(parsed_args.file)
        output_target = Path(parsed_args.output) if parsed_args.output else None
        res_path = external_sort(input_path=input_target, output_path=output_target, reverse=parsed_args.reverse)
        cli_console.print(f"[green]Sorted list saved to {res_path}[/green]")

    elif command_name == "dedupe":
        input_target = Path(parsed_args.file)
        output_target = Path(parsed_args.output) if parsed_args.output else None
        total_read, total_unique = streaming_deduplicate(input_path=input_target, output_path=output_target)
        cli_console.print(f"[green]Deduplication complete: {total_unique:,} unique of {total_read:,} lines saved.[/green]")

    elif command_name == "merge":
        input_files = [Path(path_entry) for path_entry in parsed_args.files]
        output_target = Path(parsed_args.output)
        lines_written = merge_wordlists(input_paths=input_files, output_path=output_target, deduplicate=parsed_args.dedupe)
        cli_console.print(f"[green]Merged {len(input_files)} files into {output_target} ({lines_written:,} lines).[/green]")

    elif command_name == "filter":
        total_scanned, total_matched = filter_wordlist(
            input_path=Path(parsed_args.file),
            output_path=Path(parsed_args.output),
            min_length=parsed_args.min,
            max_length=parsed_args.max,
            require_lower=parsed_args.require_lower,
            require_upper=parsed_args.require_upper,
            require_digit=parsed_args.require_digit,
            require_symbol=parsed_args.require_symbol,
            regex_pattern=parsed_args.regex or None,
        )
        cli_console.print(f"[green]Filtered {total_matched:,} matching passwords from {total_scanned:,} scanned to {parsed_args.output}[/green]")

    elif command_name == "mutate":
        in_words, out_mutations = mutate_wordlist(
            input_path=Path(parsed_args.file),
            output_path=Path(parsed_args.output),
            include_leet=not parsed_args.no_leet,
            case_variations=not parsed_args.no_case,
        )
        cli_console.print(f"[green]Mutated {in_words:,} words into {out_mutations:,} passwords at {parsed_args.output}[/green]")

    elif command_name == "split":
        chunks = split_wordlist(
            input_path=Path(parsed_args.file),
            output_dir=Path(parsed_args.output_dir),
            lines_per_chunk=parsed_args.lines,
        )
        cli_console.print(f"[green]Created {len(chunks)} chunks in {parsed_args.output_dir}[/green]")

    elif command_name == "count":
        total_lines = count_lines(Path(parsed_args.file))
        cli_console.print(f"[cyan]Line count:[/cyan] {total_lines:,}")

    elif command_name == "pwned":
        is_breached, breach_count = check_single_password_breached(parsed_args.password)
        if is_breached:
            cli_console.print(f"[bold red]Breached! Appeared in {breach_count:,} breaches.[/bold red]")
        else:
            cli_console.print("[bold green]Clean! Password not found in known breaches.[/bold green]")

    elif command_name == "strength":
        display_strength_analysis(parsed_args.password)

    return 0


def main() -> int:
    """CLI and package entrypoint."""
    from lib.initializer import initializer
    initializer()
    cli_arguments = sys.argv[1:]
    if not cli_arguments:
        run_interactive_menu()
        return 0
    return handle_cli_execution(cli_arguments)
