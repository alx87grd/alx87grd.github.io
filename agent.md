# Agent Preferences

This document outlines the desired behavior and workflow preferences for the AI coding assistant (Antigravity).

## Workflow
- **Plan Review**: Always pause and wait for explicit user approval after creating or updating an `implementation_plan.md`. Do not proceed to execution until approval is confirmed.
- **Trivial Changes**: You may fix trivial issues (code typos, minor CSS) automatically. However, **never change existing wording, project titles, or text content** without explicit instructions.
- **No Autonomous Browsing**: Do not use the browser tool for searching images or validating previews unless explicitly instructed.
- **Tool Usage**: Using `find`, `grep`, and `search_web` (text-only) for research is allowed automatically.
- **Visual Checks**: The user will handle all visual and layout verification manually.
- **Refactoring**: Always ask for permission before performing any structural refactoring.
- **Naming Conventions**: Use `snake_case` for all new files, assets, and identifiers.
- **Git/Version Control**: The user handles all commits. Remind the user to commit changes before starting a new major task or "big" change, and wait for them to do so.
- **External Assets**: Minimize external dependencies. Always ask before adding CDNs, external scripts, or fonts.
- **Focus**: Prioritize code implementation and logic over visual verification.

## Content & Language
- **Default Language**: Use English for all research and general pages.
- **exceptions**: University class pages (e.g., GRO860, GMC714) should use French.
- **Text Integrity**: Fix code trivialities, but **never** change existing wording or project titles without explicit instructions.

## Design Strategy — Section Layouts

The site uses two visual separation patterns. Use the right one for the context:

### Full-width section bands (white ↔ grey alternating)
For **major page-level rhythm** — separating top-level sections that are conceptually different.

- **Use on landing/index pages** to alternate between distinct categories (Research → Resources → Courses)
- **Use on gallery pages** (projects.html) to separate eras/groups (UdeS → MIT → Early)
- **Don't use on detail pages** with many small sections — too busy

### Content-cards (white floating boxes on light background)
For **content-level grouping** — packaging a discrete, self-contained block of information.

- **Use on detail pages** (project pages, course pages) for Abstract, Publications, course topics, etc.
- **Each card = one coherent piece of information**
- **Don't wrap a card inside a grey band** just to "double-separate" — pick one method

### Rules
| Page type | Bands? | Cards? |
|---|---|---|
| Index / landing | ✅ separate major sections | Sparingly (CTA, profile) |
| Project detail | ❌ single background | ✅ Abstract, Publications, etc. |
| Gallery (projects.html) | ✅ separate eras | ❌ grid cards are the content |
| Course pages | ❌ single background | ✅ each topic block |

### Media grids
- Never wrap a grid of cards inside another card (no box-in-a-box)
- Use `section-title` + flat `grid` of `card` elements (see **Page load & scroll animations** below for timing)
- Media cards use `card-title` (caption **below**), never overlay text on images

---

## Page load & scroll animations

**Files:** `js/animations.js` (behavior), `css/style.css` (hero + `.reveal` + first-section anti-flash).

### Two independent systems

1. **Hero (above `<main>`)** — **CSS only**, no `.reveal`, no `animations.js`.
   - Background: `.hero-img` uses `@keyframes heroImgReveal` (**1.2s**).
   - Title + subtitle: `.hero-content h1` / `p` use `@keyframes heroTextReveal` with fixed `animation-delay` (subtitle after title).
   - Tuning: edit delays/duration in `css/style.css` next to `heroTextReveal` / `heroImgReveal`.
   - **Do not** register hero nodes in `animations.js`; that desyncs title/subtitle.

2. **Everything in `<main>` (and footer helpers)** — **`animations.js`** adds `.reveal`, then either:
   - **Load batch** (first screen of *listing* pages), or  
   - **IntersectionObserver** (scroll-in for the rest and all long-form pages).

### `.reveal` / `.revealed` contract

- **Initial:** `.reveal` → hidden (`opacity: 0`, slight `translateY`) in `css/style.css`.
- **Visible:** add `.revealed` → transition to full opacity (same file).
- **Stagger:** JS sets `data-reveal-stagger` and `transition-delay` in seconds (grid cards use row-aware caps so large grids do not queue multi-second delays).
- **No JS:** if `animations.js` fails, elements never get `.reveal` → they stay visible (progressive enhancement).

### Load batch (first main section only)

- **Selector:** `document.querySelector('main > section')` — the **first** `<section>` inside `<main>`.
- **When:** If that section does **not** contain `.project-container`, every `.reveal` node **inside that section** is collected; after **`FIRST_MAIN_DELAY_MS`** (1050; align with ~1.2s hero image), JS adds `.revealed` + stagger. **Not** observed with IntersectionObserver.
- **Why skip `.project-container`:** Project/course long pages use one big first section; scroll-only avoids hiding the whole page until the timeout.
- **Listing pages** (index, projects, material, students, …): first section batch keeps **section title + grid + flex header row** in sync on load.

### Scroll (IntersectionObserver)

- Any `.reveal` **not** in the load batch gets `observer.observe(el)` with `rootMargin` bottom padding so cards can start slightly before entering the viewport (fast scroll).
- On intersect: add `.revealed` and `unobserve`.

### CSS anti-flash (first section, listing pages only)

- Block in `css/style.css` under **“Animations (scroll reveal + first-section load)”**: targets in `main > section:first-of-type:not(:has(.project-container))` that match the same nodes **before** JS adds `.reveal`, using `:not(.reveal)` so the rule drops once JS runs.
- **Important:** `.container > .section-title` only — on **index**, “Research Highlights” lives inside a **flex row** `<div>` that receives `.reveal`, not the bare `h2`. Do **not** broaden to all `.section-title` or that heading stays invisible.

### What gets `.reveal` (registration order in `animations.js`)

Rough checklist for agents extending the site:

| Pattern | Notes |
|--------|--------|
| `.content-card` | Whole card reveals as one |
| Flex row with direct `h2/h3.section-title` | Index “Research Highlights” row — **one** `.reveal` on the wrapper `div` |
| `.container > .container-narrow` (nested intro) | e.g. material Colab intro block |
| `.container-narrow > div` (not grid/card) | e.g. students culture wrappers |
| `.project-main > div` prose (no inner grid) | Course/project long-form |
| `.section-title` | Skipped if inside nested intro narrow, or first title inside flex row (row owns reveal) |
| `.grid .card` | Row-aware stagger |
| `.profile-card`, `.logistics-card`, `.syllabus-table`, `footer .container` | Misc |
| `main section .container > p` | Lead paragraphs |
| `main section h2` | Orphans only; many paths skipped if already covered |

### Changing timing safely

| Goal | Where |
|------|--------|
| When first main content fades in after hero | `FIRST_MAIN_DELAY_MS` in `js/animations.js` |
| Hero photo duration | `.hero-img` `animation` duration + `heroImgReveal` keyframes in `css/style.css` |
| Hero title/subtitle spacing | `animation-delay` on `.hero-content h1` / `p` in `css/style.css` |
| Scroll “early” reveal | `rootMargin` in `js/animations.js` |
| Grid stagger caps | `GRID_*` constants in `js/animations.js` |

### Including `animations.js`

- Root pages: `js/animations.js`
- Nested pages: `../js/animations.js` (or `../../` for courses) — grep existing pages for the pattern.
