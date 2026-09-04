"""
config.py - GitHub Contribution Graph Automator
Validates and loads configuration parameters from CLI inputs or defaults.
Provides a trusted Config object for the application.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# Sensible default application settings
DEFAULT_CHUNK_SIZE = 10
DEFAULT_COMMITS_PER_DAY = 5
DEFAULT_INTERVAL_BETWEEN_COMMITS = 60
DEFAULT_START_TIME = "09:00"


@dataclass
class Config:
    """Validated configuration for the GitHub Contribution Graph Automator."""
    repository_path: str
    chunk_size: int
    commits_per_day: int
    interval_between_commits: int
    start_time: str


def validate_start_time(start_time_str: str) -> str:
    """
    Validates a 24-hour time string in 'HH:MM' format.
    Returns normalized 'HH:MM' string.
    """
    if not isinstance(start_time_str, str):
        raise ValueError(
            f"start_time must be a string in 'HH:MM' format, got {type(start_time_str).__name__}"
        )

    cleaned = start_time_str.strip()
    parts = cleaned.split(":")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid start_time format: '{start_time_str}'. Expected 'HH:MM' (24-hour format, e.g. '09:00')."
        )

    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        raise ValueError(
            f"Invalid start_time format: '{start_time_str}'. Expected numeric 'HH:MM' (e.g. '09:00')."
        )

    if not (0 <= hour <= 23):
        raise ValueError(f"start_time hour must be between 0 and 23, got {hour}")

    if not (0 <= minute <= 59):
        raise ValueError(f"start_time minute must be between 0 and 59, got {minute}")

    return f"{hour:02d}:{minute:02d}"


def load_config(
    repo_path: Optional[str] = None,
    chunk_size: Optional[int] = None,
    commits_per_day: Optional[int] = None,
    interval_between_commits: Optional[int] = None,
    start_time: Optional[str] = None
) -> Config:
    """
    Resolves repository path, applies default settings for omitted values,
    validates all inputs, and returns a trusted Config object.
    """
    # 1. Resolve and validate repository path
    if repo_path is not None:
        target_path = Path(repo_path).expanduser().resolve()
    else:
        target_path = Path.cwd().resolve()

    if not target_path.exists():
        raise ValueError(f"Repository path does not exist: {target_path}")

    if not target_path.is_dir():
        raise ValueError(f"Repository path is not a directory: {target_path}")

    resolved_repo_path = str(target_path)

    # 2. Resolve and validate chunk_size
    resolved_chunk_size = chunk_size if chunk_size is not None else DEFAULT_CHUNK_SIZE
    if resolved_chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {resolved_chunk_size}")

    # 3. Resolve and validate commits_per_day
    resolved_commits_per_day = (
        commits_per_day if commits_per_day is not None else DEFAULT_COMMITS_PER_DAY
    )
    if resolved_commits_per_day <= 0:
        raise ValueError(f"commits_per_day must be positive, got {resolved_commits_per_day}")

    # 4. Resolve and validate interval_between_commits
    resolved_interval = (
        interval_between_commits
        if interval_between_commits is not None
        else DEFAULT_INTERVAL_BETWEEN_COMMITS
    )
    if resolved_interval < 0:
        raise ValueError(f"interval_between_commits cannot be negative, got {resolved_interval}")

    # 5. Resolve and validate start_time
    raw_start_time = start_time if start_time is not None else DEFAULT_START_TIME
    resolved_start_time = validate_start_time(raw_start_time)

    return Config(
        repository_path=resolved_repo_path,
        chunk_size=resolved_chunk_size,
        commits_per_day=resolved_commits_per_day,
        interval_between_commits=resolved_interval,
        start_time=resolved_start_time
    )
