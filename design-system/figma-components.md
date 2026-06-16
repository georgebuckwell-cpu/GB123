# Line Guide — Figma Component Documentation

**v1.0.0** · Build these as Figma components with variants & component properties. Every spec
references tokens from `tokens.json` / `tokens.css` (the `--lg-*` names). Default theme = **dark**.

> **Figma setup conventions**
> - Use **Variant properties** for `variant`, `size`, `state`. Use **Boolean** props for
>   optional slots (icon, badge). Use **Instance swap** for icons/avatars.
> - Name layers semantically (`leading-icon`, `label`, `trailing`) and bind colors/spacing to
>   Variables so theme switching works via mode.
> - State `focus-visible` = the keyboard focus ring `--lg-focus-ring`. Pointer hover is separate.
> - All measurements in px; radii/space map to tokens.

---

## Foundations recap (for component binding)
- **Radii:** sm 6 · md 10 · lg 16 · xl 22 · 2xl 28 · full
- **Space:** 4·8·12·16·20·24·32·40·48·64 …
- **Durations:** 100/150/200/300/500/800ms · **Easing:** standard `(0.2,0,0,1)`, spring `(0.34,1.56,0.64,1)`
- **Focus ring:** 2px brand ring + 2px offset (`--lg-focus-ring`)

---

# ACTIONS

## 1. Button
**Anatomy:** `[leading-icon?] label [trailing-icon?]` in a flex row, `gap 8`.
**Props:** `variant` (primary · secondary · tertiary · ghost · destructive), `size` (sm · md · lg),
`leadingIcon` (bool), `trailingIcon` (bool), `state`, `fullWidth` (bool).

| Size | Height | Padding-x | Text | Radius | Icon |
|------|--------|-----------|------|--------|------|
| sm | 32 | 12 | sm (14) | md (10) | 16 |
| md | 40 | 16 | sm/base | md (10) | 18 |
| lg | 48 | 20 | base (16) | md (10) | 20 |

**Variant styling (dark theme):**
| Variant | Fill | Text | Border |
|---------|------|------|--------|
| primary | `--lg-brand-fill` #14C765 | `--lg-text-on-brand` #04140C | none |
| secondary | transparent | `--lg-text-primary` | 1px `--lg-border-strong` |
| tertiary | `--lg-bg-overlay` | `--lg-text-primary` | none |
| ghost | transparent | `--lg-text-secondary` | none |
| destructive | `--lg-error-solid` | #fff (dark: #1a0606) | none |

**States:**
- **hover:** primary → `--lg-brand-fill-hover`; lift `translateY(-1px)` + `--lg-shadow-sm`; ghost/secondary → bg `--lg-bg-hover`. 150ms standard.
- **focus-visible:** `--lg-focus-ring`.
- **active:** `scale(0.98)`, remove lift. 100ms.
- **disabled:** opacity 0.4, no pointer events, no shadow.
- **loading:** swap leading icon for 16px spinner, label stays, `aria-busy`, pointer disabled.

**Usage:** One primary action per view. Destructive only for irreversible actions, paired with a
confirm dialog. Use `fullWidth` on mobile sticky CTA bars.

## 2. Icon Button
Square, icon-only. Sizes 32/40/48 → radius md, icon 18/20/24. Variants ghost (default), tertiary,
primary. **Must** carry an `aria-label`. Same state model as Button. Use for toolbar/table-row actions.

## 3. Button Group / Segmented Control
Row of 2–5 connected buttons sharing one outer border, radius md, inner dividers `--lg-border-subtle`.
**Segmented** = single-select toggle (e.g. *Best fit | Price | Rating* sort). Selected segment:
fill `--lg-brand-soft`, text `--lg-brand-text`, 2px inset indicator. `role="tablist"`/`radiogroup`.

## 4. Link
Inline text action. Default `--lg-secondary-400` (Ion Blue) on dark / `--lg-secondary-600` on light;
underline on hover (offset 2px). Standalone "learn more" links may use brand text + trailing arrow
that nudges `+2px` on hover (150ms). Visited state only for content links, not app navigation.

