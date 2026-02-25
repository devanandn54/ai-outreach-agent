# ⚡ AI Outreach Agent

An AI-powered local agent built with **LangGraph** that researches any company, analyzes your resume against their needs, and generates hyper-personalized outreach emails to their leadership — all running on your Mac.


---

## What It Does

Give it a **company name** + your **resume (PDF/DOCX)** and the agent will:

1. 🔍 **Research the company** — searches the web in real-time for what they do, funding, tech stack, recent news, and job postings
2. 🎯 **Identify their pain points** — analyzes job signals, product gaps, and challenges they're facing
3. 🧩 **Match your skills to their needs** — finds the overlap between what you offer and what they need
4. 👥 **Find leadership contacts** — locates CTO, CEO, VP Engineering with LinkedIn profiles
5. ✉️ **Generate 3 outreach emails** — each with a different strategy (Direct Value, Empathy Hook, Insight Gift)
6. ✏️ **Suggest resume tweaks** — tells you exactly what to change in your resume for THIS specific company

**Cost:** ~$0.05 per company research

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  INPUT: Company Name + Resume (PDF/DOCX)                 │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│  LANGGRAPH STATE MACHINE (6 Nodes)                       │
│                                                          │
│  ┌────────────┐    ┌─────────────────┐                   │
│  │ Node 1     │───▶│ Node 2          │                   │
│  │ Resume     │    │ Company         │                   │
│  │ Parser     │    │ Researcher      │                   │
│  └────────────┘    │ (6 web searches)│                   │
│                    └────────┬────────┘                   │
│                             ▼                            │
│                    ┌─────────────────┐                   │
│                    │ Node 3          │                   │
│                    │ Gap Analyzer    │                   │
│                    │ (skills ↔ pain) │                   │
│                    └────────┬────────┘                   │
│                             ▼                            │
│                    ┌─────────────────┐                   │
│                    │ Node 4          │                   │
│                    │ Leadership      │                   │
│                    │ Finder          │                   │
│                    └────────┬────────┘                   │
│                             ▼                            │
│                    ┌─────────────────┐                   │
│                    │ Node 5          │                   │
│                    │ Email Generator │                   │
│                    │ (3 variants)    │                   │
│                    └────────┬────────┘                   │
│                             ▼                            │
│                    ┌─────────────────┐                   │
│                    │ Node 6          │                   │
│                    │ Resume Advisor  │                   │
│                    └─────────────────┘                   │
└──────────────────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│  OUTPUT: Research + Emails + Resume Tweaks               │
│  Served via Streamlit on localhost                        │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | [Claude Sonnet 4](https://www.anthropic.com/) via Anthropic API |
| Web Search | [Tavily](https://tavily.com/) (real-time search API) |
| UI | [Streamlit](https://streamlit.io/) |
| Resume Parsing | PyMuPDF (PDF) + python-docx (DOCX) |
| Language | Python 3.11+ |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ai-outreach-agent.git
cd ai-outreach-agent
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```
TAVILY_API_KEY=tvly-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

| Key | Where to get it | Free tier |
|-----|----------------|-----------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/settings/keys) | Pay-as-you-go (~$0.05/run) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com/) | 1000 searches/month free |

### 5. Run

```bash
python -m streamlit run app.py
```

Opens at `http://localhost:8501`. Upload your resume, enter a company name, and hit **Research & Generate**.

---

## Project Structure

```
ai-outreach-agent/
├── .env.example              # Template for API keys
├── requirements.txt
├── app.py                    # Streamlit UI
├── agent/
│   ├── __init__.py           # Loads .env on import
│   ├── state.py              # Shared state schema (TypedDict)
│   ├── graph.py              # LangGraph state machine
│   ├── utils.py              # JSON parsing + helpers
│   ├── nodes/
│   │   ├── resume_parser.py      # Node 1: Parse & analyze resume
│   │   ├── company_researcher.py # Node 2: Web search + synthesis
│   │   ├── gap_analyzer.py       # Node 3: Skills ↔ pain points
│   │   ├── leadership_finder.py  # Node 4: Find CTO/CEO contacts
│   │   ├── email_generator.py    # Node 5: Generate 3 email variants
│   │   └── resume_advisor.py     # Node 6: Resume tweak suggestions
│   └── tools/
│       ├── search.py             # Tavily web search wrapper
│       └── doc_parser.py         # PDF/DOCX text extraction
```

---

## How Each Node Works

| Node | Input | What it does | Output |
|------|-------|-------------|--------|
| **Resume Parser** | PDF/DOCX file | Extracts text, identifies skills, strengths, weaknesses | Structured resume analysis |
| **Company Researcher** | Company name | Runs 6 targeted web searches, Claude synthesizes findings | Company overview, pain points, tech stack, news |
| **Gap Analyzer** | Resume + Company data | Maps your skills against their needs | Skill matches, value propositions, gaps |
| **Leadership Finder** | Company name + target role | Searches for CTO/CEO/VP Eng on LinkedIn | Contact names, titles, LinkedIn URLs |
| **Email Generator** | All previous data | Generates 3 email variants with different strategies | Ready-to-send outreach emails |
| **Resume Advisor** | Resume + Company + Gaps | Suggests specific text changes to your resume | Section-by-section tweaks + tailored summary |

---

## Example Output

**Input:** Company = "Vanta", Resume = my_resume.pdf, Target = CTO

**What you get:**
- 📊 Company research with pain points and tech stack
- 📧 3 personalized emails targeting the CTO
- ✏️ Specific resume tweaks like: *"Change 'Built REST APIs' to 'Designed and scaled compliance-focused APIs handling sensitive audit data' to align with Vanta's security compliance focus"*

---

## Customization

**Change the LLM:** Edit the `model` parameter in any node file:
```python
llm = ChatAnthropic(model="claude-sonnet-4-20250514")  # or any other model
```

**Add more search queries:** Edit `company_researcher.py` — add queries to the `queries` list.

**Change email style:** Edit the `PROMPT` in `email_generator.py` — modify the rules and strategies.

**Add new nodes:** Create a new file in `agent/nodes/`, add it to `graph.py`, and wire it into the flow.

---

## License

MIT — do whatever you want with it.

---

## Contributing

PRs welcome. Some ideas for improvements:

- [ ] Add streaming output (show results as each node completes)
- [ ] Add caching with SQLite (don't re-research the same company)
- [ ] Add batch mode (CSV of companies → spreadsheet of emails)
- [ ] Add human-in-the-loop (pause after research, review before email gen)
- [ ] Add LangSmith tracing for debugging
- [ ] Support more LLMs (OpenAI, Gemini, local models via Ollama)
