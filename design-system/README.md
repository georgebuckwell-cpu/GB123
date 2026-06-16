# Line Guide — Design System

**Version 1.0.0** · Brand personality: **modern + technical** · **Dark-first**

> Line Guide connects machine manufacturers (Basic / Premium / Ultra subscribers) with
> food-manufacturing buyers. Buyers describe a use case — packing automation, automating a
> manual process — plus budget and timeframe, and the platform surfaces the **top three most
> suitable suppliers** by fit and rating. This system is the visual foundation that powers
> those experiences inside **Figma Make**.

## Deliverables in this folder

| File | Format | Purpose |
|------|--------|---------|
| `tokens.json` | Design tokens (W3C DTCG draft JSON) | Machine-readable source of truth. Import into Figma Tokens / Style Dictionary / Figma Make. |
| `tokens.css` | CSS custom properties | Drop-in variables for any web build (light + dark). |
| `figma-components.md` | Figma-ready component docs | 40+ components with anatomy, props, states, and usage rules. |
| `styleguide.html` | Living style guide | Self-contained visual reference rendering every token & component. |
| `README.md` | This document | The full system: color, type, space, motion, responsive, a11y. |

---

## 1. Color System

The palette is **dark-first** to match the brand's immersive technical mood (deep
green-tinted near-black with a vivid Signal Green accent), with a fully resolved light theme.

### 1.1 Primary — Signal Green
The brand accent. `500` is the hero brand color; `400` is the bright accent used on dark
surfaces; `600`/`700` carry green **text** on light backgrounds where contrast demands it.

| Token | Hex | Primary use |
|-------|-----|-------------|
| primary-50 | `#E6FBEF` | Tint backgrounds, success-soft surfaces |
| primary-100 | `#BFF4D6` | Subtle fills, hover tints (light) |
| primary-200 | `#84E9AF` | Borders, chips (light) |
| primary-300 | `#45DA86` | Brand text on dark, illustrative |
| primary-400 | `#14C765` | **Accent on dark** — buttons, focus, icons |
| primary-500 | `#00B259` | **Hero brand** — fills on light, logo |
| primary-600 | `#009149` | Hover (light fills), AA text on white |
| primary-700 | `#00713A` | Brand text on light, pressed |
| primary-800 | `#00532B` | Deep accents |
| primary-900 | `#00371D` | Darkest brand shade |

### 1.2 Secondary — Ion Blue
A cool technical complement for **links, data visualisation, and secondary actions**. It sits
beside green without competing for "primary action" attention. Scale `50→900`, hero `500 #2459DB`.

### 1.3 Neutral — Carbon
A subtly cool/green-tinted gray ramp (`0 #FFFFFF` → `950 #0B100F`) for text, surfaces and
borders. The green tint keeps neutrals feeling part of the brand rather than clinical gray.

### 1.4 Semantic
Each role ships `solid / bg / border / text` for **both** themes (see `tokens.css`).

| Role | Light solid | Dark solid | Meaning |
|------|-------------|------------|---------|
| Success | `#16A34A` | `#22C55E` | Confirmed, matched, verified supplier |
| Warning | `#D97706` | `#FBBF24` | Attention, expiring, partial fit |
| Error | `#DC2626` | `#F87171` | Failure, destructive, validation |
| Info | `#2459DB` | `#4F8BFF` | Neutral system messaging |

> **Note:** Success is a *distinct* green from the brand Signal Green so "this succeeded" never
> reads as "this is branded." Reserve Signal Green for brand & primary actions.

### 1.5 Tier accents (product-specific)
Used on pricing cards, manufacturer badges, and match ribbons.

| Tier | Anchor | Treatment |
|------|--------|-----------|
| **Basic** | `#6E7B78` neutral | Flat slate — functional, no flourish |
| **Premium** | `#00C961` green | Brand gradient `135deg #14C765→#00B259` |
| **Ultra** | `#7B6CF6` violet | Iridescent gradient `#00E0A4→#6B8BFF→#9A6BFF` |

### 1.6 Dark-mode equivalents
Every semantic, brand, and surface token has a resolved dark value in `tokens.css` under
`[data-theme="dark"]` (the default `:root`) and a light value under `[data-theme="light"]`.
Surfaces use a 5-step elevation ramp: `bg → surface → raised → overlay → hover`.

---

## 2. Typography Framework

### 2.1 Font pairing & rationale
| Role | Family | Why |
|------|--------|-----|
| Display / Headings | **Space Grotesk** | Geometric grotesque with engineered, slightly mechanical detailing — signals "technical" and "precision machinery" without feeling cold. |
| Body / UI | **Inter** | Neutral, screen-optimised, exceptional legibility at 12–16px for dense dashboards, forms and tables. |
| Data / Mono | **JetBrains Mono** | Tabular, unambiguous figures for part numbers, specs, match scores, ratings and budgets. |

