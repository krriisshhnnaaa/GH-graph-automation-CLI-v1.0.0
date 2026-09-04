import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for repository, chunks, and timing."""
    parser = argparse.ArgumentParser(
        prog="GH-graph-automation",
        description="GitHub Contribution Graph Automator - gradually commit and push repository changes over time."
    )
    parser.add_argument(
        "-r", "--repo",
        dest="repository_path",
        default=None,
        help="Path to the Git repository (defaults to config or current directory)."
    )
    parser.add_argument(
        "-c", "--chunk-size",
        dest="chunk_size",
        type=int,
        default=None,
        help="Number of lines per chunk."
    )
    parser.add_argument(
        "-d", "--commits-per-day",
        dest="commits_per_day",
        type=int,
        default=None,
        help="Number of commits to push per day."
    )
    parser.add_argument(
        "-i", "--interval",
        dest="interval_between_commits",
        type=int,
        default=None,
        help="Interval in minutes between commits on the same day."
    )
    parser.add_argument(
        "-s", "--start-time",
        dest="start_time",
        default=None,
        help="Daily starting time for commits (format: HH:MM, e.g., 09:00)."
    )
    parser.add_argument(
        "-y", "--yes",
        dest="assume_yes",
        action="store_true",
        help="Skip the preview confirmation prompt and start execution immediately."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the entire execution without creating commits or pushing."
    )
    return parser.parse_args()

