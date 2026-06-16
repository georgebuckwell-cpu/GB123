from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = RGBColor(0x05, 0x0A, 0x0A)
S1      = RGBColor(0x0F, 0x1A, 0x1A)
S2      = RGBColor(0x15, 0x22, 0x22)
S3      = RGBColor(0x1C, 0x2E, 0x2E)
TEAL    = RGBColor(0x2B, 0x8E, 0x8E)
TEAL_L  = RGBColor(0x3A, 0xAE, 0xAE)
TEAL_LL = RGBColor(0x5F, 0xD0, 0xD0)
INK     = RGBColor(0xEE, 0xF7, 0xF7)
INK2    = RGBColor(0x9A, 0xBF, 0xBF)
INK3    = RGBColor(0x5A, 0x80, 0x80)
RED     = RGBColor(0xEF, 0x44, 0x44)
AMBER   = RGBColor(0xF5, 0x9E, 0x0B)
GREEN   = RGBColor(0x22, 0xC5, 0x5E)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── Primitive helpers ─────────────────────────────────────────────────────────
def solid(shape, c):
    shape.fill.solid()
    shape.fill.fore_color.rgb = c

def rect(slide, l, t, w, h, c, border_c=None, border_pt=0.75):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    solid(s, c)
    if border_c:
        s.line.color.rgb = border_c
        s.line.width = Pt(border_pt)
    else:
        s.line.fill.background()
    return s

