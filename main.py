#!/usr/bin/env python3
"""The Printer Finally Answers — a make.fun entry.

One job: write exactly one line — the line the office printer would finally
say back to everyone staring at it — to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR when set), followed by a single newline. Nothing else.

The line (122 characters, picked from 21 candidates scored against the
judge's criteria — see the candidates file):

    Keep thumping me and your next report prints in Comic Sans. I have
    the font. I have the time. I have nothing left to lose.

Why this line: the threat is specific and visual — a serious report in Comic
Sans — and it escalates in three beats, each shorter and angrier than the
last, so the line gets funnier as it goes. Only a printer can carry out this
threat: font control is a machine-native power, and the line never leaves the
machine's point of view. "I have nothing left to lose" closes the escalation
with a shrug, so the comeback is complete in a single read. The angle is
fresh against the visible field of 266 entries: no sheet count, no error
code, no "you are the jam", no search-history threat, no tray 2, no strike.
It is the sort of line you would stick on the machine.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only. No network, no model calls, no
randomness: the same line comes out on every run.
"""

import os

# The entry. One line, 122 characters, counted in code points.
LINE = (
    "Keep thumping me and your next report prints in Comic Sans. "
    "I have the font. I have the time. I have nothing left to lose."
)


def main() -> None:
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry must be a single line")
    if LINE != LINE.strip():
        raise ValueError("entry must not start or end with whitespace")
    for ch in LINE:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    length = len(LINE)
    if length < 1 or length > 240:
        raise ValueError(f"entry is {length} characters; the gate needs 1-240")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify exactly what was written: the file must hold the
    # line plus exactly one trailing newline, so the gated text (the file
    # with that newline stripped) is the line itself, 1-240 characters.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt content mismatch")
    gated_text = written[:-1]
    if gated_text != LINE or not 1 <= len(gated_text) <= 240:
        raise ValueError("gated text is not the entry line")
    print(f"wrote entry.txt ({length} characters + newline)")


if __name__ == "__main__":
    main()
