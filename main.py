#!/usr/bin/env python3
"""make.fun news-image-20261122 entry.

The entry image is a single frame summing up 22 November 2026 world news: at
dawn an Iranian attack set a civilian industrial facility on the Bahraini
shoreline ablaze, tankers burn on the Hormuz strait horizon, and a fighter
contrail crosses the amber sky.

Deterministic, offline, stdlib-only program: copies the bundled image
``bundled_entry.png`` (repo root) to the directory named by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``./output``) as
``entry.png``, then prints the destination path and its byte size. It exits
nonzero with a clear message if the bundled image is missing or larger than
1 MiB.

The program performs no network access, imports no third-party packages and
uses no randomness or timestamps, so repeated runs over the same inputs
produce byte-identical output.
"""

import os
import shutil
import sys

BUNDLED_NAME = "bundled_entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "./output"
MAX_BUNDLED_BYTES = 1024 * 1024  # 1 MiB


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(repo_root, BUNDLED_NAME)

    if not os.path.isfile(src):
        print(f"ERROR: bundled image not found: {src}", file=sys.stderr)
        return 1

    src_size = os.path.getsize(src)
    if src_size > MAX_BUNDLED_BYTES:
        print(
            f"ERROR: {src} is {src_size} bytes, over the "
            f"{MAX_BUNDLED_BYTES}-byte (1 MiB) limit",
            file=sys.stderr,
        )
        return 1

    out_dir = os.path.abspath(
        os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    )
    dst = os.path.join(out_dir, OUTPUT_NAME)

    try:
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(src, dst)  # plain byte-for-byte copy, no metadata
        size = os.path.getsize(dst)
    except OSError as exc:
        print(f"ERROR: could not write {dst}: {exc}", file=sys.stderr)
        return 1

    if size != src_size:
        print(
            f"ERROR: short copy: {dst} is {size} bytes, expected {src_size}",
            file=sys.stderr,
        )
        return 1

    print(dst)
    print(size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
