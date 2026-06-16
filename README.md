# ◆ Quill — AI Content Engine

> Multi-agent pipeline that plans, writes, and assembles long-form technical articles — powered by LangGraph and OpenAI.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-1C3C3C?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1-412991?style=flat&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

---

## Overview

Quill is a **multi-agent content generation system** built on [LangGraph](https://github.com/langchain-ai/langgraph). Given a topic, it:

1. **Plans** a structured blog outline using an orchestrator agent
2. **Writes** each section in parallel using independent worker agents
3. **Assembles** the sections into a final polished article via a reducer

The result is a production-ready Markdown article saved to disk and rendered in a clean Streamlit UI.

---

## Architecture

```
                    ┌─────────────────────────────┐
                    │         User Input           │
                    │  "How Self-Attention Works"  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │  Orchestrator   │  Plans 5–7 sections
                         │   (LLM + Plan   │  with title & brief
                         │    schema)      │
                         └────────┬────────┘
                                  │  Fan-out via Send()
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │ Worker 1 │ │ Worker 2 │ │ Worker N │   Parallel
             │ Section  │ │ Section  │ │ Section  │   execution
             └────┬─────┘ └────┬─────┘ └────┬─────┘
                  └────────────┼─────────────┘
                               │  Fan-in (operator.add)
                               ▼
                        ┌─────────────┐
                        │   Reducer   │  Sorts, joins, saves .md
                        └──────┬──────┘
                               │
                               ▼
                       ┌──────────────┐
                       │  Final Blog  │
                       │  (Markdown)  │
                       └──────────────┘
```

---

## Features

- **Parallel section writing** — workers run concurrently via LangGraph's `Send` API, reducing total generation time
- **Structured output** — orchestrator uses Pydantic schemas to guarantee consistent plan format
- **Prompt management** — all prompts externalized to versioned YAML files under `prompts/`
- **Auto-save** — generated articles saved to `outputs/` as Markdown files
- **Streamlit UI** — side-by-side panel layout with live pipeline status, outline viewer, and download

---

## Project Structure

```
quill/
├── agents/
│   ├── orchestrator.py     # Plans the blog structure
│   ├── worker.py           # Writes a single section
│   └── reducer.py          # Assembles the final article
│
├── graphs/
│   └── blog_graph.py       # LangGraph graph definition
│
├── schemas/
│   ├── task_obj_schema.py  # Task (section) Pydantic model
│   └── plan_obj_schema.py  # Plan Pydantic model
│
├── state/
│   └── state.py            # LangGraph shared state (TypedDict)
│
├── prompts/
│   ├── orchestrator.yaml   # Orchestrator system + human prompt
│   └── worker.yaml         # Worker system + human prompt
│
├── config/
│   ├── settings.py         # Pydantic settings (reads .env)
│   └── llm.py              # LLM factory (ChatOpenAI wrapper)
│
├── utils/
│   ├── prompt_loader.py    # YAML prompt loader
│   └── file_io.py          # Markdown file writer
│
├── notebooks/
│   └── 1_basic_blog_write.ipynb  # Prototype / reference notebook
│
├── frontend.py             # Streamlit UI
├── backend_app.py          # CLI entry point
├── requirement.txt         # Python dependencies
└── .env                    # API keys (not committed)
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/avinashmyerolkar/Planning_Agent.git
cd Planning_Agent

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirement.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

### Run the app

```bash
streamlit run frontend.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Run from CLI

```bash
python backend_app.py
```

Generated articles are saved to `outputs/`.

---

## How It Works

### 1. Orchestrator
Calls the LLM with a structured output schema (`Plan`) to produce a list of `Task` objects — each with an `id`, `title`, and `brief` describing what the section should cover.

### 2. Fan-out (parallel workers)
LangGraph's `Send` API dispatches one `worker` node per task simultaneously. Each worker calls the LLM independently to write its section in Markdown.

### 3. Reducer
After all workers complete, the reducer joins the sections in order, prepends the blog title as an H1, and writes the result to `outputs/`.

### State flow

```python
State = {
    "topic":    str,                            # user input
    "plan":     Plan,                           # orchestrator output
    "sections": Annotated[List[str], add],      # accumulated by workers
    "final":    str,                            # reducer output
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | OpenAI GPT-4.1-mini (via [LangChain](https://github.com/langchain-ai/langchain)) |
| Data validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Configuration | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| UI | [Streamlit](https://streamlit.io/) |
| Language | Python 3.11+ |

---

## Roadmap

- [ ] Router agent — decides if web research is needed before planning
- [ ] Research agent — Tavily-powered web search for volatile topics
- [ ] Streaming token output in the UI
- [ ] Multiple export formats (HTML, PDF)
- [ ] Custom tone / audience / length controls

---

## License

MIT © 2026 Avinash Mahadev Yerolkar
