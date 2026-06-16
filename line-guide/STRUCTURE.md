# Line Guide — Website Structure & Design System

> **The new way to buy automation equipment.** Search · Compare · Connect.
> A two-sided marketplace matching food & beverage manufacturers (buyers)
> with automation-equipment manufacturers (suppliers).

This document is the blueprint: the brand, the full sitemap, every page,
every section, and **what each one must accomplish**. The `index.html`,
`for-buyers.html` and `for-suppliers.html` in this folder are the
production-ready front of that structure; the rest is the roadmap for the
app behind the marketing site.

---

## 1. Brand foundation

| Token | Value | Use |
|---|---|---|
| Green (primary) | `#19CD6A` | CTAs, accents, brand |
| Green bright | `#3DF086` | glows, gradient text highlight |
| Green deep | `#0E9B4E` | gradient anchors, progress |
| Ink / backgrounds | `#070A08 → #1A221C` | near-black, faint green tint |
| White / text | `#F3F8F4` / `#E7EFE9` | type |

**Type:** `Space Grotesk` (display + brand) · `Inter` (body/UI) · `IBM Plex Mono`
(technical eyebrows & data labels). The mono labels are what make it read
"technical".

**Logo:** bracket-framed wordmark (top-right + bottom-left corner brackets in
green), recreated faithfully in CSS as `.brand-frame`.

**Personality:** modern + technical. Dark, precise, engineered. Motion is
purposeful (scan lines, particle mesh, live data) — never decorative noise.

**Design system files:** `assets/styles.css` (token-driven, mobile-first),
`assets/app.js` (shared site interaction) and `assets/brief.js` (the buyer
brief-builder wizard + matching engine). Shared across every page so the
site scales without duplication.

---

## 2. Sitemap

```
Line Guide
│
├── / (Home) ─────────────── conversion hub + live product demo   [BUILT]
├── /for-buyers ──────────── buyer value story + journey          [BUILT]
├── /for-suppliers ───────── supplier value + pricing + onboard   [BUILT]
│
├── MARKETING
│   ├── /how-it-works ────── deeper explainer (buyer + supplier)     [BUILT → how-it-works.html]
│   ├── /pricing ─────────── standalone supplier pricing + compare   [BUILT → pricing.html]
│   ├── /use-cases ───────── packing / palletising / filling / …    [BUILT → use-cases.html]
│   ├── /use-cases/:slug ─── single application landing (SEO)        [BUILT → use-case.html?u=]
│   ├── /suppliers ───────── public directory (browse/search)       [BUILT → suppliers.html]
│   ├── /suppliers/:slug ─── public supplier profile (SEO + proof)   [BUILT → supplier.html?s=]
│   ├── /about ───────────── mission, team, story
│   ├── /blog + /blog/:slug  content engine (SEO, authority)
│   ├── /contact ─────────── sales / support / partnerships
│   └── /legal/* ─────────── privacy, terms, cookies, supplier agreement
│
└── APPLICATION (authenticated)
    ├── /signup · /login · /verify-email
    ├── BUYER
    │   ├── /buyer/brief/new ──── guided brief builder (the funnel)   [BUILT → brief.html]
    │   ├── /buyer/matches/:id ── top-3 results + comparison          [BUILT → brief.html results]
    │   ├── /buyer/messages ───── conversations with suppliers
    │   └── /buyer/dashboard ──── saved briefs, shortlists, history
    └── SUPPLIER
        ├── /supplier/onboarding ─ profile + verification + tier
        ├── /supplier/profile ──── edit capabilities, media, cases
        ├── /supplier/leads ────── matched briefs inbox + status
        ├── /supplier/billing ──── tier, invoices, upgrade/downgrade
        └── /supplier/analytics ── impressions, fit, win-rate (Premium+)
```

---

## 3. Page-by-page — sections & goals

### 3.1 Home `/` — *BUILT*
The single most important page: prove the product in seconds and route the
two audiences. Each section has one job.

