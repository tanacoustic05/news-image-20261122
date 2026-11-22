#!/usr/bin/env python3
"""make.fun news-image-20261122 entry.

Deterministic, offline, stdlib-only program: copies the bundled image
bundled_entry.png (repo root) to the output directory named by
MAKEFUN_OUTPUT_DIR (default ./output) as entry.png.

The image sums up 22 November 2026 world news: an Iranian attack sets a
civilian industrial facility on the Bahraini shore ablaze at dawn, tankers
burn on the Hormuz strait horizon, and a fighter contrail crosses the amber
sky — the Gulf escalation day.
"""

import os
import shutil
import sys

MAX_BUNDLED_BYTES = 1024 * 1024  # fail cleanly if the bundled image is > 1 MiB


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "bundled_entry.png")
    if not os.path.exists(src):
        print("ERROR: bundled_entry.png missing from repo root", file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BUNDLED_BYTES:
        print(
            f"ERROR: bundled_entry.png is {os.path.getsize(src)} bytes, "
            f"larger than the {MAX_BUNDLED_BYTES}-byte guard",
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print(dst)
    print(size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
