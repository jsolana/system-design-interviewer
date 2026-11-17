# PDF researcher

LangChain agent with Tavily search that looks for legally distributable PDFs (from a title or a CSV
with `titulo, autor, editorial`) and saves them into `docs/`. Gradio front-end.

```bash
cd researcher
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env          # then fill in your keys
python app.py
```

Guardrails: the prompt only allows author/publisher/open-access sources; shadow libraries are excluded
from search and refused by `download_pdf`, which also checks the `%PDF` header and a 300 MB limit.

## Configuration

Everything is read from `../.env` (see `../.env.example`):

| Variable | Meaning |
|---|---|
| `TAVILY_API_KEY` | Tavily search key (required) |
| `LLM_PROVIDER` | `anthropic` or `openai` (any OpenAI-compatible endpoint). Optional: inferred from the keys that are set |
| `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` | OpenAI-compatible endpoint, token and model (OpenAI, Ollama, vLLM, LM Studio, OpenRouter...) |
| `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Anthropic |
