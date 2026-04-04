"""
Generate FIX Protocol Tool — Slide Deck (.pptx)
Run: python generate_deck.py
Output: FIX_Protocol_Tool_Deck.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Colour palette ─────────────────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x11, 0x17)   # dark background
BLUE       = RGBColor(0x58, 0xA6, 0xFF)   # accent blue
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY = RGBColor(0xC9, 0xD1, 0xD9)
MID_GREY   = RGBColor(0x4A, 0x52, 0x5A)
GREEN      = RGBColor(0x3F, 0xB9, 0x50)
YELLOW     = RGBColor(0xD2, 0x99, 0x22)
RED        = RGBColor(0xF8, 0x51, 0x49)

# ── Slide dimensions (16:9) ────────────────────────────────────────────────
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # completely blank layout


# ── Helper functions ────────────────────────────────────────────────────────

def add_rect(slide, x, y, w, h, fill_color=None, line_color=None, line_width=Pt(0)):
    shape = slide.shapes.add_shape(1, x, y, w, h)  # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, x, y, w, h,
             font_size=Pt(18), bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_slide(title_text, subtitle_text=None):
    slide = prs.slides.add_slide(BLANK)
    # Full background
    add_rect(slide, 0, 0, W, H, fill_color=NAVY)
    # Top accent bar
    add_rect(slide, 0, 0, W, Inches(0.06), fill_color=BLUE)
    # Bottom accent bar
    add_rect(slide, 0, H - Inches(0.06), W, Inches(0.06), fill_color=BLUE)
    # Slide number placeholder (bottom right)
    return slide


def set_title_area(slide, title, subtitle=None, top=Inches(2.5)):
    add_text(slide, title,
             Inches(1), top, Inches(11.33), Inches(1.2),
             font_size=Pt(40), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if subtitle:
        add_text(slide, subtitle,
                 Inches(1), top + Inches(1.3), Inches(11.33), Inches(0.8),
                 font_size=Pt(20), bold=False, color=BLUE, align=PP_ALIGN.CENTER)


def section_header(slide, label):
    add_rect(slide, Inches(1), Inches(0.55), Inches(2.5), Inches(0.35),
             fill_color=BLUE)
    add_text(slide, label,
             Inches(1), Inches(0.55), Inches(2.5), Inches(0.35),
             font_size=Pt(11), bold=True, color=NAVY, align=PP_ALIGN.CENTER)


def slide_title(slide, title):
    add_text(slide, title,
             Inches(1), Inches(0.9), Inches(11.33), Inches(0.7),
             font_size=Pt(30), bold=True, color=WHITE)
    add_rect(slide, Inches(1), Inches(1.55), Inches(4), Inches(0.04),
             fill_color=BLUE)


def bullet_box(slide, items, x, y, w, h, font_size=Pt(16), color=LIGHT_GREY):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = item
        run.font.size = font_size
        run.font.color.rgb = color


def card(slide, x, y, w, h, heading, body, heading_color=BLUE, body_color=LIGHT_GREY):
    add_rect(slide, x, y, w, h,
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=RGBColor(0x30, 0x36, 0x3D), line_width=Pt(1))
    add_text(slide, heading,
             x + Inches(0.15), y + Inches(0.1), w - Inches(0.3), Inches(0.4),
             font_size=Pt(14), bold=True, color=heading_color)
    add_text(slide, body,
             x + Inches(0.15), y + Inches(0.5), w - Inches(0.3), h - Inches(0.6),
             font_size=Pt(13), color=body_color, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title slide
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)

# Large blue diagonal accent
shape = slide.shapes.add_shape(1, Inches(8), 0, Inches(6), H)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1F, 0x3A, 0x5C)
shape.line.fill.background()

add_text(slide, "FIX Protocol",
         Inches(0.8), Inches(1.8), Inches(7), Inches(1.2),
         font_size=Pt(52), bold=True, color=WHITE)
add_text(slide, "Learning & Troubleshooting Tool",
         Inches(0.8), Inches(2.9), Inches(7.5), Inches(0.9),
         font_size=Pt(28), bold=False, color=BLUE)
add_rect(slide, Inches(0.8), Inches(3.85), Inches(3.5), Inches(0.06),
         fill_color=BLUE)
add_text(slide, "AI-Powered | FIXimate Reference | Cloud-Hosted",
         Inches(0.8), Inches(4.1), Inches(7), Inches(0.5),
         font_size=Pt(16), color=LIGHT_GREY)
add_text(slide, "Ken Jiang  |  April 2026",
         Inches(0.8), Inches(5.8), Inches(7), Inches(0.5),
         font_size=Pt(14), color=MID_GREY)
add_text(slide, "fix-protocol-tool.onrender.com",
         Inches(0.8), Inches(6.3), Inches(7), Inches(0.5),
         font_size=Pt(13), color=BLUE, italic=True)

# Right panel text
add_text(slide, "🔧",
         Inches(9.5), Inches(2.5), Inches(2), Inches(1.5),
         font_size=Pt(72), align=PP_ALIGN.CENTER)
add_text(slide, "claude-haiku-4-5\nFlask · Python · SQLite\nRender.com",
         Inches(8.5), Inches(4.2), Inches(4), Inches(1.5),
         font_size=Pt(14), color=LIGHT_GREY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "OVERVIEW")
slide_title(slide, "Agenda")

items = [
    ("01", "The Problem",          "Why FIX protocol support is hard today"),
    ("02", "The Solution",         "What this tool does and how it works"),
    ("03", "Key Features",         "4 core capabilities of the tool"),
    ("04", "Business Value",       "ROI, outcomes, and success metrics"),
    ("05", "Feature Roadmap",      "RICE-prioritised enhancement backlog"),
    ("06", "Architecture",         "Tech stack and deployment"),
    ("07", "Live Demo",            "See the tool in action"),
]

for i, (num, title, desc) in enumerate(items):
    row = i % 4
    col = i // 4
    x = Inches(1) + col * Inches(6.2)
    y = Inches(1.8) + row * Inches(1.2)
    add_rect(slide, x, y, Inches(5.8), Inches(1.0),
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=RGBColor(0x30, 0x36, 0x3D), line_width=Pt(1))
    add_text(slide, num, x + Inches(0.15), y + Inches(0.1),
             Inches(0.5), Inches(0.8), font_size=Pt(22), bold=True, color=BLUE)
    add_text(slide, title, x + Inches(0.65), y + Inches(0.05),
             Inches(5.0), Inches(0.45), font_size=Pt(16), bold=True, color=WHITE)
    add_text(slide, desc, x + Inches(0.65), y + Inches(0.5),
             Inches(5.0), Inches(0.4), font_size=Pt(12), color=LIGHT_GREY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — The Problem
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "01  THE PROBLEM")
slide_title(slide, "FIX Protocol Support is Expensive and Slow")

problems = [
    ("⏱  Steep Learning Curve",
     "21 workflows, 500+ tags, 4 versions.\nMonths to master through static documentation."),
    ("🔺  Slow Troubleshooting",
     "Average 3 hours to resolve a FIX incident.\nRequires escalation to scarce senior engineers."),
    ("🔒  Knowledge Silos",
     "FIX expertise locked in 1–2 individuals.\nWhen they leave, the knowledge leaves with them."),
    ("💸  Costly Downtime",
     "Every FIX outage delays trading.\nClient SLA breaches damage relationships and revenue."),
]

for i, (heading, body) in enumerate(problems):
    col = i % 2
    row = i // 2
    x = Inches(1.0) + col * Inches(5.8)
    y = Inches(1.8) + row * Inches(2.3)
    card(slide, x, y, Inches(5.5), Inches(2.1), heading, body,
         heading_color=RED)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — The Solution
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "02  THE SOLUTION")
slide_title(slide, "An AI-Powered FIX Expert, Available 24/7")

add_text(slide,
         "An instant, browser-based assistant that gives any Fintech professional — "
         "regardless of experience level — access to FIX protocol expertise on demand.",
         Inches(1), Inches(1.7), Inches(11.33), Inches(0.9),
         font_size=Pt(17), color=LIGHT_GREY)

solutions = [
    ("Ask Anything", "Natural language Q&A on any FIX concept, tag, or workflow"),
    ("21 Workflows", "Instant deep-dive on every workflow from Logon to Settlement"),
    ("Troubleshoot", "Paste an error or raw FIX message — get step-by-step diagnosis"),
    ("Build & Validate", "Construct FIX messages with live preview and AI validation"),
    ("Save & Recall", "Persistent conversation history for future reference"),
    ("Always On", "Cloud-hosted — accessible from anywhere, any device"),
]

for i, (heading, body) in enumerate(solutions):
    col = i % 3
    row = i // 3
    x = Inches(0.8) + col * Inches(4.1)
    y = Inches(2.8) + row * Inches(1.9)
    card(slide, x, y, Inches(3.8), Inches(1.7), heading, body,
         heading_color=GREEN)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Key Features
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "03  KEY FEATURES")
slide_title(slide, "4 Core Capabilities")

features = [
    ("01  Learn Mode",
     "Chat interface powered by Claude AI.\n"
     "Ask about any FIX tag, message type, or concept.\n"
     "Answers include FIXimate tag numbers and examples.",
     BLUE),
    ("02  Troubleshoot Mode",
     "Select error category + FIX version.\n"
     "Paste raw FIX message or error text.\n"
     "AI returns root cause and resolution steps.",
     YELLOW),
    ("03  FIX Message Builder",
     "Select MsgType, fill SenderCompID/TargetCompID.\n"
     "Add custom tags — live Tag=Value preview.\n"
     "AI validates required fields and structure.",
     GREEN),
    ("04  Workflow Sidebar",
     "All 21 FIX workflows grouped by phase.\n"
     "One click = detailed workflow explanation.\n"
     "Covers Session, Pre-Trade, Trade, Post-Trade, Ops.",
     RGBColor(0xD2, 0x99, 0x22)),
]

for i, (heading, body, color) in enumerate(features):
    x = Inches(0.8) + i * Inches(3.0)
    add_rect(slide, x, Inches(1.75), Inches(2.75), Inches(5.2),
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=color, line_width=Pt(2))
    add_rect(slide, x, Inches(1.75), Inches(2.75), Inches(0.08),
             fill_color=color)
    add_text(slide, heading,
             x + Inches(0.15), Inches(1.95), Inches(2.45), Inches(0.55),
             font_size=Pt(14), bold=True, color=color)
    add_text(slide, body,
             x + Inches(0.15), Inches(2.6), Inches(2.45), Inches(4.0),
             font_size=Pt(13), color=LIGHT_GREY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Business Value / ROI
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "04  BUSINESS VALUE")
slide_title(slide, "ROI: 2,900% — Payback in Under 2 Weeks")

# Big numbers
metrics = [
    ("$18,000", "Annual savings\nin engineer hours"),
    ("<$700",   "Total Year 1\ncost"),
    ("2,900%",  "Return on\ninvestment"),
    ("2 weeks", "Payback\nperiod"),
]
for i, (num, label) in enumerate(metrics):
    x = Inches(0.8) + i * Inches(3.0)
    add_rect(slide, x, Inches(1.75), Inches(2.75), Inches(1.8),
             fill_color=RGBColor(0x1F, 0x3A, 0x5C))
    add_text(slide, num,
             x, Inches(1.85), Inches(2.75), Inches(0.9),
             font_size=Pt(30), bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    add_text(slide, label,
             x, Inches(2.75), Inches(2.75), Inches(0.7),
             font_size=Pt(12), color=LIGHT_GREY, align=PP_ALIGN.CENTER)

# Outcome table
add_text(slide, "Key Outcomes",
         Inches(1), Inches(3.75), Inches(5), Inches(0.45),
         font_size=Pt(16), bold=True, color=WHITE)

outcomes = [
    ("MTTR per FIX incident",       "3 hrs  →  < 1 hr",    GREEN),
    ("Escalation rate",             "10/month  →  < 6",    GREEN),
    ("Tag lookup time",             "45 mins  →  < 5 mins", GREEN),
    ("New hire productivity",       "3 months  →  4 weeks", GREEN),
    ("Client SLA resolution",       "4 hrs  →  1 hr",      GREEN),
    ("Trading downtime / month",    "2 hrs  →  < 30 mins", GREEN),
]
for i, (metric, change, color) in enumerate(outcomes):
    y = Inches(4.3) + i * Inches(0.44)
    add_text(slide, f"▸  {metric}",
             Inches(1), y, Inches(5.5), Inches(0.4),
             font_size=Pt(13), color=LIGHT_GREY)
    add_text(slide, change,
             Inches(6.6), y, Inches(3.5), Inches(0.4),
             font_size=Pt(13), bold=True, color=color)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — RICE Roadmap
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "05  FEATURE ROADMAP")
slide_title(slide, "RICE-Prioritised Enhancement Backlog")

add_text(slide, "RICE Score = (Reach × Impact × Confidence) / Effort",
         Inches(1), Inches(1.7), Inches(11), Inches(0.4),
         font_size=Pt(14), color=BLUE, italic=True)

headers = ["Feature", "Reach", "Impact", "Conf.", "Effort", "RICE", "Outcome"]
col_widths = [Inches(3.8), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8), Inches(1.2)]
col_x = [Inches(0.8)]
for w in col_widths[:-1]:
    col_x.append(col_x[-1] + w)

# Header row
add_rect(slide, Inches(0.8), Inches(2.2), sum(col_widths), Inches(0.38),
         fill_color=RGBColor(0x1F, 0x3A, 0x5C))
for j, (h, x, w) in enumerate(zip(headers, col_x, col_widths)):
    add_text(slide, h, x + Inches(0.05), Inches(2.22), w, Inches(0.35),
             font_size=Pt(11), bold=True, color=BLUE)

rows = [
    ("FIX Tag Search",              "50", "2", "100%", "0.5", "200", "🟡 LEARN"),
    ("Error Code Reference",        "40", "2", "100%", "0.5", "160", "🟢 MTTR"),
    ("Saved Message Templates",     "30", "2", "100%", "0.5", "120", "🟢 MTTR"),
    ("FIX Message Log Parser",      "40", "3",  "80%", "1.0",  "96", "🟢 MTTR"),
    ("Sequence No. Calculator",     "20", "3",  "80%", "0.5",  "96", "🟢 MTTR"),
    ("Export Chat to PDF",          "30", "1", "100%", "0.5",  "60", "🟠 CLIENT"),
    ("User Authentication",         "50", "2",  "80%", "2.0",  "40", "🔵 ADOPT"),
    ("FIX Version Comparison",      "25", "2",  "80%", "1.0",  "40", "🟡 LEARN"),
]

for i, row_data in enumerate(rows):
    y = Inches(2.6) + i * Inches(0.52)
    bg = RGBColor(0x1C, 0x21, 0x28) if i % 2 == 0 else RGBColor(0x16, 0x1B, 0x22)
    add_rect(slide, Inches(0.8), y, sum(col_widths), Inches(0.5), fill_color=bg)
    for j, (val, x, w) in enumerate(zip(row_data, col_x, col_widths)):
        color = BLUE if j == 5 else LIGHT_GREY
        bold  = j == 5
        add_text(slide, val, x + Inches(0.05), y + Inches(0.07), w, Inches(0.38),
                 font_size=Pt(11), color=color, bold=bold)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Architecture
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "06  ARCHITECTURE")
slide_title(slide, "Tech Stack & Deployment")

layers = [
    ("USER",       "Browser (Chrome / Edge)",
     "HTML5 · CSS3 · Vanilla JS · Marked.js", BLUE),
    ("BACKEND",    "Flask 3.1 (Python 3.12)",
     "REST API · SSE Streaming · SQLite history", GREEN),
    ("AI ENGINE",  "Anthropic Claude claude-haiku-4-5",
     "FIX system prompt · 4,096 token responses · Streaming", YELLOW),
    ("HOSTING",    "Render.com (Cloud)",
     "Auto-deploy from GitHub · Free tier · HTTPS", RGBColor(0xD2, 0x99, 0x22)),
    ("SOURCE",     "GitHub",
     "github.com/ken-jiang-claude/fix-protocol-tool", MID_GREY),
]

for i, (layer, title, detail, color) in enumerate(layers):
    y = Inches(1.75) + i * Inches(1.02)
    add_rect(slide, Inches(1.0), y, Inches(1.4), Inches(0.85),
             fill_color=color)
    add_text(slide, layer,
             Inches(1.0), y, Inches(1.4), Inches(0.85),
             font_size=Pt(11), bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_rect(slide, Inches(2.5), y, Inches(9.8), Inches(0.85),
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=color, line_width=Pt(1))
    add_text(slide, title,
             Inches(2.65), y + Inches(0.05), Inches(5.0), Inches(0.4),
             font_size=Pt(14), bold=True, color=WHITE)
    add_text(slide, detail,
             Inches(2.65), y + Inches(0.45), Inches(9.5), Inches(0.35),
             font_size=Pt(12), color=LIGHT_GREY)
    if i < len(layers) - 1:
        add_text(slide, "▼",
                 Inches(1.45), y + Inches(0.85), Inches(0.5), Inches(0.2),
                 font_size=Pt(10), color=MID_GREY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Project Management
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "PROJECT GOVERNANCE")
slide_title(slide, "End-to-End Project Management")

items = [
    ("Business Justification", "Problem, solution, stakeholders, strategic alignment"),
    ("ROI & Outcomes",         "2,900% ROI · KPIs across People, Process, Business"),
    ("RACI Matrix",            "6 roles · 30 activities · clear accountability"),
    ("Definition of Ready",    "12 criteria to qualify a story for development"),
    ("Definition of Done",     "16 criteria across code, testing, deploy, docs"),
    ("Milestones",             "8 milestones · M1–M5 complete · M6–M8 planned"),
    ("RICE Prioritisation",    "14 features scored · outcome-tagged · sprint-mapped"),
    ("Testing Plan",           "Unit · Integration · E2E · Performance · Security"),
    ("SDLC",                   "6-phase Agile model · tech stack rationale"),
    ("Gantt Chart",            "Full timeline · renders as diagram on GitHub"),
]

for i, (title, desc) in enumerate(items):
    col = i % 2
    row = i // 2
    x = Inches(0.8) + col * Inches(6.1)
    y = Inches(1.75) + row * Inches(1.0)
    add_rect(slide, x, y, Inches(5.8), Inches(0.85),
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=RGBColor(0x30, 0x36, 0x3D), line_width=Pt(1))
    add_rect(slide, x, y, Inches(0.06), Inches(0.85), fill_color=BLUE)
    add_text(slide, title,
             x + Inches(0.2), y + Inches(0.05), Inches(5.4), Inches(0.38),
             font_size=Pt(13), bold=True, color=WHITE)
    add_text(slide, desc,
             x + Inches(0.2), y + Inches(0.45), Inches(5.4), Inches(0.35),
             font_size=Pt(11), color=LIGHT_GREY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Live Demo
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)
section_header(slide, "07  LIVE DEMO")
slide_title(slide, "See It In Action")

demo_steps = [
    ("Step 1", "Open the app",
     "https://fix-protocol-tool.onrender.com"),
    ("Step 2", "Ask a FIX question",
     '"What are the required tags in a NewOrderSingle?"'),
    ("Step 3", "Click a workflow",
     "Click 07 Single Order in the sidebar"),
    ("Step 4", "Try Troubleshoot mode",
     "Switch mode → paste a FIX rejection message"),
    ("Step 5", "Use the Builder",
     "Open Builder → select MsgType=D → validate"),
]

for i, (step, action, detail) in enumerate(demo_steps):
    y = Inches(1.8) + i * Inches(1.02)
    add_rect(slide, Inches(0.8), y, Inches(1.0), Inches(0.85),
             fill_color=BLUE)
    add_text(slide, step,
             Inches(0.8), y, Inches(1.0), Inches(0.85),
             font_size=Pt(11), bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_rect(slide, Inches(1.9), y, Inches(10.6), Inches(0.85),
             fill_color=RGBColor(0x1C, 0x21, 0x28),
             line_color=RGBColor(0x30, 0x36, 0x3D), line_width=Pt(1))
    add_text(slide, action,
             Inches(2.1), y + Inches(0.05), Inches(5.0), Inches(0.38),
             font_size=Pt(14), bold=True, color=WHITE)
    add_text(slide, detail,
             Inches(2.1), y + Inches(0.45), Inches(10.0), Inches(0.35),
             font_size=Pt(12), color=BLUE, italic=True)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Closing / Thank You
# ═══════════════════════════════════════════════════════════════════════════
slide = add_slide(None)

shape = slide.shapes.add_shape(1, Inches(8), 0, Inches(6), H)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1F, 0x3A, 0x5C)
shape.line.fill.background()

add_text(slide, "Thank You",
         Inches(0.8), Inches(1.8), Inches(7), Inches(1.2),
         font_size=Pt(52), bold=True, color=WHITE)
add_rect(slide, Inches(0.8), Inches(3.1), Inches(3.5), Inches(0.06),
         fill_color=BLUE)

links = [
    ("Live App",    "fix-protocol-tool.onrender.com"),
    ("GitHub",      "github.com/ken-jiang-claude/fix-protocol-tool"),
    ("User Manual", "FIX learning.md  (in repository)"),
    ("PM Doc",      "PROJECT_MANAGEMENT.md  (in repository)"),
]
for i, (label, val) in enumerate(links):
    y = Inches(3.4) + i * Inches(0.65)
    add_text(slide, f"{label}:",
             Inches(0.8), y, Inches(2.2), Inches(0.55),
             font_size=Pt(14), bold=True, color=LIGHT_GREY)
    add_text(slide, val,
             Inches(3.1), y, Inches(4.5), Inches(0.55),
             font_size=Pt(14), color=BLUE, italic=True)

add_text(slide, "Ken Jiang  |  April 2026",
         Inches(0.8), Inches(6.5), Inches(7), Inches(0.45),
         font_size=Pt(13), color=MID_GREY)

add_text(slide, "Questions?",
         Inches(9.0), Inches(3.2), Inches(3.5), Inches(0.8),
         font_size=Pt(32), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "Let's discuss",
         Inches(9.0), Inches(4.0), Inches(3.5), Inches(0.5),
         font_size=Pt(18), color=BLUE, align=PP_ALIGN.CENTER)


# ── Save ────────────────────────────────────────────────────────────────────
output = r"c:\Users\Taikary Jiang\FIX Protocol\FIX_Protocol_Tool_Deck.pptx"
prs.save(output)
print(f"Deck saved: {output}")
print(f"Slides: {len(prs.slides)}")