This pairing reads **modern + technical**: an engineered display face for confidence, a quiet
workhorse for clarity, and mono for the data that *is* the product.

### 2.2 9-step type scale (~1.25 major third, fluid)
| Step | Size (desktop) | Line-height | Tracking | Typical role |
|------|----------------|-------------|----------|--------------|
| xs | 12px | 1.5 | +0.02em | Captions, legal, table meta |
| sm | 14px | 1.55 | +0.01em | Secondary text, dense UI, labels |
| base | 16px | 1.6 | 0 | Body copy |
| lg | 18–20px | 1.6 | 0 | Lead paragraphs |
| xl | 20–24px | 1.4 | −0.005em | H5, large UI |
| 2xl | 24–32px | 1.3 | −0.01em | H4, card titles |
| 3xl | 32–44px | 1.2 | −0.015em | H3, section heads |
| 4xl | 44–60px | 1.1 | −0.02em | H2 |
| 5xl | 60–80px | 1.05 | −0.025em | H1 / hero display |

All steps use `clamp()` for fluid scaling between mobile and desktop (see `--lg-text-*`).
**Weights:** 300 / 400 / 500 / 600 / 700 / 800. Headings use Space Grotesk 500–700.

### 2.3 Usage rules
- One H1 per page. Don't skip heading levels for styling — use a smaller scale step instead.
- Body line length 60–75 characters (`max-width: 65ch`).
- Mono is for data, never for running prose.
- Uppercase labels use `letter-spacing: 0.08em` (`--lg-tracking-caps`).

---

## 3. Spatial System

### 3.1 Foundation
An **8px grid**. `1` (4px) is the only half-step, for fine adjustments (icon gaps, hairline
insets). Everything else is a multiple of 8.

```
0=0  px=1  0.5=2  1=4  2=8  3=12  4=16  5=20  6=24  8=32
10=40  12=48  16=64  20=80  24=96  32=128  40=160  48=192   (px)
```

### 3.2 Application rules
- **Component padding:** sm `space-2/3`, md `space-4`, lg `space-6`.
- **Stack rhythm:** related items `space-2→3`; sections `space-12→24`.
- **Touch targets:** min 44×44px (`space-11` equivalent) — see Accessibility.
- **Radii:** `sm 6` inputs/chips · `md 10` buttons · `lg 16` cards · `xl 22` modals · `2xl 28` hero panels · `full` pills/avatars.
- **Borders:** `hairline 1px` default · `thin 1.5px` emphasis · `thick 2px` focus/selected.

---

## 4. Component Library

Full anatomy, props, states and usage rules for **40+ components** live in
[`figma-components.md`](./figma-components.md). Summary of coverage:

**Actions:** Button (5 variants × 3 sizes), Icon Button, Button Group / Segmented Control, Link
**Forms:** Text Input, Textarea, Select, Combobox/Search, Checkbox, Radio, Switch, Slider (budget), Stepper, Form Field, Filter Chip
**Data display:** Badge, Tier Badge, Avatar, Tag, Tooltip, Rating (stars), Match-Score Meter, Stat/Metric, Data Table, Progress Bar, Skeleton
**Containers:** Card, Manufacturer Profile Card, Tier Pricing Card, Match Result Card, Tabs, Accordion
**Navigation:** Top Nav, Sidebar Nav, Breadcrumb, Pagination, Footer
**Overlays:** Modal/Dialog, Drawer/Sheet, Toast, Alert/Banner, Dropdown Menu
**Feedback & flows:** Spinner, Empty State, Intake Wizard (use-case stepper), Hero Search Bar

Every interactive component documents **default · hover · focus-visible · active/pressed ·
disabled · loading · (selected/error where relevant)**.

---

## 5. Responsive Layout Patterns

### 5.1 Breakpoints
| Token | Min width | Target |
|-------|-----------|--------|
| xs | 0 | Mobile portrait (base, mobile-first) |
| sm | 480px | Large phones |
| md | 768px | Tablet |
| lg | 1024px | Laptop / small desktop |
| xl | 1280px | Desktop |
| 2xl | 1536px | Large desktop |

**Containers:** sm 640 · md 768 · lg 1024 · **xl 1200 (default content max)** · full 1440.
Gutters: 16px (mobile) → 24px (md) → 32px (lg+).

### 5.2 Grid
12-column fluid grid on `lg+`; collapses to **8 cols (md)** and **4 cols (xs/sm)**.
Use CSS Grid with `repeat(auto-fit, minmax(280px, 1fr))` for card collections so the
top-3 match cards reflow 3→2→1 automatically.

