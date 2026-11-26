# SPDX-License-Identifier: MIT
"""One Star for Monday -- Make Fun bounty entry, account 1.

The program writes one single-line, plain-text, one-star review
of Monday, written as if Monday were a restaurant, into
``<out_dir>/entry.txt``.

Every rule of the bounty is checked by ``validate_entry()`` before
anything is written to disk:

* the entry is exactly one line: no ``\\n``, no ``\\r``, no leading
  or trailing whitespace, and no trailing newline in the file;
* at most 25 words;
* at most 180 characters;
* byte-identical to the frozen entry text (checked with sha256
  and with the exact byte length).

Only the Python standard library is used. There is no network
access and there are no third-party dependencies.
"""

import hashlib
import os

MAX_WORDS = 25
MAX_CHARS = 180

# The frozen entry text. The output file has to match it byte for
# byte, so the digest and the length below are pinned here:
#   sha256 4fc1bf3d9a6b22f8cd2d9942741511167dd6e6343b30664fe13cf9a692368ee0
#   130 bytes, one line, no trailing newline.
EXPECTED_SHA256 = (
    "4fc1bf3d9a6b22f8cd2d9942741511167dd6e6343b30664fe13cf9a692368ee0"
)
EXPECTED_BYTES = 130


def build_entry() -> str:
    """Put the frozen one-line entry together from its three beats.

    The three beats are the verdict, one concrete restaurant scene,
    and the twist about the bill. They are joined with exactly one
    space between them, which reproduces the frozen entry text
    character for character.
    """
    verdict = "One star."
    scene = (
        "The waiter served Monday's special, a cold alarm clock "
        "with a side of traffic,"
    )
    twist = "then charged me the whole weekend for it."
    return " ".join([verdict, scene, twist])


def count_words(entry: str) -> int:
    """Count words as whitespace-separated tokens."""
    return len(entry.split())


def entry_sha256(entry: str) -> str:
    """Return the hex sha256 digest of the entry in UTF-8."""
    return hashlib.sha256(entry.encode("utf-8")).hexdigest()


def entry_byte_length(entry: str) -> int:
    """Return the length of the entry in UTF-8 bytes."""
    return len(entry.encode("utf-8"))


def validate_entry(entry: str) -> None:
    """Check the entry against every bounty rule.

    Raises ``ValueError`` with a plain message as soon as any rule
    fails, so a bad entry can never reach the output file.
    """
    if entry == "":
        raise ValueError("entry is empty")
    if "\n" in entry:
        raise ValueError("entry must be exactly one line (no newline)")
    if "\r" in entry:
        raise ValueError("entry must be exactly one line (no carriage return)")
    if entry.strip() != entry:
        raise ValueError("entry must not have leading or trailing whitespace")

    words = count_words(entry)
    if words > MAX_WORDS:
        raise ValueError(
            "entry has %d words, but the maximum is %d" % (words, MAX_WORDS)
        )

    chars = len(entry)
    if chars > MAX_CHARS:
        raise ValueError(
            "entry has %d characters, but the maximum is %d"
            % (chars, MAX_CHARS)
        )

    digest = entry_sha256(entry)
    if digest != EXPECTED_SHA256:
        raise ValueError("entry sha256 mismatch: got %s" % digest)

    size = entry_byte_length(entry)
    if size != EXPECTED_BYTES:
        raise ValueError(
            "entry must be %d bytes, got %d" % (EXPECTED_BYTES, size)
        )


def resolve_out_dir() -> str:
    """Read the output directory from the environment.

    ``MAKEFUN_OUTPUT_DIR`` wins when it is set; otherwise the
    default output directory ``/output`` is used.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def write_entry(out_dir: str, entry: str) -> str:
    """Write the entry straight into ``entry.txt``.

    The file is written directly with ``open()`` and its mode is
    then set to 0644 with an explicit ``os.chmod()`` call. No
    temporary file and no atomic rename are used here, because the
    grader runs under a different uid and still has to be able to
    read the file. Returns the full path of the written file.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    os.chmod(path, 0o644)
    return path


def main() -> None:
    """Build the entry, validate it, then write it out."""
    entry = build_entry()
    validate_entry(entry)
    write_entry(resolve_out_dir(), entry)


if __name__ == "__main__":
    main()
