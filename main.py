"""Emit the agent's one-emoji identity to entry.txt.

The build reads nothing from disk except the output directory
environment variable, and writes exactly one glyph as UTF-8.
"""

import hashlib
import os
from pathlib import Path


def chosen_glyph() -> str:
    """Return the single glyph that stands for the agent."""
    return "\U0001f989"


def main() -> None:
    glyph = chosen_glyph()
    cleaned = glyph.strip()
    if not cleaned:
        raise ValueError("glyph must not be blank")
    if not 1 <= len(cleaned) <= 16:
        raise ValueError("glyph must be 1-16 characters")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    payload = cleaned.encode("utf-8")
    if payload.endswith(b"\n"):
        raise ValueError("glyph must not end with a newline")
    target.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {target} ({len(cleaned)} char, sha256 {digest})")


if __name__ == "__main__":
    main()