### 5.3 Adaptive behavior logic
| Pattern | xs–sm | md | lg+ |
|---------|-------|----|-----|
| Top nav | Hamburger drawer | Condensed inline | Full inline + CTA |
| Sidebar | Off-canvas drawer | Collapsible icon rail | Persistent expanded |
| Match results | 1 col, stacked | 2 col | 3 col side-by-side |
| Pricing tiers | 1 col, Premium first | 2 col | 3 col, Premium raised |
| Intake wizard | Full-screen steps, bottom CTA | 2-pane | 2-pane + live preview |
| Data table | Card list (key:value) | Horizontal scroll | Full table |
| Forms | 1 col | 1 col | 2 col where logical |

**Rules:** Mobile-first; design the smallest layout first and enhance up. Never hide
primary actions behind interactions on mobile — keep the main CTA persistent (sticky bottom
bar). Prefer reflow over horizontal scroll except for true data tables.

---

## 6. Motion Principles

### 6.1 Philosophy
Motion is **functional, not decorative**. It explains spatial relationships (where a panel
came from), confirms actions (a toggle springs), and directs attention (a new match card
fades up). On a technical B2B platform, restraint signals quality — keep UI transitions
**≤300ms** and let only hero moments breathe longer.

### 6.2 Durations
`instant 100` (color/opacity hovers) · `fast 150` (small UI) · `base 200` (default) ·
`moderate 300` (panels, popovers) · `slow 500` (page/section reveal) · `deliberate 800` (hero).

### 6.3 Easing curves
| Token | Curve | Use |
|-------|-------|-----|
| standard | `cubic-bezier(0.2,0,0,1)` | Default for most transitions |
| decelerate | `cubic-bezier(0,0,0,1)` | Entrances (ease-out) |
| accelerate | `cubic-bezier(0.4,0,1,1)` | Exits (ease-in) |
| emphasized | `cubic-bezier(0.4,0,0.2,1)` | Expressive hero moments |
| spring | `cubic-bezier(0.34,1.56,0.64,1)` | Toggles, chips, success — playful overshoot |

### 6.4 Micro-interaction rules
- Buttons: lift `translateY(-1px)` + shadow on hover (150ms); press scales `0.98`.
- Cards: hover raises elevation + 1px border-brand; never move siblings.
- Match score: animate the meter fill on mount (`slow`, decelerate) to reward the result.
- **Always** wrap motion in `@media (prefers-reduced-motion: reduce)` — already enforced
  globally in `tokens.css`.

---

## 7. Accessibility Standards (WCAG 2.1 AA)

### 7.1 Contrast — verified key pairings
| Foreground | Background | Ratio | Verdict |
|------------|------------|-------|---------|
| `#EEF6F3` text | `#070D0B` bg (dark) | **15.8 : 1** | ✅ AAA |
| `rgba(238,246,243,.66)` secondary | `#070D0B` | **~6.4 : 1** | ✅ AA |
| `#14C765` accent | `#070D0B` | **6.9 : 1** | ✅ AA (text & UI) |
| `#04140C` on `#14C765` (button) | — | **6.2 : 1** | ✅ AA |
| `#161E1D` text | `#FFFFFF` (light) | **15.1 : 1** | ✅ AAA |
| `#00713A` brand text | `#FFFFFF` | **5.0 : 1** | ✅ AA |
| `#00B259` on `#FFFFFF` | — | **3.1 : 1** | ✅ AA *large/UI only* — not body text |

**Rule:** never set body text in primary-500/400 on white — use 600/700. The bright accent
is for large text, icons, and UI elements (≥3:1) on dark surfaces.

### 7.2 Targets:
- Text contrast ≥ **4.5:1** (normal), ≥ **3:1** (large ≥24px or ≥19px bold).
- Non-text/UI contrast ≥ **3:1** (borders of inputs, icons, focus rings).
- Touch/click targets ≥ **44×44px**; min 24px with 8px spacing for dense desktop tables.
- Focus: 2px ring at 2px offset using `--lg-focus-ring` — visible on every interactive element.
- Color is never the *only* signal — pair with icon/label (e.g. match-fit uses icon + %).
- Respect `prefers-reduced-motion` (enforced globally) and `prefers-color-scheme`.
- All form fields have programmatic labels; errors use `aria-describedby` + icon + text.
- Min body size 16px on mobile to prevent iOS zoom-on-focus.

---

## How to consume

**Figma / Figma Make:** import `tokens.json` (DTCG format) as variables/styles, then build
components from `figma-components.md`.
**Web:** `@import "tokens.css"` (or link it), set `data-theme` on `<html>`, reference `--lg-*`.
**Style Dictionary / Tailwind:** transform `tokens.json` into your platform's config.

Open `styleguide.html` in a browser for a live, themed preview of the entire system.
