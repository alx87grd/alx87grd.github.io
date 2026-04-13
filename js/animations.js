/**
 * Scroll + first-screen load animations for <main> (and a few globals).
 *
 * CONTRACT (see also agent.md → “Page load & scroll animations”):
 *   1) revealElement(el, staggerSec?) → adds class "reveal", stores data-reveal-stagger (seconds).
 *   2a) If el is inside the FIRST <main> section AND that section has NO .project-container:
 *       el goes to loadBatch → after FIRST_MAIN_DELAY_MS, add "revealed" + transition-delay
 *       (no IntersectionObserver). Keeps section title + grid + flex rows in sync with hero end.
 *   2b) Else: set transition-delay from stagger, IntersectionObserver → "revealed" on intersect.
 *
 * Hero (<header> .hero-content) is NOT handled here — pure CSS in style.css (heroImgReveal + heroTextReveal).
 *
 * Tuning: FIRST_MAIN_DELAY_MS (~1050) should stay slightly under .hero-img animation duration (1.2s).
 */
document.addEventListener('DOMContentLoaded', () => {
    /** ~align with css .hero-img heroImgReveal (1.2s); first main batch runs once after this */
    const FIRST_MAIN_DELAY_MS = 1050;

    const observerOptions = {
        threshold: [0, 0.1, 0.5],
        /** Start reveal slightly before elements enter viewport (helps fast scroll on tall grids). */
        rootMargin: '0px 0px 180px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    /** Marks el for animation; wiring (load batch vs IO) happens after all registrations. */
    function revealElement(el, staggerSec = 0) {
        if (!el || el.classList.contains('reveal')) return;
        el.classList.add('reveal');
        el.dataset.revealStagger = String(staggerSec ?? 0);
    }

    /** Index-style row: flex container, direct h2/h3.section-title, not grid/card. */
    function isFlexSectionHeaderRow(div) {
        if (!div?.parentElement?.classList.contains('container')) return false;
        if (div.classList.contains('grid') || div.classList.contains('content-card')) return false;
        const st = getComputedStyle(div);
        if (st.display !== 'flex' && st.display !== 'inline-flex') return false;
        return !!div.querySelector(':scope > h2.section-title, :scope > h3.section-title');
    }

    function isNestedIntroNarrow(el) {
        return el?.classList.contains('container-narrow')
            && el.parentElement?.classList.contains('container')
            && !el.parentElement.classList.contains('container-narrow');
    }

    function isInNarrowWrapperDiv(el) {
        let p = el.parentElement;
        while (p && p !== document.body) {
            const gp = p.parentElement;
            if (
                gp?.classList.contains('container-narrow')
                && p.tagName === 'DIV'
                && !p.classList.contains('grid')
                && !p.classList.contains('content-card')
            ) {
                return true;
            }
            p = p.parentElement;
        }
        return false;
    }

    document.querySelectorAll('.content-card').forEach((card) => {
        revealElement(card);
    });

    document.querySelectorAll('main section .container > div').forEach((div) => {
        if (isFlexSectionHeaderRow(div)) {
            revealElement(div);
        }
    });

    document.querySelectorAll('main section .container > .container-narrow').forEach((narrow) => {
        if (isNestedIntroNarrow(narrow)) {
            revealElement(narrow);
        }
    });

    document.querySelectorAll('main section .container-narrow > div').forEach((div) => {
        if (div.classList.contains('grid') || div.classList.contains('content-card')) return;
        revealElement(div);
    });

    document.querySelectorAll('main .project-main > div').forEach((div) => {
        if (div.classList.contains('content-card')) return;
        if (div.querySelector(':scope > .grid')) return;
        revealElement(div);
    });

    document.querySelectorAll('.section-title').forEach((title) => {
        if (title.classList.contains('reveal')) return;

        const narrow = title.closest('.container-narrow');
        if (narrow && isNestedIntroNarrow(narrow)) {
            return;
        }

        const parent = title.parentElement;
        if (parent && isFlexSectionHeaderRow(parent)) {
            const first = parent.querySelector(':scope > h2.section-title, :scope > h3.section-title');
            if (first === title) {
                return;
            }
        }

        revealElement(title);
    });

    /* Grid stagger: multi-row uses row+col caps; single row uses index*step with cap (no huge delays). */
    const GRID_ROW_TOL_PX = 14;
    const GRID_SINGLE_ROW_STEP = 0.15;
    const GRID_SINGLE_ROW_CAP = 1.05;
    const GRID_MULTI_ROW_STEP = 0.09;
    const GRID_MULTI_ROW_MAX_ROWS = 7;
    const GRID_MULTI_COL_STEP = 0.05;
    const GRID_MULTI_COL_MAX = 5;

    document.querySelectorAll('.grid').forEach((grid) => {
        const cards = [...grid.querySelectorAll('.card')];
        if (cards.length === 0) return;

        cards.sort((a, b) => {
            const ra = a.getBoundingClientRect();
            const rb = b.getBoundingClientRect();
            if (Math.abs(ra.top - rb.top) < GRID_ROW_TOL_PX) return ra.left - rb.left;
            return ra.top - rb.top;
        });

        const rows = [];
        let lastTop = null;
        cards.forEach((card) => {
            const t = card.getBoundingClientRect().top;
            if (rows.length === 0 || Math.abs(t - lastTop) > GRID_ROW_TOL_PX) {
                rows.push([]);
                lastTop = t;
            }
            rows[rows.length - 1].push(card);
        });

        const multiRow = rows.length > 1;

        rows.forEach((rowCards, ri) => {
            rowCards.forEach((card, ci) => {
                let stagger;
                if (multiRow) {
                    const r = Math.min(ri, GRID_MULTI_ROW_MAX_ROWS);
                    const c = Math.min(ci, GRID_MULTI_COL_MAX);
                    stagger = r * GRID_MULTI_ROW_STEP + c * GRID_MULTI_COL_STEP;
                } else {
                    stagger = Math.min(ci * GRID_SINGLE_ROW_STEP, GRID_SINGLE_ROW_CAP);
                }
                revealElement(card, stagger);
            });
        });
    });

    ['.profile-card', '.logistics-card', '.syllabus-table', '.footer .container'].forEach((sel) => {
        document.querySelectorAll(sel).forEach((el) => revealElement(el));
    });

    document.querySelectorAll('main section .container > p').forEach((p) => {
        if (p.closest('.content-card')) return;
        if (!p.parentElement?.classList.contains('container')) return;
        revealElement(p);
    });

    document.querySelectorAll('main section h2').forEach((el) => {
        if (el.classList.contains('reveal')) return;
        if (el.closest('.content-card')) return;
        if (el.closest('.hero-content')) return;

        const nestedNarrow = el.closest('.container-narrow');
        if (nestedNarrow && isNestedIntroNarrow(nestedNarrow)) {
            return;
        }

        if (isInNarrowWrapperDiv(el)) {
            return;
        }

        const flexRow = el.closest('.container > div');
        if (flexRow && isFlexSectionHeaderRow(flexRow)) {
            return;
        }

        const prose = el.closest('.project-main > div');
        if (prose && !prose.classList.contains('content-card') && !prose.querySelector(':scope > .grid')) {
            return;
        }

        revealElement(el);
    });

    const firstMainSection = document.querySelector('main > section');
    const useFirstMainLoadBatch =
        !!firstMainSection && !firstMainSection.querySelector('.project-container');

    const loadBatch = [];
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* One pass: first-section listing → timed batch; everything else → scroll observer. */
    document.querySelectorAll('.reveal').forEach((el) => {
        if (useFirstMainLoadBatch && firstMainSection.contains(el)) {
            loadBatch.push(el);
            return;
        }

        const stagger = parseFloat(el.dataset.revealStagger || '0');
        el.style.transitionDelay = `${stagger}s`;
        observer.observe(el);
    });

    function sortTopThenLeft(a, b) {
        const ra = a.getBoundingClientRect();
        const rb = b.getBoundingClientRect();
        return ra.top - rb.top || ra.left - rb.left;
    }

    function revealLoadBatch() {
        loadBatch.sort(sortTopThenLeft);
        loadBatch.forEach((el) => {
            const stagger = parseFloat(el.dataset.revealStagger || '0');
            el.style.transitionDelay = `${stagger}s`;
            el.classList.add('revealed');
        });
    }

    if (loadBatch.length > 0) {
        if (reducedMotion) {
            revealLoadBatch();
        } else {
            setTimeout(revealLoadBatch, FIRST_MAIN_DELAY_MS);
        }
    }
});

