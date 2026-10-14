"""Tests for password, passphrase, mask, and CUPP generator routines."""

from __future__ import annotations

import tempfile
from pathlib import Path

from lib.characters import lowercase, numbers, symbols, uppercase
from lib.generators import (
    TargetProfile,
    generate_cupp_wordlist,
    generate_mask_passwords,
    generate_passphrase,
    generate_single_password,
    get_character_pool,
    stream_passwords_to_file,
)
from lib.wordlist_tools import count_lines


def test_generate_single_password() -> None:
    """Verify single password generation length and character restrictions."""
    pool = lowercase() + uppercase()
    password_text = generate_single_password(length=32, char_pool=pool)
    assert len(password_text) == 32
    assert all(char_item.isalpha() for char_item in password_text)


def test_stream_passwords_to_file() -> None:
    """Verify streaming passwords directly to file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        out_file = Path(temp_dir) / "bulk_test.txt"
        pool = numbers()
        stream_passwords_to_file(out_file, count=100, length=12, char_pool=pool)

        assert count_lines(out_file) == 100
        first_line = out_file.read_text(encoding="utf-8").splitlines()[0]
        assert len(first_line) == 12
        assert first_line.isdigit()


def test_generate_passphrase() -> None:
    """Verify Diceware passphrase generator options."""
    passphrase_text = generate_passphrase(
        word_count=5,
        separator=".",
        capitalize=True,
        include_number=True,
        include_symbol=False,
    )
    tokens = passphrase_text.split(".")
    assert len(tokens) == 6  # 5 words + 1 number token
    assert tokens[-1].isdigit()


def test_generate_mask_passwords() -> None:
    """Verify Hashcat mask combination generation."""
    # Pattern: A?d! -> A0!, A1!, ..., A9!
    combinations = list(generate_mask_passwords("A?d!"))
    assert len(combinations) == 10
    assert "A0!" in combinations
    assert "A9!" in combinations


def test_generate_cupp_wordlist() -> None:
    """Verify CUPP targeted profile combinations."""
    profile = TargetProfile(
        first_name="Alice",
        last_name="Smith",
        mother_name="Mary",
        father_name="John",
        name_abbr="AS",
        birthdate="1995",
        pet_name="Fluffy",
        company="CyberCorp",
        keywords=["admin", "vpn"],
        special_years=["2024"],
    )

    generated_words = list(generate_cupp_wordlist(profile))
    assert len(generated_words) > 50

    # Ensure names and year combinations are created
    lower_words = [word_item.lower() for word_item in generated_words]
    assert any("alice" in item and "1995" in item for item in lower_words)
    assert any("fluffy" in item and "2024" in item for item in lower_words)
    assert any("cybercorp" in item for item in lower_words)
    assert any("mary" in item for item in lower_words)
    assert any("john" in item for item in lower_words)
    assert any("as" in item for item in lower_words)
