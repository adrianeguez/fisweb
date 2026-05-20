import json
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "paginas_web"
OUT_ROOT.mkdir(parents=True, exist_ok=True)


def read_seed_urls() -> list[str]:
    urls: list[str] = []
    for rel in ["fis_scraper/input/urls_master.txt", "fis_scraper/input/urls_excluded.txt"]:
        path = ROOT / rel
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                urls.append(s)
    return urls


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text).strip("_")
    ascii_text = re.sub(r"_+", "_", ascii_text)
    return ascii_text or "pagina"


def collect_state_sources() -> tuple[dict[str, Path], dict[str, str]]:
    url_to_source: dict[str, Path] = {}
    url_to_title: dict[str, str] = {}

    state_files = sorted(
        (ROOT / "fis_scraper" / "output").glob("run_*/urls/*/state_000_base.json"),
        reverse=True,
    )

    for sf in state_files:
        try:
            data = json.loads(sf.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue

        url = (data.get("url") or "").strip()
        if not url:
            continue

        src_dir = sf.parent
        shots = sorted(src_dir.glob("screenshot_*.png"))
        if not shots:
            continue

        title = ((data.get("content") or {}).get("title") or "").strip()
        if url not in url_to_source:
            url_to_source[url] = src_dir
            url_to_title[url] = title

    return url_to_source, url_to_title


def main() -> None:
    seed_urls = read_seed_urls()
    url_to_source, url_to_title = collect_state_sources()

    all_urls = sorted(set(seed_urls) | set(url_to_source.keys()))

    used_names: set[str] = set()
    index_lines: list[str] = []

    total = 0
    with_screenshots = 0
    without_screenshots = 0

    for i, url in enumerate(all_urls, start=1):
        parsed = urlparse(url)
        leaf = Path(parsed.path).name or "inicio"
        title = url_to_title.get(url, "")

        base = slugify(title) if title else slugify(leaf)
        folder_name = f"{i:03d}_{base}"[:72].rstrip("_")

        candidate = folder_name
        n = 2
        while candidate in used_names:
            candidate = f"{folder_name}_{n}"
            n += 1
        used_names.add(candidate)

        dst = OUT_ROOT / candidate
        dst.mkdir(parents=True, exist_ok=True)

        (dst / "enlace.txt").write_text(url + "\n", encoding="utf-8")

        copied = 0
        src_dir = url_to_source.get(url)
        if src_dir:
            for shot in sorted(src_dir.glob("screenshot_*.png")):
                target = dst / shot.name
                suffix_n = 2
                while target.exists():
                    target = dst / f"{shot.stem}_{suffix_n}{shot.suffix}"
                    suffix_n += 1
                shutil.copy2(shot, target)
                copied += 1

        if copied:
            with_screenshots += 1
        else:
            without_screenshots += 1

        total += 1
        index_lines.append(f"{candidate}\t{url}\t{copied}")

    (OUT_ROOT / "_indice_paginas.tsv").write_text(
        "carpeta\turl\tscreenshots\n" + "\n".join(index_lines) + "\n",
        encoding="utf-8",
    )

    (OUT_ROOT / "_resumen.txt").write_text(
        "Estructura generada automaticamente.\n"
        f"Total URLs: {total}\n"
        f"Con screenshots: {with_screenshots}\n"
        f"Sin screenshots: {without_screenshots}\n",
        encoding="utf-8",
    )

    print(
        f"DONE total_urls={total} con_screenshots={with_screenshots} sin_screenshots={without_screenshots}"
    )


if __name__ == "__main__":
    main()
