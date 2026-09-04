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
        help="Approximate number of lines per chunk."
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
        help="Simulate the planning and preview steps without creating commits or pushing."
    )
    return parser.parse_args()


def display_preview(
    repo_path: str,
    total_files: int,
    total_lines: int,
    total_chunks: int,
    commits_per_day: int,
    estimated_duration_days: int,
    first_commit_time: Optional[datetime] = None,
    last_commit_time: Optional[datetime] = None
) -> None:
    """Displays Step 4: Preview to the user before starting execution."""
    print("\n" + "=" * 55)
    print("               COMMIT PLAN PREVIEW")
    print("=" * 55)
    print(f" Repository:         {os.path.abspath(repo_path)}")
    print(f" Total Files:        {total_files}")
    print(f" Total Lines:        {total_lines}")
    print(f" Total Chunks:       {total_chunks}")
    print(f" Commits Per Day:    {commits_per_day}")
    print(f" Estimated Duration: {estimated_duration_days} day(s)")
    if first_commit_time:
        print(f" First Commit:       {first_commit_time.strftime('%Y-%m-%d %H:%M:%S')}")
    if last_commit_time:
        print(f" Last Commit:        {last_commit_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55 + "\n")