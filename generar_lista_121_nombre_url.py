from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import re

root = Path(__file__).resolve().parent
src = root / "fis_scraper" / "input" / "urls_master.txt"
out = root / "doc_lista_121_paginas_nombre_url.md"

urls = []
for line in src.read_text(encoding="utf-8", errors="ignore").splitlines():
    s = line.strip()
    if s and not s.startswith("#"):
        urls.append(s)


def pretty_name(url: str) -> str:
    p = urlparse(url)
    path = unquote(p.path)
    seg = [x for x in path.split("/") if x]

    if seg[-2:] == ["index.php", "es"] or (seg and seg[-1] == "es"):
        return "Inicio"

    if not seg:
        return "Pagina"

    last = seg[-1]
    if last == "category-list":
        q = parse_qs(p.query)
        if "start" in q:
            return f"Category List Start {q['start'][0]}"
        if "limitstart" in q:
            return f"Category List Limitstart {q['limitstart'][0]}"
        return "Category List"

    last = last.replace("_", "-")
    last = re.sub(r"^\d+-", "", last)
    name = last.replace("-", " ").strip()
    name = re.sub(r"\s+", " ", name)
    return name.title() if name else "Pagina"


lines = ["# Lista de 121 paginas (Nombre pagina - URL)", ""]
for i, url in enumerate(urls, start=1):
    lines.append(f"{i}. {pretty_name(url)} - {url}")

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"OK: {out} total={len(urls)}")
