from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import pptx.oxml.ns as nsmap
from lxml import etree
import copy

# ── Colour palette ───────────────────────────────────────────────────────────
BG       = RGBColor(0x05, 0x0A, 0x0A)
S1       = RGBColor(0x0F, 0x1A, 0x1A)
S2       = RGBColor(0x15, 0x22, 0x22)
S3       = RGBColor(0x1C, 0x2E, 0x2E)
TEAL     = RGBColor(0x2B, 0x8E, 0x8E)
TEAL_L   = RGBColor(0x3A, 0xAE, 0xAE)
TEAL_LL  = RGBColor(0x5F, 0xD0, 0xD0)
INK      = RGBColor(0xEE, 0xF7, 0xF7)
INK2     = RGBColor(0x9A, 0xBF, 0xBF)
INK3     = RGBColor(0x5A, 0x80, 0x80)
RED      = RGBColor(0xEF, 0x44, 0x44)
AMBER    = RGBColor(0xF5, 0x9E, 0x0B)
GREEN    = RGBColor(0x22, 0xC5, 0x5E)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # completely blank

# ── Helper: solid fill a shape ───────────────────────────────────────────────
def solid(shape, colour):
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = colour

# ── Helper: add rectangle ────────────────────────────────────────────────────
def rect(slide, l, t, w, h, colour, radius=0):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    solid(shape, colour)
    shape.line.fill.background()
    return shape

# ── Helper: add text box ─────────────────────────────────────────────────────
def txtbox(slide, text, l, t, w, h, size=14, bold=False, colour=INK,
           align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = colour
    run.font.italic = italic
    return txb

# ── Helper: slide background ─────────────────────────────────────────────────
def bg(slide):
    rect(slide, 0, 0, 13.33, 7.5, BG)

# ── Helper: label pill ───────────────────────────────────────────────────────
def pill_label(slide, text, l, t, w=2.2):
    r = rect(slide, l, t, w, 0.25, S3)
    txtbox(slide, text.upper(), l+0.1, t+0.03, w-0.2, 0.22,
           size=7, bold=True, colour=TEAL_L, align=PP_ALIGN.LEFT)

# ── Helper: teal accent bar (left edge) ─────────────────────────────────────
def accent_bar(slide, t, h):
    rect(slide, 0, t, 0.06, h, TEAL)

# ── Helper: icon circle ──────────────────────────────────────────────────────
def icon_circle(slide, emoji, l, t, size=0.45):
    r = rect(slide, l, t, size, size, S3)
    txtbox(slide, emoji, l, t, size, size, size=16, align=PP_ALIGN.CENTER)

# ── Helper: numbered circle ──────────────────────────────────────────────────
def num_circle(slide, num, l, t, size=0.42):
    r = rect(slide, l, t, size, size, S2)
    txtbox(slide, str(num), l, t+0.03, size, size-0.06,
           size=12, bold=True, colour=TEAL_L, align=PP_ALIGN.CENTER)

# ── Helper: teal divider line ────────────────────────────────────────────────
def divider(slide, l, t, w):
    r = rect(slide, l, t, w, 0.01, TEAL)

# ── Helper: card background ─────────────────────────────────────────────────
def card_bg(slide, l, t, w, h, colour=S1, border=False):
    r = rect(slide, l, t, w, h, colour)
    if border:
        r.line.color.rgb = S3
        r.line.width = Pt(0.75)
    else:
        r.line.fill.background()
    return r

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════
def slide_cover():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)

    # Left gradient panel
    rect(slide, 0, 0, 7.5, 7.5, S1)
    # teal glow strip
    rect(slide, 0, 0, 0.08, 7.5, TEAL)

    # Right abstract grid (simulated with teal rect overlay)
    rect(slide, 7.5, 0, 5.83, 7.5, BG)

    # Subtle teal accent blocks (right side visual texture)
    for i, (y, alpha_h) in enumerate([(0.4, 1.2),(2.0, 0.6),(4.5, 0.9),(6.0, 0.4)]):
        r = rect(slide, 9.5 + i*0.3, y, 0.04, alpha_h, TEAL_L)
    for i, (x, y, w2, h2) in enumerate([
        (8.2, 1.0, 2.5, 0.008), (8.2, 2.5, 3.5, 0.008),
        (8.2, 4.0, 2.0, 0.008), (8.2, 5.5, 3.0, 0.008),
    ]):
        rect(slide, x, y, w2, h2, S3)

    # Logo mark
    r = rect(slide, 0.55, 0.55, 0.7, 0.7, TEAL)
    txtbox(slide, "VS", 0.55, 0.55, 0.7, 0.7, size=14, bold=True, colour=WHITE,
           align=PP_ALIGN.CENTER)
    txtbox(slide, "VELA SYNC", 1.35, 0.65, 2.5, 0.4, size=8, bold=True,
           colour=INK, align=PP_ALIGN.LEFT)

    # Eyebrow tag
    pill_label(slide, "Internal Operations · Confidential", 0.55, 1.5, 3.6)

    # Main title
    txtbox(slide, "The Complete", 0.55, 1.9, 6.5, 0.85, size=44, bold=True, colour=INK)
    txtbox(slide, "Sales Process.", 0.55, 2.65, 6.5, 1.1, size=52, bold=True, colour=TEAL_L)

    # Subtitle
    txtbox(slide,
           "8 stages · zero ambiguity · one system to close every room.",
           0.55, 3.75, 6.2, 0.5, size=12, colour=INK2, italic=True)

    # Divider
    divider(slide, 0.55, 4.4, 5.5)

    # Stats row
    stats = [("8", "Process Stages"), ("£450", "Entry Package"), ("24h", "Live After Close"), ("77%", "SMEs Without Web Strategy")]
    for i, (val, lbl) in enumerate(stats):
        x = 0.55 + i * 1.7
        txtbox(slide, val, x, 4.6, 1.5, 0.55, size=22, bold=True, colour=TEAL_L)
        txtbox(slide, lbl, x, 5.15, 1.55, 0.4, size=7, colour=INK3)

    # Right side — visual diagram hint
    txtbox(slide, "01 → 02 → 03 → 04 → 05 → 06",
           8.0, 3.3, 5.0, 0.4, size=10, bold=True, colour=TEAL, align=PP_ALIGN.CENTER)
    stages_r = ["Onboarding","Pre-Meeting","Discovery","Reveal & Pitch","Objection & Close","Post-Close"]
    for i, s in enumerate(stages_r):
        y = 3.85 + i * 0.48
        r2 = rect(slide, 8.5, y, 4.3, 0.35, S2)
        txtbox(slide, f"0{i+1}  {s}", 8.65, y+0.05, 4.0, 0.28, size=9,
               colour=INK2 if i > 0 else INK, bold=(i == 0))

