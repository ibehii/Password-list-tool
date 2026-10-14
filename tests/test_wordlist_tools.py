"""Tests for streaming wordlist manipulation algorithms."""

from __future__ import annotations

import tempfile
from pathlib import Path

from lib.wordlist_tools import (
    _atomic_replace,
    count_lines,
    external_sort,
    filter_wordlist,
    generate_word_mutations,
    merge_wordlists,
    mutate_wordlist,
    split_wordlist,
    streaming_deduplicate,
)


def test_count_lines() -> None:
    """Verify line counting works on empty and populated files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"

        test_file.write_text("", encoding="utf-8")
        assert count_lines(test_file) == 0

        test_file.write_text("line1\nline2\nline3\n", encoding="utf-8")
        assert count_lines(test_file) == 3


def test_external_sort_chunks() -> None:
    """Test external sort with very small chunk size to trigger multi-chunk merging."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "unsorted.txt"
        words = ["zebra", "apple", "mango", "banana", "cherry", "orange", "grape", "avocado"]
        input_file.write_text("\n".join(words) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "sorted.txt"
        external_sort(input_path=input_file, output_path=output_file, chunk_lines=3)

        sorted_lines = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert sorted_lines == sorted(words)


def test_external_sort_reverse_in_place() -> None:
    """Test reverse sorting in-place."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test_in_place.txt"
        words = ["delta", "alpha", "charlie", "bravo"]
        test_file.write_text("\n".join(words) + "\n", encoding="utf-8")

        external_sort(input_path=test_file, output_path=None, chunk_lines=2, reverse=True)

        result_lines = [line.strip() for line in test_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert result_lines == ["delta", "charlie", "bravo", "alpha"]


def test_streaming_deduplicate() -> None:
    """Test duplicate line removal via streaming sort and filter."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "duplicates.txt"
        words_with_dupes = ["pass1", "pass2", "pass1", "pass3", "pass2", "pass1", "pass4"]
        input_file.write_text("\n".join(words_with_dupes) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "deduped.txt"
        total_read, total_unique = streaming_deduplicate(
            input_path=input_file,
            output_path=output_file,
            sort_first=True,
            chunk_lines=2,
        )

        assert total_read == len(words_with_dupes)
        assert total_unique == 4

        unique_lines = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert unique_lines == ["pass1", "pass2", "pass3", "pass4"]


def test_merge_wordlists() -> None:
    """Test combining multiple files via streaming."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_one = Path(temp_dir) / "file1.txt"
        file_two = Path(temp_dir) / "file2.txt"

        file_one.write_text("alpha\nbravo\n", encoding="utf-8")
        file_two.write_text("charlie\ndelta\nalpha\n", encoding="utf-8")

        output_file = Path(temp_dir) / "merged.txt"
        lines_written = merge_wordlists([file_one, file_two], output_file, deduplicate=True)

        assert lines_written == 4
        result_lines = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert "alpha" in result_lines
        assert "delta" in result_lines
        assert len(result_lines) == 4


def test_filter_wordlist() -> None:
    """Test filtering by length, character classes, and regex."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "input.txt"
        passwords = [
            "short",              # len 5
            "validPass1!",        # len 10, lower, upper, digit, symbol
            "lowercaseonly123",   # len 16, no upper
            "UPPERCASE123!",      # len 14, no lower
            "LettersOnly!",       # len 12, no digit
            "MatchRegex99#",      # len 13, matches regex
        ]
        input_file.write_text("\n".join(passwords) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "filtered.txt"
        total_scanned, total_matched = filter_wordlist(
            input_path=input_file,
            output_path=output_file,
            min_length=8,
            max_length=20,
            require_lower=True,
            require_upper=True,
            require_digit=True,
            require_symbol=True,
        )

        assert total_scanned == len(passwords)
        matched_lines = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert "validPass1!" in matched_lines
        assert "MatchRegex99#" in matched_lines
        assert "short" not in matched_lines
        assert "lowercaseonly123" not in matched_lines


def test_mutate_wordlist() -> None:
    """Test wordlist mutations and leetspeak generation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "words.txt"
        input_file.write_text("admin\n", encoding="utf-8")

        output_file = Path(temp_dir) / "mutated.txt"
        input_count, mutation_count = mutate_wordlist(
            input_path=input_file,
            output_path=output_file,
            include_leet=True,
            case_variations=True,
        )

        assert input_count == 1
        assert mutation_count > 10

        mutated_words = [line.strip() for line in output_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert "@dm1n" in mutated_words or "admin" in mutated_words
        assert "ADMIN" in mutated_words


def test_split_wordlist() -> None:
    """Test splitting large wordlist into line-limited chunk files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "big.txt"
        lines = [f"password_{num}" for num in range(25)]
        input_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        output_dir = Path(temp_dir) / "chunks"
        created_chunks = split_wordlist(input_file, output_dir, lines_per_chunk=10)

        assert len(created_chunks) == 3
        # First chunk has 10 lines
        assert count_lines(created_chunks[0]) == 10
        # Second chunk has 10 lines
        assert count_lines(created_chunks[1]) == 10
        # Third chunk has 5 lines
        assert count_lines(created_chunks[2]) == 5


def test_external_sort_return_stats() -> None:
    """Verify external_sort with return_stats=True returns exact line metrics."""
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "stats_input.txt"
        words = ["echo", "bravo", "alpha", "bravo", "charlie", "alpha"]
        input_file.write_text("\n".join(words) + "\n", encoding="utf-8")

        output_file = Path(temp_dir) / "stats_output.txt"
        res_path, read_lines, written_lines = external_sort(
            input_path=input_file,
            output_path=output_file,
            chunk_lines=2,
            deduplicate=True,
            return_stats=True,
        )

        assert res_path == output_file
        assert read_lines == 6
        assert written_lines == 4
        assert count_lines(output_file) == 4


def test_atomic_replace_helper() -> None:
    """Verify _atomic_replace correctly swaps source to destination atomically."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_file = Path(temp_dir) / "source.txt"
        dest_file = Path(temp_dir) / "destination.txt"

        source_file.write_text("fresh content\n", encoding="utf-8")
        dest_file.write_text("old content\n", encoding="utf-8")

        _atomic_replace(source_file, dest_file)

        assert not source_file.exists()
        assert dest_file.exists()
        assert dest_file.read_text(encoding="utf-8") == "fresh content\n"