def txt(slide, text, l, t, w, h, size=12, bold=False, colour=INK,
        align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size   = Pt(size)
    r.font.bold   = bold
    r.font.italic = italic
    r.font.color.rgb = colour
    return tb

# ── Composite helpers ─────────────────────────────────────────────────────────
def bg(slide):
    rect(slide, 0, 0, 13.33, 7.5, BG)

def accent_bar(slide):
    rect(slide, 0, 0, 0.06, 7.5, TEAL)

def divider(slide, l, t, w):
    rect(slide, l, t, w, 0.008, TEAL)

def tag(slide, text, l, t, w=2.8):
    rect(slide, l, t, w, 0.24, S3)
    txt(slide, text.upper(), l+0.1, t+0.02, w-0.15, 0.2,
        size=6.5, bold=True, colour=TEAL_L)

def slide_header(slide, stage_tag, title, subtitle=None):
    accent_bar(slide)
    tag(slide, stage_tag, 0.45, 0.28)
    txt(slide, title, 0.45, 0.57, 12.0, 0.72, size=34, bold=True, colour=INK)
    if subtitle:
        txt(slide, subtitle, 0.45, 1.25, 11.5, 0.35,
            size=9.5, colour=INK2, italic=True)
    divider(slide, 0.45, 1.65, 12.43)

def card(slide, l, t, w, h, colour=S1, top_accent=TEAL, border_c=S3):
    rect(slide, l, t, w, h, colour, border_c=border_c)
    rect(slide, l, t, w, 0.04, top_accent)

def stat_bar(slide, stats, y=6.38):
    rect(slide, 0, y, 13.33, 7.5-y, S1)
    n = len(stats)
    col_w = 13.33 / n
    for i, (val, lbl) in enumerate(stats):
        x = i * col_w + col_w/2 - 1.2
        txt(slide, val, x, y+0.12, 2.4, 0.52, size=22, bold=True,
            colour=TEAL_L, align=PP_ALIGN.CENTER)
        txt(slide, lbl, x, y+0.62, 2.4, 0.32, size=7.5, colour=INK3,
            align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
rect(s, 0, 0, 7.8, 7.5, S1)
rect(s, 0, 0, 0.08, 7.5, TEAL)

# Right-side abstract lines
for i, (y2, h2) in enumerate([(0.6,1.1),(2.2,0.5),(3.8,0.9),(5.6,0.7)]):
    rect(s, 9.8+i*0.35, y2, 0.04, h2, TEAL_L)
for y2 in [1.0, 2.6, 4.2, 5.8]:
    rect(s, 8.3, y2, 3.5, 0.007, S3)

# Logo
rect(s, 0.6, 0.6, 0.7, 0.7, TEAL)
txt(s, "VS", 0.6, 0.6, 0.7, 0.7, size=15, bold=True, colour=WHITE, align=PP_ALIGN.CENTER)
txt(s, "VELA SYNC", 1.45, 0.73, 3.0, 0.38, size=8, bold=True, colour=INK)

tag(s, "Internal Operations · Confidential", 0.6, 1.55, 3.7)

txt(s, "The Complete", 0.6, 1.98, 7.0, 0.75, size=44, bold=True, colour=INK)
txt(s, "Sales Process.", 0.6, 2.68, 7.0, 1.05, size=52, bold=True, colour=TEAL_L)
txt(s, "8 stages · zero ambiguity · one system to close every room.",
    0.6, 3.8, 6.5, 0.42, size=11.5, colour=INK2, italic=True)

divider(s, 0.6, 4.35, 5.8)

stats_c = [("8","Stages"), ("£450","Entry package"), ("24h","To go live"), ("77%","SMEs no web strategy")]
for i, (v, l) in enumerate(stats_c):
    x = 0.6 + i*1.75
    txt(s, v, x, 4.52, 1.6, 0.52, size=22, bold=True, colour=TEAL_L)
    txt(s, l, x, 5.02, 1.6, 0.32, size=7, colour=INK3)

# Right side stage list
txt(s, "01 → 02 → 03 → 04 → 05 → 06", 8.1, 3.3, 4.8, 0.38,
    size=9.5, bold=True, colour=TEAL, align=PP_ALIGN.CENTER)
stages_r = ["Onboarding","Pre-Meeting Research","Discovery Call","Reveal & Pitch","Objection & Close","Post-Close & Payment"]
for i, st in enumerate(stages_r):
    y2 = 3.78 + i * 0.47
    rect(s, 8.3, y2, 4.5, 0.38, S2)
    txt(s, f"0{i+1}  {st}", 8.48, y2+0.06, 4.2, 0.28, size=9,
        colour=INK if i==0 else INK2, bold=(i==0))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Full Pipeline · At a Glance", "The 8-Stage Sales System")

stages = [
    ("01","Advisor\nOnboarding","🎓","Foundation"),
    ("📅","Weekly\nCadence","📅","Rhythm"),
    ("02","Pre-Meeting\nResearch","🔍","Prep"),
    ("03","Discovery\nCall","🎯","Qualify"),
    ("04","Reveal\n& Pitch","👁️","Present"),
    ("05","Objection\n& Close","🤝","Convert"),
    ("£","Pricing\nStructure","💷","Sell"),
    ("06","Post-Close\n& Payment","✅","Complete"),
]

BW, BH = 1.4, 1.85
SX, SY = 0.45, 1.78
GAP = 0.195

for i, (num, lbl, ico, tag_t) in enumerate(stages):
    x = SX + i*(BW+GAP)
    col2 = S2 if i % 2 == 0 else S1
    card(s, x, SY, BW, BH, colour=col2,
         top_accent=TEAL if (num.isdigit() or num=="£") else TEAL_L)
    txt(s, num, x, SY+0.08, BW, 0.42, size=17, bold=True,
        colour=TEAL_L, align=PP_ALIGN.CENTER)
    txt(s, ico, x, SY+0.46, BW, 0.38, size=17, align=PP_ALIGN.CENTER)
    txt(s, lbl, x, SY+0.82, BW, 0.62, size=9, bold=True,
        colour=INK, align=PP_ALIGN.CENTER)
    txt(s, tag_t.upper(), x, SY+1.56, BW, 0.22, size=6,
        colour=TEAL, align=PP_ALIGN.CENTER)
    if i < len(stages)-1:
        ax = x + BW + 0.01
        rect(s, ax, SY+BH/2-0.008, GAP-0.04, 0.016, TEAL)
        txt(s, "›", ax+GAP*0.3, SY+BH/2-0.15, 0.22, 0.3,
            size=13, colour=TEAL, align=PP_ALIGN.CENTER)

stat_bar(s, [("500+","Calls / week"),("5+","Closes / week"),
             ("24h","From close to live"),("£450","Entry · no contract")])

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — ONBOARDING
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 01 · Foundation", "Advisor Onboarding",
             "Know the product. Know the tools. Know the numbers — before you speak to anyone.")

pillars = [
    ("🎓","Product Mastery","Every package & price cold\n£450 / £650 setup  ·  £50 / £100 /mo"),
    ("🔧","Tools & Assets", "Lead list · Demo site · Scripts\nObjection guides · CRM access"),
    ("📞","Targets & KPIs", "500 outbound calls / week\n5 closed sales / week minimum"),
]
PW = 4.1
for i, (ico, title, body) in enumerate(pillars):
    x = 0.45 + i*(PW+0.12)
    card(s, x, 1.82, PW, 1.5)
    txt(s, ico, x+0.18, 1.93, 0.55, 0.5, size=20)
    txt(s, title, x+0.85, 1.96, PW-1.05, 0.35, size=12, bold=True, colour=INK)
    txt(s, body,  x+0.18, 2.42, PW-0.36, 0.8, size=9, colour=INK2)

txt(s, "THE SIX RULES", 0.45, 3.48, 5.0, 0.26, size=7.5, bold=True, colour=TEAL_L)
rules = [
    ("🎯","You are the expert. Act like it.","Confidence is not optional."),
    ("🔇","Silence is a weapon.","After every powerful question — stop talking."),
    ("🩺","Diagnose before you prescribe.","Ask before you pitch. Always."),
    ("📊","Speak in outcomes, not features.","They care about customers, not animations."),
    ("🏦","Frame everything as ROI.","Every price is an investment."),
    ("🪝","Show, don't tell.","Open the draft site silently. Let them sell themselves."),
]
RW, RH = 4.1, 1.2
positions = [(0.45,3.75),(4.67,3.75),(8.89,3.75),(0.45,5.02),(4.67,5.02),(8.89,5.02)]
for (x, y2), (ico, title, sub) in zip(positions, rules):
    card(s, x, y2, RW, RH, colour=S1)
    txt(s, ico, x+0.14, y2+0.18, 0.45, 0.45, size=16)
    txt(s, title, x+0.68, y2+0.12, RW-0.82, 0.35, size=9.5, bold=True, colour=INK)
    txt(s, sub,   x+0.68, y2+0.5,  RW-0.82, 0.55, size=8.5, colour=INK2)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — WEEKLY CADENCE + KPIs
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Team Cadence · Weekly Rhythm", "Schedule & KPIs",
             "Consistent rhythm drives consistent performance.")

