"""
enrich_list_items.py — Fix E backfill
Reads all saved html_rendered_000_base.html files and adds `list_items`
(extracted from [itemprop='articleBody'] li) to the corresponding state_000_base.json.

Run from fis_scraper/ directory:
    ..\.venv\Scripts\python.exe enrich_list_items.py
"""

import json
import re
import sys
from pathlib import Path

from parsel import Selector


def visible_text(node) -> str:
    parts = node.xpath(
        ".//text()[normalize-space() and not(ancestor::script) and not(ancestor::style) and not(ancestor::noscript)]"
    ).getall()
    text = re.sub(r"\s+", " ", " ".join(p.strip() for p in parts)).strip()
    text = re.sub(r"\s*document\.getElementById\('cloak[^\n\r]*", "", text)
    return text.strip()


def extract_list_items(html: str) -> list[str]:
    sel = Selector(text=html)
    items = []
    seen: set = set()
    for li in sel.css("[itemprop='articleBody'] li"):
        text = visible_text(li)
        if text and text not in seen:
            items.append(text)
            seen.add(text)
    return items


def main():
    output_root = Path("output")
    updated = 0
    skipped_already = 0
    skipped_no_html = 0

    # Collect unique (hash → latest run path) pairs
    run_dirs = sorted(output_root.iterdir(), reverse=True)

    seen_hashes: dict[str, Path] = {}
    for run_dir in run_dirs:
        if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
            continue
        urls_dir = run_dir / "urls"
        if not urls_dir.exists():
            continue
        for hash_dir in urls_dir.iterdir():
            h = hash_dir.name
            if h not in seen_hashes:
                seen_hashes[h] = hash_dir

    for h, hash_dir in seen_hashes.items():
        state_path = hash_dir / "state_000_base.json"
        html_path = hash_dir / "html_rendered_000_base.html"

        if not state_path.exists():
            continue
        if not html_path.exists():
            skipped_no_html += 1
            continue

        state = json.loads(state_path.read_text(encoding="utf-8"))

        if "list_items" in state.get("content", {}):
            skipped_already += 1
            continue

        html = html_path.read_text(encoding="utf-8")
        list_items = extract_list_items(html)

        state["content"]["list_items"] = list_items
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        updated += 1
        print(f"  updated: {h} ({len(list_items)} list items)")

    print(f"\nDone. Updated={updated}, AlreadyHadField={skipped_already}, NoHtml={skipped_no_html}")


if __name__ == "__main__":
    main()
