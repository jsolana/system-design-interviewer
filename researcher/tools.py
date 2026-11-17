"""Tools for the PDF researcher agent: Tavily search, CSV reader and a guarded PDF downloader."""
import csv
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DOCS_DIR = Path(os.getenv("DOCS_DIR", Path(__file__).resolve().parent.parent / "docs"))
MAX_BYTES = 300 * 1024 * 1024
MIN_PAGES = 30  # shorter files are treated as articles unless explicitly named as a sample

# Shadow libraries and sites that redistribute copyrighted books without permission.
# Never searched and never downloaded from.
BLOCKED_DOMAINS = []


def _blocked(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in BLOCKED_DOMAINS if "/" not in d)


search_pdfs = TavilySearch(
    max_results=8,
    exclude_domains=[d for d in BLOCKED_DOMAINS if "/" not in d],
    name="search_pdfs",
    description=(
        "Search the web (Tavily) for a distributable PDF of a document. "
        "Put 'filetype:pdf', the title and the author in the query. Returns urls and snippets."
    ),
)


@tool
def read_books_csv(path: str) -> str:
    """Read a CSV with columns titulo, autor, editorial (or title, author, publisher) and list its rows."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(line for line in f if line.strip()))
    lines = []
    for r in rows:
        low = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k and isinstance(v, str)}
        title = low.get("titulo") or low.get("title", "")
        author = low.get("autor") or low.get("author", "")
        pub = low.get("editorial") or low.get("publisher", "")
        lines.append(f"- {title} | {author} | {pub}")
    return f"{len(lines)} books:\n" + "\n".join(lines)


@tool
def download_pdf(url: str, filename: str) -> str:
    """Download a PDF from `url` into the docs folder as `filename` (.pdf).
    Refuses blocked domains, non-PDF content, files over 300 MB and files under 30 pages
    (unless the filename contains 'sample'). Returns the page count and host."""
    if not url.startswith(("http://", "https://")):
        return "Refused: only http(s) URLs."
    if _blocked(url):
        return "Refused: this site redistributes copyrighted books without permission. Find an official source."
    safe = re.sub(r"[^A-Za-z0-9._ -]", "_", filename).strip() or "document"
    if not safe.lower().endswith(".pdf"):
        safe += ".pdf"
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    dest = DOCS_DIR / safe
    if dest.exists():
        return f"Skipped: {dest} already exists."
    try:
        with requests.get(url, stream=True, timeout=30, headers={"User-Agent": "pdf-researcher/0.1"}) as r:
            r.raise_for_status()
            if _blocked(r.url):
                return "Refused: redirected to a blocked site."
            size, first = 0, True
            with open(dest, "wb") as f:
                for chunk in r.iter_content(1 << 16):
                    if first:
                        if not chunk.startswith(b"%PDF"):
                            f.close()
                            dest.unlink(missing_ok=True)
                            return "Failed: the URL did not return a PDF (likely a landing page)."
                        first = False
                    size += len(chunk)
                    if size > MAX_BYTES:
                        f.close()
                        dest.unlink(missing_ok=True)
                        return "Failed: file exceeds 300 MB."
                    f.write(chunk)
    except requests.RequestException as e:
        dest.unlink(missing_ok=True)
        return f"Failed: {e}"
    try:
        pages = len(PdfReader(dest).pages)
    except Exception:
        dest.unlink(missing_ok=True)
        return "Failed: the file is not a readable PDF."
    host = urlparse(url).hostname
    if pages < MIN_PAGES and "sample" not in safe.lower():
        dest.unlink(missing_ok=True)
        return (
            f"Rejected: only {pages} pages from {host}, which looks like an article, not the book. "
            "If it is an official sample chapter from the publisher or author, retry with "
            "'(sample)' in the filename."
        )
    return f"Saved {dest} ({size / 1e6:.1f} MB, {pages} pages, host {host})."


TOOLS = [search_pdfs, read_books_csv, download_pdf]
