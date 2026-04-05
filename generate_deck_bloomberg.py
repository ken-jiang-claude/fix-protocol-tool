"""
FIX Protocol Tool — Bloomberg LP Theme
Run: python generate_deck_bloomberg.py
Output: FIX_Protocol_Tool_Deck_BBG.pptx

Bloomberg palette:
  BG_BLACK   #0A0A0A  - primary background
  BG_PANEL   #141414  - card / panel background
  BG_RAISED  #1E1E1E  - raised elements
  ORANGE     #F5821F  - Bloomberg signature orange
  ORANGE_DIM #C4621A  - dimmer orange for borders
  WHITE      #FFFFFF
  GREY_LT    #E0E0E0  - body text
  GREY_MID   #888888  - secondary text
  GREY_DK    #444444  - subtle borders
  RED        #E53935  - negative / alert
  GREEN      #43A047  - positive / gain
  AMBER      #FFB300  - warning / neutral
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ─────────────────────────────────────────────────────────────────
BG_BLACK  = RGBColor(0x0A, 0x0A, 0x0A)
BG_PANEL  = RGBColor(0x14, 0x14, 0x14)
BG_RAISED = RGBColor(0x1E, 0x1E, 0x1E)
ORANGE    = RGBColor(0xF5, 0x82, 0x1F)
ORANGE_DIM= RGBColor(0x8B, 0x4A, 0x10)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GREY_LT   = RGBColor(0xE0, 0xE0, 0xE0)
GREY_MID  = RGBColor(0x88, 0x88, 0x88)
GREY_DK   = RGBColor(0x44, 0x44, 0x44)
RED       = RGBColor(0xE5, 0x39, 0x35)
GREEN     = RGBColor(0x43, 0xA0, 0x47)
AMBER     = RGBColor(0xFF, 0xB3, 0x00)

# ── Slide size (LAYOUT_WIDE  13.33" × 7.5") ─────────────────────────────────
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

FONT_TITLE = "Consolas"   # Bloomberg terminal feel for titles
FONT_BODY  = "Calibri"    # Clean readable body


# ── Helpers ──────────────────────────────────────────────────────────────────

def rect(slide, x, y, w, h, fill=None, line=None, lw=Pt(1)):
    s = slide.shapes.add_shape(1, x, y, w, h)
    s.line.fill.background()
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = line; s.line.width = lw
    else:
        s.line.fill.background()
    return s


def txt(slide, text, x, y, w, h,
        sz=Pt(16), bold=False, italic=False,
        color=GREY_LT, align=PP_ALIGN.LEFT,
        font=FONT_BODY, wrap=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.word_wrap = wrap
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = sz
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = font
    return tb


def base_slide():
    """Full black background + 3px orange top bar + 1px grey bottom line."""
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, W, H, fill=BG_BLACK)
    rect(slide, 0, 0, W, Inches(0.045), fill=ORANGE)           # orange top bar
    rect(slide, 0, H - Inches(0.012), W, Inches(0.012), fill=GREY_DK)  # grey bottom line
    return slide


def section_tag(slide, label):
    """Small orange pill label top-left."""
    rect(slide, Inches(0.6), Inches(0.18), Inches(2.6), Inches(0.28), fill=ORANGE)
    txt(slide, label,
        Inches(0.6), Inches(0.18), Inches(2.6), Inches(0.28),
        sz=Pt(9), bold=True, color=BG_BLACK, align=PP_ALIGN.CENTER, font=FONT_TITLE)


def slide_header(slide, title):
    """Large slide title, Consolas, white."""
    txt(slide, title,
        Inches(0.6), Inches(0.55), Inches(12.0), Inches(0.75),
        sz=Pt(32), bold=True, color=WHITE, font=FONT_TITLE)
    # Orange left accent bar instead of underline
    rect(slide, Inches(0.6), Inches(1.33), Inches(0.04), Inches(H - Inches(1.7)),
         fill=ORANGE_DIM)


def data_card(slide, x, y, w, h, heading, body,
              accent=ORANGE, body_color=GREY_LT, sz_head=Pt(13), sz_body=Pt(12)):
    """Dark panel card with left orange accent stripe."""
    rect(slide, x, y, w, h, fill=BG_PANEL, line=GREY_DK, lw=Pt(1))
    rect(slide, x, y, Inches(0.05), h, fill=accent)
    txt(slide, heading,
        x + Inches(0.12), y + Inches(0.08), w - Inches(0.2), Inches(0.35),
        sz=sz_head, bold=True, color=accent, font=FONT_TITLE)
    txt(slide, body,
        x + Inches(0.12), y + Inches(0.43), w - Inches(0.2), h - Inches(0.52),
        sz=sz_body, color=body_color, font=FONT_BODY, wrap=True)


def stat_box(slide, x, y, w, h, number, label, num_color=ORANGE):
    rect(slide, x, y, w, h, fill=BG_RAISED, line=GREY_DK)
    txt(slide, number,
        x, y + Inches(0.1), w, Inches(0.75),
        sz=Pt(34), bold=True, color=num_color, align=PP_ALIGN.CENTER, font=FONT_TITLE)
    txt(slide, label,
        x, y + Inches(0.85), w, Inches(0.55),
        sz=Pt(11), color=GREY_MID, align=PP_ALIGN.CENTER, font=FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()

# Right panel: dark raised block
rect(slide, Inches(8.8), 0, Inches(4.53), H, fill=BG_RAISED)
rect(slide, Inches(8.8), 0, Inches(0.04), H, fill=ORANGE)  # divider line

# Left: title block
txt(slide, "FIX PROTOCOL",
    Inches(0.65), Inches(1.4), Inches(7.8), Inches(1.4),
    sz=Pt(58), bold=True, color=WHITE, font=FONT_TITLE)
txt(slide, "Learning & Troubleshooting Tool",
    Inches(0.65), Inches(2.85), Inches(8.0), Inches(0.7),
    sz=Pt(24), bold=False, color=ORANGE, font=FONT_BODY)

rect(slide, Inches(0.65), Inches(3.65), Inches(4.5), Inches(0.035), fill=ORANGE)

txt(slide, "AI-Powered  |  FIXimate Reference  |  Cloud-Hosted",
    Inches(0.65), Inches(3.85), Inches(8.0), Inches(0.45),
    sz=Pt(14), color=GREY_MID, font=FONT_BODY)
txt(slide, "Ken Jiang  |  April 2026",
    Inches(0.65), Inches(5.5), Inches(7.0), Inches(0.45),
    sz=Pt(13), color=GREY_MID, font=FONT_BODY)
txt(slide, "fix-protocol-tool.onrender.com",
    Inches(0.65), Inches(6.1), Inches(7.0), Inches(0.45),
    sz=Pt(13), italic=True, color=ORANGE, font=FONT_BODY)

# Right panel info
txt(slide, "STACK",
    Inches(9.0), Inches(1.2), Inches(4.0), Inches(0.4),
    sz=Pt(10), bold=True, color=ORANGE, font=FONT_TITLE)

stack_items = [
    ("MODEL",    "claude-haiku-4-5"),
    ("FRAMEWORK","Flask 3.1 / Python 3.12"),
    ("DB",       "SQLite"),
    ("HOSTING",  "Render.com"),
    ("VERSION",  "v1.2 / Sprint 1"),
]
for i, (k, v) in enumerate(stack_items):
    y = Inches(1.7) + i * Inches(0.82)
    rect(slide, Inches(9.05), y, Inches(4.0), Inches(0.7), fill=BG_PANEL, line=GREY_DK)
    txt(slide, k, Inches(9.15), y + Inches(0.06), Inches(1.3), Inches(0.3),
        sz=Pt(9), bold=True, color=ORANGE, font=FONT_TITLE)
    txt(slide, v, Inches(10.5), y + Inches(0.06), Inches(2.5), Inches(0.3),
        sz=Pt(11), color=GREY_LT, font=FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "OVERVIEW")
slide_header(slide, "Agenda")

items = [
    ("01", "The Problem",       "Why FIX protocol support is hard today"),
    ("02", "The Solution",      "What this tool does and how it works"),
    ("03", "Key Features",      "4 core capabilities of the tool"),
    ("04", "Business Value",    "ROI, outcomes, and success metrics"),
    ("05", "Feature Roadmap",   "RICE-prioritised enhancement backlog"),
    ("06", "Architecture",      "Tech stack and deployment"),
    ("07", "Live Demo",         "See the tool in action"),
]

col_w = Inches(5.9)
for i, (num, title, desc) in enumerate(items):
    col = i // 4
    row = i % 4
    x = Inches(0.75) + col * Inches(6.2)
    y = Inches(1.55) + row * Inches(1.4)
    rect(slide, x, y, col_w, Inches(1.2), fill=BG_PANEL, line=GREY_DK)
    rect(slide, x, y, Inches(0.05), Inches(1.2), fill=ORANGE)
    txt(slide, num,
        x + Inches(0.12), y + Inches(0.1), Inches(0.6), Inches(0.5),
        sz=Pt(22), bold=True, color=ORANGE, font=FONT_TITLE)
    txt(slide, title,
        x + Inches(0.7), y + Inches(0.1), col_w - Inches(0.85), Inches(0.45),
        sz=Pt(15), bold=True, color=WHITE, font=FONT_TITLE)
    txt(slide, desc,
        x + Inches(0.7), y + Inches(0.55), col_w - Inches(0.85), Inches(0.5),
        sz=Pt(11), color=GREY_MID, font=FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — The Problem
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "01  THE PROBLEM")
slide_header(slide, "FIX Protocol Support is Expensive and Slow")

problems = [
    ("STEEP LEARNING CURVE",
     "21 workflows, 500+ tags, 4 versions.\nMonths to master through static documentation.",
     RED),
    ("SLOW TROUBLESHOOTING",
     "Average 3 hours to resolve a FIX incident.\nRequires escalation to scarce senior engineers.",
     RED),
    ("KNOWLEDGE SILOS",
     "FIX expertise locked in 1-2 individuals.\nWhen they leave, the knowledge leaves with them.",
     AMBER),
    ("COSTLY DOWNTIME",
     "Every FIX outage delays trading.\nClient SLA breaches damage relationships and revenue.",
     AMBER),
]

for i, (heading, body, accent) in enumerate(problems):
    col = i % 2
    row = i // 2
    x = Inches(0.75) + col * Inches(6.2)
    y = Inches(1.55) + row * Inches(2.6)
    data_card(slide, x, y, Inches(5.9), Inches(2.4),
              heading, body, accent=accent, sz_head=Pt(13), sz_body=Pt(14))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — The Solution
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "02  THE SOLUTION")
slide_header(slide, "An AI-Powered FIX Expert, Available 24/7")

txt(slide,
    "An instant, browser-based assistant giving any Fintech professional "
    "access to FIX protocol expertise on demand — regardless of experience level.",
    Inches(0.75), Inches(1.45), Inches(12.0), Inches(0.65),
    sz=Pt(15), color=GREY_LT, font=FONT_BODY)

solutions = [
    ("ASK ANYTHING",   "Natural language Q&A on any FIX concept, tag, or workflow", ORANGE),
    ("21 WORKFLOWS",   "Instant deep-dive on every workflow from Logon to Settlement", ORANGE),
    ("TROUBLESHOOT",   "Paste an error or raw FIX message — get step-by-step diagnosis", ORANGE),
    ("BUILD & VALIDATE","Construct FIX messages with live preview and AI validation", GREEN),
    ("SAVE & RECALL",  "Persistent conversation history for future reference", GREEN),
    ("ALWAYS ON",      "Cloud-hosted — accessible from anywhere, any device", GREEN),
]

for i, (heading, body, accent) in enumerate(solutions):
    col = i % 3
    row = i // 3
    x = Inches(0.75) + col * Inches(4.15)
    y = Inches(2.3) + row * Inches(2.35)
    data_card(slide, x, y, Inches(3.9), Inches(2.1),
              heading, body, accent=accent, sz_head=Pt(12), sz_body=Pt(13))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Key Features
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "03  KEY FEATURES")
slide_header(slide, "4 Core Capabilities")

features = [
    ("01  LEARN MODE",
     "Chat interface powered by Claude AI.\n"
     "Ask about any FIX tag, message type, or concept.\n"
     "Answers include FIXimate tag numbers and examples.",
     ORANGE),
    ("02  TROUBLESHOOT",
     "Select error category + FIX version.\n"
     "Paste raw FIX message or error text.\n"
     "AI returns root cause and resolution steps.",
     RED),
    ("03  MSG BUILDER",
     "Select MsgType, fill SenderCompID/TargetCompID.\n"
     "Add custom tags — live Tag=Value preview.\n"
     "AI validates required fields and structure.",
     GREEN),
    ("04  WORKFLOW SIDEBAR",
     "All 21 FIX workflows grouped by phase.\n"
     "One click = detailed workflow explanation.\n"
     "Covers Session, Pre-Trade, Trade, Post-Trade, Ops.",
     AMBER),
]

col_w = Inches(2.9)
for i, (heading, body, accent) in enumerate(features):
    x = Inches(0.7) + i * Inches(3.05)
    # Tall card
    rect(slide, x, Inches(1.5), col_w, Inches(5.55), fill=BG_PANEL, line=GREY_DK)
    rect(slide, x, Inches(1.5), col_w, Inches(0.06), fill=accent)        # top accent bar
    rect(slide, x, Inches(1.5), Inches(0.05), Inches(5.55), fill=accent) # left stripe
    txt(slide, heading,
        x + Inches(0.12), Inches(1.65), col_w - Inches(0.2), Inches(0.55),
        sz=Pt(13), bold=True, color=accent, font=FONT_TITLE)
    txt(slide, body,
        x + Inches(0.12), Inches(2.3), col_w - Inches(0.2), Inches(4.5),
        sz=Pt(13), color=GREY_LT, font=FONT_BODY, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Business Value / ROI
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "04  BUSINESS VALUE")
slide_header(slide, "ROI: 2,900%  —  Payback in Under 2 Weeks")

metrics = [
    ("$18,000",  "Annual savings\nin engineer hours", GREEN),
    ("<$700",    "Total Year 1\ncost",                AMBER),
    ("2,900%",   "Return on\ninvestment",             ORANGE),
    ("2 WEEKS",  "Payback\nperiod",                   ORANGE),
]
for i, (num, label, col) in enumerate(metrics):
    x = Inches(0.75) + i * Inches(3.05)
    stat_box(slide, x, Inches(1.5), Inches(2.8), Inches(1.7), num, label, num_color=col)

# Outcomes table
txt(slide, "KEY OUTCOMES",
    Inches(0.75), Inches(3.45), Inches(5.0), Inches(0.38),
    sz=Pt(12), bold=True, color=ORANGE, font=FONT_TITLE)

outcomes = [
    ("MTTR per FIX incident",     "3 hrs",       "< 1 hr"),
    ("Escalation rate",           "10/month",    "< 6/month"),
    ("Tag lookup time",           "45 mins",     "< 5 mins"),
    ("New hire productivity",     "3 months",    "4 weeks"),
    ("Client SLA resolution",     "4 hrs",       "1 hr"),
    ("Trading downtime / month",  "2 hrs",       "< 30 mins"),
]

# Header row
rect(slide, Inches(0.75), Inches(3.9), Inches(11.8), Inches(0.38), fill=BG_RAISED)
txt(slide, "METRIC",        Inches(0.85), Inches(3.92), Inches(5.0), Inches(0.34),
    sz=Pt(10), bold=True, color=ORANGE, font=FONT_TITLE)
txt(slide, "BEFORE",        Inches(6.0),  Inches(3.92), Inches(2.5), Inches(0.34),
    sz=Pt(10), bold=True, color=RED,    font=FONT_TITLE)
txt(slide, "AFTER",         Inches(9.0),  Inches(3.92), Inches(2.5), Inches(0.34),
    sz=Pt(10), bold=True, color=GREEN,  font=FONT_TITLE)

for i, (metric, before, after) in enumerate(outcomes):
    y = Inches(4.3) + i * Inches(0.48)
    bg = BG_PANEL if i % 2 == 0 else BG_RAISED
    rect(slide, Inches(0.75), y, Inches(11.8), Inches(0.46), fill=bg)
    txt(slide, metric, Inches(0.85), y + Inches(0.06), Inches(5.0), Inches(0.36),
        sz=Pt(12), color=GREY_LT, font=FONT_BODY)
    txt(slide, before, Inches(6.0),  y + Inches(0.06), Inches(2.5), Inches(0.36),
        sz=Pt(12), bold=True, color=RED,   font=FONT_TITLE)
    txt(slide, after,  Inches(9.0),  y + Inches(0.06), Inches(2.5), Inches(0.36),
        sz=Pt(12), bold=True, color=GREEN, font=FONT_TITLE)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — RICE Roadmap
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "05  FEATURE ROADMAP")
slide_header(slide, "RICE-Prioritised Enhancement Backlog")

txt(slide, "RICE = (Reach x Impact x Confidence) / Effort",
    Inches(0.75), Inches(1.45), Inches(10.0), Inches(0.4),
    sz=Pt(13), italic=True, color=GREY_MID, font=FONT_BODY)

headers   = ["FEATURE",                "REACH", "IMPACT", "CONF", "EFFORT", "RICE", "OUTCOME"]
col_xs    = [Inches(0.75), Inches(5.1), Inches(6.3), Inches(7.4), Inches(8.45), Inches(9.55), Inches(10.75)]
col_ws    = [Inches(4.25), Inches(1.1), Inches(1.0), Inches(0.95), Inches(1.0), Inches(1.1), Inches(1.9)]

# Header row
rect(slide, Inches(0.75), Inches(1.95), Inches(12.3), Inches(0.4), fill=BG_RAISED)
for h, x, w in zip(headers, col_xs, col_ws):
    c = ORANGE if h in ("RICE",) else GREY_MID
    txt(slide, h, x + Inches(0.05), Inches(1.97), w, Inches(0.36),
        sz=Pt(10), bold=True, color=c, font=FONT_TITLE)

rows = [
    ("FIX Tag Search",             "50", "2", "100%", "0.5", "200", "LEARN"),
    ("Error Code Reference",       "40", "2", "100%", "0.5", "160", "MTTR"),
    ("Saved Message Templates",    "30", "2", "100%", "0.5", "120", "MTTR"),
    ("FIX Message Log Parser",     "40", "3",  "80%", "1.0",  "96", "MTTR"),
    ("Sequence No. Calculator",    "20", "3",  "80%", "0.5",  "96", "MTTR"),
    ("Export Chat to PDF",         "30", "1", "100%", "0.5",  "60", "CLIENT"),
    ("User Authentication",        "50", "2",  "80%", "2.0",  "40", "ADOPT"),
    ("FIX Version Comparison",     "25", "2",  "80%", "1.0",  "40", "LEARN"),
]

RICE_COLOR = {
    "200": ORANGE, "160": ORANGE, "120": AMBER,
    "96":  AMBER,  "60":  GREY_MID, "40": GREY_MID,
}
OUTCOME_COLOR = {
    "LEARN": ORANGE, "MTTR": GREEN, "CLIENT": AMBER, "ADOPT": RGBColor(0x42, 0x85, 0xF4),
}

for i, row_data in enumerate(rows):
    y = Inches(2.37) + i * Inches(0.59)
    bg = BG_PANEL if i % 2 == 0 else BG_RAISED
    rect(slide, Inches(0.75), y, Inches(12.3), Inches(0.57), fill=bg)
    for j, (val, x, w) in enumerate(zip(row_data, col_xs, col_ws)):
        if j == 5:       c = RICE_COLOR.get(val, GREY_LT)
        elif j == 6:     c = OUTCOME_COLOR.get(val, GREY_LT)
        else:            c = GREY_LT
        bold = j in (0, 5, 6)
        txt(slide, val, x + Inches(0.05), y + Inches(0.09), w, Inches(0.4),
            sz=Pt(11), bold=bold, color=c, font=FONT_TITLE if j in (5, 6) else FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Architecture
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "06  ARCHITECTURE")
slide_header(slide, "Tech Stack & Deployment")

layers = [
    ("USER",       "Browser (Chrome / Edge)",           "HTML5  |  CSS3  |  Vanilla JS  |  Marked.js",        ORANGE),
    ("BACKEND",    "Flask 3.1  (Python 3.12)",          "REST API  |  SSE Streaming  |  SQLite history",       GREEN),
    ("AI ENGINE",  "Anthropic  claude-haiku-4-5",       "FIX system prompt  |  4,096 token responses  |  Streaming", AMBER),
    ("HOSTING",    "Render.com  (Cloud)",               "Auto-deploy from GitHub  |  Free tier  |  HTTPS",     RGBColor(0x42, 0x85, 0xF4)),
    ("SOURCE",     "GitHub",                            "github.com/ken-jiang-claude/fix-protocol-tool",        GREY_MID),
]

for i, (layer, title, detail, accent) in enumerate(layers):
    y = Inches(1.55) + i * Inches(1.1)
    # Layer badge
    rect(slide, Inches(0.75), y, Inches(1.55), Inches(0.9), fill=accent)
    txt(slide, layer,
        Inches(0.75), y, Inches(1.55), Inches(0.9),
        sz=Pt(11), bold=True, color=BG_BLACK, align=PP_ALIGN.CENTER, font=FONT_TITLE)
    # Content row
    rect(slide, Inches(2.4), y, Inches(10.65), Inches(0.9), fill=BG_PANEL, line=GREY_DK)
    rect(slide, Inches(2.4), y, Inches(0.05), Inches(0.9), fill=accent)
    txt(slide, title,
        Inches(2.6), y + Inches(0.06), Inches(6.0), Inches(0.42),
        sz=Pt(15), bold=True, color=WHITE, font=FONT_TITLE)
    txt(slide, detail,
        Inches(2.6), y + Inches(0.5), Inches(10.3), Inches(0.35),
        sz=Pt(12), color=GREY_MID, font=FONT_BODY)
    if i < len(layers) - 1:
        txt(slide, "▼",
            Inches(1.15), y + Inches(0.9), Inches(0.75), Inches(0.22),
            sz=Pt(9), color=GREY_DK, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — PM Governance
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "PROJECT GOVERNANCE")
slide_header(slide, "End-to-End Project Management")

items = [
    ("Business Justification", "Problem, solution, stakeholders, strategic alignment"),
    ("ROI & Outcomes",         "2,900% ROI  |  KPIs across People, Process, Business"),
    ("RACI Matrix",            "6 roles  |  30 activities  |  clear accountability"),
    ("Definition of Ready",    "12 criteria to qualify a story for development"),
    ("Definition of Done",     "16 criteria across code, testing, deploy, docs"),
    ("Milestones",             "8 milestones  |  M1-M5 complete  |  M6-M8 planned"),
    ("RICE Prioritisation",    "14 features scored  |  outcome-tagged  |  sprint-mapped"),
    ("Testing Plan",           "Unit  |  Integration  |  E2E  |  Performance  |  Security"),
    ("SDLC",                   "6-phase Agile model  |  tech stack rationale"),
    ("Gantt Chart",            "Full timeline  |  renders as diagram on GitHub"),
]

for i, (title, desc) in enumerate(items):
    col = i % 2
    row = i // 2
    x = Inches(0.75) + col * Inches(6.2)
    y = Inches(1.55) + row * Inches(1.12)
    rect(slide, x, y, Inches(5.9), Inches(1.0), fill=BG_PANEL, line=GREY_DK)
    rect(slide, x, y, Inches(0.05), Inches(1.0), fill=ORANGE)
    txt(slide, title,
        x + Inches(0.15), y + Inches(0.07), Inches(5.6), Inches(0.38),
        sz=Pt(13), bold=True, color=WHITE, font=FONT_TITLE)
    txt(slide, desc,
        x + Inches(0.15), y + Inches(0.5), Inches(5.6), Inches(0.42),
        sz=Pt(11), color=GREY_MID, font=FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Live Demo
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()
section_tag(slide, "07  LIVE DEMO")
slide_header(slide, "See It In Action")

demo_steps = [
    ("01", "Open the app",        "https://fix-protocol-tool.onrender.com"),
    ("02", "Ask a FIX question",  '"What are the required tags in a NewOrderSingle?"'),
    ("03", "Click a workflow",    "Click 07 Single Order in the sidebar"),
    ("04", "Try Troubleshoot",    "Switch mode  ->  paste a FIX rejection message"),
    ("05", "Use the Builder",     "Open Builder  ->  select MsgType=D  ->  validate"),
]

for i, (step, action, detail) in enumerate(demo_steps):
    y = Inches(1.55) + i * Inches(1.12)
    # Step badge
    rect(slide, Inches(0.75), y, Inches(0.95), Inches(1.0), fill=ORANGE)
    txt(slide, f"STEP\n{step}",
        Inches(0.75), y + Inches(0.1), Inches(0.95), Inches(0.8),
        sz=Pt(13), bold=True, color=BG_BLACK, align=PP_ALIGN.CENTER, font=FONT_TITLE)
    # Content
    rect(slide, Inches(1.8), y, Inches(11.25), Inches(1.0), fill=BG_PANEL, line=GREY_DK)
    rect(slide, Inches(1.8), y, Inches(0.05), Inches(1.0), fill=GREY_DK)
    txt(slide, action,
        Inches(1.95), y + Inches(0.07), Inches(6.0), Inches(0.42),
        sz=Pt(15), bold=True, color=WHITE, font=FONT_TITLE)
    txt(slide, detail,
        Inches(1.95), y + Inches(0.52), Inches(10.8), Inches(0.38),
        sz=Pt(12), italic=True, color=ORANGE, font=FONT_BODY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Thank You
# ═══════════════════════════════════════════════════════════════════════════
slide = base_slide()

# Right dark panel
rect(slide, Inches(8.8), 0, Inches(4.53), H, fill=BG_RAISED)
rect(slide, Inches(8.8), 0, Inches(0.04), H, fill=ORANGE)

txt(slide, "THANK YOU",
    Inches(0.65), Inches(1.6), Inches(7.8), Inches(1.5),
    sz=Pt(58), bold=True, color=WHITE, font=FONT_TITLE)
rect(slide, Inches(0.65), Inches(3.25), Inches(5.0), Inches(0.05), fill=ORANGE)

links = [
    ("LIVE APP",     "fix-protocol-tool.onrender.com"),
    ("GITHUB",       "github.com/ken-jiang-claude/fix-protocol-tool"),
    ("USER MANUAL",  "ReadMe.md  (in repository)"),
    ("PM DOC",       "PROJECT_MANAGEMENT.md  (in repository)"),
]
for i, (label, val) in enumerate(links):
    y = Inches(3.55) + i * Inches(0.75)
    txt(slide, label + ":",
        Inches(0.65), y, Inches(2.3), Inches(0.55),
        sz=Pt(12), bold=True, color=ORANGE, font=FONT_TITLE)
    txt(slide, val,
        Inches(3.1), y, Inches(5.3), Inches(0.55),
        sz=Pt(12), italic=True, color=GREY_LT, font=FONT_BODY)

txt(slide, "Ken Jiang  |  April 2026",
    Inches(0.65), Inches(6.6), Inches(7.0), Inches(0.45),
    sz=Pt(12), color=GREY_MID, font=FONT_BODY)

txt(slide, "QUESTIONS?",
    Inches(9.0), Inches(2.8), Inches(3.8), Inches(0.75),
    sz=Pt(32), bold=True, color=WHITE, align=PP_ALIGN.CENTER, font=FONT_TITLE)
txt(slide, "Let's discuss",
    Inches(9.0), Inches(3.6), Inches(3.8), Inches(0.5),
    sz=Pt(18), italic=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_BODY)


# ── Save ─────────────────────────────────────────────────────────────────────
output = r"c:\Users\Taikary Jiang\FIX Protocol\FIX_Protocol_Tool_Deck.pptx"
prs.save(output)
print(f"Saved: {output}")
print(f"Slides: {len(prs.slides)}")
