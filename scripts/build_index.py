#!/usr/bin/env python3
"""
Regenerates papers.csv from evidence/*.md.

Each evidence card carries its own fields (Slug, Priority, Status, Decision,
and — for a paper not yet in papers.csv — Paper/Authors/Year/Link too). This
script reads every card, updates the matching row in papers.csv, and adds a
new row for any paper that has a card but wasn't already listed.

It does NOT touch title/authors/year/link for a paper that's already in
papers.csv — those are set once, at intake, and treated as fixed. Only
priority/status/decision are considered live and get overwritten from the
card, since those are the fields the system expects to change.

Usage:
    python3 scripts/build_index.py
Run from the repo root, or point it elsewhere:
    python3 scripts/build_index.py --root /path/to/repo
"""

import argparse
import csv
import re
import sys
from pathlib import Path

FIELDS = ["slug", "title", "authors", "year", "link", "priority", "status", "decision"]

# Matches a line like "Priority: P0" or "Decision: KEEP / ADAPT / REJECT / DEFER"
# — for Decision specifically we only keep it if it's a single real value,
# not the template's own placeholder list of options.
LINE_RE = re.compile(r"^(Paper|Authors|Year|Link|Slug|Priority|Status|Decision):\s*(.+)$")
DECISION_OPTIONS = {"KEEP", "ADAPT", "REJECT", "DEFER"}


def parse_card(path: Path) -> dict:
    """Pull the labeled fields out of one evidence card. Missing fields are omitted."""
    found = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line.strip())
        if not m:
            continue
        key, value = m.group(1).lower(), m.group(2).strip()
        if key == "decision":
            # Ignore an unfilled template line like "KEEP / ADAPT / REJECT / DEFER"
            value = value.strip()
            if value.upper() not in DECISION_OPTIONS:
                continue
            value = value.upper()
        found[key] = value
    return found


def load_papers(csv_path: Path) -> dict:
    """Returns {slug: row_dict}, preserving whatever's already in papers.csv."""
    rows = {}
    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                slug = row.get("slug", "").strip()
                if slug:
                    rows[slug] = {k: (row.get(k) or "").strip() for k in FIELDS}
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root (default: current directory)")
    args = ap.parse_args()

    root = Path(args.root)
    evidence_dir = root / "evidence"
    csv_path = root / "papers.csv"

    if not evidence_dir.is_dir():
        print(f"error: no evidence/ folder at {evidence_dir}", file=sys.stderr)
        return 1

    rows = load_papers(csv_path)
    seen_slugs = set()

    for card_path in sorted(evidence_dir.glob("*.md")):
        card = parse_card(card_path)
        slug = card.get("slug")
        if not slug:
            print(f"warning: {card_path.name} has no Slug: line, skipping", file=sys.stderr)
            continue
        if slug in seen_slugs:
            print(f"warning: duplicate slug '{slug}' at {card_path.name}, skipping", file=sys.stderr)
            continue
        seen_slugs.add(slug)

        row = rows.get(slug, {k: "" for k in FIELDS})
        row["slug"] = slug
        # title/authors/year/link: fill only if genuinely missing, never overwrite.
        for src_key, dst_key in (("paper", "title"), ("authors", "authors"),
                                  ("year", "year"), ("link", "link")):
            if not row.get(dst_key) and card.get(src_key):
                row[dst_key] = card[src_key]
        # priority/status/decision: the card is the live source of truth.
        for key in ("priority", "status", "decision"):
            if card.get(key):
                row[key] = card[key]

        rows[slug] = row

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for slug in sorted(rows):
            writer.writerow(rows[slug])

    print(f"wrote {len(rows)} rows to {csv_path} ({len(seen_slugs)} from evidence cards)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
