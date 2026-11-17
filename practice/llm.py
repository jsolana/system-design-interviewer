"""Chat model factory shared by the interviewer and the evaluator (env-driven, OpenAI-compatible)."""
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def build_llm(temperature: float = 0.7):
    """LLM_PROVIDER=openai (any OpenAI-compatible endpoint: OPENAI_BASE_URL + OPENAI_API_KEY + OPENAI_MODEL)
    or anthropic. If LLM_PROVIDER is empty it is inferred from which keys are set."""
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
            temperature=temperature,
        )
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"), temperature=temperature)
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}' (use 'openai' or 'anthropic')")


def text_of(content) -> str:
    """Normalize LangChain message content (str or list of blocks) to plain text."""
    if isinstance(content, list):
        return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return content or ""
