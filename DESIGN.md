---
name: Mentio GEO Terminal
description: A live phosphor-CRT diagnostic terminal — the site is the running audit, not a website about one.
colors:
  crt-ground: "#050807"
  crt-panel: "#070B09"
  phosphor-bright: "#4AFF7F"
  phosphor-running: "#2FBE5F"
  phosphor-dim: "#2FA85C"
  phosphor-ghost: "rgba(74,255,127,.10)"
  machine-rule: "rgba(74,255,127,.28)"
  alert-phosphor: "#FF5C42"
  brand-gradient: "linear-gradient(135deg,#E5383B 0%,#FF6B35 100%)"
  overdrive-white: "#fff"
typography:
  display:
    fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "clamp(1.9rem, 4.6vw, 3.1rem)"
    fontWeight: 800
    lineHeight: 1.18
    letterSpacing: "0"
  headline:
    fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "clamp(1.35rem, 3vw, 1.9rem)"
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: "0.01em"
  title:
    fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "0.95rem"
    fontWeight: 700
    letterSpacing: "0.04em"
  body:
    fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.75
  label:
    fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace"
    fontSize: "0.72rem"
    fontWeight: 700
    letterSpacing: "0.1em"
rounded:
  none: "0"
spacing:
  section: "72px"
  section-final: "88px"
  card-pad: "1.35rem 1.3rem"
  grid-gap: "1rem"
  hero-gap: "3rem"
  gutter: "24px"
components:
  button-primary:
    backgroundColor: "{colors.phosphor-bright}"
    textColor: "{colors.crt-ground}"
    rounded: "{rounded.none}"
    padding: "0.75rem 1.15rem"
  button-primary-hover:
    backgroundColor: "{colors.overdrive-white}"
    textColor: "{colors.crt-ground}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.phosphor-bright}"
    rounded: "{rounded.none}"
    padding: "0.75rem 1.15rem"
  button-buy:
    backgroundColor: "{colors.brand-gradient}"
    textColor: "{colors.overdrive-white}"
    rounded: "{rounded.none}"
    padding: "0.75rem 1.15rem"
  nav-cta:
    backgroundColor: "{colors.phosphor-bright}"
    textColor: "{colors.crt-ground}"
    rounded: "{rounded.none}"
    padding: "0.42rem 0.8rem"
  card-readout:
    backgroundColor: "{colors.crt-panel}"
    textColor: "{colors.phosphor-running}"
    rounded: "{rounded.none}"
    padding: "{spacing.card-pad}"
  input-prompt:
    backgroundColor: "transparent"
    textColor: "{colors.phosphor-bright}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.7rem"
  tag-new:
    backgroundColor: "{colors.phosphor-bright}"
    textColor: "{colors.crt-ground}"
    rounded: "{rounded.none}"
    padding: "0.2rem 0.5rem"
---

# Design System: Mentio GEO Terminal

## Overview

**Creative North Star: "The Audit That Proves Itself"**

The page is not a website describing a diagnostic terminal; it IS one. A P1
phosphor-green session runs on near-black glass, and the visitor lands inside
it mid-boot. Every structural device is a terminal device: sections open with
`$` command lines, leads are `>` prompt output, nav links are numbered jump
targets `[01]–[06]`, cards are framed readouts, the FAQ is `man` pages, the
footer is `── SESSION LOG END ──`. Fixed scanline and vignette overlays sit in
front of everything as the tube's glass. The world explicitly refuses the
category default (dark SaaS hero, gradient glow, rounded card grid).

Hierarchy never changes typeface — one variable mono carries the entire site
(latin, latin-ext, cyrillic, cyrillic-ext for six locales). Importance is
expressed by size steps, weight, uppercase, indentation, and above all by
phosphor intensity: three greens plus glow, from dim chrome to bloom-lit
display. Two ceiling items were consciously declined at finish review:
dot-matrix bitmap display lettering (6-locale readability, incl. cyrillic;
JetBrains Mono is the recorded font concession), curved-glass edge roll-off,
and page-wide 80-column framing. The scanlines/vignette pair and `p{max-width:72ch}`
are the shipped extent of those ideas.

