import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List
from urllib.parse import urlparse, urlunparse

import scrapy
from parsel import Selector
from scrapy.http import Response


class FisPilotSpider(scrapy.Spider):
    name = "fis_pilot"
    allowed_domains = ["fis.epn.edu.ec"]

    start_urls = [
        "https://fis.epn.edu.ec/index.php/es/",
        "https://fis.epn.edu.ec/index.php/es/estudiante",
        "https://fis.epn.edu.ec/index.php/es/docente",
        "https://fis.epn.edu.ec/index.php/es/category-list/309-proceso-de-admision",
        "https://fis.epn.edu.ec/index.php/es/category-list/126-informacion/312-vida-estudiantil",
    ]

    max_interactions_per_page = 3

    def __init__(self, *args, **kwargs):
        pilot_limit = int(kwargs.pop("pilot_limit", 5))
        max_interactions = int(kwargs.pop("max_interactions", 3))
        batch_start = int(kwargs.pop("batch_start", 0))
        batch_size = int(kwargs.pop("batch_size", 5))
        scope_limit = int(kwargs.pop("scope_limit", 0))
        review_from = int(kwargs.pop("review_from", 0))
        seed_file = kwargs.pop("seed_file", "")
        super().__init__(*args, **kwargs)
        self.pilot_limit = max(1, pilot_limit)
        self.max_interactions_per_page = max(0, max_interactions)
        self.batch_start = max(0, batch_start)
        self.batch_size = max(1, batch_size)
        self.scope_limit = max(0, scope_limit)
        self.review_from = max(0, review_from)
        self.seed_file = (seed_file or "").strip()

        self.seed_urls = self._load_seed_urls()

        if self.scope_limit > 0:
            # Modo acumulativo: 5 -> 10 -> 15 ...
            self.selection_mode = "cumulative"
            effective_limit = min(self.scope_limit, len(self.seed_urls))
            self.selected_urls = self.seed_urls[:effective_limit]
        else:
            # Modo por bloque fijo de 5
            self.selection_mode = "batch"
            end_index = self.batch_start + self.batch_size
            self.selected_urls = self.seed_urls[self.batch_start:end_index]

        # Ventana de URLs nuevas para revisar en QA (delta del alcance)
        self.review_from = min(self.review_from, len(self.selected_urls))
        self.review_to = len(self.selected_urls)
        self.review_urls = self.selected_urls[self.review_from : self.review_to]

        run_id = datetime.utcnow().strftime("run_%Y%m%d_%H%M%S")
        self.output_root = Path("output") / run_id
        self.urls_root = self.output_root / "urls"
        self.urls_root.mkdir(parents=True, exist_ok=True)
        self.index = {
            "run_id": run_id,
            "schema_version": "1.0",
            "domain": "fis.epn.edu.ec",
            "generated_at_utc": datetime.utcnow().isoformat() + "Z",
            "selection": {
                "mode": self.selection_mode,
                "pilot_limit": self.pilot_limit,
                "batch_start": self.batch_start,
                "batch_size": self.batch_size,
                "scope_limit": self.scope_limit,
                "review_from": self.review_from,
                "review_to_exclusive": self.review_to,
                "new_urls_count": len(self.review_urls),
                "new_urls": self.review_urls,
                "selected_urls": len(self.selected_urls),
                "total_seed_urls": len(self.seed_urls),
                "seed_source": self.seed_file or "default_start_urls",
            },
            "pages": [],
        }

    async def start(self):
        if not self.selected_urls:
            self.logger.warning(
                "No hay URLs seleccionadas para procesar (mode=%s, batch_start=%s, batch_size=%s, scope_limit=%s, total=%s)",
                self.selection_mode,
                self.batch_start,
                self.batch_size,
                self.scope_limit,
                len(self.seed_urls),
            )
            return

        for url in self.selected_urls[: self.pilot_limit]:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_goto_kwargs": {"wait_until": "domcontentloaded", "timeout": 60000},
                },
                dont_filter=True,
            )

    async def parse(self, response: Response):
        page = response.meta["playwright_page"]
        page_dir = self._page_dir(response.url)
        page_dir.mkdir(parents=True, exist_ok=True)

        base_selector = Selector(text=await page.content())
        base_state = self._extract_state_data(
            url=response.url,
            state_id="state_000_base",
            selector=base_selector,
            actions=[],
            screenshot_name="screenshot_000_base.png",
            html_name="html_rendered_000_base.html",
        )

        await page.screenshot(path=str(page_dir / base_state["assets"]["screenshot"]), full_page=True)
        (page_dir / base_state["assets"]["html_rendered"]).write_text(await page.content(), encoding="utf-8")
        (page_dir / "state_000_base.json").write_text(json.dumps(base_state, ensure_ascii=False, indent=2), encoding="utf-8")

        states = [base_state]

        interaction_selectors = [
            '.djtabs-title.djtabs-accordion',  # Joomla DJTabs (template de este sitio)
            '[role="tab"]',
            '.nav-tabs a',
            '.accordion-button',
            '.panel-title a',
            '.collapse-toggle',
        ]

        clicks = 0
        for selector in interaction_selectors:
            if clicks >= self.max_interactions_per_page:
                break

            locators = page.locator(selector)
            count = await locators.count()
            if count == 0:
                continue

            for i in range(min(count, self.max_interactions_per_page - clicks)):
                locator = locators.nth(i)
                try:
                    text = (await locator.inner_text(timeout=2000)).strip()
                    if not text:
                        text = f"item_{i}"
                    safe_text = self._slug(text)

                    await locator.click(timeout=5000)
                    await page.wait_for_timeout(600)

                    state_idx = clicks + 1
                    state_id = f"state_{state_idx:03d}_{safe_text}"
                    screenshot_name = f"screenshot_{state_idx:03d}_{safe_text}.png"
                    html_name = f"html_rendered_{state_idx:03d}_{safe_text}.html"

                    state_selector = Selector(text=await page.content())
                    state_data = self._extract_state_data(
                        url=response.url,
                        state_id=state_id,
                        selector=state_selector,
                        actions=[{"type": "click", "selector": selector, "index": i, "label": text}],
                        screenshot_name=screenshot_name,
                        html_name=html_name,
                    )

                    await page.screenshot(path=str(page_dir / screenshot_name), full_page=True)
                    (page_dir / html_name).write_text(await page.content(), encoding="utf-8")
                    (page_dir / f"{state_id}.json").write_text(
                        json.dumps(state_data, ensure_ascii=False, indent=2), encoding="utf-8"
                    )

                    states.append(state_data)
                    clicks += 1
                    if clicks >= self.max_interactions_per_page:
                        break
                except Exception as exc:
                    self.logger.debug("Interaction skipped for %s [%s]: %s", response.url, selector, exc)

        meta = {
            "url": response.url,
            "url_hash": self._url_hash(response.url),
            "title": states[0]["content"].get("title", ""),
            "states_captured": len(states),
            "external_links": states[0]["content"].get("external_links", []),
            "attachments": states[0]["content"].get("attachments", []),
        }

        (page_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        self.index["pages"].append(meta)
        await page.close()

    def closed(self, reason):
        self.index["closed_reason"] = reason
        self.index["total_pages"] = len(self.index["pages"])
        index_path = self.output_root / "index.json"
        index_path.write_text(json.dumps(self.index, ensure_ascii=False, indent=2), encoding="utf-8")

    def _extract_state_data(self, url, state_id, selector, actions, screenshot_name, html_name):
        links = []
        external_links = []
        attachments = []

        for href in selector.css("a::attr(href)").getall():
            # Fix C: strip whitespace characters (tabs, newlines) that appear in some Joomla hrefs
            href = re.sub(r'[\t\n\r]', '', (href or "")).strip()
            if not href:
                continue
            links.append(href)
            if href.lower().endswith((".pdf", ".doc", ".docx", ".xls", ".xlsx")):
                attachments.append(href)
            elif href.startswith("http") and "fis.epn.edu.ec" not in href:
                external_links.append(href)

        # Fix A: expanded paragraph extraction
        # - Full <p> text (including nested elements like <strong>, <a>)
        # - JoomlaMonster card/contact blocks (.jmm-text)
        # - Camera/carousel slide descriptions (.camera_caption_desc)
        seen_texts: set = set()
        paragraphs = []

        for p in selector.css("p"):
            text = self._visible_text(p)
            if text and text not in seen_texts:
                paragraphs.append(text)
                seen_texts.add(text)

        for el in selector.css(".jmm-text, .camera_caption_desc"):
            text = self._visible_text(el)
            if text and text not in seen_texts:
                paragraphs.append(text)
                seen_texts.add(text)

        # Fix A: h2 — standard HTML headings + DJTabs section labels + carousel titles
        h2_seen: set = set()
        h2 = []
        for text in selector.css("h2::text").getall():
            t = text.strip()
            if t and t not in h2_seen:
                h2.append(t)
                h2_seen.add(t)
        for el in selector.css(".djtab-text, .camera_caption_title"):
            t = self._visible_text(el)
            if t and t not in h2_seen:
                h2.append(t)
                h2_seen.add(t)

        # Fix A: h3 — DJTabs sub-panel titles (sub-sections within each accordion block)
        h3_seen: set = set()
        h3 = []
        for el in selector.css(".djtabs-panel-title"):
            t = self._visible_text(el)
            if t and t not in h3_seen:
                h3.append(t)
                h3_seen.add(t)

        tables = []
        for table in selector.css("table"):
            headers = [h.strip() for h in table.css("thead th::text, tr th::text").getall() if h.strip()]
            rows = []
            for row in table.css("tbody tr, tr"):
                cells = [c.strip() for c in row.css("td::text, th::text").getall()]
                if any(cells):
                    rows.append(cells)
            if headers or rows:
                tables.append({"headers": headers, "rows": rows})

        content = {
            "title": (selector.css("title::text").get() or "").strip(),
            "h1": [h.strip() for h in selector.css("h1::text").getall() if h.strip()],
            "h2": h2,
            "h3": h3,
            "paragraphs": paragraphs,
            "bold_texts": [b.strip() for b in selector.css("strong::text, b::text").getall() if b.strip()],
            "links": sorted(list(set(links))),
            "external_links": sorted(list(set(external_links))),
            "attachments": sorted(list(set(attachments))),
            "tables": tables,
        }

        return {
            "url": url,
            "state_id": state_id,
            "actions": actions,
            "content": content,
            "assets": {
                "screenshot": screenshot_name,
                "html_rendered": html_name,
            },
        }

    def _page_dir(self, url: str) -> Path:
        return self.urls_root / self._url_hash(url)

    def _load_seed_urls(self) -> List[str]:
        if not self.seed_file:
            return self._dedupe_seed_urls(self.start_urls)

        seed_path = Path(self.seed_file)
        if not seed_path.exists():
            self.logger.warning("seed_file no existe: %s. Se usaran start_urls por defecto.", self.seed_file)
            return self._dedupe_seed_urls(self.start_urls)

        urls = []
        for raw in seed_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)

        if not urls:
            self.logger.warning("seed_file vacio: %s. Se usaran start_urls por defecto.", self.seed_file)
            return self._dedupe_seed_urls(self.start_urls)

        return self._dedupe_seed_urls(urls)

    def _dedupe_seed_urls(self, urls: List[str]) -> List[str]:
        cleaned = []
        seen = set()

        for raw_url in urls:
            normalized = self._normalize_seed_url(raw_url)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            cleaned.append(normalized)

        return cleaned

    @staticmethod
    def _normalize_seed_url(url: str) -> str:
        raw = re.sub(r"[\t\n\r]", "", (url or "")).strip()
        if not raw:
            return ""

        parsed = urlparse(raw)
        host = (parsed.netloc or "").lower()
        path = re.sub(r"/{2,}", "/", parsed.path or "/")

        if host != "fis.epn.edu.ec":
            return raw

        if path.startswith("/cdn-cgi/"):
            return ""

        if path == "/":
            path = "/index.php/es"

        if path != "/" and path.endswith("/"):
            path = path[:-1]

        return urlunparse(((parsed.scheme or "https").lower(), host, path, "", parsed.query, ""))

    @staticmethod
    def _url_hash(url: str) -> str:
        return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _slug(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"\s+", "-", text)
        text = re.sub(r"[^a-z0-9\-]", "", text)
        return text[:40] or "state"

    @staticmethod
    def _visible_text(node) -> str:
        parts = node.xpath(
            ".//text()[normalize-space() and not(ancestor::script) and not(ancestor::style) and not(ancestor::noscript)]"
        ).getall()
        text = re.sub(r"\s+", " ", " ".join(p.strip() for p in parts)).strip()
        # Joomla email cloak can inject JS fragments as inline text nodes; keep only user-facing text.
        text = re.sub(r"\s*document\.getElementById\('cloak[^\n\r]*", "", text)
        return text.strip()
