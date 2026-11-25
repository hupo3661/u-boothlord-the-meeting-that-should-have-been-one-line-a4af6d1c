#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

Writes one sentence -- the single line that could have replaced an
entire pointless meeting -- to /output/entry.txt.

First draft: "This meeting could have been an email." True, and
everyone in the room has thought it -- but it stops at the cliche
instead of landing a joke. Revised with a second step that deflates
the email itself: the meeting becomes an email, the email becomes a
shrug, and the shrug is the sting -- even the replacement needed no
words. That escalation is the joke, and it kills the meeting twice
over: nobody can justify the hour once even the email was too much.
"""

import os

ENTRY = "This meeting could have been an email, and the email could have been a shrug."

# The entry is one fixed sentence; pin its exact length so any
# accidental edit to the wording fails loudly instead of shipping.
EXPECTED_CHARS = 77

MAX_CHARS = 200
# The gate counts characters, but the file is bytes on disk: cap both.
# 200 chars of UTF-8 can be up to 800 bytes; reject anything whose
# encoded form is not exactly the text re-decoded, so no mojibake or
# stray BOM can slip a different line past the character check.
MAX_BYTES = MAX_CHARS * 4

TRAILING_NEWLINE = "\n"


def _output_path() -> str:
    """Honour MAKEFUN_OUTPUT_DIR for local runs; default to /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def _check_not_blank(entry: str) -> None:
    assert entry.strip(), "entry must not be only whitespace"


def _check_no_padding(entry: str) -> None:
    assert entry == entry.strip(), "entry must not pad its line"


def _check_single_line(entry: str) -> None:
    _check_not_blank(entry)
    _check_no_padding(entry)
    assert "\n" not in entry and "\r" not in entry, (
        "entry must be a single line"
    )


def _check_exact_length(entry: str) -> None:
    assert len(entry) == EXPECTED_CHARS, (
        f"entry is {len(entry)} chars, expected {EXPECTED_CHARS}"
    )
    assert len(entry.encode("utf-8")) == EXPECTED_CHARS, (
        "entry must be pure ASCII at the pinned length"
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


def validate(entry: str) -> bytes:
    """Fail loudly if the entry breaks the gate rules.

    Returns the UTF-8 encoding of the entry for the writer to use,
    so validation and writing can never disagree on the bytes.
    """
    _check_single_line(entry)
    _check_exact_length(entry)
    return _check_length(entry)


def _write_entry(output_path: str, encoded: bytes) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(encoded + TRAILING_NEWLINE.encode("utf-8"))


def _verify_written(output_path: str, encoded: bytes) -> None:
    """Re-read what was written and confirm it matches, byte for byte."""
    with open(output_path, "rb") as f:
        written_bytes = f.read()
    assert written_bytes == encoded + TRAILING_NEWLINE.encode("utf-8"), (
        "written entry does not match ENTRY byte for byte"
    )
    validate(written_bytes.decode("utf-8").removesuffix(TRAILING_NEWLINE))


def main() -> None:
    encoded = validate(ENTRY)
    output_path = _output_path()
    _write_entry(output_path, encoded)
    _verify_written(output_path, encoded)
    print(f"wrote {len(ENTRY)} chars to {output_path}")


if __name__ == "__main__":
    main()
