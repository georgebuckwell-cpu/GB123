# VelaSync — Website

A modern, technical, production-ready marketing site for **VelaSync Technology Solutions** — a company that builds websites, CRMs and automated tools, with transparent scaling packages.

Brand personality: **modern + technical**. Dark, teal-immersive UI with a `Space Grotesk` display typeface, `Inter` body, custom SVG graphics, scroll animations and four interactive tools.

---

## Tech & structure

Static, dependency-free HTML/CSS/JS — host anywhere (GitHub Pages, Netlify, S3, any web server). No build step.

```
index.html        Home
services.html     Services
packages.html     Packages  ← the scalable "packages tab" + interactive tools
work.html         Work / portfolio
team.html         Team / skills showcase
contact.html      Contact + FAQ
assets/
  css/styles.css  Shared design system (tokens, components, responsive)
  js/main.js      Shared interaction layer (guards per-page; one file runs everywhere)
  img/logo.svg    VS sail monogram (favicon, nav, loader)
```

A single shared CSS + JS file keeps the system consistent and easy to extend — add a page by reusing the nav/footer markup and existing component classes.

---

## Page-by-page: what each stage accomplishes

### 1. Home (`index.html`) — *capture & orient*
Establish credibility instantly and route visitors to the right next step.
- **Hero** — positioning ("Enterprise tech. Local prices."), floating proof cards, animated stat counters.
- **Services preview** — the four disciplines at a glance → Services.
- **Process timeline** — interactive, scroll-triggered "enquiry → live in 24h" line fill.
- **Why VelaSync** — six credibility cards (speed, awards, traffic, sectors, ML, zero-risk draft).
- **Packages preview** — the two scaling tiers → Packages, plus the savings banner.
- **Locations + CTA** — global reach, then a single clear call to book.

### 2. Services (`services.html`) — *demonstrate capability*
Show depth across the four offerings and prove design skill with bespoke graphics.
- Four detailed service cards (Websites, Custom CRMs, Automated tools, Traffic & growth), each with a **hand-built SVG illustration**, capability checklist and tech tags.
- **Approach** section — how the team works (design-led, built-to-last, measured).

### 3. Packages (`packages.html`) — *convert via clarity & interactivity*  ← core of the brief
The scalable commercial centre of the site.
- **Three tier cards** — Website (£400 + £50/mo), SEO & Growth (£650 + £100/mo), CRM & Automation (custom).
- **Interactive Package Builder** — pick a base tier, stack add-ons, watch the one-off total **and** monthly cost update live. "Request this package" carries intent to Contact.
- **Monthly support comparison** — maintenance vs growth vs custom, benchmarked against agency averages.
- **ROI calculator** — sliders for visitors / order value / conversion rate produce an estimated yearly revenue and a return-on-cost multiple.
- **Why we're affordable** — pre-empts the "what's the catch?" objection.

### 4. Work (`work.html`) — *prove it*
Sales-pitch evidence of design and engineering skill.
- Stat bar (projects, peak users, ranking lift, launch time).
- **Filterable portfolio** (All / Websites / CRM / Automation / Growth) — six project cards with custom SVG mockups and result metrics.

### 5. Team (`team.html`) — *sell the people*
The skills-showcase the brief calls for.
- Four leadership/engineering cards with avatars, achievement lists, **animated skill bars** and award pills.
- Partners & network section for third-party credibility.

### 6. Contact (`contact.html`) — *close*
- Project enquiry **form** with package selector (auto-prefills from `?plan=` links, e.g. `contact.html?plan=growth`) and an inline success state.
- Contact details + "why book now" reassurance.
- **FAQ accordion** handling the top objections (speed, monthly fee, scaling, instalments, who builds it).

---

## Interactive tools (all four from the brief)

| Tool | Where | What it does |
|------|-------|--------------|
| Package builder | `packages.html#builder` | Live-priced configurator (one-off + monthly) |
| ROI / savings calculator | `packages.html#calc` | Slider-driven revenue & return estimate |
| Animated process timeline | `index.html` | Scroll-triggered stage reveal + line fill |
| Filterable portfolio | `work.html` | Category-filtered work showcase |

Plus: scroll progress bar, cursor glow, page loader, animated counters, scroll-reveal, skill bars, FAQ accordion, sticky mobile CTA.

---

## Scaling the packages (how to extend)

The package model is data-driven in the builder. To add or change a package/add-on, edit the `.opt` elements in `packages.html`:

```html
<div class="opt" data-name="New add-on" data-price="250" data-mo="0"> … </div>
```

- `data-price` — one-off cost · `data-mo` — monthly cost · `data-group="base"` — makes it a single-select base tier.
The summary totals recalculate automatically. Update the tier cards and the `<select>` in `contact.html` to match.

---

## Accessibility & performance
- Semantic landmarks, labelled form fields, keyboard-operable controls.
- `prefers-reduced-motion` disables animation.
- No external JS dependencies; fonts preconnected; SVG graphics (crisp, tiny).