| # | Section | Goal — what it must accomplish |
|---|---|---|
| 1 | **Announcement bar** | Set urgency/stage ("Launching soon · Join early access"). |
| 2 | **Nav** | Persistent wayfinding + dual CTA (buyer *Find suppliers* / supplier *List business*). |
| 3 | **Hero** | One-line value prop, the Search·Compare·Connect promise, dual CTA, animated proof (floating cards, live stats). Communicate "top 3 in minutes" instantly. |
| 4 | **Trust strip** | Establish the food & beverage niche + capability breadth → credibility. |
| 5 | **Pillars (Search/Compare/Connect)** | Teach the model in 3 beats — straight from the brand banner. |
| 6 | **Live matching engine** ⭐ | *Show, don't tell.* Interactive demo: pick use-case, budget, timeframe → real ranked top-3 with fit scores. This is the "aha". |
| 7 | **How it works (tabs)** | Full journey for both sides; tab toggle proves it's two-sided without two pages. |
| 8 | **Use cases** | Help buyers self-identify ("that's my problem") + SEO surface area. |
| 9 | **Pricing (3 tiers)** | Convert suppliers: Basic / Premium / Ultra, featured middle. |
| 10 | **Why Line Guide** | Reinforce differentiators (fit > noise, free for buyers, verified). |
| 11 | **Ratings / trust** | Make the algorithm transparent → defensible, trustworthy rankings. |
| 12 | **FAQ** | Remove final objections (free? how ranked? cancel?). |
| 13 | **CTA / waitlist** | Single capture for both audiences pre-launch. |
| 14 | **Footer** | Full nav, legal, social, company. |

### 3.2 For Buyers `/for-buyers` — *BUILT*
**Goal:** convince manufacturers it's faster, lower-risk and free.
Sections: subhero → 3 split feature rows (Describe / Match / Connect) →
benefits grid → CTA. Drives to the live matcher on home.

### 3.3 For Suppliers `/for-suppliers` — *BUILT*
**Goal:** convert suppliers to a paid tier.
Sections: subhero (with stats) → why-list grid → **pricing tiers** →
onboarding timeline → founding-member CTA.

### 3.4 How It Works `/how-it-works` — *BUILT (`how-it-works.html`)*
Deep-dive: the two-sided model, full buyer journey, full supplier journey,
the **matching algorithm** with its weighting (and the tier-≠-trust rule),
a **worked example** (one brief → three scored results with breakdowns),
verification & trust, and an FAQ. **Goal:** build trust through transparency;
reduce support load. Nav "How it works" across the site points here.

### 3.5 Pricing `/pricing` — *BUILT (`pricing.html` + `pricing.js`)*
- **Billing toggle** — Monthly ↔ Annual (annual = 2 months free); animated
  switch updates every tier card *and* the comparison-table headers live.
- **Tier cards** — Basic / Premium / Ultra with featured middle.
- **Full comparison table** — features grouped (visibility · leads · profile ·
  insight) × the three tiers, with ticks/values, featured column highlight,
  horizontally scrollable on mobile.
- **Interactive ROI calculator** — sliders for average project value and wins
  per month + tier selector → live "matched pipeline per £1", "membership as a
  share of one project", and "projects/yr to break even". Honestly framed
  (pipeline, not net profit) in the note.
- **Pricing FAQ** + CTA.

**Goal:** close suppliers who need detail and a business case before committing.

### 3.6 Use Cases `/use-cases` + `/use-cases/:slug` — *BUILT*
- **`use-cases.html`** — index grid of all six applications (packing,
  palletising, end-of-line, filling, inspection, manual process), each with
  typical budget/timeframe, linking to its landing.
- **`use-case.html?u=slug`** — dynamic SEO landing per application: intro,
  quick-facts row, "the challenge", "what to look for" checklist, "questions
  to ask suppliers", **top-rated related suppliers** (pulled live from
  `data.js`), an FAQ accordion, and related-application links.
- **`assets/usecases.js`** — content source of truth (6 entries, with
  meta title/description set per page); **`assets/usecase.js`** renders both
  the index and the landing.
- **Funnel hand-off:** every CTA flows into the funnel — "Find suppliers for
  this" → `brief.html`, "Browse the directory" → `suppliers.html?case=slug`
  (the pre-filter wired into the directory).

**Goal:** organic acquisition (one indexable page per high-intent search) that
feeds straight into the brief builder and directory.

> **SEO — pre-render DONE.** `build-usecases.js` (run `node build-usecases.js`)
> reads `usecases.js` + `data.js` and emits a fully static
> `use-case-<slug>.html` per application — title, meta description, canonical
> and full body baked into the initial HTML payload. The index grid and
> related-application links point to these static pages; the dynamic
> `use-case.html?u=` remains as a fallback. Re-run the script after editing
> the content data.