**Key Characteristics:**
- One monochrome phosphor voice; the only non-green ink is the brand alert gradient (logo mark, BUY) and diagnostic FAIL states
- One monospace face at every level; hierarchy = size, caps, indentation, glow
- Zero border-radius anywhere; dashed 1px machine rules divide everything
- Text is the interface: brackets, prompts, counters, and gutters are CSS-generated content
- Motion = phosphor physics: stepped print-in with bloom, blinking block cursors

## Colors

An almost-monochrome phosphor ramp on dark glass, with one alert ink held in reserve for the brand and for failure.

### Primary
- **Bright Phosphor** (#4AFF7F): the lit trace. Headings, links on hover, focused input text, `$` command prefixes, inverse-video fills, cursors, selection background. Almost always paired with a glow (`0 0 6px rgba(74,255,127,.45)`; strong: `0 0 2px …,.9 + 0 0 14px …,.5`).
- **Running Phosphor** (#2FBE5F): body/running text — the default `color` on `body`.
- **Dim Phosphor** (#2FA85C): dimmed history and chrome — nav links at rest, notes, meta, line-number gutters, panel borders (`1px solid`).
- **Phosphor Ghost** (rgba(74,255,127,.10)): faint surface fill — demo title bar, progress-track, chips, blog-item hover, inline code background.
- **Machine Rule** (rgba(74,255,127,.28)): every dashed 1px divider — nav border, section rules, step frames, table cells, `details` separators.

### Secondary
- **Alert Phosphor** (#FF5C42) and the **Brand Gradient** (135deg, #E5383B → #FF6B35): the binding brand ink. The gradient lives only in the logo mark and the BUY action (`.buy-btn`, with an orange glow `0 0 18px rgba(255,107,53,.45)`). The flat alert red carries FAIL titles, `[!!]` markers, and invalid-input borders. This is the contract's one cited deviation: FAIL/error/invalid states share the alert ink because diagnostic semantics require it.

### Neutral
- **CRT Ground** (#050807): the tube's dark page background and input wells.
- **CRT Panel** (#070B09): raised panel ground — `section.alt`, cards, the TTY demo frame. Cards invert grounds inside alt sections (card on alt = #050807).
- **Overdrive White** (#fff): overdriven phosphor. Only as hover state of inverse-video buttons and as text on the gradient BUY button.

### Named Rules
**The One Ink Rule.** Everything on the tube is green. The red→orange alert ink appears in exactly three places: the logo mark, the BUY action, and diagnostic failure states (FAIL, `[!!]`, invalid input). No other element may borrow it.
**The Glow-Is-Hierarchy Rule.** Depth of importance is phosphor intensity: dim → running → bright → bright+glow → bright+strong-glow (display). Never introduce a fourth green or express emphasis with a new hue.

## Typography

**Display/Body/Label Font:** JetBrains Mono (variable, 100–800), with `ui-monospace, 'SF Mono', Menlo, monospace` fallback. Four subset files cover latin, latin-ext, cyrillic and cyrillic-ext — the six locales share one face.

**Character:** One voice at every volume. There is no display face and no UI face; the terminal speaks one mono and modulates size, weight, case and glow. (Dot-matrix bitmap lettering was considered and declined for 6-locale readability; JetBrains Mono is the recorded concession.)

### Hierarchy
- **Display** (800, clamp(1.9rem–3.1rem), 1.18): hero H1 only. Uppercase, strong glow. Emphasis spans use `.grad-text` — which, despite the legacy name, renders bright phosphor + strong glow, not the gradient.
- **Headline** (700, clamp(1.35rem–1.9rem), 1.35): section H2. Uppercase, glow, preceded by its section's `$` command line (`.wrap[data-cmd]::before`, 0.85rem bright).
- **Title** (700, 0.95rem, uppercase, +0.04em): card H3s, founder name. Inside the TTY panel, H2 drops uppercase and glow to read as panel text.
- **Body** (400, 15px base, 1.75): running copy at 0.82–0.9rem inside components; `p{max-width:72ch}`, leads 68ch, answers 70ch.
- **Label** (700, 0.68–0.72rem, +0.1em–0.18em, uppercase): `[nn]` card numbers, `[step n]`, tags, `── framed ──` readout titles, marquee entries, demo-bar caption.

### Named Rules
**The One Face Rule.** JetBrains Mono for everything — headings, prose, labels, buttons, code. A second typeface is a broken tube.
**The Prefix Rule.** Text roles are declared by machine prefixes, generated in CSS, never typed into content: `$ ` command (section openers), `> ` output (leads, card bullets, blog titles), `>> ` status, `? ` question, `man ` FAQ entries, `[01]` nav counters, `[ok]`/`[!!]` verdicts, `▸` ticker items, decimal-leading-zero line gutters.

## Layout

A single 1080px transcript column (`.wrap`, 24px side gutters) scrolling as one continuous session. Sections are 72px vertical blocks (final CTA 88px) separated by full-width 1px dashed machine rules inset to the gutters; every section opens with its `$ command` line, then H2, then a `> ` lead capped at 68ch.

Grids inside the column: hero is 1.05fr/1fr (copy left, TTY panel right, 3rem gap); features `repeat(3,1fr)`; compare 1fr/1fr; process `repeat(4,1fr)`; report-peek 1fr/1fr — all with 1rem gaps. Interactive panels (quiz, calc) cap at 660px, service card at 660px, founder card and post bodies at 760px, FAQ at 800px.

Responsive: 960px stacks the hero; 860px collapses all grids to one column and swaps nav links for a burger-built dropdown panel (44px tap targets, numbered `[01]…` counters preserved); 640px stacks the founder card; 480px compacts nav/buttons (bracket decorations dropped from the nav CTA) and removes the scan-result line-number gutter. Alternating section grounds (`#050807` / `#070B09`) provide the only large-scale rhythm change.

## Elevation & Depth

No drop shadows for elevation — depth is light, not lift. Surfaces are distinguished by the two grounds plus 1px borders (solid dim-phosphor for panels, dashed machine-rule for sub-frames), and importance glows instead of floating. Two fixed overlays render in front of all content: scanlines (`repeating-linear-gradient`, 1px dark line per 3px, multiply, z-90) and a vignette (radial, to rgba(0,0,0,.42), z-91).

### Shadow Vocabulary
- **Glow** (`0 0 6px rgba(74,255,127,.45)`): standard phosphor bloom on primary buttons, focused prompt, lit tags, progress bars.
- **Strong glow** (`0 0 2px rgba(74,255,127,.9), 0 0 14px rgba(74,255,127,.5)`): display text and score numerals only.
- **Panel aura** (`0 0 0 1px rgba(74,255,127,.06), 0 0 34px rgba(74,255,127,.07), inset 0 0 60px rgba(74,255,127,.03)`): the TTY demo frame — screen-glow, not elevation.
- **Alert glow** (`0 0 18px rgba(255,107,53,.45)`, hover `0 0 30px …,.7`): the BUY button; invalid inputs glow `0 0 10px rgba(229,56,59,.4)`.

### Named Rules
**The Light-Not-Lift Rule.** Nothing casts a shadow downward; elements emit light outward. (The one exception, the mobile nav dropdown's `0 18px 40px` black shadow, exists to separate the panel from page content and is not a pattern to extend.)

## Shapes

Zero border-radius, everywhere, explicitly: `border-radius:0` is re-declared on every control that browsers would otherwise round (inputs, buttons, selects, chips, bars). Frames are rectangles: 1px solid dim-phosphor for primary panels (cards, demo, founder), 1px dashed machine-rule for secondary frames (steps, pre blocks, scan results, tags). Enclosure is typographic where possible — buttons wear generated `[ ]` brackets, numbers wear `[ ]`, readout titles wear `── ──` rules. Blocks that would be icons are glyphs (`▊` cursor, `▸` ticker, `↺` reset) or plain 8px squares (demo-bar "lights").

**The Zero-Radius Rule.** No rounded corners exist in this world. The only curves on screen are inside letterforms and the brand mark.

## Components

### Buttons (bracket commands)
- **Shape:** square (0 radius); label wrapped in generated `[ ` / ` ]` brackets; 700 weight, 0.88rem, no wrap.
- **Primary (inverse-video):** bright phosphor fill, CRT-ground text, glow (`.75rem 1.15rem`). Hover: overdrives to #fff with `0 0 18px rgba(74,255,127,.7)`.
- **Ghost:** transparent, `1px solid` dim-phosphor border, bright text. Hover: border brightens, text glows.
- **BUY (alert action):** the brand gradient fill, white text, orange glow; hover deepens the glow only. Exactly one purchase action per surface wears this.
- **Text-reset:** bare underlined dim text (`.scan-reset`, `.quiz-restart`), `↺` prefix where it re-runs a scan.

### Status-line Nav
- Sticky 52px bar on rgba(5,8,7,.94), dashed bottom rule. Logo = gradient mark + wordmark + blinking `▊` cursor. Links are dim, auto-numbered `[01]–[06]` via CSS counters; hover lifts to bright + glow. Language `<select>` is a square bordered field. CTA is a small inverse-video block with brackets. ≤860px: links hide behind a bordered burger; JS builds a dropdown panel repeating the numbered counters with 44px rows.

### TTY Panel (the scanner) — signature
- `.demo` frame: panel ground, solid dim border, panel-aura glow. Title bar: ghost fill, three 8px squares (first lit), `tty1 — ` caption at 0.7rem/+0.12em caps.
- **Boot transcript** (JS-built): 0.78rem dim lines with decimal-leading-zero gutters, printing in at 380ms intervals; final line is a bright `> type your domain to begin` prompt with a glowing block cursor blinking at 1.1s `steps(1)`. The cursor freezes to 20% opacity while the real input is focused — attention passes to the live caret.
- **Prompt input:** a `$`-prefixed row (CRT-ground well, dim border → bright border + glow on focus-within); transparent input with bright text and phosphor caret; inverse-video submit button. Invalid: alert border + red glow. Stage 2 swaps in a `✓ domain` ghost chip and a contact placeholder.
- **Scan transcript rows:** dashed-framed well, `── PASS ──` (bright, glow) and `── FAIL ──` (alert) group titles; rows carry `[ok]`/`[!!]` markers left and decimal-leading-zero gutters, printing in staggered 140ms.

### Framed Readouts (cards)
- Panel ground (inverted inside alt sections), solid dim border, 0 radius, `1.35rem 1.3rem` padding. `[nn]` label, uppercase title, `> `-prefixed list rows. The featured card (`.geo-card`) brightens its border and gains a wide soft glow. Score bars are 9px ghost tracks with glowing phosphor fills and tabular-numeral values.

### Inputs / Fields
- Square, CRT-ground fill, dim solid border, mono bright text. Focus: bright border + glow, no default outline (elsewhere, focus-visible = `2px solid` phosphor outline, offset 2px — the keyboard block cursor). Invalid: alert border. Range inputs use `accent-color` phosphor.

### Man-page FAQ
- Borderless `details` separated by dashed rules; summary prefixed `man ` in dim, toggled by `[+]`/`[-]` at the right edge; answers are 0.85rem running text at 70ch.

### Marquee (signal ticker)
- Dashed-ruled strip; 0.72rem dim caps at +0.18em with `▸` prefixes; 42s linear loop.

### Motion (print-in grammar)
- Content prints onto the tube: `.pline.in` runs `printin` — 0.5s, `steps(6)`, from bright-bloom blur (`brightness(2.2) blur(1px)`) to rest. JS staggers siblings 90ms apart (capped at 6 steps); scan rows 140ms; boot lines 380ms. Cursors blink at 1.1s `steps(1)`. All entrance motion is gated behind `prefers-reduced-motion: no-preference`; scan step delays collapse from 950ms to 50ms when reduced.
- **The Stepped-Motion Rule.** Nothing eases smoothly into view; phosphor prints in discrete steps and blooms. Continuous easing is reserved for utility movement (progress bar width, marquee scroll, color/glow transitions at 0.15s).

## Do's and Don'ts

### Do:
- **Do** open every new section with a `$ command` line via `data-cmd` on `.wrap`; it is the section's kicker, natively in-world.
- **Do** express every new state in the phosphor ramp first; reach for alert ink only for failure semantics or the single purchase action.
- **Do** generate all prefixes, brackets, counters and gutters in CSS (`::before`/`::after`, counters) so content stays plain text.
- **Do** keep interactive tap targets ≥44px under 860px, and re-declare `border-radius:0` on any new form control.
- **Do** gate every entrance animation behind `prefers-reduced-motion` and give JS-driven sequences a reduced fast path.

### Don't:
- **Don't** introduce a second typeface, a fourth green, or any rounded corner.
- **Don't** use drop shadows for elevation; light glows outward, panels separate by ground + border.
- **Don't** put the brand gradient on anything but the logo mark and the BUY action; `.grad-text` is phosphor+glow despite its name — never restyle it as an actual gradient.
- **Don't** reintroduce the declined ceiling items as if they were pending work: dot-matrix display lettering, curved-glass edge roll-off, and page-wide 80-column framing were consciously declined at finish review.
- **Don't** use pictorial or glyph-font icons; the world's iconography is characters (`▊`, `▸`, `↺`, `[ok]`, `[!!]`) and bare squares.


## Amendment 2026-08-12 — readability pass (owner feedback: "one canvas, hard to read")

- New token `--ink: #D8EFE0` (white-hot phosphor) carries ALL running text (body, cards, leads, FAQ answers, bios, blog paragraphs, labels). Physically in-world: phosphor driven hard blooms to white at the core. Green stays for headings, accents, chrome, and machine labels. Contrast: ~16:1 on #050807.
- One Ink rule unchanged in spirit: the ink ramp is now dim-green -> mid-green -> bright-green -> white-hot; the alert gradient remains the only non-green ink.
- Section separation: 88px padding; `.alt` sections use #0A100C with solid 1px frame lines rgba(74,255,127,.16); cards use #0B130E with rgba(74,255,127,.34) border + drop shadow; scanlines quieted to rgba(0,0,0,.09)/4px pitch.
- Type: base 16px/1.7; h2 up to clamp(1.5rem,3.4vw,2.2rem); leads 1.02rem.


## Amendment 2026-08-12b — technical-audit pass (14/20 baseline, 20 findings fixed)

- BUY buttons: text ink is `--crt` on the alert gradient (white failed AA at the orange stop).
- Motion: `mscroll`, both `blink` cursors and `scroll-behavior:smooth` now sit behind `prefers-reduced-motion: no-preference`; marquee pauses on hover; quiz count-up skips under reduce. Scanline overlay lost `mix-blend-mode:multiply` (compositor cost) — visual delta negligible.
- Landmarks: skip-link (`.skip`, inverse block on focus) + `<main id="main">` on all 6 homepages; `color-scheme:dark` + `theme-color` metas on all 46 pages.
- Live regions: scan results `role="status"`; quiz question `aria-live=polite`; verdict `role=status`; focus managed on quiz finish/restart and burger Escape.
- Tokens: `--panel/--card-bg/--card-alt` promoted from amendment literals; report-peek code sample recolored to tokens (fourth green removed).
- Touch targets: nav CTA/burger/lang-select ≥44px mobile; footer links padded.
- Print block added (palette near-black on paper). Known detector false positive: `rgb(0,0,0)` reported on the off-screen skip link — its computed color is `--crt`; the detector cannot resolve colors of off-viewport elements.
- Dead weight removed: Inter/Space Grotesk woff2 files, unused JS vars, legacy hooks.


## Amendment 2026-08-12c — re-audit pass (17/20 -> fixes)

Re-audit caught a scoping regression from the previous batch: `reduced` was read in the quiz module but declared in the first IIFE — quiz finish crashed (score never rendered, CTA unbuilt). Fixed: each module derives its own live-updating reduced-motion flag (matchMedia change listener). Also: calc sliders got label/for associations (x6 locales), scan results now insert an EMPTY role=status container before rows (announce-order correctness), quiz verdict role set at bind, quiz inputs aria-label + aria-invalid, scan errors aria-describedby, marquee-rule suppressor re-anchored inside main, .demo-bar aria-hidden, logo >=24px target, lang-select keeps the global focus outline, pre inherits --mono. Lesson recorded: shared state between the two IIFEs must travel through window.__mentioLead, never ambient scope.


## Amendment 2026-08-12d — third-audit polish (18/20 baseline)

- Boot transcript and burger button now ship in static HTML (JS animates/wires only) — hero and nav CLS eliminated.
- Decorative pseudo-prefixes (counters, brackets, $-prompts, man/PASS/FAIL/[ok] markers, footer session line) carry the alt-text mute (content: X / "") as a second declaration — legacy engines keep the visible form, AT skips the noise.
- Quiz hint: id + role=status + aria-describedby wiring (parity with the scanner); quiz CTA toggles aria-disabled.
- .tag-old at full opacity (6.17:1). Dead residue removed: --alert2, .founder-name, pre-span flattener, unreachable localStorage branch.
- Scan rows insert via setTimeout(0) after the empty role=status container (order-correct for AT, background-tab safe).
- Accepted as documented: lang-select navigates on pointer change (keyboard guarded); GoatCounter unpinned (prod CSP allowlists its origin).
