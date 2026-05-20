import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import scrapy


class FisDiscoverySpider(scrapy.Spider):
    name = "fis_discovery"
    allowed_domains = ["fis.epn.edu.ec"]

    start_urls = [
        "https://fis.epn.edu.ec/index.php/es/",
    ]

    # For discovery we use plain Scrapy HTTP handlers (faster than Playwright for this task).
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy.core.downloader.handlers.http11.HTTP11DownloadHandler",
            "https": "scrapy.core.downloader.handlers.http11.HTTP11DownloadHandler",
        }
    }

    def __init__(self, *args, **kwargs):
        max_urls = int(kwargs.pop("max_urls", 1200))
        output_file = kwargs.pop("output_file", "input/urls_master.txt")
        super().__init__(*args, **kwargs)
        self.max_urls = max(1, max_urls)
        self.output_file = Path(output_file)
        self.discovered_urls = set()

    async def start(self):
        for url in self.start_urls:
            normalized = self._normalize_url(url)
            self.discovered_urls.add(normalized)
            yield scrapy.Request(normalized, callback=self.parse, dont_filter=True)

    def parse(self, response: scrapy.http.Response):
        if len(self.discovered_urls) >= self.max_urls:
            return

        content_type = (response.headers.get("Content-Type") or b"").decode("latin-1").lower()
        if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
            return

        for href in response.css("a::attr(href)").getall():
            absolute = response.urljoin(href)
            normalized = self._normalize_url(absolute)

            if not normalized:
                continue
            if not self._is_internal(normalized):
                continue
            if not self._is_html_candidate(normalized):
                continue
            if normalized in self.discovered_urls:
                continue

            self.discovered_urls.add(normalized)
            if len(self.discovered_urls) > self.max_urls:
                break

            yield scrapy.Request(normalized, callback=self.parse)

    def closed(self, reason):
        urls = sorted(self.discovered_urls)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# URLs semilla descubiertas automaticamente para fis.epn.edu.ec",
            f"# generated_at_utc: {datetime.utcnow().isoformat()}Z",
            f"# total_urls: {len(urls)}",
            "",
        ]
        lines.extend(urls)
        self.output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        report_dir = Path("output")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"discovery_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report = {
            "reason": reason,
            "total_urls": len(urls),
            "max_urls": self.max_urls,
            "output_file": str(self.output_file).replace("\\", "/"),
        }
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _is_internal(url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        return host == "fis.epn.edu.ec"

    @staticmethod
    def _is_html_candidate(url: str) -> bool:
        path = (urlparse(url).path or "").lower()
        if not path:
            return True

        if path.startswith("/cdn-cgi/"):
            return False

        excluded_extensions = (
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".zip",
            ".rar",
            ".7z",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".webp",
            ".css",
            ".js",
            ".json",
            ".xml",
            ".txt",
            ".mp4",
            ".mp3",
            ".avi",
            ".mov",
            ".woff",
            ".woff2",
            ".ttf",
            ".eot",
        )
        return not path.endswith(excluded_extensions)

    @staticmethod
    def _normalize_url(url: str) -> str:
        # Strip whitespace and obvious fragments.
        raw = re.sub(r"[\t\n\r]", "", (url or "")).strip()
        if not raw:
            return ""

        parsed = urlparse(raw)
        scheme = (parsed.scheme or "https").lower()
        netloc = parsed.netloc.lower()
        path = parsed.path or "/"

        # Remove duplicate slashes in path while preserving leading slash.
        path = re.sub(r"/{2,}", "/", path)

        # Canonicalize the site root to the Spanish home page used by the site.
        if netloc == "fis.epn.edu.ec" and path == "/":
            path = "/index.php/es"

        # Remove trailing slash except site root.
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        # Keep query params that may identify Joomla pages, remove common noise.
        drop_params = {
            "fontsize",
            "fbclid",
            "gclid",
            "yclid",
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "tmpl",
            "print",
            "highlight",
            "searchword",
            "ordering",
            "searchphrase",
        }
        kept_params = []
        for k, v in parse_qsl(parsed.query, keep_blank_values=False):
            key = k.strip().lower()
            if key in drop_params:
                continue
            kept_params.append((k.strip(), v.strip()))
        kept_params.sort(key=lambda x: (x[0].lower(), x[1]))

        query = urlencode(kept_params, doseq=True)

        return urlunparse((scheme, netloc, path, "", query, ""))
