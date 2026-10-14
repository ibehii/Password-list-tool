"""Tests for CLI subcommands dispatcher."""

from __future__ import annotations

import tempfile
from pathlib import Path

from lib.cli import handle_cli_execution
from lib.wordlist_tools import count_lines


def test_cli_generate_file() -> None:
    """Test CLI 'generate' command creating passwords in file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "cli_generated.txt"
        cli_args = ["generate", "-c", "50", "-l", "14", "-o", str(output_file)]
        exit_code = handle_cli_execution(cli_args)

        assert exit_code == 0
        assert output_file.exists()
        assert count_lines(output_file) == 50


def test_cli_generate_stdout() -> None:
    """Test CLI 'generate' command streaming to stdout."""
    cli_args = ["generate", "-c", "5", "-l", "10"]
    exit_code = handle_cli_execution(cli_args)
    assert exit_code == 0


def test_cli_passphrase() -> None:
    """Test CLI 'passphrase' command."""
    cli_args = ["passphrase", "-w", "4", "-s", "_"]
    exit_code = handle_cli_execution(cli_args)
    assert exit_code == 0


def test_cli_mask_to_file() -> None:
    """Test CLI 'mask' command."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "cli_mask.txt"
        cli_args = ["mask", "Test?d?d!", "-o", str(output_file)]
        exit_code = handle_cli_execution(cli_args)

        assert exit_code == 0
        assert count_lines(output_file) == 100


def test_cli_sort_and_dedupe() -> None:
    """Test CLI 'sort' and 'dedupe' subcommands."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "words.txt"
        test_file.write_text("z\na\nz\nb\n", encoding="utf-8")

        # Sort
        sorted_file = Path(temp_dir) / "sorted.txt"
        exit_code_sort = handle_cli_execution(["sort", str(test_file), "-o", str(sorted_file)])
        assert exit_code_sort == 0
        assert sorted_file.read_text(encoding="utf-8").splitlines() == ["a", "b", "z", "z"]

        # Dedupe
        deduped_file = Path(temp_dir) / "deduped.txt"
        exit_code_dedupe = handle_cli_execution(["dedupe", str(sorted_file), "-o", str(deduped_file)])
        assert exit_code_dedupe == 0
        assert deduped_file.read_text(encoding="utf-8").splitlines() == ["a", "b", "z"]


def test_cli_cupp_extended() -> None:
    """Test CLI 'cupp' command with extended family and abbreviation arguments."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "cupp_output.txt"
        cli_args = [
            "cupp",
            "--first-name", "Alice",
            "--last-name", "Smith",
            "--mother", "Mary",
            "--father", "John",
            "--name-abbr", "AS, admin",
            "--birthdate", "1995",
            "-o", str(output_file),
        ]
        exit_code = handle_cli_execution(cli_args)
        assert exit_code == 0
        assert output_file.exists()
        file_lines = output_file.read_text(encoding="utf-8").splitlines()
        assert len(file_lines) > 20
        lower_content = [line_item.lower() for line_item in file_lines]
        assert any("mary" in line_item for line_item in lower_content)
        assert any("john" in line_item for line_item in lower_content)
        assert any("as" in line_item for line_item in lower_content)
