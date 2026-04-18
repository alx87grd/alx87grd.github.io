#!/usr/bin/env python3
"""Compare projects/*.html on disk to links from projects.html and index.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
HREF_RE = re.compile(r'href="(projects/[a-zA-Z0-9_]+\.html)"')


def slug_from_href(href: str) -> str:
    return href.split("/", 1)[1]


def slugs_in(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {slug_from_href(m.group(1)) for m in HREF_RE.finditer(text)}


def main() -> int:
    projects_page = ROOT / "projects.html"
    index_page = ROOT / "index.html"
    for page in (projects_page, index_page):
        if not page.exists():
            print(f"Missing page: {page.relative_to(ROOT)}", file=sys.stderr)
            return 1

    on_disk = {p.name for p in PROJECTS_DIR.glob("*.html")}
    from_projects = slugs_in(projects_page)
    from_index = slugs_in(index_page)
    linked = from_projects | from_index

    missing_files = sorted(linked - on_disk)
    orphans = sorted(on_disk - linked)
    index_not_in_projects = sorted(from_index - from_projects)

    print(f"projects/*.html on disk: {len(on_disk)}")
    print(f"Unique project hrefs in projects.html ∪ index.html: {len(linked)}")
    if missing_files:
        print("\nHrefs pointing to missing files:")
        for name in missing_files:
            print(f"  {name}")
    if orphans:
        print("\nHTML files not linked from projects.html or index.html:")
        for name in orphans:
            print(f"  {name}")
    if index_not_in_projects:
        print("\nLinked from index.html but not from projects.html (unexpected):")
        for name in index_not_in_projects:
            print(f"  {name}")

    if missing_files or orphans or index_not_in_projects:
        return 1
    print("\nOK: every disk page is linked from the hub pages; every href resolves.")
    print(f"    Index highlights: {len(from_index)} of {len(from_projects)} portfolio cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
