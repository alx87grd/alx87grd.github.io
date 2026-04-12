/**
 * Scroll Reveal Animations
 * Triggered by IntersectionObserver with staggering support
 */
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: [0.1, 0.5], // Multiple thresholds to catch fast scrolls
        rootMargin: '0px 0px -50px 0px' 
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // SAFETY: If the element is already well into the view (e.g. fast scroll),
                // we clear the delay to avoid "missing" content.
                // EXCLUSION: We don't apply this for the hero content to preserve its staggered entry.
                const isHeroContent = entry.target.closest('.hero-content');
                if (!isHeroContent && (entry.intersectionRatio > 0.4 || entry.boundingClientRect.top < window.innerHeight * 0.7)) {
                    entry.target.style.transitionDelay = '0s';
                }
                
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // 1. Define selectors for different types of elements
    const revealSelectors = [
        '.card',
        '.profile-card',
        'section h2',
        '.hero-content h1',
        '.hero-content p',
        '.footer .container',
        '.logistics-card',
        '.syllabus-table'
    ];

    // 2. Apply reveal class and observer
    const revealElements = document.querySelectorAll(revealSelectors.join(','));
    
    // 3. Implement staggering for children of grid containers or lists
    const parents = new Set();
    revealElements.forEach(el => {
        el.classList.add('reveal');
        // Group by parent if it's a grid, a hero content area, or a list row
        if (el.parentElement && (
            el.parentElement.classList.contains('grid') || 
            el.parentElement.classList.contains('action-links-row') ||
            el.parentElement.classList.contains('hero-content') ||
            el.parentElement.classList.contains('content-card') ||
            el.parentElement.classList.contains('card') ||
            el.parentElement.classList.contains('project-sidebar') ||
            el.parentElement.classList.contains('project-main')
        )) {
            parents.add(el.parentElement);
        } else {
            observer.observe(el);
        }
    });

    // 4. Batch observe parents or direct children with staggering
    parents.forEach(parent => {
        const isHero = parent.classList.contains('hero-content');
        const children = parent.querySelectorAll('.reveal');
        children.forEach((child, index) => {
            // Standard delay of 200ms, but longer (600ms) for the hero title/subtitle
            const step = isHero ? 0.6 : 0.2;
            const delay = (index % 6) * step; 
            child.style.transitionDelay = `${delay}s`;
            observer.observe(child);
        });
    });

    // Observe any remaining elements that weren't part of a known group
    revealElements.forEach(el => {
        if (!el.classList.contains('revealed')) {
            observer.observe(el);
        }
    });
});
