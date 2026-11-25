#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — entry writer.

Writes a two-part micro-confession (a To: line and the unsent message
itself) to /output/entry.txt and checks it against the bounty gate:
the whole file must be 1-260 characters of UTF-8 text, and the unsent
message itself is one line of at most 200 characters.
"""

import os
import sys
from pathlib import Path

TO_LINE = "To: my younger brother"

MESSAGE = (
    "it was me who broke the garage window, not you. i let you take the "
    "grounding for it and i have been sorry for eleven years. i just "
    "cannot be the one who tells dad."
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def build_entry() -> str:
    return f"{TO_LINE}\n{MESSAGE}"


def check_entry(text: str) -> list[str]:
    problems = []
    if not text.strip():
        problems.append("entry is only whitespace")
    if not 1 <= len(text) <= MAX_TOTAL_CHARS:
        problems.append(f"total length {len(text)} outside 1-{MAX_TOTAL_CHARS}")
    if "@" in text:
        problems.append("entry must not contain a handle")
    lines = text.split("\n")
    if len(lines) != 2:
        problems.append(f"entry must have exactly 2 lines, has {len(lines)}")
    else:
        if not lines[0].startswith("To:"):
            problems.append("first line must be the To: line")
        addressee = lines[0][len("To:"):].strip()
        # The kit allows a role, a first name or a relationship in the
        # To: line, never a real full name: keep it to three words.
        if not addressee or len(addressee.split()) > 3:
            problems.append("To: line must name a role, first name or "
                            "relationship, not a full name")
        if len(lines[1]) > MAX_MESSAGE_CHARS:
            problems.append(
                f"message is {len(lines[1])} chars, over {MAX_MESSAGE_CHARS}"
            )
    return problems


def main() -> int:
    entry = build_entry()
    problems = check_entry(entry)
    if problems:
        for problem in problems:
            print(f"INVALID: {problem}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(entry, encoding="utf-8")
    print(f"wrote {out_path} ({len(entry)} chars total, "
          f"message {len(MESSAGE)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
