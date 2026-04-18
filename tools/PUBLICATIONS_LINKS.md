# Publication links on project pages

Use this HTML pattern for **Publications & Resources** (and similar) blocks so layout and pill buttons stay consistent across `projects/*.html`.

## Markup template

```html
<div class="content-card">
  <h3>Publications &amp; Resources</h3>
  <div class="action-links-row" style="flex-direction: column; align-items: flex-start;">
    <a href="https://doi.org/..." class="btn-action">📄 <strong>Journal (…):</strong> Authors, &quot;Title,&quot; venue details, year.</a>
    <a href="https://arxiv.org/abs/...." class="btn-action">📄 <strong>arXiv preprint:</strong> Authors, &quot;Title,&quot; year.</a>
  </div>
</div>
```

## Rules

1. **Wrapper** — `class="action-links-row"` with **only**  
   `style="flex-direction: column; align-items: flex-start;"`  
   Do not add `stretch`, `nowrap`, extra `gap`, or per-link `display` / `width` overrides unless the global CSS changes.

2. **Links** — `class="btn-action"` only (no `style="display: block; width: 100%; …"` on the `<a>`). Global styles in `css/style.css` (`.action-links-row .btn-action`) handle wrapping and alignment.

3. **Line content** — Emoji + **bold label** (venue type: Journal, Conference, arXiv preprint, thesis, etc.) + citation: authors, quoted title (`&quot;…&quot;`), year, DOI/journal/conference details as appropriate.

4. **Bibliography data** — Prefer recording BibTeX in `tools/biblio.json` for each canonical URL; `scraper_bib.py` can refresh entries.

This matches pages such as `projects/snowcontrol.html`, `projects/softsensor.html`, and `projects/optimalcontrolmit.html`.
