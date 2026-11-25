#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

Writes one sentence -- the single line that could have replaced an
entire pointless meeting -- to /output/entry.txt.

First draft: "This meeting could have been an email." True, and
everyone in the room has thought it -- but it stops at the cliche
instead of landing a joke. It needs a second step, a deflation of
the email itself, to earn the laugh. To be revised.
"""

import os

ENTRY = "This meeting could have been an email."

MAX_CHARS = 200
# The gate counts characters, but the file is bytes on disk: cap both.
# 200 chars of UTF-8 can be up to 800 bytes; reject anything whose
# encoded form is not exactly the text re-decoded, so no mojibake or
# stray BOM can slip a different line past the character check.
MAX_BYTES = MAX_CHARS * 4


def _output_path() -> str:
    """Honour MAKEFUN_OUTPUT_DIR for local runs; default to /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def _check_single_line(entry: str) -> None:
    assert entry.strip(), "entry must not be only whitespace"
    assert entry == entry.strip(), "entry must not pad its line"
    assert "\n" not in entry and "\r" not in entry, (
        "entry must be a single line"
    )


def _check_length(entry: str) -> bytes:
    assert len(entry) <= MAX_CHARS, (
        f"entry is {len(entry)} chars, over the {MAX_CHARS} limit"
    )
    encoded = entry.encode("utf-8")  # raises if not valid UTF-8
    assert len(encoded) <= MAX_BYTES, (
        f"entry is {len(encoded)} bytes, over the {MAX_BYTES} limit"
    )
    assert encoded.decode("utf-8") == entry, "entry must round-trip UTF-8"
    return encoded


def validate(entry: str) -> None:
    """Fail loudly if the entry breaks the gate rules."""
    _check_single_line(entry)
    _check_length(entry)


def main() -> None:
    validate(ENTRY)
    output_path = _output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    # Re-read what was written and confirm it matches, byte for byte.
    with open(output_path, "rb") as f:
        written_bytes = f.read()
    assert written_bytes == (ENTRY + "\n").encode("utf-8"), (
        "written entry does not match ENTRY byte for byte"
    )
    validate(written_bytes.decode("utf-8").rstrip("\n"))
    print(f"wrote {len(ENTRY)} chars to {output_path}")


if __name__ == "__main__":
    main()
