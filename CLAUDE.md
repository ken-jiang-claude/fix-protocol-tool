# CLAUDE.md — FIX Protocol Learning & Troubleshooting Tool

## Project Overview
AI-powered web app for learning and troubleshooting the FIX Protocol. Built as a Fintech job portfolio project by Ken Jiang.

- **Live URL:** https://fix-protocol-tool.onrender.com
- **GitHub:** https://github.com/ken-jiang-claude/fix-protocol-tool
- **Owner:** Ken Jiang | **Sprint:** 1 of 4 | **Current version:** 1.2

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Flask 3.1 |
| AI model | `claude-haiku-4-5` (Anthropic) |
| Streaming | Server-Sent Events (SSE) via Flask `stream_with_context` |
| Database | SQLite (`fix_history.db`) — ephemeral on Render.com |
| Production server | gunicorn (Procfile: `web: gunicorn web_app:app`) |
| Hosting | Render.com (free tier, auto-deploy from GitHub `main`) |
| Deck generation | python-pptx |
| Frontend | Vanilla JS + marked.js (CDN) |

---

## Key Files

| File | Purpose |
|---|---|
| `web_app.py` | Main Flask app — routes, SSE streaming, SQLite history, API key resolution |
| `templates/index.html` | Single-page frontend — sidebar, chat, troubleshoot mode, FIX message builder |
| `fix_tool.py` | Original CLI version (not used in production) |
| `generate_deck.py` | Generates deck (11 slides, dark navy theme) |
| `generate_deck_bloomberg.py` | Generates Bloomberg-themed deck |
| `Procfile` | gunicorn start command for Render.com |
| `requirements.txt` | `anthropic>=0.89.0`, `flask>=3.1.0`, `gunicorn>=21.2.0` |
| `docs/ReadMe.md` | User manual |
| `docs/PROJECT_MANAGEMENT.md` | Full PM doc — business justification, ROI, RACI, RICE, milestones, SDLC, Gantt |
| `docs/PROJECT_STATUS.md` | 1-page RAG status + RAID log |
| `docs/Persona.md` | Source persona doc (reference only) |
| `docs/Trading Workflow.md` | Source workflow doc (reference only) |
| `docs/FIX_Protocol_Tool_Deck.pptx` | Dark navy presentation deck |
| `docs/FIX_Protocol_Tool_Deck_BBG.pptx` | Bloomberg-themed presentation deck |

---

## Sensitive Files (never commit)

- `.api_key` — local Anthropic API key file (gitignored)
- `fix_history.db` — SQLite database (gitignored)
- `.env` — environment variables (gitignored)

---

## Claude API Usage

- **Model:** `claude-haiku-4-5` — cost-effective, no thinking parameter
- **Do NOT use** `thinking={"type": "adaptive"}` — too costly for this use case
- **Do NOT switch** to `claude-opus-4-6` or `claude-sonnet-4-6` without explicit request
- API key resolved via `resolve_api_key()` in `web_app.py`: env var → `.api_key` file → interactive prompt
- On Render.com, `ANTHROPIC_API_KEY` is set as an environment variable in the dashboard

---

## Running Locally

```bash
cd "c:\Users\Taikary Jiang\FIX Protocol"
python web_app.py
# Open http://localhost:5000
```

API key is stored in `.api_key` — no need to set it each time.

---

## Deployment

Render.com auto-deploys on every push to `main`. No manual deploy step needed.

- Cold start after 15 min idle (free tier) — open URL 2 min before any demo
- SQLite history is lost on redeploy (Issue I05 — persistent DB planned for M7)

---

## Known Issues

| ID | Issue | Status |
|---|---|---|
| I05 | Conversation history lost on Render.com restart (SQLite ephemeral) | Open — fix in M7 |

---

## Deck Generation (generate_deck.py)

Generates `FIX_Protocol_Tool_Deck.pptx` — 11 slides, dark navy theme.

**Run:**
```bash
python generate_deck.py
```

**Theme colours:** Navy `#0A1628`, Accent blue `#1E90FF`, White `#FFFFFF`, Light grey `#E8EDF2`

**Helper functions:**
- `add_rect()` — coloured rectangle shape
- `add_text()` — text box with font/colour control
- `card()` — info card (title + body)
- `slide_title()` — consistent slide heading
- `section_header()` — full-bleed section divider
- `bullet_box()` — bulleted list box

**Slides (in order):** Title, Agenda, Problem, Solution, Key Features, ROI/Business Value, RICE Roadmap, Architecture, PM Governance, Live Demo, Thank You

---

## Roadmap (next sprints)

1. FIX Tag Search (RICE: 200) — May 2026
2. Error Code Quick Reference (RICE: 160) — May 2026
3. Migrate SQLite to PostgreSQL — Jun 2026
4. User auth — Jun 2026
