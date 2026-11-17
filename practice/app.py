"""Gradio app for mock interviews (interviewer + evaluator). Run: python app.py"""
import html
import re

import gradio as gr
import plotly.graph_objects as go
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, ToolMessage

from evaluator import evaluate
from interviewer import GREETING, build_interviewer
from knowledge_tools import level_guide_text, load_problem, reference_text
from llm import build_llm, text_of

interviewer = build_interviewer(build_llm(0.7))
evaluator_llm = build_llm(0)

LEVEL_LABEL = {"junior": "Junior", "mid": "Mid-level", "senior": "Senior", "staff": "Staff", "staff_plus": "Staff+"}
LEVEL_COLOR = {"junior": "#0ea5e9", "mid": "#14b8a6", "senior": "#6366f1", "staff": "#a855f7", "staff_plus": "#ec4899"}
MERMAID_START = ("graph", "flowchart", "sequenceDiagram", "classDiagram", "stateDiagram", "erDiagram", "gantt",
                 "journey", "pie", "mindmap", "timeline", "C4Context", "architecture", "block")

HEAD = """
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
const dark = () => document.body.classList.contains("dark");
let counter = 0, timer = null;
async function scan() {
  mermaid.initialize({startOnLoad: false, securityLevel: "strict", theme: dark() ? "dark" : "default"});
  for (const code of document.querySelectorAll("code.language-mermaid")) {
    const src = code.textContent.trim();
    const host = code.closest(".code_wrap") || code.closest("pre") || code;
    const next = host.nextElementSibling;
    if (next && next.classList.contains("mermaid-out") && next.dataset.src === src) continue;
    try { await mermaid.parse(src); } catch (e) { continue; }   // incomplete (still streaming) or invalid: keep code
    try {
      const {svg} = await mermaid.render("mmd" + (counter++), src);
      if (next && next.classList.contains("mermaid-out")) next.remove();
      const out = document.createElement("div");
      out.className = "mermaid-out"; out.dataset.src = src; out.innerHTML = svg;
      host.after(out);
      host.style.display = "none";
    } catch (e) { /* leave the code visible */ }
  }
}
new MutationObserver(() => { clearTimeout(timer); timer = setTimeout(scan, 400); })
  .observe(document.documentElement, {childList: true, subtree: true, characterData: true});
</script>
"""

CSS = """
.gradio-container {max-width: 1500px !important;}
.mermaid-out {background: var(--background-fill-secondary); border: 1px solid var(--border-color-primary);
  border-radius: 12px; padding: 12px; margin: 8px 0; overflow-x: auto; text-align: center;}
.mermaid-out svg {max-width: 100%; height: auto;}
#title h1 {margin-bottom: 0;}
.level-badge {display: inline-block; padding: 8px 18px; border-radius: 999px; color: white; font-weight: 700;
  font-size: 1.2rem; letter-spacing: .02em;}
"""


def _wb_html(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return "<p style='opacity:.6'>The diagram preview will appear here.</p>"
    t = re.sub(r"^```(?:mermaid)?\s*|\s*```$", "", t).strip()
    if t.startswith(MERMAID_START):
        return f"<pre><code class='language-mermaid'>{html.escape(t)}</code></pre>"
    return f"<pre style='white-space:pre-wrap'>{html.escape(t)}</pre>"


def _new_state():
    return {"msgs": [], "wb_sent": ""}


def respond(user_msg, history, wb, state):
    user_msg = (user_msg or "").strip()
    if not user_msg:
        yield history, "", state
        return
    content = user_msg
    if wb.strip() and wb.strip() != state["wb_sent"]:
        content += f"\n\n[Whiteboard]\n{wb.strip()}"
        state["wb_sent"] = wb.strip()
    history = history + [{"role": "user", "content": user_msg}, {"role": "assistant", "content": ""}]
    yield history, "", state
    buf, final = "", None
    try:
        stream = interviewer.stream({"messages": state["msgs"] + [{"role": "user", "content": content}]},
                                    stream_mode=["messages", "values"])
        for mode, data in stream:
            if mode == "messages":
                chunk, meta = data
                if isinstance(chunk, ToolMessage):
                    buf = ""
                elif isinstance(chunk, AIMessageChunk) and meta.get("langgraph_node") == "model":
                    buf += text_of(chunk.content)
                    history[-1]["content"] = buf
                    yield history, "", state
            else:
                final = data["messages"]
        if final:
            state["msgs"] = final
            last = next((m for m in reversed(final) if isinstance(m, AIMessage) and text_of(m.content)), None)
            if last:
                history[-1]["content"] = text_of(last.content)
    except Exception as e:  # surface LLM/config errors in the chat instead of crashing the UI
        history[-1]["content"] = f"⚠️ LLM error: `{e}`. Check your `.env` (OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL)."
    yield history, "", state


def _problem_info(msgs):
    slug, kind = None, "any"
    for m in msgs:
        if isinstance(m, AIMessage):
            for call in m.tool_calls or []:
                if call["name"] == "get_problem":
                    slug, kind = call["args"].get("slug"), call["args"].get("kind", "any")
    doc = load_problem(slug, kind) if slug else None
    return (doc["slug"], doc["kind"], doc["meta"].get("title", slug)) if doc else (None, "system-design", None)


def _transcript(msgs):
    lines = []
    for m in msgs:
        t = text_of(m.content).strip()
        if isinstance(m, HumanMessage) and t:
            lines.append(f"CANDIDATE: {t}")
        elif isinstance(m, AIMessage) and t:
            lines.append(f"INTERVIEWER: {t}")
    return "\n\n".join(lines)


def _radar(scores):
    names = [s.name.replace(" & ", "<br>& ") if len(s.name) > 16 else s.name for s in scores]
    vals = [s.score for s in scores]
    fig = go.Figure(go.Scatterpolar(r=vals + vals[:1], theta=names + names[:1], fill="toself",
                                    line=dict(color="#6366f1", width=3), fillcolor="rgba(99,102,241,0.3)",
                                    hovertemplate="%{theta}: %{r}/10<extra></extra>"))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 10], tickvals=[2, 4, 6, 8, 10], gridcolor="rgba(128,128,128,.3)"),
                                 angularaxis=dict(gridcolor="rgba(128,128,128,.3)"), bgcolor="rgba(0,0,0,0)"),
                      showlegend=False, margin=dict(l=120, r=140, t=30, b=30), height=430,
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#888"))
    return fig


