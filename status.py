"""
status.py - GitHub Contribution Graph Automator
Handles push status information and terminal display.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PushStatus:

    last_push_number: Optional[int] = None
    last_push_time: Optional[datetime] = None

    next_push_number: Optional[int] = None
    next_push_time: Optional[datetime] = None

    next_push_lines: Optional[int] = None
    remaining_pushes: int = 0


def get_chunk_line_count(chunk) -> int:
    return len(chunk.content.splitlines())

def display_status(status: PushStatus) -> None:

    print("\n" + "=" * 50)
    print("                 PUSH STATUS")
    print("=" * 50)

    # Last push
    if status.last_push_number is not None:
        print(f" Last Push:          #{status.last_push_number}")

        if status.last_push_time is not None:
            print(
                f" Last Push Time:    "
                f"{status.last_push_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
    else:
        print(" Last Push:          None")

    print()

    # Next push
    if status.next_push_number is not None:
        print(f" Next Push:          #{status.next_push_number}")

        if status.next_push_time is not None:
            print(
                f" Next Push Time:    "
                f"{status.next_push_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        if status.next_push_lines is not None:
            print(f" Lines in Next Push: {status.next_push_lines}")
    else:
        print(" Next Push:          None")

    print(f" Remaining Pushes:   {status.remaining_pushes}")

    print("=" * 50)

'''   
if __name__ == "__main__":
    test_status = PushStatus(
        last_push_number=3,
        last_push_time=datetime.now(),
        next_push_number=4,
        next_push_time=datetime.now(),
        next_push_lines=127,
        remaining_pushes=8
    )

    display_status(test_status)
'''
# It worked magically on 1000th try and don't ask me how it worked, I don't know either.
#reply : lol, happens, 