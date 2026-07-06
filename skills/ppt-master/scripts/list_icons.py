#!/usr/bin/env python3
"""List available icon names in a ppt-master icon library.

Usage:
    python3 scripts/list_icons.py <library> [<keyword> ...]

Examples:
    python3 scripts/list_icons.py tabler-outline
    python3 scripts/list_icons.py tabler-outline chart
    python3 scripts/list_icons.py tabler-outline robot chart brain network source trending building

Single keyword: prints one icon name per line (no header), exits 1 if no match.
Multiple keywords: prints grouped results with [keyword] headers, exits 0 always.
Use icon names as arguments to icon_sync.py: icon_sync.py <project> tabler-outline/<name>
"""

from __future__ import annotations

import sys
from pathlib import Path

_ICONS_DIR = Path(__file__).resolve().parent.parent / "templates" / "icons"


def main() -> int:
    library = sys.argv[1] if len(sys.argv) > 1 else "tabler-outline"
    keywords = [a.lower() for a in sys.argv[2:]]

    lib_dir = _ICONS_DIR / library
    if not lib_dir.is_dir():
        available = [d.name for d in _ICONS_DIR.iterdir() if d.is_dir()]
        print(f"Library not found: {library}", file=sys.stderr)
        print(f"Available libraries: {', '.join(sorted(available))}", file=sys.stderr)
        return 1

    all_stems = sorted(p.stem for p in lib_dir.glob("*.svg"))

    # No keyword — list everything
    if not keywords:
        print("\n".join(all_stems))
        return 0

    # Single keyword — backward-compatible output (no header, exit 1 on no match)
    if len(keywords) == 1:
        kw = keywords[0]
        names = [s for s in all_stems if kw in s.lower()]
        if not names:
            print(f"No icons matching '{kw}' in library '{library}'", file=sys.stderr)
            return 1
        print("\n".join(names))
        return 0

    # Multiple keywords — grouped output, always exit 0
    parts: list[str] = []
    for kw in keywords:
        names = [s for s in all_stems if kw in s.lower()]
        parts.append(f"[{kw}]")
        if names:
            parts.extend(names)
        else:
            parts.append("(no match — pick closest from other results)")
        parts.append("")
    print("\n".join(parts).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
