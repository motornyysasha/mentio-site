# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Small-business owners worldwide (restaurants, clinics, shops, local services, small B2B) — non-technical people who have heard customers now "ask ChatGPT" and worry they are invisible there. They arrive from LinkedIn posts, blog articles, or a shared link, usually knowing nothing about GEO. Secondary audience: the developers/freelancers who will implement the fixes from the audit report.

## Product Purpose

Mentio sells exactly one service: a €99 one-time GEO audit — a diagnosis of how visible a business is to AI assistants (ChatGPT, Perplexity, Gemini, Google AI Overviews, Bing Copilot) plus a complete, developer-ready fix plan with copy-paste code. Success = the visitor either runs the free on-site check (lead) or buys the audit (sale). Delivery: report by email within 2 business days.

## Positioning

"Honest measurement" — a QA engineer's discipline applied to AI visibility. No guaranteed citations (explicitly stated: nobody controls AI output), no packages, no upsells, no retainer. The company runs its own audit on itself and publishes the scores, including the embarrassing first one (53/100 → 77/100 series in the blog). A neighboring agency could not truthfully copy the self-audit paper trail.

## Operating Context

Static site (GitHub Pages behind Cloudflare) in 6 languages: EN at root, UA/DE/FR/PL/ES in subfolders. Blog (16 posts EN + UA mirrors) is a core proof asset. The hero contains a REAL scanner: a Cloudflare Worker fetches the visitor's robots.txt/llms.txt/homepage and returns genuine findings, then captures a lead to Telegram. Also on page: 7-question quiz, loss calculator, FAQ, founder section, Stripe payment link (static href).

## Capabilities and Constraints

- CSP has no 'unsafe-inline' for scripts: NO inline event handlers ever; all JS lives in assets/site.js. Inline style="" attributes are allowed.
- Everything must stay server-rendered static HTML — GEO/SEO is the product's own proof; JSON-LD schema graph (Organization, Person/founder, ProfessionalService+Offer, FAQPage, speakable, BreadcrumbList), llms.txt, hreflang ×6 must survive any redesign.
- Self-hosted fonts only (GDPR; current: Inter + Space Grotesk variable woff2 — replaceable, but any new face must be self-hostable webfonts).
- After changing assets/style.css or site.js: run `python3 bump-assets.py` before commit.
- Functional units that must keep working: hero scanner (stays in the hero per owner decision), quiz, calculator, buy buttons (static Stripe hrefs), language switcher, burger nav, lead relay.
- All texts and their 6-language localizations are preserved; copy changes are out of redesign scope.
- Redesign ships on branch `redesign` only; production (main) untouched until owner approves.

## Brand Commitments

- Name: Mentio. Logo mark is BINDING: two vertical bars + underline in red→orange gradient (#E5383B→#FF6B35), used across 6 external profiles — never a generic "M". The mark and its gradient stay; everything else (palette beyond the mark, typography, theme, composition, motion) is open.
- Light vs dark theme: owner delegated to design judgment.
- Owner's stated direction for the redesign: "much more technological, more beautiful — a visitor should instantly see it was made by professionals, not an amateur."
- Voice (preserved in existing copy): direct, honest, anti-hype; consequences over jargon; no fake urgency, counters, or invented logos.

## Evidence on Hand

- Real self-audit score series 53 → 71 → 77 with published method (blog: /blog/geo-score-53-to-71/), per-platform scores (AIO 82, ChatGPT 80, Copilot 78, Perplexity 74, Gemini 72).
- Working live scanner (the product demonstrates itself).
- Founder: Oleksandr Motornyy, QA background, LinkedIn public; uses "OM" monogram by choice — no photo, do not add one.
- ZERO reviews/testimonials/clients so far — must NOT be fabricated; Trustpilot page exists and waits for real ones.

## Product Principles

1. Prove, don't claim — the site itself is the portfolio; every trust signal must be real and verifiable.
2. One decision per screen — a single service, a single price, one primary action at a time.
3. The free check gives real value first; the audit sells as "the patches to the leaks the check named."
4. Honesty is the differentiator: admit limits (no guaranteed citations, zero reviews yet) louder than competitors hide them.
5. Non-technical readers first: consequences in owner language; code only where a developer will paste it.