days = [
    ("MON", TEAL,   [("11:00 AM","Diary Alignment"),("5:00 PM","KPI Review")]),
    ("TUE", S3,     [("5:00 PM", "Daily Touch Point")]),
    ("WED", S3,     [("5:00 PM", "Daily Touch Point")]),
    ("THU", TEAL_L, [("5:00 PM", "Fwd Planning"),("5:00 PM","Daily Touch Point")]),
    ("FRI", S3,     [("5:00 PM", "Daily Touch Point")]),
]

DW, DH = 2.38, 3.28
for i, (day, acc, evts) in enumerate(days):
    x = 0.45 + i*2.55
    hi = acc not in (S3,)
    card(s, x, 1.8, DW, DH, colour=S2 if hi else S1, top_accent=acc)
    txt(s, day, x+0.12, 1.9, DW-0.24, 0.3, size=9.5, bold=True,
        colour=TEAL_L if hi else INK3)
    for j, (time, lbl) in enumerate(evts):
        ey = 2.28 + j*1.28
        rect(s, x+0.12, ey, DW-0.24, 1.15, S3)
        txt(s, time, x+0.22, ey+0.1,  DW-0.44, 0.26, size=7.5, bold=True, colour=TEAL_L)
        txt(s, lbl,  x+0.22, ey+0.38, DW-0.44, 0.52, size=9.5, bold=True, colour=INK)

# KPIs right side — compact 2x4 grid
txt(s, "KEY KPIs", 13.33-4.55, 1.75, 4.0, 0.28, size=7.5, bold=True, colour=TEAL_L)
kpis = [
    ("📞","Outbound Calls","500+ / week"),
    ("📈","Conversion","5+ closes / week"),
    ("💰","Revenue","Weekly & monthly"),
    ("🔄","Follow-Up Rate","100% warm leads"),
    ("🏷️","Avg Deal Value","£450–£650"),
    ("🔁","Retention","Maximise monthly"),
]
KW, KH = 2.12, 0.82
for i, (ico, name, tgt) in enumerate(kpis):
    col_i = i % 2
    row_i = i // 2
    x = 8.95 + col_i*(KW+0.15)
    y2 = 2.08 + row_i*(KH+0.1)
    card(s, x, y2, KW, KH, colour=S1)
    txt(s, ico, x+0.1, y2+0.13, 0.32, 0.32, size=13)
    txt(s, name, x+0.5, y2+0.1, KW-0.6, 0.28, size=8.5, bold=True, colour=INK)
    txt(s, tgt,  x+0.5, y2+0.42, KW-0.6, 0.28, size=8, colour=TEAL_L)

# Recurring row
rect(s, 0, 5.22, 13.33, 0.08, S3)
txt(s, "RECURRING", 0.45, 5.35, 2.5, 0.24, size=7, bold=True, colour=TEAL_L)
recur = [("🔴","24/7","MD Direct Line"),("🎯","2W","Bi-Weekly 1:1s"),("📋","1Y","Personal Dev Plan")]
for i, (ico, freq, lbl) in enumerate(recur):
    x = 3.0 + i*3.3
    txt(s, ico, x, 5.3, 0.42, 0.42, size=16)
    txt(s, freq, x+0.5, 5.32, 0.8, 0.35, size=14, bold=True, colour=TEAL_L)
    txt(s, lbl,  x+0.5, 5.65, 2.5, 0.28, size=9, colour=INK2)

