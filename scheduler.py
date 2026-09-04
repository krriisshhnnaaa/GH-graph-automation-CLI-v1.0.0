"""
scheduler.py - GitHub Contribution Graph Automator
Handles scheduling, commit plan generation, and timed delays.
Pure scheduling logic: completely decoupled from Git, file I/O, and CLI arguments.
"""

from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
import time as time_module
from typing import Any, List, Optional, Union


@dataclass
class CommitPlanItem:
    """Represents a single scheduled commit task."""
    chunk: Any
    scheduled_time: datetime
    commit_message: Optional[str] = None


def parse_start_time(start_time_input: Union[str, time]) -> time:
    """
    Parses a 'HH:MM' string into a datetime.time object.
    If already a datetime.time instance, returns it directly.
    """
    if isinstance(start_time_input, time):
        return start_time_input

    if not isinstance(start_time_input, str):
        raise ValueError(
            f"Expected start_time as str or datetime.time, got {type(start_time_input).__name__}"
        )

    cleaned = start_time_input.strip()
    try:
        parts = cleaned.split(":")
        if len(parts) != 2:
            raise ValueError()
        hour = int(parts[0])
        minute = int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError()
        return time(hour=hour, minute=minute)
    except Exception:
        raise ValueError(
            f"Invalid start time format: '{cleaned}'. Expected 'HH:MM' (24-hour format, e.g. '09:30')."
        )


def create_commit_plan(
    chunks: List[Any],
    commits_per_day: int,
    start_time_str: Union[str, time] = "09:00",
    interval_minutes: int = 60,
    start_date: Optional[date] = None
) -> List[CommitPlanItem]:
    """
    Assigns each chunk to a scheduled datetime slot.

    Parameters:
    - chunks: List of chunk objects or arbitrary data to commit
    - commits_per_day: Number of commits to perform each day
    - start_time_str: Daily start time (e.g. "09:00" or datetime.time object)
    - interval_minutes: Minutes between consecutive commits on the same day
    - start_date: Starting calendar date (defaults to today)

    Returns:
    - List of CommitPlanItem instances
    """
    if commits_per_day <= 0:
        raise ValueError(f"commits_per_day must be positive, got {commits_per_day}")

    if interval_minutes < 0:
        raise ValueError(f"interval_minutes cannot be negative, got {interval_minutes}")

    if not chunks:
        return []

    daily_start_time = parse_start_time(start_time_str)

    # Validate that all commits for a day fit within a single 24-hour window
    total_span_minutes = (commits_per_day - 1) * interval_minutes
    start_minute_of_day = daily_start_time.hour * 60 + daily_start_time.minute
    if start_minute_of_day + total_span_minutes >= 24 * 60:
        raise ValueError(
            f"Invalid schedule: start_time ({daily_start_time.strftime('%H:%M')}) with "
            f"{commits_per_day} commits every {interval_minutes} min spans past midnight "
            f"into the next day ({start_minute_of_day + total_span_minutes} minutes from start of day). "
            f"Reduce commits_per_day, reduce interval_minutes, or choose an earlier start_time."
        )

    base_date = start_date or date.today()
    plan: List[CommitPlanItem] = []

    for index, chunk in enumerate(chunks):
        day_offset = index // commits_per_day
        slot = index % commits_per_day

        commit_date = base_date + timedelta(days=day_offset)
        base_datetime = datetime.combine(commit_date, daily_start_time)
        scheduled_dt = base_datetime + timedelta(minutes=slot * interval_minutes)

        plan.append(
            CommitPlanItem(
                chunk=chunk,
                scheduled_time=scheduled_dt,
                commit_message=None
            )
        )

    return plan


def wait_until(scheduled_time: datetime) -> None:
    """
    Sleeps until scheduled_time if it is in the future.
    If scheduled_time is in the past or now, returns immediately.
    """
    now = datetime.now()
    if scheduled_time > now:
        delay_seconds = (scheduled_time - now).total_seconds()
        time_module.sleep(delay_seconds)