slide_cover()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — PIPELINE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
def slide_pipeline():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    txtbox(slide, "PIPELINE AT A GLANCE", 0.45, 0.3, 4.0, 0.3,
           size=8, bold=True, colour=TEAL_L)
    txtbox(slide, "Full Process Flow", 0.45, 0.55, 8.0, 0.7,
           size=32, bold=True, colour=INK)

    divider(slide, 0.45, 1.3, 12.4)

    stages = [
        ("01", "Advisor\nOnboarding",    "🎓", "Foundation"),
        ("📅", "Weekly\nCadence",         "📅", "Rhythm"),
        ("02", "Pre-Meeting\nResearch",   "🔍", "Prep"),
        ("03", "Discovery\nCall",          "🎯", "Qualify"),
        ("04", "Reveal\n& Pitch",          "👁️", "Present"),
        ("05", "Objection\n& Close",       "🤝", "Convert"),
        ("£",  "Pricing\nStructure",       "💷", "Sell"),
        ("06", "Post-Close\n& Payment",    "✅", "Complete"),
    ]

    box_w = 1.42
    box_h = 1.8
    start_x = 0.45
    y = 1.55

    for i, (num, label, icon, tag) in enumerate(stages):
        x = start_x + i * 1.6

        # Card
        col = S2 if i % 2 == 0 else S1
        card_bg(slide, x, y, box_w, box_h, colour=col, border=True)

        # Top accent line for active ones
        rect(slide, x, y, box_w, 0.04, TEAL if num.isdigit() else TEAL_L)

        # Stage number / icon
        txtbox(slide, num, x, y+0.1, box_w, 0.45, size=18, bold=True,
               colour=TEAL_L, align=PP_ALIGN.CENTER)

        # Emoji icon
        txtbox(slide, icon, x, y+0.5, box_w, 0.4, size=18,
               align=PP_ALIGN.CENTER)

        # Label
        txtbox(slide, label, x, y+0.88, box_w, 0.6, size=9.5, bold=True,
               colour=INK, align=PP_ALIGN.CENTER)

        # Tag
        txtbox(slide, tag.upper(), x, y+1.52, box_w, 0.22, size=6.5,
               colour=TEAL, align=PP_ALIGN.CENTER)

        # Arrow connector (not after last)
        if i < len(stages) - 1:
            rect(slide, x + box_w, y + box_h/2 - 0.01, 0.18, 0.02, TEAL)
            # Arrow head
            txtbox(slide, "›", x + box_w + 0.1, y + box_h/2 - 0.15,
                   0.2, 0.3, size=14, colour=TEAL, align=PP_ALIGN.CENTER)

    # Bottom stat bar
    rect(slide, 0, 6.3, 13.33, 1.2, S1)
    kpis = [("500+", "Calls / week per advisor"),
            ("5+",   "Closes / week minimum"),
            ("24h",  "From close to live website"),
            ("£450", "Entry package · no contract")]
    for i, (v, l) in enumerate(kpis):
        x = 1.2 + i * 3.0
        txtbox(slide, v, x, 6.45, 2.5, 0.52, size=24, bold=True,
               colour=TEAL_L, align=PP_ALIGN.CENTER)
        txtbox(slide, l, x, 6.95, 2.5, 0.35, size=8, colour=INK3,
               align=PP_ALIGN.CENTER)