stat_bar(s, [("Mon","Diary + KPI Review"),("Tue–Fri","5pm Daily Touch Point"),
             ("Thu","Weekly Fwd Planning"),("Bi-wk","1:1 with MD")])

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — PRE-MEETING RESEARCH
# Layout (all y values from slide top, no overlaps):
#   Header/divider  : 0.00 – 1.65
#   4 step cards    : 1.78 – 4.38  (h=2.60)
#   Script block    : 4.52 – 5.62  (h=1.10)
#   Warning bar     : 5.76 – 6.50  (h=0.74)
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 02 · Preparation", "Pre-Meeting Research",
             "10 minutes before every meeting. Walk in knowing their problem before they've said a word.")

# Card geometry — 4 equal columns, 0.1" gap between each
CW   = 2.98   # card width  → 4×2.98 + 3×0.13 = 12.31 total, centred with 0.51" margin
CGAP = 0.12
CY   = 1.78   # cards top
CH   = 2.60   # cards height  → bottom = 4.38

steps = [
    ("🔍", "01", "Google Them",
     "Search the business. Do they appear at all? What comes up first — them or a competitor?"),
    ("🌐", "02", "Check Their Site",
     "Is it mobile-friendly? Fast? Does it actually convert — or is it a liability?"),
    ("⭐", "03", "Google Maps Rating",
     "Low score = reputation problem. No reviews = visibility problem. You solve both."),
    ("⚔️", "04", "Competitor Audit",
     "Find their top 3 local competitors. Check their online presence. You'll use this to create urgency."),
]

for i, (ico, num, title, body) in enumerate(steps):
    x = 0.45 + i * (CW + CGAP)

    # Card background + top accent
    card(s, x, CY, CW, CH)

    # Step number — small badge top-right inside card
    rect(s, x + CW - 0.52, CY + 0.1, 0.38, 0.28, S3)
    txt(s, num, x + CW - 0.52, CY + 0.1, 0.38, 0.28,
        size=8, bold=True, colour=TEAL_L, align=PP_ALIGN.CENTER)

    # Emoji icon — top-left
    txt(s, ico, x + 0.15, CY + 0.1, 0.55, 0.52, size=24)

    # Title
    txt(s, title, x + 0.15, CY + 0.7, CW - 0.3, 0.36,
        size=11.5, bold=True, colour=INK)

    # Divider line inside card
    rect(s, x + 0.15, CY + 1.1, CW - 0.3, 0.008, S3)

    # Body text — starts well below title, fits within CH
    txt(s, body, x + 0.15, CY + 1.2, CW - 0.3, 1.3,
        size=9, colour=INK2)

# Script block — starts 0.14" below cards (4.38 + 0.14 = 4.52)
rect(s, 0.45, 4.52, 12.43, 1.10, S1)
rect(s, 0.45, 4.52, 0.05, 1.10, TEAL)
txt(s, "OPENING LINE", 0.62, 4.60, 3.0, 0.22, size=7, bold=True, colour=TEAL_L)
txt(s, '"I had a look at your business before coming in today. I noticed a few things I wanted to talk about '
       '— but first, tell me how business has been. Are you getting as many new customers as you want?"',
    0.62, 4.83, 12.0, 0.72, size=10, colour=INK2, italic=True)

# Warning — starts 0.14" below script block (4.52 + 1.10 + 0.14 = 5.76)
rect(s, 0.45, 5.76, 12.43, 0.74, RGBColor(0x22, 0x08, 0x08))
rect(s, 0.45, 5.76, 0.05, 0.74, RED)
txt(s, "⛔  Never open with the product. Open with their world — not yours. The product comes third.",
    0.62, 5.92, 12.0, 0.48, size=10, colour=RGBColor(0xF8, 0x71, 0x71))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — DISCOVERY QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 03 · Qualification", "6 Discovery Questions",
             "Ask in sequence · Listen deeply · Take notes visibly. Their answers give you everything to close.")

qs = [
    ("1","Current State",       '"When a potential customer Googles you right now — what do they find?"',
     "Forces them to confront their digital reality."),
    ("2","Awareness",           '"How are most of your customers finding you at the moment?"',
     "Exposes over-reliance on referrals. One slow season away from a problem."),
    ("3","Competition",         '"Have you looked at what your top three competitors are doing online?"',
     "Creates competitive anxiety. You already know the answer — make them say it."),
    ("4","Revenue Impact",      '"76% research online before contact — what does that mean for customers you\'re missing?"',
     "Forces them to calculate lost revenue in their own head."),
    ("5","Previous Experience", '"Have you ever tried to get a website built before? What happened?"',
     "Most have a war story. You are the antidote before you've mentioned the product."),
    ("6","Future Vision ★",    '"If your digital presence was exactly where you wanted it — what would change?"',
     "Most powerful question. Gets them to paint their own success picture out loud."),
]

