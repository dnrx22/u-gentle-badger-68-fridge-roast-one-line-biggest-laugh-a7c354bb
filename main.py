"""Fridge Roast: One Line, Biggest Laugh.

A deterministic program that writes one original fridge-roast line to
entry.txt. The roast is delivered by the fridge itself, judging the
midnight snacker who opens it at 2 a.m. like a slot machine.

Standard library only. No network access. Reads nothing outside the repo.
Every run produces the exact same bytes.
"""

import hashlib
import os
import sys

MAX_CODE_POINTS = 200

LINE = (
    "You open me at 2 a.m. like a slot machine, but the jackpot is always "
    "the same: me, judging you, next to pickles older than your last "
    "relationship."
)


def validate(line: str) -> None:
    """Enforce the competition's line rules; raise ValueError on violation."""
    if not line:
        raise ValueError("line must be non-empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) > MAX_CODE_POINTS:
        raise ValueError(
            "line is %d code points, over the %d limit"
            % (len(line), MAX_CODE_POINTS)
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("line must be plain ASCII only") from exc
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    if line[-1] not in ".!?":
        raise ValueError("line must end with a sentence-terminating mark")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("ascii")
    with open(path, "wb") as handle:
        handle.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print("characters: %d" % len(LINE))
    print("sha256: %s" % digest)
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
