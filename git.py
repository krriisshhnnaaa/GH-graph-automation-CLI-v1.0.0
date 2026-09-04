"""
git.py - GitHub Contribution Graph Automator
Encapsulates all Git interactions: worktree verification, staging, committing, and pushing.
Maintains strict separation: knows only Git operations, without CLI, scheduling, or UI logic.
"""

from pathlib import Path
import subprocess
from typing import List, Optional


class GitError(RuntimeError):
    """Raised when a Git command fails."""
    pass


def _run_git(
    repo_path: str,
    args: List[str],
    check: bool = True
) -> subprocess.CompletedProcess:
    """
    Executes a Git command inside the target repository.
    Uses argument lists and avoids shell=True for security and consistency.
    """
    cmd = ["git"] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError:
        raise GitError("Git executable not found. Please ensure Git is installed and in your system PATH.")
    except Exception as exc:
        raise GitError(f"Failed to execute Git command: {' '.join(cmd)}\nError: {exc}") from exc

    if check and result.returncode != 0:
        err_msg = result.stderr.strip() or result.stdout.strip()
        raise GitError(f"Git command failed: {' '.join(cmd)}\n{err_msg}")

    return result


def is_git_repository(repo_path: str) -> bool:
    """
    Verifies whether the given path is a valid Git worktree using Git rev-parse.
    Returns False if the directory is not a repository or Git is unavailable.
    """
    try:
        path = Path(repo_path).resolve()
        if not path.is_dir():
            return False

        result = _run_git(
            repo_path=str(path),
            args=["rev-parse", "--is-inside-work-tree"],
            check=False
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def add(repo_path: str, file_path: str) -> None:
    """
    Stages a specific file in the repository.
    Does not stage the entire tree (no git add .).
    """
    _run_git(repo_path, ["add", str(file_path)])


def commit(repo_path: str, message: str) -> None:
    """
    Commits the currently staged changes with the provided commit message.
    """
    _run_git(repo_path, ["commit", "-m", message])


def push(repo_path: str) -> None:
    """
    Pushes committed changes to the configured upstream remote repository.
    Relies on standard Git authentication / credential helper.
    """
    _run_git(repo_path, ["push"])