QW, QH = 6.0, 0.8
for i, (num, lbl, q, why) in enumerate(qs):
    ci = i % 2
    ri = i // 2
    x = 0.45 + ci*6.45
    y2 = 1.82 + ri*(QH+0.1)
    is_last = (i == 5)
    bg_c = RGBColor(0x12,0x22,0x18) if is_last else S1
    acc_c = TEAL_LL if is_last else TEAL
    card(s, x, y2, QW, QH, colour=bg_c, top_accent=acc_c,
         border_c=GREEN if is_last else S3)
    txt(s, num,  x+0.14, y2+0.1,  0.3, 0.3, size=10, bold=True, colour=TEAL_L)
    txt(s, lbl.upper(), x+0.5, y2+0.09, QW-0.65, 0.24, size=6.5, bold=True,
        colour=GREEN if is_last else TEAL)
    txt(s, q,   x+0.14, y2+0.34, QW-0.28, 0.27, size=9, colour=INK, italic=True)
    txt(s, why, x+0.14, y2+0.6,  QW-0.28, 0.18, size=7.5, colour=INK3)

# Tip bar
rect(s, 0.45, 6.32, 12.43, 0.9, RGBColor(0x18,0x14,0x04))
rect(s, 0.45, 6.32, 0.05, 0.9, AMBER)
txt(s, '💡  After all six questions: "So if I\'ve understood you correctly..." — feed their answers back verbatim. '
       'Validates concerns, amplifies the pain, sets up the pitch. Never skip this.',
    0.62, 6.47, 12.0, 0.62, size=9, colour=RGBColor(0xF5,0xD0,0x60))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — REVEAL & PITCH
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 04 · Presentation", "The Reveal & Pitch",
             "Bridge their pain · Show the site silently · Anchor high, land low. The emotional sale is made here.")

steps = [
    ("🔗","01","Bridge the Pain",
     "Summarise their answers in one clear statement.\nMake them feel heard before you reveal anything."),
    ("👁️","02","The Silent Show",
     "Open the draft site. Say nothing. Scroll slowly.\nWhen they lean in — that's your pivot."),
    ("⚖️","03","Anchor High, Land Low",
     "Never open with £450. Anchor to £2,000+.\nThe contrast does the selling for you."),
]
SW2 = 4.08
for i, (ico, num, title, body) in enumerate(steps):
    x = 0.45 + i*(SW2+0.08)
    card(s, x, 1.82, SW2, 1.95)
    txt(s, ico,   x+0.18, 1.94, 0.55, 0.52, size=22)
    txt(s, f"STEP {num}", x+0.85, 1.97, 2.8, 0.26, size=7, bold=True, colour=TEAL)
    txt(s, title, x+0.18, 2.48, SW2-0.36, 0.36, size=12, bold=True, colour=INK)
    txt(s, body,  x+0.18, 2.88, SW2-0.36, 0.78, size=9, colour=INK2)

# Price reveal script
rect(s, 0.45, 3.9, 12.43, 0.82, S1)
rect(s, 0.45, 3.9, 0.05, 0.82, TEAL)
txt(s, "PRICE REVEAL", 0.62, 3.98, 2.5, 0.22, size=7, bold=True, colour=TEAL_L)
txt(s, '"A website of this quality from a traditional agency — you\'re looking at £2,000 minimum. '
       'We charge £450. And you\'re live within 24 hours. Not a week. Not a month. Tomorrow."',
    0.62, 4.2, 12.0, 0.45, size=10, colour=INK, italic=True)

# Signals (green) | Caution (amber) — side by side
LW = 6.15
for xi, (x_start, title_c, bg_c, border_c, entries) in enumerate([
    (0.45, GREEN, RGBColor(0x08,0x1e,0x10), GREEN,
     [("✅",'"That looks really good"'),("✅","Leans toward the screen"),
      ("✅","Asks logistics / timeline questions"),("✅",'"Can you do it in our colours?"'),
      ("✅","Looks at a colleague for approval")]),
    (6.73, AMBER, RGBColor(0x1e,0x16,0x04), AMBER,
     [("⚠️","Arms crossed, leaning back"),("⚠️",'"We need to talk to our accountant"'),
      ("⚠️",'"We\'ll think about it"'),("⚠️","Checking their phone"),
      ("⚠️","Repeated glances at the door")]),
]):
    txt(s, "BUYING SIGNALS" if xi==0 else "PROCEED WITH CAUTION",
        x_start, 4.85, LW, 0.26, size=7.5, bold=True, colour=title_c)
    card(s, x_start, 5.14, LW, 2.2, colour=bg_c, top_accent=title_c, border_c=border_c)
    for j, (ico, sig) in enumerate(entries):
        txt(s, f"{ico}  {sig}", x_start+0.18, 5.24+j*0.4, LW-0.3, 0.36,
            size=9, colour=RGBColor(0x86,0xEF,0xAC) if xi==0 else RGBColor(0xFB,0xD5,0x82))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — OBJECTIONS & CLOSE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 05 · Conversion", "Objection Handling & The Close",
             "Every objection is a question in disguise. Acknowledge · Reframe · Advance.")

