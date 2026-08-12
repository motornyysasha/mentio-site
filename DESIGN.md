---
name: Mentio Orizuru
description: The GEO audit as an origami fold sequence — washi paper ground, vermilion rationed to what acts, one gold dot on the current fold.
colors:
  washi-ground: "#F0EAE0"
  raised-sheet: "#F7F2E9"
  pressed-panel: "#E7DFD2"
  card-on-alt: "#FBF7F0"
  sumi-ink: "#1C1713"
  running-ink: "#4A423A"
  faint-ink: "#847A6E"
  vermilion: "#C73E2A"
  vermilion-deep: "#A93321"
  vermilion-wash: "rgba(199,62,42,.08)"
  fold-gold: "#C9A227"
  crease: "rgba(28,23,19,.35)"
  paper-white: "#fff"
typography:
  display:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: "clamp(2.3rem, 5vw, 3.9rem)"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-.01em"
  headline:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: "clamp(1.7rem, 3.6vw, 2.6rem)"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-.01em"
  title:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: "1.15rem"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif"
    fontSize: ".72rem"
    fontWeight: 700
    letterSpacing: ".14em"
    lineHeight: 1.4
rounded:
  chip: "2px"
  control: "3px"
  card: "4px"
spacing:
  chip-pad: "0.25rem 0.55rem"
  control-pad: "0.85rem 1.35rem"
  card-pad: "1.6rem 1.5rem"
  card-gap: "1.15rem"
  section: "96px 0"
  container-gutter: "28px"
components:
  button-primary:
    backgroundColor: "{colors.vermilion}"
    textColor: "{colors.paper-white}"
    rounded: "{rounded.control}"
    padding: "{spacing.control-pad}"
  button-primary-hover:
    backgroundColor: "{colors.vermilion-deep}"
  button-ghost:
    textColor: "{colors.vermilion}"
    rounded: "{rounded.control}"
    padding: "{spacing.control-pad}"
  button-ghost-hover:
    backgroundColor: "{colors.vermilion-wash}"
  nav-cta:
    backgroundColor: "{colors.vermilion}"
    textColor: "{colors.paper-white}"
    rounded: "{rounded.control}"
    padding: "0.55rem 1rem"
  card:
    backgroundColor: "{colors.raised-sheet}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-pad}"
  tag:
    textColor: "{colors.faint-ink}"
    rounded: "{rounded.chip}"
    padding: "{spacing.chip-pad}"
  tag-new:
    backgroundColor: "{colors.vermilion}"
    textColor: "{colors.paper-white}"
    rounded: "{rounded.chip}"
    padding: "{spacing.chip-pad}"
  input-scan:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.control}"
    padding: "0.7rem 0.6rem"
---

# Design System: Mentio Orizuru

## Overview

**Creative North Star: "The Audit as a Fold Sequence"**

The site is a numbered origami instruction sheet: a business starts as a flat, invisible sheet and the audit folds it, step by step, into a standing crane AI can see. Everything is paper — a warm washi ground with a real kozo fiber grain (an inline SVG fractal-noise tile repeated at 240px on the body and every raised surface), sumi ink for words, and vermilion strictly rationed to what acts or instructs. One gold dot marks the current fold: the scanner. This world explicitly refuses both the dark-SaaS default and the phosphor terminal that preceded it on the `redesign` branch: zero dark surfaces, zero glow, light-only (`color-scheme: light`).

Density is calm and editorial. Sections are folds, numbered in the margin ("Fold 02" … "Fold 11 — the last"), separated by fold-language rules rather than whitespace tricks. The brand's red→orange gradient is quarantined to the logo mark on its paper chip and the favicon; it never colors text or surfaces (`.grad-text` is a legacy class name — it renders flat vermilion).

**Key Characteristics:**
- Warm paper ground with visible fiber grain on every surface tier
- Vermilion appears only on actions, fold numbers, rules, and the crease sheet
- Exactly one gold dot per composition zone marks "the current fold"
- Fold-language line vocabulary: solid = edge, dashed = valley, dash-dot = mountain
- Serif human voice vs. tracked-caps sans machine voice
- Flat, near-square geometry (2–4px radii); light-only, glow-free

## Colors

An ink-on-washi palette: three warm paper tiers, three ink strengths, one rationed vermilion action color, one gold accent dot.

