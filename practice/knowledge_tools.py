"""Read-only access to knowledge/ for the interviewer (tools) and the evaluator (plain functions)."""
import re
from functools import lru_cache
from pathlib import Path

from langchain_core.tools import tool

KB = Path(__file__).resolve().parent.parent / "knowledge"
FOLDERS = {"system-design": "interviews", "coding": "coding-problems"}
MAX_CHARS = 14000
_STOP = {"a", "an", "the", "of", "for", "to", "and", "in", "on", "i", "want", "like", "practice", "problem",
         "design", "system", "interview", "question", "about", "with", "me", "some", "something", "my", "is"}


def _parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    body = text
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.split("#")[0].strip()
    return {"slug": path.stem, "meta": meta, "body": body, "text": text}


@lru_cache(maxsize=None)
def _load(kind: str) -> tuple:
    folder = KB / FOLDERS[kind]
    return tuple({**_parse(p), "kind": kind} for p in sorted(folder.glob("*.md")))


def _section(body: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def _stem(w: str) -> str:
    return w[:-1] if len(w) > 3 and w.endswith("s") else w


def _stems(text: str) -> str:
    return " " + " ".join(_stem(w) for w in re.findall(r"[a-z0-9]+", text.lower())) + " "


def _completeness(doc: dict) -> int:
    return doc["text"].count("Not covered in the source")


def search(query: str, kind: str = "any", limit: int = 5) -> list[dict]:
    kinds = list(FOLDERS) if kind == "any" else [kind]
    words = [_stem(w) for w in re.findall(r"[a-z0-9]+", query.lower()) if w not in _STOP]
    scored = []
    for k in kinds:
        for d in _load(k):
            title = _stems(d["meta"].get("title", ""))
            tags = _stems(" ".join(d["meta"].get(f, "") for f in ("concepts", "algorithms")))
            body = _stems(d["body"])
            score = 0
            for w in words:
                score += 4 * (f' {w} ' in title) + 2 * (f' {w} ' in tags) + min(body.count(f' {w} '), 3)
            score -= 2 * _completeness(d) if score else 0
            if score > 0:
                scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    return [d for _, d in scored[:limit]]


def load_problem(slug: str, kind: str = "any"):
    for k in ([kind] if kind in FOLDERS else list(FOLDERS)):
        for d in _load(k):
            if d["slug"] == slug:
                return d
    return None


def reference_text(slug: str, kind: str = "any") -> str:
    d = load_problem(slug, kind)
    return d["text"][:MAX_CHARS] if d else ""


@tool
def search_problems(query: str, kind: str = "any") -> str:
    """Search the knowledge base for interview problems. kind: 'system-design', 'coding' or 'any'.
    Returns up to 5 candidates (slug, kind, title, difficulty, how complete the reference is)."""
    res = search(query, kind)
    if not res:
        return "No problems found. Try broader keywords (e.g. 'cache', 'graph', 'chat', 'ranking')."
    lines = []
    for d in res:
        m = d["meta"]
        gaps = _completeness(d)
        lines.append(f"- slug={d['slug']} kind={d['kind']} title={m.get('title')} difficulty={m.get('difficulty')} "
                     f"reference_gaps={gaps}")
    return "\n".join(lines)


@tool
def get_problem(slug: str, kind: str = "any") -> str:
    """Load a problem from the knowledge base: the candidate-facing prompt plus the full reference
    (requirements, design, deep dives, trade-offs). The reference is for YOU only: never show it to the candidate."""
    d = load_problem(slug, kind)
    if not d:
        return f"Problem '{slug}' not found."
    return f"KIND: {d['kind']}\nPROMPT TO PRESENT:\n{_section(d['body'], 'Prompt')}\n\nFULL REFERENCE (private):\n{d['text'][:MAX_CHARS]}"


@tool
def get_concept(slug: str) -> str:
    """Read a concept or algorithm note (to prepare follow-up questions). Private to the interviewer."""
    for folder in ("concepts", "algorithms"):
        p = KB / folder / f"{slug}.md"
        if p.exists():
            return p.read_text(encoding="utf-8")[:6000]
    return f"Note '{slug}' not found."


LEVELS_DIR = KB / "levels"
_ML_TAGS = ("ml-", "embeddings", "feature-engineering", "retrieval-augmented", "transformer", "llm-", "recommendation")


def level_guide_text(kind: str, slug: str | None = None) -> str:
    """Level-expectation guide for the interview type (+ the ML guide for ML/GenAI problems)."""
    names = ["coding" if kind == "coding" else "system-design"]
    doc = load_problem(slug, kind) if slug else None
    if doc and any(t in doc["meta"].get("concepts", "") for t in _ML_TAGS):
        names.append("ml-design")
    parts = []
    for n in names:
        p = LEVELS_DIR / f"{n}.md"
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


@tool
def get_level_guide(kind: str = "system-design") -> str:
    """Level expectations (junior to staff+) and probing questions per level. kind: 'system-design' or 'coding'.
    Use it to calibrate difficulty and choose follow-up questions for the candidate's target level."""
    return level_guide_text(kind)


TOOLS = [search_problems, get_problem, get_concept, get_level_guide]
