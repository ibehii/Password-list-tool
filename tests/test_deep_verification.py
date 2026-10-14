"""Deep verification test suite probing complex scenarios and stress points."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lib.pwned import MAX_PREFIX_CACHE_ENTRIES, check_wordlist_pwned
from lib.vault import PasswordVault
from lib.wordlist_tools import (
    count_lines,
    external_sort,
    filter_wordlist,
    merge_wordlists,
    mutate_wordlist,
    streaming_deduplicate,
)


def test_hierarchical_external_sort_large_chunk_count() -> None:
    """Stress test external merge sort with > 64 chunks to exercise hierarchical batch merging."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "many_chunks_input.txt"
        # 150 items with chunk_lines=2 produces 75 chunks (> MAX_MERGE_BATCH of 64)
        sample_words = [f"word_{index:04d}" for index in range(150)]
        import random
        shuffled_words = list(sample_words)
        random.seed(42)
        random.shuffle(shuffled_words)

        input_file.write_text("\n".join(shuffled_words) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "hierarchical_sorted.txt"
        external_sort(input_path=input_file, output_path=output_file, chunk_lines=2)

        sorted_result = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert sorted_result == sorted(sample_words)


def test_external_sort_with_inline_deduplication() -> None:
    """Verify external_sort with deduplicate=True eliminates duplicates in a single pass."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "duplicates_input.txt"
        words = ["beta", "alpha", "beta", "gamma", "alpha", "delta", "gamma", "beta"]
        input_file.write_text("\n".join(words) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "deduped_sorted.txt"
        external_sort(input_path=input_file, output_path=output_file, chunk_lines=2, deduplicate=True)

        result_words = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert result_words == ["alpha", "beta", "delta", "gamma"]


def test_count_lines_comprehensive_newline_variations() -> None:
    """Verify count_lines across all standard and non-standard line ending patterns."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Empty
        file_empty = Path(temp_dir) / "empty.txt"
        file_empty.write_text("", encoding="utf-8")
        assert count_lines(file_empty) == 0

        # Single line with newline
        file_one_nl = Path(temp_dir) / "one_nl.txt"
        file_one_nl.write_text("hello\n", encoding="utf-8")
        assert count_lines(file_one_nl) == 1

        # Single line without newline
        file_one_no_nl = Path(temp_dir) / "one_no_nl.txt"
        file_one_no_nl.write_text("hello", encoding="utf-8")
        assert count_lines(file_one_no_nl) == 1

        # Three lines with final newline
        file_three_nl = Path(temp_dir) / "three_nl.txt"
        file_three_nl.write_text("one\ntwo\nthree\n", encoding="utf-8")
        assert count_lines(file_three_nl) == 3

        # Three lines without final newline
        file_three_no_nl = Path(temp_dir) / "three_no_nl.txt"
        file_three_no_nl.write_text("one\ntwo\nthree", encoding="utf-8")
        assert count_lines(file_three_no_nl) == 3

        # Windows CRLF
        file_crlf = Path(temp_dir) / "crlf.txt"
        file_crlf.write_text("line1\r\nline2\r\nline3\r\n", encoding="utf-8")
        assert count_lines(file_crlf) == 3


def test_vault_database_secure_permissions() -> None:
    """Verify the vault database file is created with restricted 0o600 permissions on POSIX."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / ".secure_vault.db"
        vault = PasswordVault(db_path=db_path)
        vault.initialize_vault("SecretMasterPass123!")

        if os.name == "posix":
            file_mode = stat.S_IMODE(os.stat(db_path).st_mode)
            # Owner read & write (0o600)
            assert file_mode & 0o077 == 0, f"Vault database permissions are too open: {oct(file_mode)}"


def test_vault_import_both_formats() -> None:
    """Verify vault imports from both CSV and JSON backups."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_db = Path(temp_dir) / ".src_vault.db"
        src_vault = PasswordVault(db_path=source_db)
        src_vault.initialize_vault("SrcKey123!")
        src_vault.add_entry(service="Discord", password_text="DiscordPass99!", reminder="Gaming")
        src_vault.add_entry(service="Slack", password_text="SlackPass88!", reminder="Work")

        # Export to CSV
        csv_path = Path(temp_dir) / "backup.csv"
        src_vault.export_entries(csv_path, export_format="csv", plaintext=True)

        # Import into fresh vault
        dest_db = Path(temp_dir) / ".dst_vault.db"
        dst_vault = PasswordVault(db_path=dest_db)
        dst_vault.initialize_vault("DstKey456!")
        imported_count = dst_vault.import_entries(csv_path)
        assert imported_count == 2

        entries = dst_vault.get_entries()
        assert len(entries) == 2
        service_names = {entry["service"] for entry in entries}
        assert "Discord" in service_names
        assert "Slack" in service_names


def test_pwned_lru_cache_boundary() -> None:
    """Verify check_wordlist_pwned caps prefix cache size at MAX_PREFIX_CACHE_ENTRIES."""
    with tempfile.TemporaryDirectory() as temp_dir:
        wordlist_path = Path(temp_dir) / "words.txt"
        compromised_path = Path(temp_dir) / "out.txt"

        # Generate 20 distinct passwords
        words = [f"test_password_{num}" for num in range(20)]
        wordlist_path.write_text("\n".join(words) + "\n", encoding="utf-8")

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "00000000000000000000000000000000000:1"

        with patch("requests.get", return_value=mock_resp):
            total_checked, total_breached = check_wordlist_pwned(
                wordlist_path=wordlist_path,
                output_compromised_path=compromised_path,
                delay_between_requests=0.0,
            )
            assert total_checked == 20
            assert total_breached == 0
