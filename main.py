#!/usr/bin/env python3
"""
GitHubContributionGraph CLI (main.py)
Automates GitHub activity graphs by scheduling and gradually pushing repository chunks.
Follows the specification outlined in README.md.
"""

import sys
import os
import argparse
from datetime import datetime
from typing import Optional

import config
import git
import splitter
import scheduler
from cli import parse_args



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




def confirm_start() -> bool:
    """Prompts the user for confirmation to proceed."""
    try:
        response = input("Start? [y/N]: ").strip().lower()
        return response in ("y", "yes")
    except (KeyboardInterrupt, EOFError):
        print("\nAborted by user.")
        return False


def main():
    args = parse_args()

    # ─────────────────────────────────────
    # 1. INITIALIZE
    # ─────────────────────────────────────
    cfg = config.load_config(
        repo_path=args.repository_path,
        chunk_size=args.chunk_size,
        commits_per_day=args.commits_per_day,
        interval_between_commits=args.interval_between_commits,
        start_time=args.start_time
    )

    repo_path = cfg.repository_path or os.getcwd()

    if not git.is_git_repository(repo_path):
        print(f"Error: '{repo_path}' is not a valid git repository.", file=sys.stderr)
        sys.exit(1)

    print(f"Initialized repository target: {repo_path}")

    # ─────────────────────────────────────
    # 2. READ REPOSITORY
    # ─────────────────────────────────────
    print("Reading repository and preparing chunks...")
    files = splitter.get_repository_files(repo_path)
    if not files:
        print("Error: No eligible files found in repository to chunk.", file=sys.stderr)
        sys.exit(1)

    chunks, total_lines = splitter.divide_into_chunks(repo_path, files, cfg.chunk_size)
    total_chunks = len(chunks)

    if total_chunks == 0:
        print("Error: No chunks generated. Repository might be empty or all files are ignored.", file=sys.stderr)
        sys.exit(1)

    # ─────────────────────────────────────
    # 3. CREATE COMMIT PLAN
    # ─────────────────────────────────────
    commit_plan = scheduler.create_commit_plan(
        chunks=chunks,
        commits_per_day=cfg.commits_per_day,
        start_time_str=cfg.start_time,
        interval_minutes=cfg.interval_between_commits
    )

    estimated_days = (total_chunks + cfg.commits_per_day - 1) // cfg.commits_per_day
    first_commit_time = commit_plan[0].scheduled_time if commit_plan else None
    last_commit_time = commit_plan[-1].scheduled_time if commit_plan else None

    # ─────────────────────────────────────
    # 4. PREVIEW
    # ─────────────────────────────────────
    display_preview(
        repo_path=repo_path,
        total_files=len(files),
        total_lines=total_lines,
        total_chunks=total_chunks,
        commits_per_day=cfg.commits_per_day,
        estimated_duration_days=estimated_days,
        first_commit_time=first_commit_time,
        last_commit_time=last_commit_time
    )

    if not args.assume_yes:
        if not confirm_start():
            print("Execution aborted.")
            sys.exit(0)

    # ─────────────────────────────────────
    # 5. EXECUTE
    # ─────────────────────────────────────
    print("\nStarting execution plan...\n")
    for idx, item in enumerate(commit_plan, 1):
        next_time = commit_plan[idx].scheduled_time.strftime("%Y-%m-%d %H:%M:%S") if idx < len(commit_plan) else "None (Done)"

        if not args.dry_run:
            # Wait until the assigned scheduled time
            scheduler.wait_until(item.scheduled_time)

            # Apply chunk to the repository
            splitter.apply_chunk(repo_path, item.chunk)

            # Stage, commit, and push
            git.add(repo_path, item.chunk.file_path)
            message = item.commit_message or f"feat: update {os.path.basename(item.chunk.file_path)} (part {item.chunk.part_index}/{item.chunk.total_parts})"
            git.commit(repo_path, message)
            git.push(repo_path)
        else:
            print(f"[DRY-RUN] Simulating commit at {item.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

        progress_pct = (idx / total_chunks) * 100
        print(f"[{idx}/{total_chunks}] ({progress_pct:.1f}%) Committed: {item.chunk.file_path} (chunk {item.chunk.part_index}/{item.chunk.total_parts})")
        print(f"   Next scheduled commit: {next_time}")

    # ─────────────────────────────────────
    # 6. FINISH
    # ─────────────────────────────────────
    print("\nAll chunks have been committed.")


if __name__ == "__main__":
    main()
