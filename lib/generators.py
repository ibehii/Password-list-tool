"""Password and wordlist generation engines.

Includes:
- Cryptographic random password generator (single & streaming bulk)
- Diceware / Passphrase generator
- Hashcat-style Pattern / Mask generator (lazy itertools.product streaming)
- Targeted profile-based wordlist generator (CUPP style)
"""

from __future__ import annotations

import itertools
import re
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Generator, Iterable, Optional

from lib.characters import Ambiguous, lowercase, numbers, symbols, uppercase
from lib.diceware_words import DICEWARE_WORDS


def get_character_pool(
    include_symbols: bool = True,
    include_numbers: bool = True,
    include_lower: bool = True,
    include_upper: bool = True,
    include_ambiguous: bool = False,
) -> list[str]:
    """Build a combined character pool based on boolean flags."""
    pool: list[str] = []
    if include_symbols:
        pool.extend(symbols())
    if include_numbers:
        pool.extend(numbers())
    if include_lower:
        pool.extend(lowercase())
    if include_upper:
        pool.extend(uppercase())
    if include_ambiguous:
        pool.extend(Ambiguous())
    return pool


def generate_single_password(length: int = 16, char_pool: Optional[list[str]] = None) -> str:
    """Generate a single cryptographically secure random password."""
    if char_pool is None:
        char_pool = get_character_pool(include_symbols=True, include_numbers=True, include_lower=True, include_upper=True)
    elif len(char_pool) == 0:
        raise ValueError("Character pool cannot be empty")
    if length <= 0:
        raise ValueError("Password length must be greater than zero")

    return "".join(secrets.choice(char_pool) for _ in range(length))


def generate_passwords_stream(
    count: int,
    length: int,
    char_pool: list[str],
) -> Generator[str, None, None]:
    """Generate random passwords lazily one by one to prevent high memory usage."""
    if not char_pool:
        raise ValueError("Character pool cannot be empty")
    for _ in range(count):
        yield "".join(secrets.choice(char_pool) for _ in range(length))


