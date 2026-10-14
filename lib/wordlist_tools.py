#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  ____________________________________________
"""High-performance, streaming wordlist manipulation engine.

Designed for massive password lists (multi-gigabyte files) with minimum RAM
usage and maximum throughput. None of the routines load entire lists into memory.
"""

from __future__ import annotations

import heapq
import os
import re
import shutil
import tempfile
from contextlib import ExitStack
from pathlib import Path
from typing import Callable, Generator, Iterable, Optional, Union

# Read and write buffer size: 64 KB for fast streaming I/O
STREAM_BUFFER_SIZE: int = 64 * 1024
DEFAULT_CHUNK_LINES: int = 250_000
MAX_MERGE_BATCH: int = 64

_RE_LOWER: re.Pattern = re.compile(r"[a-z]")
_RE_UPPER: re.Pattern = re.compile(r"[A-Z]")
_RE_DIGIT: re.Pattern = re.compile(r"[0-9]")
_RE_SYMBOL: re.Pattern = re.compile(r"[^a-zA-Z0-9]")


def _atomic_replace(source_path: Path, target_path: Path) -> None:
    """Safely and atomically replace target_path with source_path."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(source_path, target_path)
    except OSError:
        shutil.move(str(source_path), str(target_path))


def count_lines(file_path: Path) -> int:
    """Count total number of lines in a file using fast binary chunking.

    Memory footprint is constant (~1 MB). Correctly accounts for non-empty
    files whose final line lacks a trailing newline.
    """
    resolved_path = Path(file_path).resolve()
    if not resolved_path.is_file():
        return 0

    total_lines = 0
    buffer_size = 1024 * 1024  # 1 MB binary buffer
    last_byte = b""

    with open(resolved_path, "rb") as source_stream:
        while chunk_bytes := source_stream.read(buffer_size):
            total_lines += chunk_bytes.count(b"\n")
            last_byte = chunk_bytes[-1:]

    # Count final line if non-empty and lacks trailing newline
    if last_byte and last_byte != b"\n":
        total_lines += 1

    return total_lines


def _ensure_newline(text: str) -> str:
    """Ensure a string terminates with a single newline."""
    return text if text.endswith("\n") else f"{text}\n"


def _create_temp_workspace(preferred_parent: Path, prefix: str) -> Path:
    """Create a temporary directory, preferring the target file's parent partition.

    This avoids filling up RAM-backed /tmp (tmpfs) on large files and ensures
    atomic, same-filesystem renaming.
    """
    try:
        preferred_parent.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix=prefix, dir=str(preferred_parent)))
    except (OSError, PermissionError):
        return Path(tempfile.mkdtemp(prefix=prefix))


def external_sort(
    input_path: Path,
    output_path: Optional[Path] = None,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    reverse: bool = False,
    deduplicate: bool = False,
    progress_callback: Optional[Callable[[int], None]] = None,
    return_stats: bool = False,
) -> Union[Path, tuple[Path, int, int]]:
    """Sort multi-gigabyte files using external merge sort.

    Memory complexity: O(chunk_lines) during partitioning, O(batch_size) during merge.
    Time complexity: O(N log N).
    Supports inline deduplication during chunking and merging for 2x faster deduping.
    When return_stats is True, returns (output_path, total_read, total_written) without extra disk passes.
    """
    input_path = Path(input_path).resolve()
    target_output_path = Path(output_path).resolve() if output_path else input_path

    if not input_path.is_file():
        raise FileNotFoundError(f"Source file not found: {input_path}")

    temp_directory = _create_temp_workspace(target_output_path.parent, prefix="pass_tool_sort_")
    chunk_paths: list[Path] = []
    chunk_sizes: list[int] = []
    chunk_counter = 0
    total_read_lines = 0

    try:
        current_chunk: list[str] = []
        with open(input_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream:
            for raw_line in source_stream:
                total_read_lines += 1
                normalized_line = raw_line if raw_line.endswith("\n") else f"{raw_line}\n"
                current_chunk.append(normalized_line)

                if len(current_chunk) >= chunk_lines:
                    if deduplicate:
                        current_chunk = sorted(set(current_chunk), reverse=reverse)
                    else:
                        current_chunk.sort(reverse=reverse)

                    temp_chunk_path = temp_directory / f"chunk_{chunk_counter}.tmp"
                    with open(temp_chunk_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as temp_out:
                        temp_out.writelines(current_chunk)

                    chunk_paths.append(temp_chunk_path)
                    chunk_sizes.append(len(current_chunk))
                    chunk_counter += 1
                    current_chunk.clear()

                    if progress_callback:
                        progress_callback(chunk_counter * chunk_lines)

            # Flush final chunk if any lines remain
            if current_chunk:
                if deduplicate:
                    current_chunk = sorted(set(current_chunk), reverse=reverse)
                else:
                    current_chunk.sort(reverse=reverse)

                temp_chunk_path = temp_directory / f"chunk_{chunk_counter}.tmp"
                with open(temp_chunk_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as temp_out:
                    temp_out.writelines(current_chunk)

                chunk_paths.append(temp_chunk_path)
                chunk_sizes.append(len(current_chunk))
                current_chunk.clear()

        final_temp_output = temp_directory / "merged_output.tmp"
        total_written_lines = 0

        # Handle empty file edge case
        if not chunk_paths:
            final_temp_output.touch()
            total_written_lines = 0
        elif len(chunk_paths) == 1:
            # Single chunk: avoid redundant heapq merge pass
            _atomic_replace(chunk_paths[0], final_temp_output)
            total_written_lines = chunk_sizes[0]
        else:
            # Hierarchical multi-way merge in bounded batches
            active_chunks = list(chunk_paths)
            intermediate_counter = 0

            while len(active_chunks) > MAX_MERGE_BATCH:
                next_round_chunks: list[Path] = []
                for batch_start in range(0, len(active_chunks), MAX_MERGE_BATCH):
                    batch_slice = active_chunks[batch_start : batch_start + MAX_MERGE_BATCH]
                    if len(batch_slice) == 1:
                        next_round_chunks.append(batch_slice[0])
                        continue

                    batch_out_path = temp_directory / f"intermediate_{intermediate_counter}.tmp"
                    intermediate_counter += 1

                    with ExitStack() as exit_stack:
                        opened_streams = [
                            exit_stack.enter_context(
                                open(cp, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE)
                            )
                            for cp in batch_slice
                        ]
                        merged_stream = heapq.merge(*opened_streams, reverse=reverse)
                        with open(batch_out_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as batch_out:
                            previous_line: Optional[str] = None
                            for line_item in merged_stream:
                                if deduplicate:
                                    if previous_line is None or line_item != previous_line:
                                        batch_out.write(line_item)
                                        previous_line = line_item
                                else:
                                    batch_out.write(line_item)

                    # Delete consumed temporary chunks to free disk space immediately
                    for old_chunk in batch_slice:
                        if old_chunk.is_file():
                            old_chunk.unlink()

                    next_round_chunks.append(batch_out_path)

                active_chunks = next_round_chunks

            # Final merge round for remaining <= MAX_MERGE_BATCH chunks
            with ExitStack() as exit_stack:
                opened_streams = [
                    exit_stack.enter_context(
                        open(cp, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE)
                    )
                    for cp in active_chunks
                ]
                merged_stream = heapq.merge(*opened_streams, reverse=reverse)
                with open(final_temp_output, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as final_out:
                    previous_line: Optional[str] = None
                    for line_item in merged_stream:
                        if deduplicate:
                            if previous_line is None or line_item != previous_line:
                                final_out.write(line_item)
                                previous_line = line_item
                                total_written_lines += 1
                        else:
                            final_out.write(line_item)
                            total_written_lines += 1

        _atomic_replace(final_temp_output, target_output_path)
        if return_stats:
            return target_output_path, total_read_lines, total_written_lines
        return target_output_path

    finally:
        if temp_directory.exists():
            shutil.rmtree(temp_directory, ignore_errors=True)


def streaming_deduplicate(
    input_path: Path,
    output_path: Optional[Path] = None,
    sort_first: bool = True,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> tuple[int, int]:
    """Deduplicate lines in a wordlist without loading the file into memory.

    If sort_first is True, performs a single-pass external merge sort with inline
    deduplication (O(1) memory, maximum speed).
    If sort_first is False, assumes the file is already sorted and removes consecutive duplicates.
    Returns: (total_lines_read, unique_lines_written)
    """
    input_path = Path(input_path).resolve()
    target_output_path = Path(output_path).resolve() if output_path else input_path

    if not input_path.is_file():
        return 0, 0

    if sort_first:
        # Zero-extra-pass sort + deduplicate: counts are captured directly during sorting
        _, total_read, total_unique = external_sort(
            input_path=input_path,
            output_path=target_output_path,
            chunk_lines=chunk_lines,
            reverse=False,
            deduplicate=True,
            progress_callback=progress_callback,
            return_stats=True,
        )
        return total_read, total_unique

    # Streaming adjacent deduplication for already-sorted input
    temp_dir = _create_temp_workspace(target_output_path.parent, prefix="pass_tool_dedupe_")
    deduped_temp_output = temp_dir / "deduped_output.tmp"
    total_read = 0
    total_written = 0
    previous_line: Optional[str] = None

    try:
        with open(input_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream, \
             open(deduped_temp_output, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as output_stream:
            for raw_line in source_stream:
                total_read += 1
                normalized_line = raw_line if raw_line.endswith("\n") else f"{raw_line}\n"
                if previous_line is None or normalized_line != previous_line:
                    output_stream.write(normalized_line)
                    previous_line = normalized_line
                    total_written += 1

        _atomic_replace(deduped_temp_output, target_output_path)
        return total_read, total_written

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def merge_wordlists(
    input_paths: list[Path],
    output_path: Path,
    deduplicate: bool = False,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> int:
    """Merge multiple wordlists into a single destination file via streaming.

    Safely handles cases where output_path is one of the input_paths.
    If deduplicate is True, runs streaming deduplication on the combined result.
    Returns total lines written.
    """
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = _create_temp_workspace(output_path.parent, prefix="pass_tool_merge_")
    temp_output_path = temp_dir / "merged_intermediate.tmp"

    total_lines_streamed = 0
    try:
        with open(temp_output_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as output_stream:
            for file_path in input_paths:
                resolved_path = Path(file_path).resolve()
                if not resolved_path.is_file():
                    continue
                with open(resolved_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream:
                    for raw_line in source_stream:
                        normalized_line = raw_line if raw_line.endswith("\n") else f"{raw_line}\n"
                        output_stream.write(normalized_line)
                        total_lines_streamed += 1
                        if progress_callback and total_lines_streamed % 50_000 == 0:
                            progress_callback(total_lines_streamed)

        if deduplicate:
            _, unique_count = streaming_deduplicate(input_path=temp_output_path, output_path=output_path, sort_first=True)
            return unique_count

        _atomic_replace(temp_output_path, output_path)
        return total_lines_streamed

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def filter_wordlist(
    input_path: Path,
    output_path: Path,
    min_length: int = 0,
    max_length: int = 0,
    require_lower: bool = False,
    require_upper: bool = False,
    require_digit: bool = False,
    require_symbol: bool = False,
    regex_pattern: Optional[str] = None,
    allowed_charset: Optional[set[str]] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> tuple[int, int]:
    """Filter lines of a massive wordlist using criteria without loading into memory.

    Safely handles in-place filtering (input_path == output_path).
    Returns: (total_scanned, total_matched)
    """
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    compiled_regex: Optional[re.Pattern] = re.compile(regex_pattern) if regex_pattern else None

    temp_dir = _create_temp_workspace(output_path.parent, prefix="pass_tool_filter_")
    temp_output_path = temp_dir / "filtered_result.tmp"

    total_scanned = 0
    total_matched = 0

    try:
        with open(input_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream, \
             open(temp_output_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as output_stream:
            for raw_line in source_stream:
                total_scanned += 1
                cleaned_word = raw_line.rstrip("\r\n")

                word_length = len(cleaned_word)
                if min_length > 0 and word_length < min_length:
                    continue
                if max_length > 0 and word_length > max_length:
                    continue

                if require_lower and not _RE_LOWER.search(cleaned_word):
                    continue
                if require_upper and not _RE_UPPER.search(cleaned_word):
                    continue
                if require_digit and not _RE_DIGIT.search(cleaned_word):
                    continue
                if require_symbol and not _RE_SYMBOL.search(cleaned_word):
                    continue

                if compiled_regex and not compiled_regex.search(cleaned_word):
                    continue

                if allowed_charset:
                    has_disallowed_char = False
                    for char_element in cleaned_word:
                        if char_element not in allowed_charset:
                            has_disallowed_char = True
                            break
                    if has_disallowed_char:
                        continue

                output_stream.write(f"{cleaned_word}\n")
                total_matched += 1

                if progress_callback and total_scanned % 50_000 == 0:
                    progress_callback(total_scanned, total_matched)

        _atomic_replace(temp_output_path, output_path)
        return total_scanned, total_matched

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


LEET_REPLACEMENTS: dict[str, list[str]] = {
    "a": ["@", "4"],
    "e": ["3"],
    "i": ["1", "!"],
    "o": ["0"],
    "s": ["$", "5"],
    "t": ["7", "+"],
    "b": ["8"],
    "g": ["9"],
}

DEFAULT_MUTATION_SUFFIXES: list[str] = [
    "", "1", "12", "123", "1234", "!", "!!", "?", "@", "0", "01", "2024", "2025", "2026"
]
DEFAULT_MUTATION_PREFIXES: list[str] = ["", "!", "@", "#", "$", "1"]


def generate_word_mutations(
    word: str,
    include_leet: bool = True,
    case_variations: bool = True,
    suffixes: Optional[list[str]] = None,
    prefixes: Optional[list[str]] = None,
) -> Generator[str, None, None]:
    """Generate rule-based mutations for a single word lazily.

    Yields strings one-by-one.
    """
    suffixes_to_use = suffixes if suffixes is not None else DEFAULT_MUTATION_SUFFIXES
    prefixes_to_use = prefixes if prefixes is not None else DEFAULT_MUTATION_PREFIXES

    candidate_forms: set[str] = {word}

    if case_variations:
        candidate_forms.add(word.lower())
        candidate_forms.add(word.upper())
        candidate_forms.add(word.capitalize())
        candidate_forms.add(word.swapcase())

    if include_leet:
        leet_chars: list[str] = []
        for char_item in word.lower():
            if char_item in LEET_REPLACEMENTS:
                leet_chars.append(LEET_REPLACEMENTS[char_item][0])
            else:
                leet_chars.append(char_item)
        full_leet_form = "".join(leet_chars)
        candidate_forms.add(full_leet_form)
        if case_variations:
            candidate_forms.add(full_leet_form.capitalize())
            candidate_forms.add(full_leet_form.upper())

    seen_in_batch: set[str] = set()
    for base_candidate in candidate_forms:
        for prefix_item in prefixes_to_use:
            for suffix_item in suffixes_to_use:
                mutated_result = f"{prefix_item}{base_candidate}{suffix_item}"
                if mutated_result not in seen_in_batch:
                    seen_in_batch.add(mutated_result)
                    yield mutated_result


def mutate_wordlist(
    input_path: Path,
    output_path: Path,
    include_leet: bool = True,
    case_variations: bool = True,
    suffixes: Optional[list[str]] = None,
    prefixes: Optional[list[str]] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> tuple[int, int]:
    """Mutate words in an input wordlist into a new output file via streaming.

    Safely handles in-place mutation (input_path == output_path).
    Returns: (total_input_words, total_mutations_generated)
    """
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = _create_temp_workspace(output_path.parent, prefix="pass_tool_mutate_")
    temp_output_path = temp_dir / "mutated_result.tmp"

    input_count = 0
    mutations_count = 0

    try:
        with open(input_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream, \
             open(temp_output_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE) as output_stream:
            for raw_line in source_stream:
                cleaned_word = raw_line.rstrip("\r\n")
                if not cleaned_word:
                    continue
                input_count += 1

                for mutated_word in generate_word_mutations(
                    word=cleaned_word,
                    include_leet=include_leet,
                    case_variations=case_variations,
                    suffixes=suffixes,
                    prefixes=prefixes,
                ):
                    output_stream.write(f"{mutated_word}\n")
                    mutations_count += 1

                if progress_callback and input_count % 10_000 == 0:
                    progress_callback(input_count, mutations_count)

        _atomic_replace(temp_output_path, output_path)
        return input_count, mutations_count

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def split_wordlist(
    input_path: Path,
    output_dir: Path,
    lines_per_chunk: int = 1_000_000,
    prefix: str = "chunk_",
    extension: str = ".txt",
) -> list[Path]:
    """Split a massive wordlist into smaller numbered files using line streaming.

    Constant memory usage.
    """
    if lines_per_chunk <= 0:
        raise ValueError("lines_per_chunk must be greater than zero")

    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    created_chunk_paths: list[Path] = []
    chunk_counter = 1
    current_line_count = 0
    current_stream = None

    try:
        with open(input_path, "r", encoding="utf-8", errors="ignore", buffering=STREAM_BUFFER_SIZE) as source_stream:
            for raw_line in source_stream:
                if current_stream is None:
                    chunk_file_name = f"{prefix}{chunk_counter:04d}{extension}"
                    chunk_file_path = output_dir / chunk_file_name
                    current_stream = open(chunk_file_path, "w", encoding="utf-8", buffering=STREAM_BUFFER_SIZE)
                    created_chunk_paths.append(chunk_file_path)

                normalized_line = raw_line if raw_line.endswith("\n") else f"{raw_line}\n"
                current_stream.write(normalized_line)
                current_line_count += 1

                if current_line_count >= lines_per_chunk:
                    current_stream.close()
                    current_stream = None
                    chunk_counter += 1
                    current_line_count = 0

    finally:
        if current_stream and not current_stream.closed:
            current_stream.close()

    return created_chunk_paths
