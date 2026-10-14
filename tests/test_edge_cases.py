"""Comprehensive edge case and boundary condition test suite."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from lib.characters import Ambiguous, all_characters, numbers
from lib.generators import (
    TargetProfile,
    generate_cupp_wordlist,
    generate_mask_passwords,
    generate_passphrase,
    generate_single_password,
    stream_passwords_to_file,
)
from lib.pwned import check_single_password_breached, check_wordlist_pwned
from lib.vault import (
    InvalidMasterPasswordError,
    PasswordVault,
    VaultError,
    derive_encryption_key,
)
from lib.wordlist_tools import (
    count_lines,
    external_sort,
    filter_wordlist,
    generate_word_mutations,
    merge_wordlists,
    mutate_wordlist,
    split_wordlist,
    streaming_deduplicate,
)


def test_edge_case_empty_files() -> None:
    """External sort, dedupe, merge, filter on completely empty files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        empty_file = Path(temp_dir) / "empty.txt"
        empty_file.touch()

        # Count lines
        assert count_lines(empty_file) == 0

        # Sort empty file
        sorted_empty = Path(temp_dir) / "sorted_empty.txt"
        external_sort(empty_file, sorted_empty)
        assert count_lines(sorted_empty) == 0

        # Dedupe empty file
        deduped_empty = Path(temp_dir) / "deduped_empty.txt"
        read_count, unique_count = streaming_deduplicate(empty_file, deduped_empty)
        assert read_count == 0
        assert unique_count == 0

        # Filter empty file
        filtered_empty = Path(temp_dir) / "filtered_empty.txt"
        scanned, matched = filter_wordlist(empty_file, filtered_empty, min_length=5)
        assert scanned == 0
        assert matched == 0

        # Mutate empty file
        mutated_empty = Path(temp_dir) / "mutated_empty.txt"
        words_in, mutations_out = mutate_wordlist(empty_file, mutated_empty)
        assert words_in == 0
        assert mutations_out == 0

        # Split empty file
        split_chunks = split_wordlist(empty_file, Path(temp_dir) / "chunks", lines_per_chunk=10)
        assert len(split_chunks) == 0


def test_edge_case_single_line_without_trailing_newline() -> None:
    """Verify files without final newline are handled properly without corrupting records or miscounting."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Single line without newline
        no_newline_file = Path(temp_dir) / "no_nl.txt"
        no_newline_file.write_text("sole_password", encoding="utf-8")
        assert count_lines(no_newline_file) == 1

        sorted_file = Path(temp_dir) / "sorted_nl.txt"
        external_sort(no_newline_file, sorted_file)
        lines = sorted_file.read_text(encoding="utf-8").splitlines()
        assert lines == ["sole_password"]
        assert count_lines(sorted_file) == 1

        # Multiple lines without final newline
        multi_no_newline = Path(temp_dir) / "multi_no_nl.txt"
        multi_no_newline.write_text("pass_one\npass_two", encoding="utf-8")
        assert count_lines(multi_no_newline) == 2


def test_edge_case_in_place_operations_and_self_merge() -> None:
    """Verify in-place filtering, mutating, and self-merging do not truncate or wipe files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # In-place filtering
        filter_target = Path(temp_dir) / "in_place_filter.txt"
        filter_target.write_text("short\nvalidPassword123!\nanotherValid99$\n", encoding="utf-8")
        scanned, matched = filter_wordlist(filter_target, filter_target, min_length=10)
        assert scanned == 3
        assert matched == 2
        assert filter_target.read_text(encoding="utf-8").splitlines() == ["validPassword123!", "anotherValid99$"]

        # In-place mutation
        mutate_target = Path(temp_dir) / "in_place_mutate.txt"
        mutate_target.write_text("admin\n", encoding="utf-8")
        words_in, mutations_out = mutate_wordlist(mutate_target, mutate_target, include_leet=True)
        assert words_in == 1
        assert mutations_out > 5
        assert count_lines(mutate_target) == mutations_out

        # Merge where destination is also an input file
        file_one = Path(temp_dir) / "merge_self1.txt"
        file_two = Path(temp_dir) / "merge_self2.txt"
        file_one.write_text("alpha\nbravo\n", encoding="utf-8")
        file_two.write_text("charlie\n", encoding="utf-8")
        total_merged = merge_wordlists([file_one, file_two], file_one, deduplicate=False)
        assert total_merged == 3
        merged_lines = file_one.read_text(encoding="utf-8").splitlines()
        assert merged_lines == ["alpha", "bravo", "charlie"]

        # Split with lines_per_chunk <= 0 raises ValueError
        with pytest.raises(ValueError):
            split_wordlist(file_one, Path(temp_dir) / "chunks", lines_per_chunk=0)


def test_edge_case_all_identical_lines() -> None:
    """Deduplicating a file where all lines are identical should yield exactly 1 line."""
    with tempfile.TemporaryDirectory() as temp_dir:
        dup_file = Path(temp_dir) / "all_dups.txt"
        dup_file.write_text("password123\n" * 50, encoding="utf-8")

        dedup_file = Path(temp_dir) / "all_dups_out.txt"
        total_read, total_unique = streaming_deduplicate(dup_file, dedup_file)
        assert total_read == 50
        assert total_unique == 1
        assert dedup_file.read_text(encoding="utf-8").splitlines() == ["password123"]


def test_edge_case_generators_boundary_values() -> None:
    """Test boundary lengths and special character options in generators."""
    # Length = 1
    single_char_pass = generate_single_password(length=1, char_pool=numbers())
    assert len(single_char_pass) == 1
    assert single_char_pass.isdigit()

    # Invalid length <= 0
    with pytest.raises(ValueError):
        generate_single_password(length=0)

    # Empty pool
    with pytest.raises(ValueError):
        generate_single_password(length=5, char_pool=[])

    # Passphrase with 1 word and custom separator
    passphrase_single = generate_passphrase(word_count=1, separator=":", include_number=False, include_symbol=False)
    assert ":" not in passphrase_single
    assert len(passphrase_single) > 1

    # Mask with literal question mark escape
    mask_escaped = list(generate_mask_passwords("??test??"))
    assert mask_escaped == ["?test?"]

    # Mask with only literal chars
    mask_literal = list(generate_mask_passwords("ExactMatch123"))
    assert mask_literal == ["ExactMatch123"]

    # CUPP with completely empty profile fields
    empty_profile = TargetProfile()
    cupp_words = list(generate_cupp_wordlist(empty_profile))
    # Should still yield standard variations/years without crashing
    assert isinstance(cupp_words, list)


def test_edge_case_vault_corrupted_metadata() -> None:
    """Test vault handling corrupted verifier or missing metadata."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / ".corrupt.db"
        vault = PasswordVault(db_path=db_path)
        vault.initialize_vault("InitialPass!")

        # Corrupt the verifier token directly in database
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            conn.execute("UPDATE vault_meta SET meta_value = 'corrupted_garbage_token' WHERE meta_key = 'verifier'")
            conn.commit()

        vault.lock()
        with pytest.raises(InvalidMasterPasswordError):
            vault.unlock("InitialPass!")


def test_edge_case_pwned_network_failure() -> None:
    """Verify HIBP gracefully returns False, 0 on timeout or connection error."""
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        is_breached, breach_count = check_single_password_breached("any_pass")
        assert is_breached is False
        assert breach_count == 0

    # Empty password
    is_breached, breach_count = check_single_password_breached("")
    assert is_breached is False
    assert breach_count == 0