---

# FORMS

## 5. Text Input
**Anatomy:** `[leading-icon?] field [trailing-icon/clear?]`. Height 40 (md) / 48 (lg), padding-x 12,
radius md, bg `--lg-bg-surface`, border 1px `--lg-border-default`, text base.
**States:** hover → border `--lg-border-strong`; focus → border `--lg-primary-400` + `--lg-focus-ring`;
filled → text-primary; error → border `--lg-error-solid` + error text below; disabled → opacity 0.4;
read-only → no border, bg transparent. Placeholder = `--lg-text-tertiary`.

## 6. Textarea
As Text Input; min-height 96, resize-vertical only, padding 12. Optional character counter (xs,
`--lg-text-tertiary`) bottom-right; turns `--lg-warning-text` at 90%, `--lg-error-text` over limit.

## 7. Select (native-styled)
Text-Input shell + trailing chevron (18). Open → chevron rotates 180° (200ms). Menu = Dropdown (#37).
Placeholder until chosen. Supports option groups for use-case categories.

## 8. Combobox / Search Select
Typeahead input + filtered popover list. Matched substring bolded. Keyboard: ↑/↓ move, Enter select,
Esc close. Multi-select variant renders chips (#16) inside the field. Empty result → inline Empty State.

## 9. Checkbox
16×16 box, radius sm(4 here), border 1.5px `--lg-border-strong`. Checked → fill `--lg-brand-fill`,
white check, spring pop (200ms). Indeterminate → dash. Focus ring around box. Label sm, gap 8,
whole row clickable (≥44px hit area).

## 10. Radio
16×16 circle, same border. Selected → 2px brand ring + 8px brand dot, spring. Group with
`role="radiogroup"`. Use for mutually exclusive intake answers (e.g. *New line vs. retrofit*).

## 11. Switch / Toggle
Track 36×20 radius full. Off → `--lg-border-strong` track, knob `--lg-neutral-300`. On → track
`--lg-brand-fill`, knob white slides 16px (200ms spring). Use for settings/instant toggles, never
for form submission choices (use checkbox/radio).

## 12. Slider — Budget Range
Track h4 radius full, filled portion `--lg-brand-gradient`. Handles 20px circle, `--lg-shadow-sm`,
focus ring on handle. Single or **dual-thumb range** for budget min/max. Live value bubble (mono)
above active thumb. Step ticks optional. Used in intake for budget; format £ with thousands.

## 13. Stepper (numeric)
`[−] value [+]`. Buttons = Icon Button sm, center field 56px mono, centered. Clamps to min/max,
disables the relevant button at bounds. Used for quantities / line counts.

## 14. Form Field (wrapper)
**Anatomy:** `label` (sm, medium) → `[control]` → `help-text` (xs, tertiary) **or** `error-text`
(xs, error + 14px alert icon). Required → `*` in `--lg-error-text`. Spacing: label→control 6,
control→help 6. Binds `for`/`id`/`aria-describedby`. This is the standard wrapper for #5–13.

## 15. Filter Chip
Pill (radius full), height 32, padding-x 12, sm text. Default: border 1px `--lg-border-default`,
text secondary. Selected: bg `--lg-brand-soft`, border `--lg-border-brand`, text `--lg-brand-text`,
leading check (14). Removable variant adds trailing × (Icon Button xs). Used for use-case &
result filtering. `role="button"` / `aria-pressed`.

---

# DATA DISPLAY

## 16. Tag
Static label pill, height 24, padding-x 8, xs text, bg `--lg-bg-overlay`, text secondary. Non-interactive
metadata (e.g. *Packaging*, *Robotics*). Color variants map to semantic/tier soft backgrounds.

## 17. Badge
Small status indicator. Two shapes: **dot** (8px, paired with label) and **pill** (height 20,
padding-x 8, xs, uppercase tracking-caps). Semantic color sets: success/warning/error/info using
`*-bg` + `*-text` + 1px `*-border`. Count variant = circle for notifications.

## 18. Tier Badge *(product)*
Pill marking subscription tier. **Basic** slate flat · **Premium** brand gradient, white text ·
**Ultra** iridescent gradient + subtle sheen sweep on hover (spring). Leading 14px tier glyph.
Appears on profile cards & match ribbons.

## 19. Avatar / Company Mark
Square-rounded (radius md) for **company logos**; circle for people. Sizes 24/32/40/48/64.
Fallback: brand-soft bg + 2-letter initials (Space Grotesk). Optional status dot (online/verified)
bottom-right. **Verified** suppliers get a brand check overlay.

## 20. Tooltip
Dark `--lg-bg-overlay` surface, radius sm, padding 8×6, xs text, `--lg-shadow-md`, 6px arrow.
Appears after 400ms hover / on focus; fades 150ms. Max-width 240. For supplementary info only —
never essential content (not keyboard-dwell accessible on touch).

## 21. Rating (stars)
5 stars, 16px (compact) / 20px (default). Filled `--lg-warning-solid` (amber), empty
`--lg-border-strong`; supports half-star. Trailing numeric (mono, e.g. `4.8`) + count `(124)` in
tertiary. Interactive variant for leaving reviews (hover preview + keyboard ←/→).

## 22. Match-Score Meter *(product, signature component)*
Communicates supplier fit for the buyer's use case. **Radial** (donut, 64/96px) or **linear** (bar).
Track `--lg-bg-hover`; fill `--lg-brand-gradient`. Center/label = % (mono, 2xl) + caption "fit".
Thresholds add an icon + word so meaning isn't color-only: ≥85 "Excellent fit" ✓ · 65–84 "Strong"
· <65 "Partial" (warning). Animates fill on mount (slow, decelerate). `role="meter"` with aria values.

## 23. Stat / Metric
KPI block: value (Space Grotesk 3xl) + label (xs uppercase tertiary) + optional delta (▲/▼ with
success/error). Mono for numbers. Used on dashboards (active matches, response rate, profile views).

## 24. Data Table
Header row (sm, medium, tertiary, uppercase optional), rows h48, zebra optional via `--lg-bg-surface`,
1px `--lg-border-subtle` row dividers. Sortable headers show chevron + are buttons. Sticky header on
scroll. Row hover `--lg-bg-hover`. Selectable rows = leading checkbox. Numeric cells right-aligned,
mono. **Responsive:** below md collapse each row into a key/value card list.

## 25. Progress Bar
Linear determinate (h6, radius full, fill brand) or indeterminate (animated sweep). For uploads,
multi-step completion. Pair with % label (mono) for determinate. Distinct from Match-Score Meter.

## 26. Skeleton
Loading placeholder. Shapes: line (h12, radius sm), block, circle. Shimmer = gradient sweep
`--lg-bg-surface → --lg-bg-hover`, 1.2s loop, **paused under reduced-motion** (static surface).
Mirror the real content's layout to prevent shift.

---

# CONTAINERS

## 27. Card (base)
bg `--lg-bg-surface`, border 1px `--lg-border-subtle`, radius lg, padding 24, `--lg-shadow-sm`.
Optional header / media / body / footer slots. Hover (interactive cards only): border
`--lg-border-brand`, `--lg-shadow-md`, lift `-2px` (200ms). Never reflow neighbours on hover.

## 28. Manufacturer Profile Card *(product)*
**Anatomy:** Avatar/logo (48) + name (lg, display) + Tier Badge → Rating row → 2-line capability
summary → capability Tags → footer: Match-Score Meter (compact) + primary "View profile" + ghost
"Save". Verified check by name. lg variant adds cover strip with brand gradient wash.

## 29. Tier Pricing Card *(product)*
For Basic / Premium / Ultra subscription. **Anatomy:** tier name (xl display) + price (Space Grotesk
4xl, mono digits) + `/mo` + feature list (check rows) + CTA Button (fullWidth). **Premium** is the
recommended/raised card: `--lg-shadow-lg`, 1.5px brand border, "Most popular" Badge top-right, lifted
−8px on lg. **Ultra** uses iridescent border + Ultra gradient CTA. Responsive: stack 1-col mobile
(Premium first), 3-col lg.

## 30. Match Result Card *(product, top-3)*
The headline output. Ranked variant (`rank` prop 1–3): rank chip (#1 brand-gradient, #2/#3 neutral)
top-left. Contains Manufacturer summary + prominent Match-Score Meter (radial) + "why this match"
chip list (budget ✓ / timeframe ✓ / capability ✓) + CTA "Connect". #1 card gets `--lg-shadow-glow`.
Layout: 3-up (lg) → 2-up (md) → stacked (sm), rank order preserved.

## 31. Tabs
Tab list (sm/base, medium) with active = `--lg-text-primary` + 2px brand underline indicator that
**slides** between tabs (250ms standard). Inactive = secondary. Underline or pill style. `role="tablist"`,
arrow-key navigation, `aria-selected`. Panels lazy-mount.

## 32. Accordion
Header row (base, medium) + chevron that rotates 180° on expand. Body expands height (300ms standard).
1px `--lg-border-subtle` between items. Single- or multi-open. Used for FAQ, profile spec sections.
`aria-expanded` + `aria-controls`.

---

# NAVIGATION

## 33. Top Nav
Height 64, bg `rgba(7,13,11,.75)` + `backdrop-blur(24px)`, bottom border `--lg-border-subtle`.
**Anatomy:** logo (left) · nav links (center/left) · search · theme toggle · primary CTA + Avatar (right).
Link hover → text-primary + brand underline grow (200ms). Scrolled state → opaque bg. Sticky, z-nav.
**Responsive:** below md collapse links into hamburger → Drawer (#35).

## 34. Sidebar Nav
Width 264 (expanded) / 72 (rail). Item = icon (20) + label (sm) + optional badge, h44, radius md.
Active: bg `--lg-brand-soft`, text `--lg-brand-text`, 2px leading brand bar. Hover `--lg-bg-hover`.
Section headers xs uppercase tertiary. Collapsible to icon rail (tooltips on hover). For dashboards.
**Responsive:** off-canvas Drawer below lg.

## 35. Drawer / Sheet
Off-canvas panel from left (nav) / right (filters, details) / bottom (mobile actions). Width 320–400
(side) or auto (bottom). Slides in 300ms decelerate; scrim `rgba(0,0,0,.5)` fades in. Close on scrim
click / Esc. Traps focus. Mobile filter panels and the mobile menu use this.

## 36. Breadcrumb
sm text, tertiary links + `/` or chevron separators (12, border color), current page = text-primary
non-link. Collapses middle items to `…` menu below md. `aria-label="Breadcrumb"`.

## 37. Pagination
Prev / numbered pages / Next as Icon/text Buttons sm. Current page = brand-soft fill + brand text.
Truncate with `…`. Optional "rows per page" Select + range label (mono). Below md → Prev/Next + "Page x/y".

## 38. Footer
bg `--lg-bg-surface`, top border subtle, padding 64/32. Columns: brand + tagline, Product, For
Suppliers, For Buyers, Company, legal. Link hover → text-primary. Bottom strip: copyright (xs tertiary)
+ socials + theme toggle. Collapses to stacked accordion-style columns on mobile.

---

# OVERLAYS

## 39. Dropdown Menu
Popover list, bg `--lg-bg-overlay`, radius lg, `--lg-shadow-lg`, padding 6. Items h36, radius md,
hover `--lg-bg-hover`, leading icon + label + optional trailing shortcut/check. Dividers + section
labels. Origin-aware scale+fade in (150ms). Arrow-key nav, Esc close, focus trap. Powers Select/menus.

## 40. Modal / Dialog
Centered panel, max-width 480 (sm) / 640 (md) / 800 (lg), bg `--lg-bg-overlay`, radius xl, padding 32,
`--lg-shadow-xl`. Scrim `rgba(0,0,0,.6)` + `backdrop-blur(4px)`. **Anatomy:** title (xl display) +
close Icon Button + body + footer actions (ghost cancel + primary confirm, right-aligned). Enter:
scale 0.96→1 + fade (200ms standard); scrim fades. Focus trapped, returns to trigger on close.
`role="dialog"` `aria-modal`. Esc + scrim close (suppress Esc for destructive confirms).

## 41. Toast / Notification
Bottom-right stack (top on mobile), width ≤400, bg `--lg-bg-overlay`, radius lg, `--lg-shadow-lg`,
leading semantic icon + message + optional action link + close. Slides in 300ms decelerate, auto-
dismiss 5s (pause on hover), exit accelerate. `role="status"` (polite) / `alert` for errors. Max 3 visible.

## 42. Alert / Banner
Inline contextual message. Semantic bg `*-bg` + 1px `*-border` + leading icon + title/body + optional
actions + dismiss. Full-width page banner variant (e.g. "Launching soon — join early access") uses
brand gradient. radius md (inline) / 0 (page banner). Not auto-dismissing.

---

# FEEDBACK & FLOWS

## 43. Spinner
Circular indeterminate, brand stroke, sizes 16/20/24/40. 0.8s linear rotation. Under reduced-motion,
swap for a pulsing dot. Always paired with `aria-label`/`aria-busy`. Inline (button) or centered (page).

## 44. Empty State
Centered: illustration/icon (48–64, brand-soft circle) + title (xl display) + supporting text (sm,
tertiary, max 40ch) + primary action. Variants: no-results (search), no-data (first run), error.
Used in Combobox results, dashboard sections, saved-suppliers.

## 45. Intake Wizard / Stepper *(product, core flow)*
Multi-step buyer intake: **Use case → Application detail → Budget → Timeframe → Review → Matches**.
**Anatomy:** step indicator (numbered nodes connected by a progress line; complete = brand fill +
check, current = brand ring, upcoming = neutral) + step title + form content + footer (Back ghost /
Next primary, Next disabled until valid). Progress line animates between steps (300ms). Mobile:
full-screen steps, indicator condenses to "Step 3 of 6" + thin Progress Bar, sticky bottom CTA.
`aria-current="step"`. Final step transitions to the 3-up Match Result Cards.

## 46. Hero Search Bar *(product)*
Large entry point ("Search. Compare. Find the right suppliers."). Height 56–64, radius full or xl,
bg `--lg-bg-overlay`, 1.5px border, `--lg-shadow-lg`. Leading search icon (20) + input (lg) +
optional category Select divider + primary "Search" Button. Focus → border brand + `--lg-shadow-glow`.
Suggestions render as Dropdown. The marquee component of the landing page.

---

## Component → token quick map
| Concern | Tokens |
|---------|--------|
| Brand fills/CTAs | `--lg-brand-fill`, `--lg-brand-gradient`, `--lg-brand-fill-hover` |
| Surfaces (elevation) | `--lg-bg → surface → raised → overlay → hover` |
| Text hierarchy | `--lg-text-primary / secondary / tertiary / disabled` |
| Borders | `--lg-border-subtle / default / strong / brand` |
| Status | `--lg-{success,warning,error,info}-{solid,bg,border,text}` |
| Tiers | `--lg-tier-{basic,premium,ultra}` (+ `-grad`) |
| Focus | `--lg-focus-ring` |
| Motion | `--lg-duration-*`, `--lg-ease-*` |

**Build order recommendation:** tokens → primitives (Button, Input, Badge, Avatar, Card) →
product components (Match-Score Meter, Match Result Card, Tier Pricing Card, Intake Wizard) → pages.