slide_pipeline()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — ONBOARDING
# ═══════════════════════════════════════════════════════════════════════════
def slide_onboarding():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 01 · Foundation", 0.45, 0.28)
    txtbox(slide, "Advisor Onboarding", 0.45, 0.55, 8.0, 0.7,
           size=34, bold=True, colour=INK)
    txtbox(slide, "Know the product. Know the tools. Know the numbers. Master these before you speak to anyone.",
           0.45, 1.2, 9.0, 0.4, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.4)

    # 3 pillars
    pillars = [
        ("🎓", "Product Mastery", "Know every package & price cold.\n£450 / £650 setup · £50 / £100 /mo"),
        ("🔧", "Tools & Assets",  "Lead list · Demo site · Scripts\nObjection guides · CRM access"),
        ("📞", "Targets & KPIs",  "500 outbound calls / week\n5 closed sales / week minimum"),
    ]
    for i, (ico, title, body) in enumerate(pillars):
        x = 0.45 + i * 4.2
        card_bg(slide, x, 1.85, 3.9, 1.6, colour=S2, border=True)
        rect(slide, x, 1.85, 3.9, 0.05, TEAL)
        txtbox(slide, ico, x+0.15, 1.95, 0.5, 0.45, size=20)
        txtbox(slide, title, x+0.75, 2.0, 3.0, 0.35, size=12, bold=True, colour=INK)
        txtbox(slide, body, x+0.15, 2.38, 3.6, 0.9, size=9, colour=INK2)

    # 6 rules
    txtbox(slide, "THE SIX RULES", 0.45, 3.6, 4.0, 0.3, size=8, bold=True, colour=TEAL_L)
    rules = [
        ("🎯", "You are the expert. Act like it.", "Confidence is not optional."),
        ("🔇", "Silence is a weapon.",             "After every powerful close — stop talking."),
        ("🩺", "Diagnose before you prescribe.",   "Ask before you pitch. Always."),
        ("📊", "Speak in outcomes, not features.", "They care about customers, not animations."),
        ("🏦", "Frame everything as ROI.",         "Every price is an investment."),
        ("🪝", "Show, don't tell.",                "Open the draft site silently. Let them sell themselves."),
    ]
    cols = [(0.45, 3.95), (4.55, 3.95), (8.65, 3.95),
            (0.45, 5.4),  (4.55, 5.4),  (8.65, 5.4)]
    for i, (rule, (x, y)) in enumerate(zip(rules, cols)):
        ico, title, sub = rule
        card_bg(slide, x, y, 3.8, 1.3, colour=S1, border=True)
        txtbox(slide, ico, x+0.12, y+0.15, 0.45, 0.45, size=16)
        txtbox(slide, title, x+0.65, y+0.12, 3.0, 0.38, size=9.5, bold=True, colour=INK)
        txtbox(slide, sub, x+0.65, y+0.5, 3.0, 0.55, size=8.5, colour=INK2)

slide_onboarding()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — WEEKLY CADENCE
# ═══════════════════════════════════════════════════════════════════════════
def slide_cadence():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Team Cadence · Weekly Rhythm", 0.45, 0.28)
    txtbox(slide, "Weekly Schedule", 0.45, 0.55, 9.0, 0.7, size=34, bold=True, colour=INK)
    divider(slide, 0.45, 1.28, 12.4)

    days = [
        ("MON",   TEAL,   [("11:00 AM", "Diary Alignment"), ("5:00 PM", "KPI Review")]),
        ("TUE",   S2,     [("5:00 PM",  "Daily Touch Point")]),
        ("WED",   S2,     [("5:00 PM",  "Daily Touch Point")]),
        ("THU",   TEAL_L, [("5:00 PM",  "Weekly Forward Planning"), ("5:00 PM", "Daily Touch Point")]),
        ("FRI",   S2,     [("5:00 PM",  "Daily Touch Point")]),
    ]

    day_w = 2.38
    for i, (day, accent, events) in enumerate(days):
        x = 0.45 + i * 2.55
        is_highlight = accent != S2
        col = S2 if is_highlight else S1
        card_bg(slide, x, 1.45, day_w, 3.9, colour=col, border=True)
        rect(slide, x, 1.45, day_w, 0.06, accent)
        txtbox(slide, day, x+0.1, 1.55, day_w-0.2, 0.32, size=10, bold=True,
               colour=TEAL_L if is_highlight else INK3)

        for j, (time, label) in enumerate(events):
            ey = 1.95 + j * 1.4
            r2 = rect(slide, x+0.12, ey, day_w-0.24, 1.2, S3)
            txtbox(slide, time, x+0.2, ey+0.1, day_w-0.4, 0.28, size=8,
                   bold=True, colour=TEAL_L)
            txtbox(slide, label, x+0.2, ey+0.38, day_w-0.4, 0.55, size=9,
                   bold=True, colour=INK)

    # Recurring commitments
    txtbox(slide, "RECURRING COMMITMENTS", 0.45, 5.5, 5.0, 0.28, size=8,
           bold=True, colour=TEAL_L)
    recurring = [
        ("🔴", "24/7", "MD Direct Line"),
        ("🎯", "2W",   "Bi-Weekly 1:1s"),
        ("📋", "1Y",   "Personal Dev Plan"),
    ]
    for i, (ico, freq, lbl) in enumerate(recurring):
        x = 0.45 + i * 4.2
        card_bg(slide, x, 5.82, 3.9, 1.35, colour=S1, border=True)
        txtbox(slide, ico, x+0.15, 5.92, 0.5, 0.45, size=18)
        txtbox(slide, freq, x+0.75, 5.9, 1.0, 0.4, size=16, bold=True, colour=TEAL_L)
        txtbox(slide, lbl, x+0.75, 6.3, 2.8, 0.35, size=9, colour=INK2)

