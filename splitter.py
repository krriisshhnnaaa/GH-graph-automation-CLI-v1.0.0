"""
splitter.py - GitHub Contribution Graph Automator
Reads a repository and divides its files into ordered, reconstructable chunks.
Pure file/content chunking logic: decoupled from Git, scheduling, and CLI.
"""

from dataclasses import dataclass
import math
from pathlib import Path
from typing import List, Tuple


@dataclass
class Chunk:
    """Represents a discrete slice of a file to be committed."""
    file_path: str
    content: str
    part_index: int
    total_parts: int


def is_text_file(path: Path) -> bool:
    """
    Checks if a file is readable as UTF-8 text.
    Returns False for binary files or decoding errors.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, PermissionError, OSError):
        return False


def get_repository_files(repo_path: str) -> List[Path]:
    """
    Recursively scans repo_path for text files, ignoring .git/ directory.
    Returns a deterministically sorted list of relative Path objects.
    Empty files (0 bytes) are skipped for v1.
    """
    root = Path(repo_path).resolve()
    discovered_files: List[Path] = []

    for item in root.rglob("*"):
        # Only process regular files
        if not item.is_file():
            continue

        # Ignore .git directory and anything inside it
        try:
            rel_path = item.relative_to(root)
        except ValueError:
            continue

        parts = rel_path.parts
        if any(part == ".git" for part in parts):
            continue

        # Skip empty files for v1
        if item.stat().st_size == 0:
            continue

        # Text files only
        if not is_text_file(item):
            continue

        discovered_files.append(rel_path)

    # Deterministic sorting by path string
    discovered_files.sort(key=lambda p: str(p))
    return discovered_files


def divide_into_chunks(
    repo_path: str,
    files: List[Path],
    chunk_size: int
) -> Tuple[List[Chunk], int]:
    """
    Reads the given files and divides them into chunks of ~chunk_size lines.
    Preserves exact whitespace, indentations, and newlines.
    Chunks never cross file boundaries.

    Returns:
    - chunks: List of Chunk objects
    - total_lines: Sum of all lines processed across files
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    root = Path(repo_path).resolve()
    chunks: List[Chunk] = []
    total_lines = 0

    for rel_path in files:
        full_path = root / rel_path

        try:
            with full_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue

        line_count = len(lines)
        if line_count == 0:
            continue

        total_lines += line_count
        total_parts = math.ceil(line_count / chunk_size)

        for part_idx in range(1, total_parts + 1):
            start_idx = (part_idx - 1) * chunk_size
            end_idx = min(start_idx + chunk_size, line_count)
            chunk_lines = lines[start_idx:end_idx]
            chunk_content = "".join(chunk_lines)

            chunks.append(
                Chunk(
                    file_path=str(rel_path),
                    content=chunk_content,
                    part_index=part_idx,
                    total_parts=total_parts
                )
            )

    return chunks, total_lines


def apply_chunk(repo_path: str, chunk: Chunk) -> None:
    """
    Applies a chunk to the destination repository.
    - If part_index == 1: creates or overwrites the file.
    - If part_index > 1: appends content to the existing file.
    Ensures parent directories exist before writing.
    """
    dest_path = Path(repo_path).resolve() / chunk.file_path
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if chunk.part_index == 1:
        with dest_path.open("w", encoding="utf-8") as f:
            f.write(chunk.content)
    else:
        with dest_path.open("a", encoding="utf-8") as f:
            f.write(chunk.content)