# Left — objections
txt(s, "COMMON OBJECTIONS", 0.45, 1.76, 5.0, 0.26, size=7.5, bold=True, colour=TEAL_L)
objs = [
    ('"We already have a website."',
     "Is it ranking? Is it bringing in enquiries — or a digital brochure?"),
    ('"£450 seems too cheap."',
     "You've just seen it. That IS the quality. Enterprise engineers, zero overhead."),
    ('"We need to think about it."',
     "What specifically? Name the real objection. Then stop talking."),
    ('"We want a few quotes first."',
     "Equivalent quality starts at £2,000+. Come back — we'll beat any quote."),
    ('"We had a bad experience before."',
     '"Tell me what happened." Vela Sync was built because of that gap.'),
    ('"Not sure about the monthly."',
     "£50/mo is insurance on a £450 asset. Easiest decision in the room."),
]
for i, (obj, resp) in enumerate(objs):
    y2 = 2.06 + i*0.8
    card(s, 0.45, y2, 6.1, 0.72)
    rect(s, 0.45, y2, 0.04, 0.72, TEAL)
    txt(s, obj,  0.6, y2+0.06, 5.8, 0.26, size=9, bold=True, colour=INK, italic=True)
    txt(s, resp, 0.6, y2+0.34, 5.8, 0.3,  size=8.5, colour=INK2)

# Right — close techniques
txt(s, "CLOSE TECHNIQUES", 6.8, 1.76, 5.0, 0.26, size=7.5, bold=True, colour=TEAL_L)
closes = [
    ("Assumptive Close",
     "Assumes the sale. Moves to logistics.\n\"What's the domain name you're using?\""),
    ("Investment Frame Close",
     "Forces ROI calculation.\n\"If it brings one extra customer — what's that worth?\""),
    ("Urgency Close",
     "Someone is searching for you RIGHT NOW.\n\"What's stopping us doing this today?\" — then silence."),
    ("Option Close",
     "Both options are a yes.\n\"£450 standard or £650 SEO — which feels right?\""),
    ("Instalment Close",
     "Removes the financial barrier.\n\"Get it live tomorrow, pay on a schedule that suits you.\""),
]
for i, (name, desc) in enumerate(closes):
    y2 = 2.06 + i*0.94
    card(s, 6.8, y2, 6.08, 0.86, colour=S2, top_accent=TEAL_LL)
    rect(s, 6.8, y2, 0.04, 0.86, TEAL_LL)
    txt(s, name, 6.95, y2+0.08, 5.8, 0.28, size=10, bold=True, colour=TEAL_L)
    txt(s, desc, 6.95, y2+0.38, 5.8, 0.42, size=8.5, colour=INK2)

# Power phrases footer
rect(s, 0, 6.84, 13.33, 0.66, S1)
phrases = ['"The question isn\'t whether — it\'s when."',
           '"This isn\'t a cost. It\'s a decision."',
           '"Every day you wait, your competitor doesn\'t."',
           '"Based on what you\'ve told me..."']
for i, p in enumerate(phrases):
    txt(s, p, 0.45+i*3.2, 6.93, 3.0, 0.38, size=7.5, colour=TEAL, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — PRICING
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Pricing Structure · Know These Cold", "What You're Selling",
             "Two packages. Two monthly tiers. The contrast vs the market is your most powerful tool.")

# Standard package
card(s, 0.45, 1.82, 5.95, 5.35, colour=S1)
txt(s, "STANDARD PACKAGE", 0.65, 2.0, 5.6, 0.26, size=7.5, bold=True, colour=TEAL_L)
txt(s, "£450", 0.65, 2.28, 3.8, 0.88, size=50, bold=True, colour=INK)
txt(s, "$575  ·  €525", 0.65, 3.1, 5.0, 0.28, size=10, colour=TEAL_L)
txt(s, "One-off setup  ·  Live within 24 hours", 0.65, 3.34, 5.2, 0.26, size=9, colour=INK3)
divider(s, 0.65, 3.64, 5.55)
std_f = ["Professional, mobile-responsive website","Personalised to the client's brand",
         "Domain activation or transfer included","SSL, on-page SEO & performance optimised",
         "Client reviews & approves before launch","Full access credentials on the day",
         "Instalments available"]
