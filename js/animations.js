/**
 * Scroll Reveal Animations
 * Two patterns:
 *  1. .content-card — reveals as a single block
 *  2. .section-title + .grid > .card — title first, then cards stagger
 * Plus: hero content, footer, standalone cards in grids
 */
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: [0.1, 0.5],
        rootMargin: '0px 0px -50px 0px' 
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Skip delay clearing for hero content (preserve stagger)
                const isHeroContent = entry.target.closest('.hero-content');
                if (!isHeroContent && (entry.intersectionRatio > 0.4 || entry.boundingClientRect.top < window.innerHeight * 0.7)) {
                    entry.target.style.transitionDelay = '0s';
                }
                
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Helper: add reveal class and observe with optional delay
    function revealElement(el, delay) {
        el.classList.add('reveal');
        if (delay !== undefined) {
            el.style.transitionDelay = `${delay}s`;
        }
        observer.observe(el);
    }

    // ── Pattern 1: Content cards — animate as one block ──
    document.querySelectorAll('.content-card').forEach(card => {
        revealElement(card);
    });

    // ── Pattern 2: Section titles + grid cards ──
    // Section titles animate independently  
    document.querySelectorAll('.section-title').forEach(title => {
        revealElement(title);
    });

    // Grid cards stagger within their parent grid
    document.querySelectorAll('.grid').forEach(grid => {
        const cards = grid.querySelectorAll('.card');
        cards.forEach((card, index) => {
            revealElement(card, index * 0.15);
        });
    });

    // ── Hero content — title then subtitle ──
    document.querySelectorAll('.hero-content h1').forEach(el => revealElement(el, 0));
    document.querySelectorAll('.hero-content p').forEach(el => revealElement(el, 0.6));

    // ── Standalone elements ──
    document.querySelectorAll('.profile-card').forEach(el => revealElement(el));
    document.querySelectorAll('.logistics-card').forEach(el => revealElement(el));
    document.querySelectorAll('.syllabus-table').forEach(el => revealElement(el));
    document.querySelectorAll('.footer .container').forEach(el => revealElement(el));

    // ── Section h2 headers not inside content-cards (e.g. on index/projects pages) ──
    document.querySelectorAll('section h2').forEach(el => {
        // Skip if already inside a content-card (it will animate with the card)
        if (!el.closest('.content-card') && !el.classList.contains('reveal')) {
            revealElement(el);
        }
    });
});
