/**
 * Scroll Reveal Animations
 *
 * Registers elements in dependency order so headings/text are not double-animated.
 * Patterns:
 *   - .content-card — one block
 *   - Flex “section header” rows (index): title + link move together
 *   - Nested .container > .container-narrow — intro title + paragraph together
 *   - .container-narrow > div wrappers (students, etc.)
 *   - Course pages: .project-main > div prose blocks (no direct .grid child)
 *   - .section-title, then .grid > .card stagger
 *   - Direct intro paragraphs under .container
 *   - Hero, footer, misc components
 */
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: [0.1, 0.5],
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const isHeroContent = entry.target.closest('.hero-content');
                if (!isHeroContent && (entry.intersectionRatio > 0.4 || entry.boundingClientRect.top < window.innerHeight * 0.7)) {
                    entry.target.style.transitionDelay = '0s';
                }

                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    function revealElement(el, delay) {
        if (!el || el.classList.contains('reveal')) return;
        el.classList.add('reveal');
        if (delay !== undefined) {
            el.style.transitionDelay = `${delay}s`;
        }
        observer.observe(el);
    }

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

    /** h2 sits in a block wrapper whose parent is .container-narrow (students culture, etc.) */
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

    // ── 1. Content cards — single block ──
    document.querySelectorAll('.content-card').forEach(card => {
        revealElement(card);
    });

    // ── 2. Section header rows: flex container with leading .section-title (e.g. index) ──
    document.querySelectorAll('main section .container > div').forEach(div => {
        if (isFlexSectionHeaderRow(div)) {
            revealElement(div);
        }
    });

    // ── 3. Nested intro: .container > .container-narrow (e.g. material colab lead) ──
    document.querySelectorAll('main section .container > .container-narrow').forEach(narrow => {
        if (isNestedIntroNarrow(narrow)) {
            revealElement(narrow);
        }
    });

    // ── 4. Block wrappers inside narrow columns (students culture, location, etc.) ──
    document.querySelectorAll('main section .container-narrow > div').forEach(div => {
        if (div.classList.contains('grid') || div.classList.contains('content-card')) return;
        revealElement(div);
    });

    // ── 5. Course / long-form: prose blocks under .project-main ──
    document.querySelectorAll('main .project-main > div').forEach(div => {
        if (div.classList.contains('content-card')) return;
        if (div.querySelector(':scope > .grid')) return;
        revealElement(div);
    });

    // ── 6. Section titles (skip when parent block already animates them) ──
    document.querySelectorAll('.section-title').forEach(title => {
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

    // ── 7. Grid cards — stagger ──
    document.querySelectorAll('.grid').forEach(grid => {
        const cards = grid.querySelectorAll('.card');
        cards.forEach((card, index) => {
            revealElement(card, index * 0.15);
        });
    });

    // ── 8. Hero — title then subtitle ──
    document.querySelectorAll('.hero-content h1').forEach(el => revealElement(el, 0));
    document.querySelectorAll('.hero-content p').forEach(el => revealElement(el, 0.6));

    // ── 9. Other named blocks ──
    document.querySelectorAll('.profile-card').forEach(el => revealElement(el));
    document.querySelectorAll('.logistics-card').forEach(el => revealElement(el));
    document.querySelectorAll('.syllabus-table').forEach(el => revealElement(el));
    document.querySelectorAll('.footer .container').forEach(el => revealElement(el));

    // ── 10. Lead copy: direct <p> children of .container inside sections ──
    document.querySelectorAll('main section .container > p').forEach(p => {
        if (p.closest('.content-card')) return;
        if (!p.parentElement?.classList.contains('container')) return;
        revealElement(p);
    });

    // ── 11. h2 outside content-cards (skip if part of a block already revealed) ──
    document.querySelectorAll('main section h2').forEach(el => {
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
});
