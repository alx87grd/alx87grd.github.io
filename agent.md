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
