# Interview practice (interviewer + evaluator)

Mock system design and coding interviews grounded in `knowledge/`. Two LangChain agents behind a Gradio UI:

- **Interviewer** asks what you want to practice, searches the knowledge base, picks a problem and runs the interview
  like a real interviewer (short turns, open-ended, non-assertive, accepts alternative solutions, small hints only on request).
- **Evaluator** runs when you press *Finish & evaluate*: it reads the whole conversation, your whiteboard and the
  reference solution, and returns a radar chart (8 dimensions), strengths, improvements, a comparison with the reference
  and a level (junior / mid / senior / staff / staff+). The level is an LLM judgment of one conversation, not a verdict.

Mermaid diagrams are rendered in the chat (any ```mermaid block) and in the *Whiteboard* tab. No session persistence.

## Run

```bash
cd practice
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env        # set OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL (LLM_PROVIDER=openai)
python app.py                     # http://127.0.0.1:7860
```

Any OpenAI-compatible endpoint works (OpenAI, OpenRouter, Ollama, vLLM, LM Studio). The model must support tool calling;
structured output is used for the evaluation with a JSON fallback. Mermaid is loaded from the jsDelivr CDN.

## Files
`llm.py` (model factory) · `knowledge_tools.py` (search/read `knowledge/`) · `interviewer.py` · `evaluator.py` · `app.py`