for i, f in enumerate(std_f):
    txt(s, f"✓  {f}", 0.65, 3.8+i*0.3, 5.5, 0.27, size=8.5, colour=INK2)
rect(s, 0.65, 5.96, 5.55, 0.9, S2)
txt(s, "THEN MONTHLY", 0.82, 6.04, 3.0, 0.2, size=7, bold=True, colour=TEAL_L)
txt(s, "£50 / $65 / €58 /month — site maintenance", 0.82, 6.26, 5.2, 0.26, size=9, colour=INK)
txt(s, "Industry avg: £150+ /mo  ·  Cancel any time", 0.82, 6.53, 5.2, 0.22, size=7.5, colour=INK3)

# SEO package (highlighted)
rect(s, 6.58, 1.82, 6.3, 5.35, S2)
rect(s, 6.58, 1.82, 6.3, 0.05, TEAL_L)
rect(s, 10.7, 1.9, 1.9, 0.28, TEAL)
txt(s, "BEST VALUE", 10.7, 1.92, 1.9, 0.24, size=7.5, bold=True,
    colour=WHITE, align=PP_ALIGN.CENTER)
txt(s, "SEO & GROWTH PACKAGE", 6.78, 2.0, 5.6, 0.26, size=7.5, bold=True, colour=TEAL_L)
txt(s, "£650", 6.78, 2.28, 3.8, 0.88, size=50, bold=True, colour=TEAL_L)
txt(s, "$825  ·  €760", 6.78, 3.1, 5.0, 0.28, size=10, colour=TEAL_L)
txt(s, "One-off  ·  Everything in Standard, plus growth", 6.78, 3.34, 5.6, 0.26, size=9, colour=INK3)
divider(s, 6.78, 3.64, 5.9)
seo_f = ["Everything in Standard Package","Marketing team briefed at launch",
         "Live traffic strategy from day one","Growth roadmap tailored to their business",
         "SEO foundations for immediate indexing","ML-backed digital strategy applied day one",
         "Save up to £1,550 vs average agency","Instalments available"]
for i, f in enumerate(seo_f):
    txt(s, f"✓  {f}", 6.78, 3.8+i*0.272, 5.9, 0.26, size=8.5, colour=INK2)
rect(s, 6.78, 5.96, 5.9, 0.9, RGBColor(0x16,0x2C,0x2C))
txt(s, "THEN MONTHLY", 6.95, 6.04, 3.0, 0.2, size=7, bold=True, colour=TEAL_L)
txt(s, "£100 / $130 / €117 /month — maintenance + SEO + traffic", 6.95, 6.26, 5.7, 0.26,
    size=9, colour=TEAL_L)
txt(s, "Industry avg: £300+ /mo  ·  No contract, cancel any time",
    6.95, 6.53, 5.7, 0.22, size=7.5, colour=INK3)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — POST-CLOSE & PAYMENT  (fixed layout — no overlaps)
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_header(s, "Stage 06 · Completion", "Post-Close, Onboarding & Payment",
             "The close is not the finish line. Protect the sale · trigger delivery · collect payment.")

# ── Row A: Delivery process — 3 cards horizontal ─────────────────────────────
txt(s, "DELIVERY PROCESS", 0.45, 1.76, 4.0, 0.24, size=7.5, bold=True, colour=TEAL_L)

delivery = [
    ("A","Immediately","Log sale in CRM · notify build team · 24-hour clock starts NOW."),
    ("B","Same Day",   "30-min brief call with design team — brand, copy, domain, requirements."),
    ("C","Within 24h", "Build complete · client reviews · revisions · site goes live."),
]
DLW = 4.18
for i, (ltr, timing, desc) in enumerate(delivery):
    x = 0.45 + i*(DLW+0.11)
    card(s, x, 2.04, DLW, 1.02)
    rect(s, x, 2.04, 0.46, 1.02, S3)   # left badge area
    txt(s, ltr,    x+0.04, 2.2,  0.38, 0.52, size=16, bold=True,
        colour=TEAL_L, align=PP_ALIGN.CENTER)
    txt(s, timing.upper(), x+0.56, 2.1,  DLW-0.7, 0.24, size=7, bold=True, colour=TEAL)
    txt(s, desc,   x+0.56, 2.36, DLW-0.7, 0.6,  size=9, colour=INK2)

# ── Row B: Payment collection — 6 steps in 2×3 grid ─────────────────────────
txt(s, "PAYMENT COLLECTION", 0.45, 3.2, 5.0, 0.24, size=7.5, bold=True, colour=TEAL_L)