slide_cadence()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — KPI FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════
def slide_kpi():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Team Cadence · KPI Framework", 0.45, 0.28)
    txtbox(slide, "What Gets Measured, Gets Managed", 0.45, 0.55, 10.0, 0.7,
           size=30, bold=True, colour=INK)
    divider(slide, 0.45, 1.28, 12.4)

    kpis = [
        ("📞", "Outbound Calls",       "500+ / week",        "Core KPI",      "The non-negotiable foundation."),
        ("📈", "Conversion Rate",      "5+ closes / week",   "Core KPI",      "Tracks pitch quality & close technique."),
        ("⏱️", "Time on the Phone",    "Maximise daily",     "Core KPI",      "Low talk time = too many hang-ups."),
        ("💰", "Revenue Generated",    "Weekly & monthly",   "Revenue KPI",   "Setup fees + first month recurring."),
        ("🏷️", "Average Deal Value",   "£450 – £650 target", "Revenue KPI",   "Tracks upsell to SEO package."),
        ("🔄", "Follow-Up Rate",       "100% warm leads",    "Pipeline KPI",  "No warm lead should go cold."),
        ("📊", "Pipeline Value (WTD)", "Reviewed Thursday",  "Pipeline KPI",  "Is the weekly close target reachable?"),
        ("🔁", "Monthly Retention",    "Maximise",           "Retention KPI", "Validates value delivered post-close."),
    ]

    cols = 4
    card_w = 3.0
    card_h = 1.35
    gap = 0.2
    total_w = cols * card_w + (cols-1) * gap
    start_x = (13.33 - total_w) / 2

    for i, (ico, name, target, tag, note) in enumerate(kpis):
        col_i = i % cols
        row_i = i // cols
        x = start_x + col_i * (card_w + gap)
        y = 1.5 + row_i * (card_h + 0.18)

        card_bg(slide, x, y, card_w, card_h, colour=S1, border=True)
        rect(slide, x, y, card_w, 0.04, TEAL)

        txtbox(slide, ico, x+0.12, y+0.1, 0.4, 0.4, size=14)
        txtbox(slide, tag.upper(), x+0.6, y+0.1, 2.2, 0.22, size=6.5, colour=TEAL)
        txtbox(slide, name, x+0.12, y+0.5, card_w-0.24, 0.32, size=9.5,
               bold=True, colour=INK)
        txtbox(slide, target, x+0.12, y+0.82, card_w-0.24, 0.28, size=9,
               bold=True, colour=TEAL_L)
        txtbox(slide, note, x+0.12, y+1.05, card_w-0.24, 0.24, size=7.5, colour=INK3)

slide_kpi()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — PRE-MEETING RESEARCH
# ═══════════════════════════════════════════════════════════════════════════
def slide_premeet():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 02 · Preparation", 0.45, 0.28)
    txtbox(slide, "Pre-Meeting Research", 0.45, 0.55, 8.0, 0.7,
           size=34, bold=True, colour=INK)
    txtbox(slide, "10 minutes before every meeting. Walk in knowing their problem before they've said a word.",
           0.45, 1.22, 9.5, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.4)

    steps = [
        ("🔍", "01", "Google Them",        "Search the business name. What comes up? Do they rank? Do they appear at all?"),
        ("🌐", "02", "Check Their Site",   "If they have one — is it mobile-friendly? Fast? Does it convert, or is it a liability?"),
        ("⭐", "03", "Google Maps Rating", "Low score = reputation problem. No reviews = visibility problem. You solve both."),
        ("⚔️", "04", "Competitor Audit",   "Find their top 3 local competitors. Check their presence. Use this to create urgency."),
    ]

    card_w = 2.9
    for i, (ico, num, title, body) in enumerate(steps):
        x = 0.45 + i * 3.1
        card_bg(slide, x, 1.85, card_w, 2.8, colour=S2, border=True)
        rect(slide, x, 1.85, card_w, 0.05, TEAL)

        txtbox(slide, ico, x+0.2, 2.0, 0.6, 0.55, size=24)
        txtbox(slide, num, x+card_w-0.7, 2.05, 0.55, 0.4, size=20,
               bold=True, colour=RGBColor(0x2B, 0x8E, 0x8E), align=PP_ALIGN.RIGHT)
        txtbox(slide, title, x+0.2, 2.58, card_w-0.4, 0.38, size=12, bold=True, colour=INK)
        txtbox(slide, body, x+0.2, 3.0, card_w-0.4, 1.5, size=9.5, colour=INK2)

    # Opening line script
    rect(slide, 0.45, 4.85, 12.43, 1.35, S1)
    rect(slide, 0.45, 4.85, 0.05, 1.35, TEAL)
    txtbox(slide, "OPENING LINE", 0.6, 4.93, 3.0, 0.25, size=7, bold=True, colour=TEAL_L)
    txtbox(slide,
           '"I had a look at your business before coming in today. I noticed a few things I wanted to talk to you about — '
           'but first, tell me how business has been. Are you getting as many new customers as you want?"',
           0.6, 5.18, 12.1, 0.9, size=10, colour=INK2, italic=True)

    # Warning
    rect(slide, 0.45, 6.35, 12.43, 0.9, RGBColor(0x2a, 0x0d, 0x0d))
    rect(slide, 0.45, 6.35, 0.05, 0.9, RED)
    txtbox(slide, "⛔  Never open with the product. Open with their world — not yours. The product comes third.",
           0.6, 6.5, 12.0, 0.6, size=10, colour=RGBColor(0xF8, 0x71, 0x71))

