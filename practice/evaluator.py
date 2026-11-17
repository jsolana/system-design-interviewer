"""Evaluator agent: scores a finished interview (radar dimensions + level) with structured output."""
import json
import re
from typing import Literal

from pydantic import BaseModel, Field

from llm import build_llm

SYSTEM_DESIGN_DIMS = ["Requirements & scoping", "Data modeling", "API design", "High-level architecture",
                      "Scalability", "Resilience & reliability", "Trade-off reasoning", "Communication"]
CODING_DIMS = ["Problem understanding", "Algorithm choice", "Data structures", "Complexity analysis",
               "Correctness & edge cases", "Code quality", "Testing mindset", "Communication"]

LEVELS = ["junior", "mid", "senior", "staff", "staff_plus"]


class DimensionScore(BaseModel):
    name: str = Field(description="Exactly one of the dimension names given in the instructions")
    score: float = Field(ge=0, le=10)
    rationale: str = Field(description="1-2 sentences citing evidence from the conversation")


class Evaluation(BaseModel):
    scores: list[DimensionScore]
    strengths: list[str]
    improvements: list[str]
    compared_to_reference: str = Field(description="What the candidate proposed vs the reference; valid alternatives "
                                                   "are credited, not penalized")
    conversation_quality: str = Field(description="How the conversation went: initiative, structure, handling of "
                                                  "follow-ups, communication")
    level: Literal["junior", "mid", "senior", "staff", "staff_plus"]
    level_justification: str
    next_steps: list[str]


PROMPT = """You are a rigorous but fair hiring-committee evaluator. Evaluate the candidate in the mock interview below.

Interview type: {kind}. Score EXACTLY these dimensions (0-10, one entry each, use these names): {dims}.
Score 0-2 when there is no evidence for a dimension; do not invent evidence. Base everything on what the candidate
actually said or drew; the interviewer's hints count against the score of the dimension they helped with.

Reference for the problem (the interviewer's private notes). It is a guide, not an answer key: alternative designs or
algorithms that are sound must be credited. Mention in compared_to_reference what matches, what is missing and what
differs validly.
<reference>
{reference}
</reference>

Level guide from the knowledge base (primary calibration; use the signals and common down-leveling reasons):
<level_guide>
{level_guide}
</level_guide>

Summary rubric (judge by quality of the conversation and depth, not only the final design):
- junior: follows guidance, covers the basics, needs prompting for structure and trade-offs.
- mid: complete working solution, reasonable structure, some trade-offs, needs prompting on scale/failures.
- senior: drives the conversation, clarifies requirements, justifies trade-offs, handles scale and failure modes.
- staff: challenges and reshapes requirements, reasons about operability, cost, evolution, multiple viable options.
- staff_plus: org/platform-level thinking, strategic trade-offs across systems, exceptional ambiguity handling.
A short or shallow interview must not receive a high level: say so in level_justification.

<whiteboard>
{whiteboard}
</whiteboard>

<transcript>
{transcript}
</transcript>
Write in the language the candidate used."""


def _extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0))


def evaluate(transcript: str, reference: str, kind: str, whiteboard: str = "", llm=None, level_guide: str = "") -> Evaluation:
    dims = CODING_DIMS if kind == "coding" else SYSTEM_DESIGN_DIMS
    prompt = PROMPT.format(kind=kind, dims=", ".join(dims), reference=reference or "(none: problem not found)",
                           whiteboard=whiteboard or "(empty)", transcript=transcript,
                           level_guide=level_guide or "(not available)")
    llm = llm or build_llm(0)
    try:
        result = llm.with_structured_output(Evaluation).invoke(prompt)
        if result is not None:
            return result
    except Exception:
        pass
    schema = json.dumps(Evaluation.model_json_schema())
    raw = llm.invoke(prompt + f"\n\nReply with ONLY a JSON object matching this JSON schema:\n{schema}")
    from llm import text_of

    return Evaluation.model_validate(_extract_json(text_of(raw.content)))
