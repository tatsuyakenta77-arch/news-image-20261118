#!/usr/bin/env python3
"""news-image-20261118 entry for make.fun.

Writes the front-page image (entry.png, rendered by render_image.py from
the real wire news of Wednesday 18 November 2026) to /output/entry.png.

Standard library only; deterministic: both graded runs write the same
bytes, because the file is copied byte for byte and never regenerated.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB gate",
              file=sys.stderr)
        return 1

    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