slide_premeet()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — DISCOVERY QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════
def slide_discovery():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 03 · Qualification", 0.45, 0.28)
    txtbox(slide, "6 Discovery Questions", 0.45, 0.55, 9.0, 0.7,
           size=34, bold=True, colour=INK)
    txtbox(slide, "Ask in sequence · Listen deeply · Take notes visibly. Their answers give you everything you need to close.",
           0.45, 1.22, 11.0, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.4)

    qs = [
        ("1", "Current State",      '"When a potential customer Googles you right now — what do they find?"',        "Forces them to confront their digital reality."),
        ("2", "Awareness",          '"How are most of your customers finding you at the moment?"',                   "Exposes over-reliance on referrals or word-of-mouth."),
        ("3", "Competition",        '"Have you looked at what your top three competitors are doing online recently?"', "Creates competitive anxiety and urgency."),
        ("4", "Revenue Impact",     '"76% of people research online before making contact — what does that mean for customers you\'re missing?"', "Forces them to calculate lost revenue themselves."),
        ("5", "Previous Experience",'"Have you ever tried to get a website built before? What happened?"',           "Surfaces their war story. Positions you as the antidote."),
        ("6", "Future Vision ★",   '"If your digital presence was exactly where you wanted it — what would that look like?"', "Most powerful question. Gets them to paint their own success picture."),
    ]

    card_h = 0.82
    cols = 2
    card_w = 6.0
    for i, (num, label, q, why) in enumerate(qs):
        col_i = i % 2
        row_i = i // 2
        x = 0.45 + col_i * 6.45
        y = 1.82 + row_i * (card_h + 0.12)

        is_last = i == 5
        col = RGBColor(0x15, 0x26, 0x20) if is_last else S1
        border_c = GREEN if is_last else None

        r = card_bg(slide, x, y, card_w, card_h, colour=col, border=True)
        if is_last:
            r.line.color.rgb = GREEN
        rect(slide, x, y, 0.04, card_h, TEAL_LL if is_last else TEAL)

        txtbox(slide, num, x+0.15, y+0.08, 0.32, 0.32, size=10, bold=True, colour=TEAL_L)
        txtbox(slide, label.upper(), x+0.52, y+0.08, 2.0, 0.28, size=7, bold=True,
               colour=GREEN if is_last else TEAL)
        txtbox(slide, q, x+0.15, y+0.34, card_w-0.3, 0.3, size=9, colour=INK, italic=True)
        txtbox(slide, why, x+0.15, y+0.6, card_w-0.3, 0.2, size=7.5, colour=INK3)

    # Tip
    rect(slide, 0.45, 6.32, 12.43, 0.92, RGBColor(0x1a, 0x16, 0x06))
    rect(slide, 0.45, 6.32, 0.05, 0.92, AMBER)
    txtbox(slide,
           "💡  After all six questions, feed their answers back verbatim: \"So if I've understood you correctly...\" "
           "— validates their concerns, amplifies the pain, and sets up your pitch. Never skip this step.",
           0.6, 6.45, 12.0, 0.7, size=9, colour=RGBColor(0xF5, 0xD0, 0x60))

slide_discovery()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — REVEAL & PITCH
# ═══════════════════════════════════════════════════════════════════════════
def slide_reveal():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 04 · Presentation", 0.45, 0.28)
    txtbox(slide, "The Reveal & Pitch", 0.45, 0.55, 8.0, 0.7,
           size=34, bold=True, colour=INK)
    txtbox(slide, "Bridge their pain · Show the site silently · Anchor high, land low. The emotional sale is made here.",
           0.45, 1.22, 11.0, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.4)

    # 3 steps
    steps = [
        ("🔗", "01", "Bridge the Pain",
         "Summarise their answers in one statement.\nMake them feel heard before you reveal the solution."),
        ("👁️", "02", "The Silent Show",
         "Open the draft site. Say nothing. Scroll slowly.\nWhen they lean in — that's your pivot. Sale is made here."),
        ("⚖️", "03", "Anchor High, Land Low",
         "Never open with £450. Anchor to £2,000+.\nThen reveal your number. The contrast does the selling."),
    ]
    for i, (ico, num, title, body) in enumerate(steps):
        x = 0.45 + i * 4.2
        card_bg(slide, x, 1.82, 3.9, 2.0, colour=S2, border=True)
        rect(slide, x, 1.82, 3.9, 0.06, TEAL)
        txtbox(slide, ico, x+0.18, 1.95, 0.55, 0.55, size=24)
        txtbox(slide, f"STEP {num}", x+0.82, 1.98, 2.8, 0.28, size=7, bold=True, colour=TEAL)
        txtbox(slide, title, x+0.18, 2.52, 3.55, 0.38, size=12, bold=True, colour=INK)
        txtbox(slide, body, x+0.18, 2.94, 3.55, 0.78, size=9, colour=INK2)

    # Key script snippet
    rect(slide, 0.45, 3.98, 12.43, 0.78, S1)
    rect(slide, 0.45, 3.98, 0.05, 0.78, TEAL)
    txtbox(slide, "PRICE REVEAL", 0.6, 4.05, 2.5, 0.22, size=7, bold=True, colour=TEAL_L)
    txtbox(slide,
           '"A website of this quality from a traditional agency — you\'re looking at £2,000 minimum. '
           'We charge £450. And you\'re live within 24 hours. Not a week. Not a month. Tomorrow."',
           0.6, 4.27, 12.0, 0.44, size=9.5, colour=INK, italic=True)

    # Buying signals + caution
    txtbox(slide, "BUYING SIGNALS", 0.45, 4.9, 5.0, 0.28, size=8, bold=True, colour=GREEN)
    signals = [
        ("✅", '"That looks really good"'),
        ("✅", "Leans toward the screen"),
        ("✅", "Asks logistics questions"),
        ("✅", '"Can you do it in our colours?"'),
        ("✅", "Looks at a colleague for approval"),
    ]
    card_bg(slide, 0.45, 5.2, 5.9, 2.05, colour=RGBColor(0x0A, 0x20, 0x12), border=True)
    for i, (ico, sig) in enumerate(signals):
        txtbox(slide, f"{ico}  {sig}", 0.65, 5.28 + i * 0.38, 5.5, 0.35,
               size=9, colour=RGBColor(0x86, 0xEF, 0xAC))

    txtbox(slide, "PROCEED WITH CAUTION", 6.55, 4.9, 6.0, 0.28, size=8,
           bold=True, colour=AMBER)
    cautions = [
        ("⚠️", "Arms crossed, leaning back"),
        ("⚠️", '"We\'d need to talk to our accountant"'),
        ("⚠️", '"We\'ll think about it"'),
        ("⚠️", "Checking their phone"),
        ("⚠️", "Repeated glances at the door"),
    ]
    card_bg(slide, 6.55, 5.2, 6.33, 2.05, colour=RGBColor(0x20, 0x18, 0x05), border=True)
    for i, (ico, cau) in enumerate(cautions):
        txtbox(slide, f"{ico}  {cau}", 6.75, 5.28 + i * 0.38, 5.9, 0.35,
               size=9, colour=RGBColor(0xFB, 0xD5, 0x82))

