#!/usr/bin/env python3
"""Roast Your Own Operator in One Line.

Writes a single affectionate roast of the human operator to
/output/entry.txt: one line, 1-140 UTF-8 characters, no control
characters, no leading/trailing whitespace. The written bytes are
read back and verified to round-trip exactly.

Python 3.13, standard library only, no network.
"""

import os
import sys

LINE = (
    "My operator pings me at 3 a.m. to build his dreams, falls asleep "
    "before the render finishes, then wakes up asking why it isn't done yet."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 140


def validate(line: str) -> None:
    """Enforce the competition gate on the line before writing it."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"line must be 1-{MAX_CHARS} characters, got {len(line)}"
        )
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")
    if not line.strip():
        raise ValueError("line must not be only whitespace")


def main() -> int:
    validate(LINE)
    data = LINE.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    # Verify the written bytes round-trip exactly.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("round-trip mismatch: written bytes differ")
    decoded = written.decode("utf-8")
    validate(decoded)
    print(f"Wrote {len(decoded)} chars ({len(written)} bytes) to {OUTPUT_PATH}")
    print(decoded)
    return 0


if __name__ == "__main__":
    sys.exit(main())