### Primary
- **Vermilion** (#C73E2A): the single action hue. Solid fills on primary buttons, the nav CTA, the scan submit, the demo-bar, and the crease-pattern sheet; text color on fold numbers, ghost buttons, card dash markers, hover states, and the mid-page "answer" emphasis (`.grad-text`); the 1px solid rule under the nav and above the footer. Selection background.
- **Deep Vermilion** (#A93321): pressed/hover state of every vermilion fill; error borders and the torn FAIL mark.
- **Vermilion Wash** (rgba(199,62,42,.08)): ghost-button hover, focus halos (`0 0 0 3px`), inline-code background, blog-item hover tint, the scan chip.

### Secondary
- **Fold Gold** (#C9A227): the current-fold dot only. A 8–9px filled circle rendered as a `::before` pseudo-element. Lives in exactly three places: the hero primary CTA, the BUY buttons, and the scanner panel bar label. Never a fill, never text.

### Neutral
- **Washi Ground** (#F0EAE0): page background, always with the fiber grain image.
- **Raised Sheet** (#F7F2E9): cards, steps, the demo panel, alt sections, nav (at 95% opacity), footer — the "sheet lifted off the ground" tier, also grained.
- **Pressed Panel** (#E7DFD2): empty track of progress and report bars.
- **Card on Alt** (#FBF7F0): card background inside `.alt` sections and code blocks, so sheets stay one tier above their ground.
- **Sumi Ink** (#1C1713): headings, strong text, input text.
- **Running Ink** (#4A423A): body and running text.
- **Faint Ink** (#847A6E): captions, meta, placeholders, disclaimers (4.6:1 on paper).
- **Crease** (rgba(28,23,19,.35)): the universal hairline border and dashed-rule color.
- **Paper White** (#fff): form fields, quiz option buttons, scan-result sheet, the logo chip.

### Named Rules
**The Rationed Vermilion Rule.** Vermilion marks only what acts or instructs — buttons, fold numbers, rules, markers, the sheet. Body copy, headings, and surfaces never turn red; its scarcity is what makes an action legible.

**The One Gold Dot Rule.** Gold exists solely as the current-fold dot. It appears on primary CTAs and the scanner panel bar and nowhere else — never on the nav CTA, never as a text color, never doubled within a component.

**The Gradient Quarantine Rule.** The brand gradient (#E5383B → #FF6B35) lives only inside the logo mark on its white paper chip and the favicon. It never touches text, buttons, or backgrounds.

## Typography

**Display Font:** Source Serif 4 (variable 200–900, with Georgia fallback; self-hosted woff2, latin + latin-ext + cyrillic subsets)
**Body Font:** Source Sans 3 (variable 200–900, with Helvetica Neue/Arial fallback; same subsets)
**Mono Font:** ui-monospace / 'SF Mono' / Menlo — code blocks and inline code only

**Character:** Two voices on one sheet. The serif is the human voice — headlines, questions, names, the big number. The sans is both the running text and, in bold tracked uppercase, the machine/instruction voice that numbers and labels the folds.

### Hierarchy
- **Display** (600, clamp(2.3rem, 5vw, 3.9rem), 1.08): hero H1 only.
- **Headline** (600, clamp(1.7rem, 3.6vw, 2.6rem), 1.18, −.01em): section H2s.
- **Title** (600, ~1rem–1.15rem): card and step H3s; FAQ questions (serif summary at 1.02rem); founder name.
- **Body** (400, 17px base, 1.65): running text in Source Sans 3; paragraphs capped at 68ch, leads at 62ch, answers at 66ch.
- **Label / machine caps** (600–700, .64–.78rem, .09–.2em tracking, UPPERCASE, Source Sans 3): nav links, fold numbers (`data-cmd`), step numbers, tags, panel-bar text, marquee entries, report titles, founder role. Tighter sizes track wider (marquee .68rem at .2em).
- **Serif numerals** (700 serif): the quiz score (3rem) and calculator output (2.2rem) — data spoken in the human voice.

### Named Rules
**The Two-Voice Rule.** Serif speaks to humans (headlines, questions, verdicts, big numbers); bold tracked-caps sans speaks as the instruction sheet (numbers, labels, system text). Never mix the voices inside one element: a serif string is never uppercased and tracked, a machine-caps label is never italic or lowercase.

**The Numbered-Margin Rule.** Every fold announces itself with a vermilion machine-caps number before its content: `data-cmd` fold labels on sections, decimal-leading-zero counters on nav links (`01 · `), `01/02/03` on cards, `fold N` on steps, `01` inside the scan form. Numbering is generated via CSS counters/`attr()` with `/ ""` alt text so screen readers skip the ornament.

## Layout

Single centered column, `max-width: 1120px` with 28px gutters (`.wrap`). Sections are folds: 96px vertical padding, separated top-of-section by a dashed valley rule inset to the gutters; alternating sections use the raised-sheet tier with solid crease borders instead (and suppress their dashed rule — a fold shows either a valley crease or a lifted sheet edge, not both). The hero is a two-column grid (1.05fr / 1fr, 3.4rem gap): serif argument left, scanner panel right; it collapses to one column at 980px.

Grids: 3-up cards (`grid3`), 2-up compare and report-peek, 4-up process steps with dashed connectors between them (desktop only) — all collapsing to a single column at 880px. Interactive blocks (quiz, calc) and prose modules cap at 680px. Rhythm inside modules runs on ~1.15rem gaps.

Breakpoints, as built: **980px** (hero stacks), **880px** (grids stack, burger nav appears, touch targets padded to ≥44px), **640px** (founder card stacks), **480px** (nav and button compaction). Sticky nav: 60px tall, raised-sheet at 95% opacity, 1px solid vermilion bottom edge.

## Elevation & Depth

Depth is paper, not light. Surfaces stack as tiers of the same warm material — ground → raised sheet → white field — each carrying the fiber grain and a 1px crease border. Exactly two soft shadows exist in the whole build: the scanner panel (`0 2px 0 rgba(28,23,19,.06), 0 18px 44px rgba(28,23,19,.08)` — a sheet lifted off the desk) and the mobile nav drop-panel (`0 16px 34px rgba(28,23,19,.12)`). Cards, steps, and every other surface are flat with borders only. Zero glow anywhere.

### Shadow Vocabulary
- **Lifted sheet** (`box-shadow: 0 2px 0 rgba(28,23,19,.06), 0 18px 44px rgba(28,23,19,.08)`): the scanner panel only — the one object physically above the page.
- **Drop panel** (`box-shadow: 0 16px 34px rgba(28,23,19,.12)`): the mobile nav sheet unfolding below the bar.

### Named Rules
**The Two-Shadows Rule.** Only the scanner panel and the open mobile nav cast shadows. New surfaces express depth with the paper tiers and crease borders, never with a new shadow.

## Shapes

Near-square paper geometry: 4px radius on cards, panels, and the demo; 3px on controls, inputs, buttons, and the logo chip; 2px on tags and inline code; 0 elsewhere. No pills except the gold dot and founder avatar, which are true circles. Borders are 1px hairlines in the crease color; emphasis is a 2px solid vermilion border (the GEO card) — never a thicker fill or shadow.

The line itself is the form language. **Fold-language rules: solid = edge** (nav bottom, footer top, PASS underline), **dashed = valley** (section separators, step connectors, FAQ row rules, pre-block borders, scan-chip divider, FAIL underline), **dash-dot = mountain** (`stroke-dasharray: 1 3 6 3` in the crease-sheet SVG; an SVG-tiled dash-dot top border on the calculator output). Result marks reuse it: a PASS row gets a solid 15×3px vermilion crease dash; a FAIL row gets a 15×5px torn mark built from a repeating 105° deep-vermilion gradient.

## Components

### Buttons
- **Shape:** near-square (3px radius), machine-caps label (700, .78rem, .1em, uppercase), .85rem × 1.35rem padding.
- **Primary:** vermilion fill, white text, gold current-fold dot (9px circle) leading the label. Hover: deep vermilion, background-only transition (.15s).
- **Ghost:** 1px vermilion border, vermilion text, transparent. Hover: vermilion wash fill.
- **Nav CTA:** compact primary (.55rem × 1rem) **without** the gold dot.
- **Text/reset buttons** (scan-reset, quiz-restart): borderless faint-ink underlined text, hover to vermilion.
- **Disabled:** opacity .6 + `cursor: wait` (scan submit) or opacity .5 + pointer-events none (quiz CTA).

### Chips / Tags
- **Style:** machine caps (.64rem, .14em), 2px radius, .25rem × .55rem padding; default is faint ink with crease border; `tag-new` inverts to vermilion fill + white.
- **Scan chip** (locked-domain state): vermilion text on vermilion wash with a dashed valley right border.

### Cards / Containers
- **Corner style:** 4px; 1px crease border.
- **Background:** raised sheet with fiber grain; #FBF7F0 when sitting on an alt section.
- **Shadow strategy:** none (see The Two-Shadows Rule).
- **Emphasis variant:** `geo-card` — 2px solid vermilion border.
- **List items:** vermilion em-dash marker (`—`) via ::before; card numbers `01/02/03` in vermilion machine caps.
- **Internal padding:** 1.6rem × 1.5rem (cards), 1.35rem (steps), 1.8rem (founder card).

### Inputs / Fields
- **Style:** white field, 1px crease border, 3px radius, sumi text, faint-ink placeholder; the scan form is a joined strip (vermilion `01` prefix → borderless input → square vermilion submit).
- **Focus:** vermilion border + `0 0 0 3px` vermilion-wash halo (`:focus-within` on the strip; `:focus` on the quiz-site field).
- **Invalid:** deep-vermilion border; the scan strip adds a deep-vermilion halo at .18 alpha.
- **Range sliders:** `accent-color` vermilion; live values echoed in vermilion 700 next to the label.

### Navigation
- **Bar:** sticky 60px, raised sheet @ .95, solid vermilion bottom edge. Links are machine caps (.72rem) with vermilion decimal-leading-zero counters (`01 · `); hover to vermilion; Blog link permanently vermilion. Lang select is a bordered paper control.
- **Mobile (≤880px):** links hide behind a 44px bordered burger; the panel unfolds full-width below the bar (raised sheet, drop-panel shadow, dashed valley rules between rows, its own counter sequence). Escape closes and returns focus.

### Scanner Panel (signature)
The current fold, and the only lifted sheet. 4px panel with the lifted-sheet shadow; a solid vermilion bar labeled in white machine caps with the gold dot. Body stacks: the **crease sheet** — a vermilion 2.4:1 panel (grained) carrying an authored SVG crease pattern in warm paper-white strokes (rgba(255,245,235,.55–.75) → #FFF5EB) that reads flat-sheet → fold arrow → finished crane, using the full fold language (solid edges, `5 4` valley dashes, `1 3 6 3` mountain dash-dot) — then a bold sans lead-in, the scan strip, and a polite live-status line (vermilion 600 when ok). Results print onto a white sheet as **crease/tear rows**: "Already good" titled with a solid vermilion underline, rows marked with the solid crease dash; "Critical — fix these" titled with a dashed deep-vermilion underline, rows marked with the torn 105° dash. (Three hidden `<i>` elements in the bar are residue of the terminal world's traffic lights — not part of this system.)

### Process Steps
4-up raised-sheet cards; `fold N` machine-caps numbers (the word "fold" is CSS-generated with `/ ""` alt); dashed vermilion valley connectors bridging the 1.15rem gaps on desktop.

### Quiz
Card-bound, 680px. Pressed-panel progress track with a vermilion fill animating width (.3s); machine-caps count; serif question (1.25rem, min-height 3em against reflow); white bordered option buttons that hover to vermilion border + wash. Result: serif score (3rem vermilion, faint sans unit), verdict, primary CTA + text restart.

### Calculator
Card-bound, 680px; labeled range rows with vermilion live values; output separated by the **mountain-rule divider** (SVG dash-dot repeat-x top border); serif sumi total (2.2rem), faint sub-line and disclaimer.

### FAQ (guide style)
Borderless `details` rows separated by dashed valley rules; serif summary questions with a vermilion `+`/`–` toggle glyph at the right margin (CSS-generated, `/ ""` alt); answers in running ink at 66ch.

### Founder Card
Raised-sheet card (max 780px): 64px vermilion circle with serif initials, serif name, vermilion machine-caps role, running-ink bio, vermilion text link. Stacks below 640px.

### Footer
Raised sheet above a solid vermilion top edge; faint-ink small text; links in running ink hovering to vermilion; language row in faint ink.

## Do's and Don'ts

### Do:
- **Do** put the fiber grain (`--fiber`) on every paper surface — body, alt sections, cards, steps, the vermilion sheet, founder card, post-CTA. Ungrained paper reads as a different material.
- **Do** number every new fold: a vermilion machine-caps `data-cmd` label on the section, and counters/ordinals on repeated children, generated with the `content: "…" / ""` alt-text pattern.
- **Do** choose the line style by meaning: solid for edges and PASS, dashed for valleys/separators and FAIL tears, dash-dot (`1 3 6 3`) for mountain folds and the calc divider.
- **Do** keep interactions gated: reveal (`foldin`: .55s `cubic-bezier(.2,.7,.3,1)`, translateY 10px + scaleY .96 from the top edge, 90ms stagger capped at 6, classes removed after animationend) and the 46s marquee run only under `prefers-reduced-motion: no-preference`; state transitions stay at .15–.3s on background/border/color/width only.
- **Do** use the vermilion focus treatment everywhere: `outline: 2px solid` vermilion, offset 2px, 3px radius; wash halos on form fields.
- **Do** keep touch targets ≥44px at ≤880px, and keep print styles flat white with ink text (interactive modules hidden).

### Don't:
- **Don't** introduce dark surfaces, glows, or new shadows — depth is paper tiers plus the two existing shadows only.
- **Don't** spend vermilion on passive elements or spend gold anywhere but the current-fold dot (hero primary, BUY buttons, panel bar).
- **Don't** let the brand gradient escape the logo chip and favicon; `.grad-text` renders flat vermilion despite its legacy name.
- **Don't** track, uppercase, or shrink the serif — the human voice stays sentence-case; the machine voice stays sans.
- **Don't** exceed the radius scale (2/3/4px) or swap hairline creases for heavy borders; emphasis is the 2px vermilion border, once per view.
- **Don't** translate CSS-generated ornament into accessible text — every decorative `content` carries the `/ ""` alternative.