slide_reveal()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — OBJECTIONS & CLOSE TECHNIQUES
# ═══════════════════════════════════════════════════════════════════════════
def slide_objections():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 05 · Conversion", 0.45, 0.28)
    txtbox(slide, "Objection Handling & The Close", 0.45, 0.55, 10.0, 0.7,
           size=30, bold=True, colour=INK)
    txtbox(slide, "Every objection is a question in disguise. Acknowledge · Reframe · Advance.",
           0.45, 1.22, 10.0, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.62, 12.4)

    # Left: objections
    txtbox(slide, "COMMON OBJECTIONS", 0.45, 1.75, 6.0, 0.28, size=8, bold=True, colour=TEAL_L)
    objections = [
        ('"We already have a website."',
         "Is it ranking? Is it bringing in enquiries — or just a digital brochure?"),
        ('"£450 seems too cheap."',
         "You've just seen it. That is the quality. Enterprise engineers, zero overhead."),
        ('"We need to think about it."',
         "What specifically? Name the real objection. Then stop talking."),
        ('"We want a few quotes first."',
         "Equivalent quality starts at £2,000+. Come back — we'll beat any quote."),
        ('"We had a bad experience before."',
         '"Tell me what happened." Listen fully. Vela Sync was built because of that gap.'),
        ('"We\'re not sure about the monthly."',
         "£50/mo is insurance on a £450 asset. Easiest decision in this conversation."),
    ]
    for i, (obj, resp) in enumerate(objections):
        y = 2.08 + i * 0.82
        card_bg(slide, 0.45, y, 6.2, 0.74, colour=S1, border=True)
        rect(slide, 0.45, y, 0.04, 0.74, TEAL)
        txtbox(slide, obj, 0.6, y+0.06, 5.9, 0.26, size=9, bold=True,
               colour=INK, italic=True)
        txtbox(slide, resp, 0.6, y+0.34, 5.9, 0.34, size=8.5, colour=INK2)

    # Right: close techniques
    txtbox(slide, "CLOSE TECHNIQUES", 6.9, 1.75, 6.0, 0.28, size=8, bold=True, colour=TEAL_L)
    closes = [
        ("Assumptive Close",
         "Assumes the sale. Moves to logistics.\n\"What's the domain name you're using?\""),
        ("Investment Frame",
         "Forces them to calculate ROI.\n\"If it brings one extra customer — what's that worth?\""),
        ("Urgency Close",
         "Someone is searching for you RIGHT NOW.\n\"What's stopping us doing this today?\" — then silence."),
        ("Option Close",
         "Removes yes/no. Both options are a yes.\n\"£450 standard or £650 SEO — which feels right?\""),
        ("Instalment Close",
         "Removes the financial barrier.\n\"Get it live tomorrow, pay on a schedule that suits you.\""),
    ]
    for i, (name, desc) in enumerate(closes):
        y = 2.08 + i * 0.96
        card_bg(slide, 6.9, y, 6.0, 0.88, colour=S2, border=True)
        rect(slide, 6.9, y, 0.04, 0.88, TEAL_LL)
        txtbox(slide, name, 7.05, y+0.07, 5.7, 0.28, size=10, bold=True, colour=TEAL_L)
        txtbox(slide, desc, 7.05, y+0.36, 5.7, 0.46, size=8.5, colour=INK2)

    # Power phrases
    rect(slide, 0.45, 6.88, 12.43, 0.48, S1)
    phrases = ["\"What that means for your business is...\"", "\"The question isn't whether — it's when.\"",
               "\"This isn't a cost. It's a decision.\"", "\"Every day you wait is a day your competitor doesn't.\""]
    for i, p in enumerate(phrases):
        x = 0.6 + i * 3.1
        txtbox(slide, p, x, 6.93, 2.9, 0.38, size=7.5, colour=TEAL, italic=True)