def finish(history, wb, state):
    msgs = state["msgs"]
    if not any(isinstance(m, HumanMessage) for m in msgs):
        gr.Warning("Have a conversation first, then finish.")
        return gr.skip(), gr.skip(), gr.skip(), gr.skip()
    slug, kind, title = _problem_info(msgs)
    gr.Info("Evaluating the interview...", duration=3)
    try:
        ev = evaluate(_transcript(msgs), reference_text(slug, kind) if slug else "", kind, wb, evaluator_llm,
                      level_guide_text(kind, slug))
    except Exception as e:
        return gr.skip(), gr.skip(), f"⚠️ Evaluation failed: `{e}`", gr.Tabs(selected="eval")
    badge = (f"<div style='text-align:center;margin:8px 0'><span class='level-badge' "
             f"style='background:{LEVEL_COLOR[ev.level]}'>{LEVEL_LABEL[ev.level]}</span></div>")
    dims = "\n".join(f"| {s.name} | **{s.score:g}/10** | {s.rationale} |" for s in ev.scores)
    report = (
        f"### {title or 'Interview'} ({kind})\n\n"
        f"**Level assessment:** {LEVEL_LABEL[ev.level]}: {ev.level_justification}\n\n"
        f"_Indicative only: this is an LLM judgment of this single conversation._\n\n"
        f"**Conversation quality:** {ev.conversation_quality}\n\n"
        f"**Compared with the reference solution:** {ev.compared_to_reference}\n\n"
        f"| Dimension | Score | Evidence |\n|---|---|---|\n{dims}\n\n"
        f"**Strengths**\n" + "\n".join(f"- {s}" for s in ev.strengths) +
        "\n\n**Areas to improve**\n" + "\n".join(f"- {s}" for s in ev.improvements) +
        "\n\n**Next steps**\n" + "\n".join(f"- {s}" for s in ev.next_steps)
    )
    return badge, _radar(ev.scores), report, gr.Tabs(selected="eval")


def reset():
    return ([{"role": "assistant", "content": GREETING}], "", "", _new_state(), "", None, "", gr.Tabs(selected="board"))


with gr.Blocks(title="Interview practice") as demo:
    state = gr.State(_new_state())
    gr.Markdown("# Interview practice\nMock system design and coding interviews grounded in your knowledge base. "
                "Press **Finish & evaluate** when you are done.", elem_id="title")
    with gr.Row():
        with gr.Column(scale=5):
            chat = gr.Chatbot(value=[{"role": "assistant", "content": GREETING}], height=600, label="Interviewer",
                              buttons=["copy"], render_markdown=True)
            msg = gr.Textbox(placeholder="Type your answer... (Enter to send, Shift+Enter for a new line). "
                                         "You can paste ```mermaid blocks.", lines=2, show_label=False)
            with gr.Row():
                send = gr.Button("Send", variant="primary")
                done = gr.Button("Finish & evaluate", variant="secondary")
                new = gr.Button("New interview")
        with gr.Column(scale=4):
            with gr.Tabs(selected="board") as tabs:
                with gr.Tab("Whiteboard", id="board"):
                    wb = gr.Textbox(label="Diagram (Mermaid) or notes", lines=10, placeholder=(
                        "flowchart LR\n  Client --> LB[Load balancer] --> API\n  API --> Cache[(Redis)]\n  API --> DB[(DB)]"))
                    wb_prev = gr.HTML(_wb_html(""))
                with gr.Tab("Evaluation", id="eval"):
                    badge_out = gr.HTML()
                    plot_out = gr.Plot(label="Skill radar")
                    report_out = gr.Markdown("The evaluation will appear here after you finish the interview.")

    wb.change(_wb_html, wb, wb_prev)
    run_ins, run_outs = [msg, chat, wb, state], [chat, msg, state]
    msg.submit(respond, run_ins, run_outs)
    send.click(respond, run_ins, run_outs)
    done.click(finish, [chat, wb, state], [badge_out, plot_out, report_out, tabs])
    new.click(reset, None, [chat, msg, wb, state, badge_out, plot_out, report_out, tabs])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"), css=CSS, head=HEAD)
