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
- Use `section-title` (animates first) + flat `grid` of `card` elements (stagger in)
- Media cards use `card-title` (caption **below**), never overlay text on images