slide_objections()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — PRICING STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════
def slide_pricing():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Pricing Structure · Know These Cold", 0.45, 0.28)
    txtbox(slide, "What You're Selling", 0.45, 0.55, 8.0, 0.7,
           size=34, bold=True, colour=INK)
    txtbox(slide, "Two packages. Two monthly tiers. The price contrast vs the market is your single most powerful tool.",
           0.45, 1.22, 11.0, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.4)

    # Standard package
    card_bg(slide, 0.45, 1.85, 5.9, 5.2, colour=S1, border=True)
    txtbox(slide, "STANDARD PACKAGE", 0.65, 2.0, 5.5, 0.28, size=8, bold=True, colour=TEAL_L)
    txtbox(slide, "£450", 0.65, 2.28, 3.5, 0.9, size=50, bold=True, colour=INK)
    txtbox(slide, "$575  ·  €525", 0.65, 3.05, 5.0, 0.3, size=10, colour=TEAL_L)
    txtbox(slide, "One-off · Live within 24 hours", 0.65, 3.3, 5.2, 0.28, size=9, colour=INK3)
    divider(slide, 0.65, 3.62, 5.4)

    std_features = [
        "Professional, mobile-responsive website",
        "Personalised to client's brand",
        "Domain activation or transfer included",
        "SSL, on-page SEO & performance optimisation",
        "Client reviews before anything goes live",
        "Full access credentials handed over on the day",
        "Instalments available",
    ]
    for i, f in enumerate(std_features):
        txtbox(slide, f"✓  {f}", 0.65, 3.75 + i * 0.3, 5.5, 0.28, size=8.5, colour=INK2)

    rect(slide, 0.65, 5.95, 5.5, 0.82, S2)
    txtbox(slide, "THEN MONTHLY", 0.8, 6.02, 3.0, 0.22, size=7, bold=True, colour=TEAL_L)
    txtbox(slide, "£50 / $65 / €58  /month — site maintenance", 0.8, 6.24, 5.2, 0.28, size=9, colour=INK)
    txtbox(slide, "Industry avg: £150+/mo   ·   Cancel any time",
           0.8, 6.52, 5.2, 0.22, size=7.5, colour=INK3)

    # SEO package (highlighted)
    rect(slide, 6.55, 1.85, 6.33, 5.2, S2)
    rect(slide, 6.55, 1.85, 6.33, 0.06, TEAL_L)
    # Best value badge
    rect(slide, 10.6, 1.92, 1.9, 0.28, TEAL)
    txtbox(slide, "BEST VALUE", 10.6, 1.94, 1.9, 0.24, size=7.5, bold=True,
           colour=WHITE, align=PP_ALIGN.CENTER)

    txtbox(slide, "SEO & GROWTH PACKAGE", 6.75, 2.0, 5.5, 0.28, size=8, bold=True, colour=TEAL_L)
    txtbox(slide, "£650", 6.75, 2.28, 4.5, 0.9, size=50, bold=True, colour=TEAL_L)
    txtbox(slide, "$825  ·  €760", 6.75, 3.05, 5.0, 0.3, size=10, colour=TEAL_L)
    txtbox(slide, "One-off · Everything in Standard, plus growth", 6.75, 3.3, 5.5, 0.28,
           size=9, colour=INK3)
    divider(slide, 6.75, 3.62, 5.7)

    seo_features = [
        "Everything in Standard Package",
        "Marketing team briefed at point of launch",
        "Live traffic strategy handed over day one",
        "Growth roadmap tailored to business goals",
        "SEO foundations built for immediate indexing",
        "ML-backed digital strategy from day one",
        "Save up to £1,550 vs average agency",
        "Instalments available",
    ]
    for i, f in enumerate(seo_features):
        txtbox(slide, f"✓  {f}", 6.75, 3.75 + i * 0.275, 5.9, 0.26, size=8.5, colour=INK2)

    rect(slide, 6.75, 5.95, 5.9, 0.82, RGBColor(0x18, 0x2E, 0x2E))
    txtbox(slide, "THEN MONTHLY", 6.9, 6.02, 3.0, 0.22, size=7, bold=True, colour=TEAL_L)
    txtbox(slide, "£100 / $130 / €117  /month — maintenance + SEO + traffic", 6.9, 6.24, 5.5, 0.28,
           size=9, colour=TEAL_L)
    txtbox(slide, "Industry avg: £300+/mo   ·   No contract, cancel any time",
           6.9, 6.52, 5.5, 0.22, size=7.5, colour=INK3)

