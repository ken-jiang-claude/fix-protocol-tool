# FIX Protocol Learning & Troubleshooting Tool
## Project Status Update

**Date:** April 4, 2026 | **Version:** 1.2 | **Owner:** Ken Jiang | **Sprint:** 1 of 4

---

## RAG Status Summary

| Area | Status | Comment |
|---|:---:|---|
| Overall Project | 🟢 **GREEN** | On track — all planned deliverables complete |
| Development | 🟢 **GREEN** | Web app live, all 4 features deployed |
| Deployment | 🟢 **GREEN** | Live at fix-protocol-tool.onrender.com |
| Budget | 🟢 **GREEN** | Within $700/year estimate |
| Timeline | 🟢 **GREEN** | M1–M5 complete; M6 iteration starts May 2026 |
| Documentation | 🟢 **GREEN** | User manual, PM doc, and slide deck complete |
| User Adoption | 🟡 **AMBER** | Tool launched; active adoption tracking not yet started |
| Feature Backlog | 🟡 **AMBER** | RICE backlog defined; Sprint 1 enhancements not yet started |

---

## Milestone Progress

| # | Milestone | Target | Status |
|---|---|---|:---:|
| M1 | Project Kickoff & Requirements | Apr 2026 | ✅ Complete |
| M2 | Core Chat MVP | Apr 2026 | ✅ Complete |
| M3 | Full Feature Release (4 features) | Apr 2026 | ✅ Complete |
| M4 | Cloud Deployment (Render.com) | Apr 2026 | ✅ Complete |
| M5 | Documentation & Slide Deck | Apr 2026 | ✅ Complete |
| M6 | User Feedback & Iteration (v1.1) | May 2026 | 🔄 Planned |
| M7 | Enhanced Features (Auth, Tag Search) | Jun 2026 | 🔄 Planned |
| M8 | Production Hardening | Jul 2026 | 🔄 Planned |

---

## RAID Log

### Risks

| ID | Risk | Probability | Impact | Severity | Mitigation | Owner |
|---|---|:---:|:---:|:---:|---|---|
| R01 | Anthropic API price increase raises running cost above budget | Low | Medium | 🟡 Medium | Monitor monthly API spend; switch to lower-tier model if cost exceeds $50/month | Ken Jiang |
| R02 | Render.com free tier spins down after 15 min idle — slow cold start during demo | High | Medium | 🟡 Medium | Open URL 2 min before any demo; upgrade to paid tier ($7/mo) for interviews | Ken Jiang |
| R03 | Claude AI response contains incorrect FIX tag numbers | Medium | High | 🟠 High | System prompt anchored to FIXimate; validate AI answers against FIXimate during UAT | Ken Jiang |
| R04 | API key exposed in GitHub repository | Low | High | 🟠 High | `.api_key` and `.env` in `.gitignore`; confirmed not in repo | Ken Jiang |
| R05 | SQLite history lost on Render.com redeploy (ephemeral disk) | Medium | Low | 🟡 Medium | Migrate to persistent storage (PostgreSQL) in M7 | Ken Jiang |

---

### Assumptions

| ID | Assumption | Impact if Wrong | Status |
|---|---|---|:---:|
| A01 | Users have a modern browser (Chrome/Edge) | UI may break on older browsers | ✅ Valid |
| A02 | Anthropic Claude claude-haiku-4-5 model remains available and cost-effective | Need to re-evaluate model choice | ✅ Valid |
| A03 | Render.com free tier is sufficient for demo and early adoption | May need to upgrade hosting plan | ✅ Valid |
| A04 | FIX team has ~10 incidents/month (basis of ROI calculation) | ROI figures would need recalculation | 🔄 To validate |
| A05 | Users are comfortable sharing FIX error details in a browser-based AI tool | Sensitive data policy may restrict usage | 🔄 To validate |

---

### Issues

| ID | Issue | Raised | Priority | Status | Resolution |
|---|---|---|:---:|:---:|---|
| I01 | API key not persisting between terminal sessions on Windows | Apr 4, 2026 | 🔴 High | ✅ Resolved | Implemented `.api_key` file-based fallback in `web_app.py` |
| I02 | Unicode characters causing crash on Windows terminal (fix_tool.py) | Apr 4, 2026 | 🟡 Medium | ✅ Resolved | Replaced special chars; added `sys.stdout.reconfigure(encoding='utf-8')` |
| I03 | Claude API 400 error — credits too low on first run | Apr 4, 2026 | 🔴 High | ✅ Resolved | User added billing credits; removed deprecated `thinking` parameter |
| I04 | GitHub push rejected on first attempt (remote had auto-generated file) | Apr 4, 2026 | 🟡 Medium | ✅ Resolved | Used `git push --force` to overwrite |
| I05 | Conversation history lost on Render.com restart (SQLite ephemeral) | Apr 4, 2026 | 🟡 Medium | 🔄 Open | Workaround: users save manually; persistent DB planned for M7 |

---

### Dependencies

| ID | Dependency | Type | Status | Risk if Unavailable |
|---|---|---|:---:|---|
| D01 | Anthropic Claude API | External | ✅ Active | Core AI functionality unavailable |
| D02 | Render.com hosting | External | ✅ Active | App offline; no public URL |
| D03 | GitHub repository | External | ✅ Active | No version control or deployment trigger |
| D04 | Python 3.12 + Flask + python-pptx | Internal | ✅ Installed | Local development and deck generation unavailable |
| D05 | FIXimate (reference standard) | External | ✅ Active | AI responses may lack authoritative tag references |

---

## Next Actions

| # | Action | Owner | Due | Priority |
|---|---|---|---|:---:|
| 1 | Begin user feedback collection from 3+ FIX team members | Ken Jiang | May 15, 2026 | 🔴 High |
| 2 | Implement FIX Tag Search feature (RICE: 200 — highest priority) | Ken Jiang | May 31, 2026 | 🔴 High |
| 3 | Implement Error Code Quick Reference (RICE: 160) | Ken Jiang | May 31, 2026 | 🔴 High |
| 4 | Validate ROI assumption A04 — confirm actual incident rate with ops team | Ken Jiang | May 15, 2026 | 🟡 Medium |
| 5 | Migrate SQLite to persistent storage to resolve I05 | Ken Jiang | Jun 2026 | 🟡 Medium |
| 6 | Upgrade Render.com to paid tier before any live interview demo | Ken Jiang | Before next demo | 🟡 Medium |

---

*Status update prepared by Ken Jiang | April 4, 2026 | github.com/ken-jiang-claude/fix-protocol-tool*
