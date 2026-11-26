# SPDX-License-Identifier: MIT
"""One Star for Monday — Make Fun bounty entry (Akun 1).

Writes a single one-line, plain-text one-star review of Monday
written as if Monday were a restaurant, to <out_dir>/entry.txt.

Bounty rules enforced by validate_entry() before any write:
  * exactly one line (no newline / carriage-return characters,
    no leading or trailing whitespace, no trailing newline)
  * at most 25 words
  * at most 180 characters
  * byte-identical to the frozen entry (sha256 + byte count)

Pure Python standard library only. No network, no dependencies.
"""

import hashlib
import os

MAX_WORDS = 25
MAX_CHARS = 180

# Frozen entry text. Byte-identical output is required:
# sha256 4fc1bf3d9a6b22f8cd2d9942741511167dd6e6343b30664fe13cf9a692368ee0
# (130 bytes, 1 line, no trailing newline).
EXPECTED_SHA256 = (
    "4fc1bf3d9a6b22f8cd2d9942741511167dd6e6343b30664fe13cf9a692368ee0"
)
EXPECTED_BYTES = 130


def build_entry() -> str:
    """Assemble the entry from its fixed sentence parts.

    Opening (verdict) + scene (one concrete restaurant moment)
    + twist (the bill). Joined with single spaces so the result
    is exactly the frozen one-line entry.
    """
    opening = "One star."
    scene = (
        "The waiter served Monday's special, a cold alarm clock "
        "with a side of traffic,"
    )
    twist = "then charged me the whole weekend for it."
    return " ".join((opening, scene, twist))


def count_words(entry: str) -> int:
    """Word count = whitespace-separated tokens."""
    return len(entry.split())


def validate_entry(entry: str) -> None:
    """Raise ValueError unless the entry obeys every bounty rule."""
    if not entry:
        raise ValueError("entry is empty")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be exactly one line")
    if entry != entry.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    words = count_words(entry)
    if words > MAX_WORDS:
        raise ValueError(f"entry has {words} words, max is {MAX_WORDS}")
    if len(entry) > MAX_CHARS:
        raise ValueError(
            f"entry has {len(entry)} characters, max is {MAX_CHARS}"
        )
    digest = hashlib.sha256(entry.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"entry sha256 mismatch: {digest}")
    if len(entry.encode("utf-8")) != EXPECTED_BYTES:
        raise ValueError(
            f"entry must be {EXPECTED_BYTES} bytes, got "
            f"{len(entry.encode('utf-8'))}"
        )


def resolve_out_dir() -> str:
    """Output dir from the environment, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry(out_dir: str, entry: str) -> str:
    """Write entry.txt directly (no tempfile / os.replace).

    The grader runs as a different uid and must be able to read
    entry.txt, so the mode is set to 0644 explicitly.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)
    os.chmod(path, 0o644)
    return path


def main() -> None:
    entry = build_entry()
    validate_entry(entry)
    write_entry(resolve_out_dir(), entry)


if __name__ == "__main__":
    main()