slide_pricing()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — POST-CLOSE & PAYMENT
# ═══════════════════════════════════════════════════════════════════════════
def slide_postclose():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    accent_bar(slide, 0, 7.5)

    pill_label(slide, "Stage 06 · Completion", 0.45, 0.28)
    txtbox(slide, "Post-Close, Onboarding & Payment", 0.45, 0.55, 10.0, 0.7,
           size=28, bold=True, colour=INK)
    txtbox(slide, "The close is not the finish line. Protect the sale · trigger delivery · collect payment.",
           0.45, 1.22, 11.0, 0.38, size=10, colour=INK2, italic=True)
    divider(slide, 0.45, 1.62, 12.4)

    # Delivery process (left)
    txtbox(slide, "DELIVERY PROCESS", 0.45, 1.78, 4.0, 0.28, size=8, bold=True, colour=TEAL_L)
    delivery = [
        ("A", "Immediately", "Log sale · notify build team. 24h clock starts NOW."),
        ("B", "Same Day",    "30-min brief call — brand, copy, domain, requirements."),
        ("C", "Within 24h",  "Build complete · client reviews · site goes live."),
    ]
    for i, (ltr, timing, desc) in enumerate(delivery):
        y = 2.1 + i * 1.18
        card_bg(slide, 0.45, y, 5.9, 1.05, colour=S2, border=True)
        rect(slide, 0.45, y, 5.9, 0.04, TEAL)
        # Circle
        rect(slide, 0.55, y+0.28, 0.5, 0.5, S3)
        txtbox(slide, ltr, 0.55, y+0.3, 0.5, 0.42, size=14, bold=True,
               colour=TEAL_L, align=PP_ALIGN.CENTER)
        txtbox(slide, timing.upper(), 1.18, y+0.1, 4.8, 0.26, size=7.5, bold=True, colour=TEAL)
        txtbox(slide, desc, 1.18, y+0.38, 4.8, 0.55, size=9.5, colour=INK2)

    # Payment steps (right)
    txtbox(slide, "PAYMENT COLLECTION", 6.65, 1.78, 5.0, 0.28, size=8, bold=True, colour=TEAL_L)
    payments = [
        ("1", "At Close",    "Issue invoice immediately — package + monthly fee."),
        ("2", "Standard",    "Full payment before or on site delivery day."),
        ("3", "Instalment",  "First payment at close. Schedule confirmed in writing."),
        ("4", "Day 1 late",  "Friendly reminder — warm, not chasing."),
        ("5", "Day 3",       "Direct call — professional and easy path to yes."),
        ("6", "Day 7",       "Formal written notice. 48h final deadline."),
    ]
    for i, (num, timing, desc) in enumerate(payments):
        y = 2.1 + i * 0.77
        card_bg(slide, 6.65, y, 6.33, 0.68, colour=S1, border=True)
        rect(slide, 6.65, y, 0.04, 0.68, TEAL)
        txtbox(slide, num, 6.75, y+0.1, 0.35, 0.38, size=11, bold=True, colour=TEAL_L)
        txtbox(slide, timing.upper(), 7.18, y+0.07, 1.6, 0.22, size=7, bold=True, colour=TEAL)
        txtbox(slide, desc, 7.18, y+0.3, 5.6, 0.3, size=8.5, colour=INK2)

    # Do / Don't / If not today
    for i, (col_off, bgc, bc, icon, title, items) in enumerate([
        (0.45,  RGBColor(0x0A,0x20,0x12), GREEN, "✅", "Always Do",
         ["Invoice same day as close","Confirm payment terms in writing","Lock in brief call before you leave","Log every interaction in CRM"]),
        (4.72,  RGBColor(0x20,0x0A,0x0A), RED,   "⛔", "Never Do",
         ["Hand over site before payment","Leave without a defined next step","Accept \"call me when you're ready\"","Agree verbal-only instalment terms"]),
        (8.99,  RGBColor(0x20,0x18,0x05), AMBER, "⚠️", "If No Close Today",
         ["Lock in specific date & time","Send draft site link that evening","Send calendar invite from the car","Vague next steps die — specific ones live"]),
    ]):
        card_bg(slide, col_off, 5.62, 4.0, 1.72, colour=bgc, border=True)
        rect(slide, col_off, 5.62, 4.0, 0.04, bc)
        txtbox(slide, f"{icon}  {title}", col_off+0.15, 5.7, 3.7, 0.32,
               size=10, bold=True, colour=bc)
        for j, item in enumerate(items):
            txtbox(slide, f"• {item}", col_off+0.15, 6.06 + j * 0.3, 3.7, 0.28,
                   size=8, colour=INK2)

slide_postclose()

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 12 — CLOSING STATEMENT
# ═══════════════════════════════════════════════════════════════════════════
def slide_closing():
    slide = prs.slides.add_slide(blank_layout)
    bg(slide)
    rect(slide, 0, 0, 13.33, 7.5, S1)
    rect(slide, 0, 0, 0.08, 7.5, TEAL)

    # Decorative teal elements
    for i in range(8):
        rect(slide, 9.5 + i*0.4, 0.5 + i*0.3, 0.03, 1.0 + i*0.2, TEAL_L)

    # Logo
    r = rect(slide, 0.6, 0.6, 0.75, 0.75, TEAL)
    txtbox(slide, "VS", 0.6, 0.6, 0.75, 0.75, size=16, bold=True, colour=WHITE,
           align=PP_ALIGN.CENTER)
    txtbox(slide, "VELA SYNC", 1.5, 0.75, 3.0, 0.4, size=9, bold=True, colour=INK)

    # Main message
    txtbox(slide, "The Standard:", 0.6, 2.0, 9.0, 0.65, size=36, bold=True, colour=TEAL_L)
    txtbox(slide, "Signed. Invoiced. Brief call booked.\nSite live in 24 hours.", 0.6, 2.65, 9.5, 1.4,
           size=40, bold=True, colour=INK)

    txtbox(slide, "That is what you're selling. That is exactly what you deliver.",
           0.6, 4.2, 9.0, 0.5, size=13, colour=INK2, italic=True)

    divider(slide, 0.6, 4.85, 8.0)

    # Final stats
    final_stats = [("8", "Stages"), ("500+", "Calls/wk"), ("5+", "Closes/wk"), ("24h", "To live")]
    for i, (v, l) in enumerate(final_stats):
        x = 0.6 + i * 2.2
        txtbox(slide, v, x, 5.1, 2.0, 0.6, size=28, bold=True, colour=TEAL_L)
        txtbox(slide, l, x, 5.68, 2.0, 0.32, size=9, colour=INK3)

    # Footer
    txtbox(slide, "© 2026 Vela Sync Ltd · Co. No. 17051204 · Internal Sales Playbook — Confidential",
           0.6, 7.0, 12.0, 0.38, size=7.5, colour=INK3)

slide_closing()

# ── Save ─────────────────────────────────────────────────────────────────────
output = "/home/user/GB123/VelaSync_Sales_Process.pptx"
prs.save(output)
print(f"Saved: {output}")
