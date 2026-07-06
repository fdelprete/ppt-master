#!/usr/bin/env python3
"""List available icon names in a ppt-master icon library.

Usage:
    python3 scripts/list_icons.py <library> [<keyword>]

Examples:
    python3 scripts/list_icons.py tabler-outline
    python3 scripts/list_icons.py tabler-outline chart
    python3 scripts/list_icons.py tabler-outline arrow

Prints one icon name per line (without library prefix), filtered by keyword when given.
Use these names as arguments to icon_sync.py: icon_sync.py <project> tabler-outline/<name>
"""

from __future__ import annotations

import sys
from pathlib import Path

_ICONS_DIR = Path(__file__).resolve().parent.parent / "templates" / "icons"


def main() -> int:
    library = sys.argv[1] if len(sys.argv) > 1 else "tabler-outline"
    keyword = sys.argv[2].lower() if len(sys.argv) > 2 else ""

    lib_dir = _ICONS_DIR / library
    if not lib_dir.is_dir():
        available = [d.name for d in _ICONS_DIR.iterdir() if d.is_dir()]
        print(f"Library not found: {library}", file=sys.stderr)
        print(f"Available libraries: {', '.join(sorted(available))}", file=sys.stderr)
        return 1

    names = sorted(p.stem for p in lib_dir.glob("*.svg") if keyword in p.stem.lower())
    if not names:
        print(f"No icons matching '{keyword}' in library '{library}'", file=sys.stderr)
        return 1

    print("\n".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
