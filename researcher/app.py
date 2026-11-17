"""Gradio front-end for the PDF researcher agent. Run: python app.py"""
import gradio as gr

from agent import build_agent

agent = build_agent()


def _text(content):
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return content


def respond(message, history, csv_file):
    text = message
    if csv_file:
        text = f"{message}\n\nCSV path: {csv_file}"
    msgs = [{"role": m["role"], "content": _text(m["content"])} for m in history] + [{"role": "user", "content": text}]
    result = agent.invoke({"messages": msgs})
    content = result["messages"][-1].content
    if isinstance(content, list):
        content = "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return content


demo = gr.ChatInterface(
    respond,
    additional_inputs=[gr.File(label="Books CSV (titulo, autor, editorial)", type="filepath", file_types=[".csv"])],
    title="PDF researcher",
    description="Finds and downloads legally distributable PDFs (open access, author or publisher editions) into docs/.",
)

if __name__ == "__main__":
    demo.launch()