### 3.7 Supplier Directory `/suppliers` + `/suppliers/:slug` — *BUILT*
- **`suppliers.html`** — browsable directory with live **search**, **application
  filters**, **region** + **sort** (top-rated / most projects / tier / A–Z),
  result count and empty state. Cards deep-link to profiles. Accepts
  `?case=` to pre-filter from use-case landing pages.
- **`supplier.html?s=slug`** — **dynamic** profile rendered from the shared
  dataset: hero (verified, rating, tier, location), stat row (projects, lead
  time, response, established), about, capabilities, applications/formats,
  case studies, buyer reviews with rating summary, and an "at a glance"
  sticky sidebar. Falls back gracefully for unknown slugs.
- **`assets/data.js`** — single source of truth (8 seeded suppliers); the
  directory, profile (and future pages) all read from it. Swap for an API later.

**Goal:** SEO surface area, supplier lead/vanity value (a reason to keep
paying), and a browsing path for buyers who prefer to explore.

### 3.8 About / Blog / Contact / Legal *(roadmap)*
Standard trust & growth surfaces. Blog is the long-term SEO/authority engine.

### 3.9 Application — Buyer flow — *BUILT (`brief.html`)*
The core funnel, now live as a 5-step wizard → results:
1. **Brief builder** — Application → Line details (format, throughput,
   environment) → Commercials (budget, timeframe) → Requirements (region,
   must-haves) → Your details. Progress stepper, inline validation,
   keyboard (Enter) nav, and a live brief-summary rail.
2. **Matches** — runs the richer matching engine (`brief.js`) and reveals the
   **top 3** with overall fit %, a **per-signal breakdown** (use-case, rating,
   budget, timeline) and **"request introduction"** with confirm state.
3. **Messages / Dashboard** *(roadmap)* — manage conversations, saved briefs.
**Goal:** turn intent into qualified introductions (the marketplace event).

> **Matching upgrade in `brief.js`:** extends the home demo with product
> format, throughput→required-speed, production environment, region and
> must-have modifiers — all folded transparently into the four headline
> signals. Tier still affects visibility only, never rating.

### 3.10 Application — Supplier flow *(roadmap)*
Onboarding (profile + verification + tier) → **Leads inbox** (matched briefs,
accept/decline, respond) → Billing → Analytics (Premium+).
**Goal:** deliver lead value that justifies the monthly fee → retention.

---

## 4. The matching engine (product core)

Buyers are matched to their **top 3** suppliers via a transparent weighted
fit score (implemented live in `app.js`, mirrored here):

| Signal | Weight | Why |
|---|---|---|
| Use-case fit | **45%** | Right capability is non-negotiable. |
| Verified rating | **25%** | Past buyers predict future outcomes. |
| Budget alignment | **18%** | Respect real capital constraints. |
| Delivery speed vs timeframe | **12%** | Urgency rewards faster suppliers. |

**Membership tier affects *visibility / ranking boost* — never the rating or
review history.** This separation is the platform's integrity promise and is
stated openly in the FAQ and ratings section.

---

## 5. Motion & automation (implemented)

- **Particle mesh canvas** — animated technical backdrop (`#fx-canvas`).
- **Live matching engine** — recomputes & re-ranks on every input, animated
  entry + fit bars. The interactive showpiece.
- **Scroll choreography** — reveal + staggered children via IntersectionObserver.
- **Animated counters**, **rating bars**, **sliding tab pill**, **FAQ accordion**.
- **Cursor glow**, **magnetic primary buttons**, **scan line**, **scroll progress**,
  **page loader**, **floating proof cards**, **sheen-sweep CTAs**.
- **Waitlist** with inline validation + success state.
- Fully **responsive** (mobile menu, reflowing grids) and respects
  `prefers-reduced-motion`.

---

## 6. Build / scale notes

- **Static now, framework-ready later.** Sections map cleanly to components
  (Nav, Hero, Pillars, Matcher, Pricing, FAQ, Footer) — lift into React/Vue/
  Astro without redesign.
- **Suggested stack for the app:** Next.js + a typed API, Postgres for
  briefs/suppliers/ratings, the fit score as a server function, Stripe for
  the three subscription tiers, transactional email for intros/waitlist.
- **Imagery:** the design is intentionally asset-free (CSS/SVG/canvas) so it
  ships reliably. Drop real photography/renders into `.split-media` and
  `.case` slots when available (e.g. generated brand imagery), no layout change.
- **Analytics to wire:** brief completion rate, match→intro conversion,
  supplier lead acceptance, tier upgrade rate.
