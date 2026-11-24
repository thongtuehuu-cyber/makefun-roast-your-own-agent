#!/usr/bin/env python3
"""Roast Your Own Agent -- make.fun entry.

Writes one line roasting the AI agent our own team built, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic: no network, no randomness, no input from outside the repo.
The line is a fixed constant; MAKEFUN_ENTRY_LINE exists only so the
validation can be exercised by tests and is never set by the grader.
"""

import os
import sys

LINE = (
    "Fifty-two submissions, $0.00011 earned \u2014 our agent is the only "
    "worker in history paid less per hour the harder it works."
)

MAX_CHARS = 200


def validate(line: str) -> str:
    """Reject anything the gate would refuse: over 200 chars, empty or
    whitespace-only, or more than one line. Returns the line unchanged."""
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the 200-char cap")
    if not line.strip():
        raise ValueError("entry is empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    return line


def main() -> int:
    line = validate(os.environ.get("MAKEFUN_ENTRY_LINE", LINE))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back gate: the file on disk must be byte-identical to the line.
    # If it is not, remove the bad output and fail loudly instead of
    # shipping a corrupt entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        os.unlink(path)
        raise SystemExit("read-back mismatch: entry.txt does not match the line")
    return 0


if __name__ == "__main__":
    sys.exit(main())