def stream_passwords_to_file(
    output_path: Path,
    count: int,
    length: int,
    char_pool: list[str],
    progress_callback: Optional[Callable[[int], None]] = None,
) -> Path:
    """Stream bulk-generated passwords directly to a file with minimal RAM usage."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    buffer_size = 64 * 1024
    generated_count = 0

    with open(output_path, "w", encoding="utf-8", buffering=buffer_size) as output_stream:
        for password_item in generate_passwords_stream(count=count, length=length, char_pool=char_pool):
            output_stream.write(f"{password_item}\n")
            generated_count += 1
            if progress_callback and generated_count % 25_000 == 0:
                progress_callback(generated_count)

    return output_path


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    capitalize: bool = True,
    include_number: bool = True,
    include_symbol: bool = False,
    custom_wordlist: Optional[list[str]] = None,
) -> str:
    """Generate a memorable, high-entropy Diceware-style passphrase."""
    chosen_words = custom_wordlist if custom_wordlist is not None else DICEWARE_WORDS
    if not chosen_words:
        raise ValueError("Diceware wordlist is empty")

    selected_words: list[str] = [secrets.choice(chosen_words) for _ in range(word_count)]
    if capitalize:
        selected_words = [word_item.capitalize() for word_item in selected_words]

    passphrase_text = separator.join(selected_words)

    if include_number:
        random_digits = str(secrets.randbelow(90) + 10)
        passphrase_text = f"{passphrase_text}{separator}{random_digits}"

    if include_symbol:
        random_symbol = secrets.choice(["!", "@", "#", "$", "%", "*"])
        passphrase_text = f"{passphrase_text}{random_symbol}"

    return passphrase_text


# Hashcat Mask definitions:
# ?l = abcdefghijklmnopqrstuvwxyz
# ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ?d = 0123456789
# ?s = symbols
# ?a = all
# ?h = 0123456789abcdef
# ?H = 0123456789ABCDEF
MASK_SETS: dict[str, list[str]] = {
    "l": lowercase(),
    "u": uppercase(),
    "d": numbers(),
    "s": symbols(),
    "a": lowercase() + uppercase() + numbers() + symbols(),
    "h": list("0123456789abcdef"),
    "H": list("0123456789ABCDEF"),
}


def parse_mask(mask_expression: str) -> list[list[str]]:
    """Parse a Hashcat-style mask string into a list of character option lists."""
    token_lists: list[list[str]] = []
    char_index = 0
    mask_length = len(mask_expression)

    while char_index < mask_length:
        char_item = mask_expression[char_index]
        if char_item == "?" and char_index + 1 < mask_length:
            next_char = mask_expression[char_index + 1]
            if next_char in MASK_SETS:
                token_lists.append(MASK_SETS[next_char])
                char_index += 2
                continue
            if next_char == "?":
                token_lists.append(["?"])
                char_index += 2
                continue
        token_lists.append([char_item])
        char_index += 1

    return token_lists


def generate_mask_passwords(mask_expression: str) -> Generator[str, None, None]:
    """Generate all password combinations satisfying a mask using lazy streaming."""
    token_lists = parse_mask(mask_expression)
    for combination_tuple in itertools.product(*token_lists):
        yield "".join(combination_tuple)


@dataclass
class TargetProfile:
    """Target user profile used for CUPP-style targeted wordlist generation."""

    first_name: str = ""
    last_name: str = ""
    nickname: str = ""
    birthdate: str = ""  # YYYY-MM-DD, DDMMYYYY, or YYYY
    partner_name: str = ""
    partner_nickname: str = ""
    partner_birthdate: str = ""
    child_name: str = ""
    pet_name: str = ""
    company: str = ""
    mother_name: str = ""
    father_name: str = ""
    mother_birthdate: str = ""
    father_birthdate: str = ""
    child_birthdate: str = ""
    name_abbr: str = ""
    name_abbreviations: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    special_years: list[str] = field(default_factory=list)


def _generate_name_abbreviations(profile: TargetProfile) -> list[str]:
    """Generate abbreviations, initials, and short combinations from names."""
    abbreviations: list[str] = []

    # Include explicit abbreviations from profile
    if profile.name_abbr:
        for raw_abbr in re.split(r"[,;\s]+", profile.name_abbr):
            clean_abbr = raw_abbr.strip()
            if clean_abbr:
                abbreviations.append(clean_abbr)

    for custom_abbr in profile.name_abbreviations:
        clean_custom = custom_abbr.strip()
        if clean_custom:
            abbreviations.append(clean_custom)

    first = profile.first_name.strip()
    last = profile.last_name.strip()
    nick = profile.nickname.strip()
    mother = profile.mother_name.strip()
    father = profile.father_name.strip()

    # Combinations from first and last name
    if first and last:
        first_init = first[0]
        last_init = last[0]

        # Initials: e.g. "as", "sa", "a_s", "a.s", "a-s"
        abbreviations.extend([
            f"{first_init}{last_init}",
            f"{last_init}{first_init}",
            f"{first_init}_{last_init}",
            f"{first_init}.{last_init}",
            f"{first_init}-{last_init}",
        ])

        # First initial + last name: e.g. "asmith", "a_smith", "a.smith", "a-smith"
        abbreviations.extend([
            f"{first_init}{last}",
            f"{first_init.upper()}{last}",
            f"{first_init}_{last}",
            f"{first_init}.{last}",
            f"{first_init}-{last}",
        ])

        # First name + last initial: e.g. "alices", "alice_s", "alice.s", "alice-s"
        abbreviations.extend([
            f"{first}{last_init}",
            f"{first}{last_init.upper()}",
            f"{first}_{last_init}",
            f"{first}.{last_init}",
            f"{first}-{last_init}",
        ])

        # Last name + first initial: e.g. "smitha", "smith_a", "smith.a"
        abbreviations.extend([
            f"{last}{first_init}",
            f"{last}{first_init.upper()}",
            f"{last}_{first_init}",
            f"{last}.{first_init}",
        ])

        # Short 3-char / truncated name forms if long enough
        if len(first) >= 3:
            abbreviations.append(f"{first[:3]}{last_init}")
            abbreviations.append(f"{first[:3]}_{last}")
        if len(last) >= 3:
            abbreviations.append(f"{first_init}{last[:3]}")

    # Combinations with nickname
    if nick and last:
        abbreviations.extend([
            f"{nick[0]}{last[0]}",
            f"{nick[0]}{last}",
            f"{nick}{last[0]}",
            f"{nick}_{last[0]}",
            f"{nick}.{last[0]}",
        ])

    # Combinations with mother's name
    if mother and last:
        abbreviations.extend([
            f"{mother[0]}{last[0]}",
            f"{mother[0]}{last}",
            f"{mother}_{last[0]}",
            f"{mother}.{last[0]}",
        ])
    if mother and first:
        abbreviations.extend([
            f"{first[0]}{mother[0]}",
            f"{mother[0]}{first[0]}",
        ])

    # Combinations with father's name
    if father and last:
        abbreviations.extend([
            f"{father[0]}{last[0]}",
            f"{father[0]}{last}",
            f"{father}_{last[0]}",
            f"{father}.{last[0]}",
        ])
    if father and first:
        abbreviations.extend([
            f"{first[0]}{father[0]}",
            f"{father[0]}{first[0]}",
        ])

    return list(dict.fromkeys(abbreviations))


def _extract_date_tokens(date_text: str) -> list[str]:
    """Extract day, month, 4-digit year, and 2-digit year representations from date string."""
    tokens: list[str] = []
    if not date_text:
        return tokens

    clean_digits = re.sub(r"[^0-9]", "", date_text)
    if len(clean_digits) == 8:
        # Assuming either YYYYMMDD or DDMMYYYY
        part_one = clean_digits[:4]
        part_two = clean_digits[4:]
        tokens.extend([clean_digits, part_one, part_two])
        # 2-digit years
        if part_one.isdigit() and 1900 <= int(part_one) <= 2099:
            tokens.append(part_one[-2:])
            tokens.append(part_two[:2])
            tokens.append(part_two[2:])
            tokens.append(part_one[-2:] + part_two)
            tokens.append(part_two + part_one[-2:])
        if part_two.isdigit() and 1900 <= int(part_two) <= 2099:
            tokens.append(part_two[-2:])
            tokens.append(part_one[:2])
            tokens.append(part_one[2:])
            tokens.append(part_one + part_two[-2:])
            tokens.append(part_two[-2:] + part_one)
    elif len(clean_digits) == 6:
        tokens.append(clean_digits)
        tokens.append(clean_digits[:2])
        tokens.append(clean_digits[2:4])
        tokens.append(clean_digits[4:])
    elif len(clean_digits) == 4:
        tokens.append(clean_digits)
        if clean_digits.isdigit() and 1900 <= int(clean_digits) <= 2099:
            tokens.append(clean_digits[-2:])
    elif clean_digits:
        tokens.append(clean_digits)

    return [token_item for token_item in dict.fromkeys(tokens) if token_item]


def generate_cupp_wordlist(
    profile: TargetProfile,
    include_leet: bool = True,
    include_reverse: bool = True,
) -> Generator[str, None, None]:
    """Generate custom, intelligent candidate passwords for a targeted profile.

    Yields items lazily without exhausting memory.
    """
    primary_words: list[str] = []
    for raw_word in [
        profile.first_name,
        profile.last_name,
        profile.nickname,
        profile.mother_name,
        profile.father_name,
        profile.partner_name,
        profile.partner_nickname,
        profile.child_name,
        profile.pet_name,
        profile.company,
        *profile.keywords,
    ]:
        cleaned = raw_word.strip()
        if cleaned and cleaned not in primary_words:
            primary_words.append(cleaned)

    # Gather abbreviations and initials
    abbreviation_words = _generate_name_abbreviations(profile)

    # Years and numbers
    number_tokens: list[str] = []
    number_tokens.extend(_extract_date_tokens(profile.birthdate))
    number_tokens.extend(_extract_date_tokens(profile.mother_birthdate))
    number_tokens.extend(_extract_date_tokens(profile.father_birthdate))
    number_tokens.extend(_extract_date_tokens(profile.partner_birthdate))
    number_tokens.extend(_extract_date_tokens(profile.child_birthdate))
    for year_entry in profile.special_years:
        year_clean = year_entry.strip()
        if year_clean:
            number_tokens.append(year_clean)
            if len(year_clean) == 4 and year_clean.isdigit():
                number_tokens.append(year_clean[-2:])

    # Default common number and symbol additions
    common_number_tokens = ["1", "12", "123", "1234", "01", "007", "777", "2024", "2025", "2026"]
    number_tokens.extend(common_number_tokens)
    number_tokens = list(dict.fromkeys(number_tokens))

    symbol_tokens = ["", "!", "@", "#", "$", "_", ".", "*"]

    # Generate word variations
    word_variants: list[str] = []
    base_pool = primary_words + abbreviation_words
    for base_word in base_pool:
        word_variants.append(base_word.lower())
        word_variants.append(base_word.capitalize())
        word_variants.append(base_word.upper())
        if include_reverse and len(base_word) > 1 and not any(punc in base_word for punc in [".", "_", "-"]):
            word_variants.append(base_word[::-1].lower())

        if include_leet:
            leet_map = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}
            leet_chars = [leet_map.get(char_item.lower(), char_item) for char_item in base_word]
            leet_text = "".join(leet_chars)
            word_variants.append(leet_text)
            word_variants.append(leet_text.capitalize())

    word_variants = list(dict.fromkeys(word_variants))

    seen_set: set[str] = set()

    # 1. Base variations
    for word_item in word_variants:
        if word_item not in seen_set:
            seen_set.add(word_item)
            yield word_item

    # 2. Base + Numbers + Symbols (and prefixes)
    for word_item in word_variants:
        for number_item in number_tokens:
            for symbol_item in symbol_tokens:
                variant_one = f"{word_item}{number_item}{symbol_item}"
                if variant_one not in seen_set:
                    seen_set.add(variant_one)
                    yield variant_one

                variant_two = f"{word_item}{symbol_item}{number_item}"
                if variant_two not in seen_set:
                    seen_set.add(variant_two)
                    yield variant_two

                if symbol_item:
                    variant_prefix_sym = f"{symbol_item}{word_item}{number_item}"
                    if variant_prefix_sym not in seen_set:
                        seen_set.add(variant_prefix_sym)
                        yield variant_prefix_sym

                variant_prefix_num = f"{number_item}{word_item}{symbol_item}"
                if variant_prefix_num not in seen_set:
                    seen_set.add(variant_prefix_num)
                    yield variant_prefix_num

    # 3. Pair combinations between primary words
    for entity_one_idx, entity_one in enumerate(primary_words[:12]):
        for entity_two_idx, entity_two in enumerate(primary_words[:12]):
            if entity_one_idx != entity_two_idx:
                for sep_item in ["", "_", ".", "-"]:
                    pair_lower = f"{entity_one.lower()}{sep_item}{entity_two.lower()}"
                    pair_cap = f"{entity_one.capitalize()}{sep_item}{entity_two.capitalize()}"

                    for pair_text in [pair_lower, pair_cap]:
                        if pair_text not in seen_set:
                            seen_set.add(pair_text)
                            yield pair_text

                        for number_item in number_tokens[:8]:
                            variant_pair_num = f"{pair_text}{number_item}"
                            if variant_pair_num not in seen_set:
                                seen_set.add(variant_pair_num)
                                yield variant_pair_num

                            variant_pair_num_excl = f"{pair_text}{number_item}!"
                            if variant_pair_num_excl not in seen_set:
                                seen_set.add(variant_pair_num_excl)
                                yield variant_pair_num_excl

                        for symbol_item in ["!", "@", "#", "$"]:
                            variant_pair_sym = f"{pair_text}{symbol_item}"
                            if variant_pair_sym not in seen_set:
                                seen_set.add(variant_pair_sym)
                                yield variant_pair_sym