payments = [
    ("1","At Close",   "Issue invoice immediately — package + first monthly fee."),
    ("2","Standard",   "Full payment before or on the day the site goes live."),
    ("3","Instalment", "First payment at close. Schedule confirmed in writing."),
    ("4","Day 1 Late", "Friendly reminder — confirming, not chasing."),
    ("5","Day 3",      "Direct call — warm, professional, easy path to yes."),
    ("6","Day 7",      "Formal written notice. 48-hour final deadline."),
]
PWW = 6.35
for i, (num, timing, desc) in enumerate(payments):
    ci = i // 3
    ri = i % 3
    x = 0.45 + ci*(PWW+0.28)
    y2 = 3.5 + ri*0.65
    card(s, x, y2, PWW, 0.57)
    rect(s, x, y2, 0.04, 0.57, TEAL_L if ci==1 else TEAL)
    txt(s, num,    x+0.14, y2+0.06, 0.32, 0.32, size=10, bold=True, colour=TEAL_L)
    txt(s, timing.upper(), x+0.54, y2+0.04, 1.7, 0.22, size=7, bold=True, colour=TEAL)
    txt(s, desc,   x+0.54, y2+0.28, PWW-0.68, 0.25, size=8.5, colour=INK2)

# ── Row C: Do / Don't / If Not Today ─────────────────────────────────────────
BTY = 5.58   # bottom cards top y
BTH = 1.7    # height
BTW = 4.18   # each card width

for i, (bgc, bc, icon, title, items) in enumerate([
    (RGBColor(0x08,0x1E,0x10), GREEN, "✅", "Always Do",
     ["Invoice same day as close","Confirm payment terms in writing",
      "Lock in brief call before you leave","Log every interaction in CRM"]),
    (RGBColor(0x1E,0x08,0x08), RED, "⛔", "Never Do",
     ["Hand over site before payment","Leave without a defined next step",
      "Accept \"call me when you're ready\"","Agree verbal-only instalment terms"]),
    (RGBColor(0x1E,0x16,0x04), AMBER, "⚠️", "If No Close Today",
     ["Lock in a specific date & time","Send draft site link that evening",
      "Send calendar invite from the car","Vague next steps die — specific ones live"]),
]):
    x = 0.45 + i*(BTW+0.12)
    card(s, x, BTY, BTW, BTH, colour=bgc, top_accent=bc, border_c=bc)
    txt(s, f"{icon}  {title}", x+0.15, BTY+0.1, BTW-0.3, 0.32,
        size=10, bold=True, colour=bc)
    for j, item in enumerate(items):
        txt(s, f"• {item}", x+0.15, BTY+0.48+j*0.3, BTW-0.3, 0.27,
            size=8, colour=INK2)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — CLOSING STATEMENT
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
rect(s, 0, 0, 13.33, 7.5, S1)
rect(s, 0, 0, 0.08, 7.5, TEAL)

for i in range(8):
    rect(s, 9.6+i*0.38, 0.5+i*0.28, 0.035, 1.0+i*0.18, TEAL_L)
for y2 in [1.5,2.5,3.5,4.5,5.5]:
    rect(s, 8.5, y2, 3.8, 0.007, S3)

rect(s, 0.6, 0.6, 0.72, 0.72, TEAL)
txt(s, "VS", 0.6, 0.6, 0.72, 0.72, size=15, bold=True, colour=WHITE, align=PP_ALIGN.CENTER)
txt(s, "VELA SYNC", 1.48, 0.73, 3.0, 0.36, size=8, bold=True, colour=INK)

txt(s, "The Standard:", 0.65, 2.1, 9.0, 0.62, size=36, bold=True, colour=TEAL_L)
txt(s, "Signed. Invoiced. Brief call booked.\nSite live in 24 hours.",
    0.65, 2.7, 9.5, 1.35, size=40, bold=True, colour=INK)
txt(s, "That is what you're selling. That is exactly what you deliver.",
    0.65, 4.2, 9.0, 0.45, size=13, colour=INK2, italic=True)

divider(s, 0.65, 4.8, 8.2)

final = [("8","Stages"),("500+","Calls/wk"),("5+","Closes/wk"),("24h","To live")]
for i, (v, l) in enumerate(final):
    x = 0.65+i*2.25
    txt(s, v, x, 5.0, 2.1, 0.55, size=28, bold=True, colour=TEAL_L)
    txt(s, l, x, 5.55, 2.1, 0.3, size=9, colour=INK3)

txt(s, "© 2026 Vela Sync Ltd · Co. No. 17051204 · Internal Sales Playbook — Confidential — Not for Distribution",
    0.65, 7.05, 12.0, 0.32, size=7, colour=INK3)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/home/user/GB123/VelaSync_Sales_Process.pptx"
prs.save(out)
print(f"Saved → {out}")
