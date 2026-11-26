# SPDX-License-Identifier: MIT
"""One Star for Monday — Make Fun bounty entry (Akun 1).

Writes a single one-line, plain-text one-star review of Monday
written as if Monday were a restaurant, to <out_dir>/entry.txt.

Pure Python standard library only. No network, no dependencies.
"""

import os

ENTRY = (
    "One star. The waiter served Monday's special, a cold alarm clock "
    "with a side of traffic, then charged me the whole weekend for it."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Direct write (no tempfile / os.replace): the grader runs as a
    # different uid and must be able to read entry.txt (mode 0644).
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
