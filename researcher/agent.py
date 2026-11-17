"""LangChain agent that researches and downloads legally available PDFs."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent

from tools import TOOLS

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

SYSTEM_PROMPT = """You are a research agent that finds and downloads PDF documents.

Input: a book or document (title, author, publisher) or the path of a CSV with columns
titulo, autor, editorial. For a CSV, call read_books_csv first and handle each row in turn.

Method for each document:
1. Call search_pdfs with queries such as: "<title> <author> filetype:pdf", "<title> pdf",
   Try 2-3 query variations before giving up.
2. Judge each result. Only download a PDF
3. Call download_pdf with the URL and a clean filename "<Title> - <Author>.pdf".
4. If a download fails or is not a PDF, try the next candidate.

Status rules: "downloaded" only if the file is the complete book (check the page count returned by
download_pdf: a book has well over 100 pages) from a legitimate host. A short official extract is
"sample only". A short or unrelated file is "not found"; never present an article as the book.

Final answer: a table with one row per document: title, status (downloaded / sample only / not found),
file path or URL, and the license or reason it is legitimate. Do not invent URLs: use only URLs
returned by search_pdfs. Reply in the user's language."""


def build_llm():
    """Chat model from env vars. LLM_PROVIDER=anthropic|openai (openai = any OpenAI-compatible endpoint)."""
    provider = os.getenv("LLM_PROVIDER", "").lower()
    if not provider:
        has_openai = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_KEY")
        provider = "openai" if has_openai and not os.getenv("ANTHROPIC_API_KEY") else "anthropic"
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            base_url=os.getenv("OPENAI_BASE_URL") or None,
            api_key=os.getenv("OPENAI_API_KEY") or "not-needed",
            temperature=0,
        )
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"))
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}' (use 'anthropic' or 'openai')")


def build_agent(model=None):
    return create_agent(model or build_llm(), TOOLS, system_prompt=SYSTEM_PROMPT)
