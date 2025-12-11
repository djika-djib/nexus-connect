// static/js/main.js
(function () {
  "use strict";

  // Helper: respect reduced motion
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // IntersectionObserver options
  const ioOptions = {
    root: null,
    rootMargin: '0px 0px -8% 0px',
    threshold: 0.12
  };

  // Reveal callback
  function onIntersect(entries, obs) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        // allow stagger via data-delay attribute (ms)
        const delayAttr = el.dataset.delay;
        if (delayAttr) {
          el.style.setProperty('--delay', `${delayAttr}ms`);
        }
        el.classList.add('visible');
        obs.unobserve(el);
      }
    });
  }

  // If reduced motion, just reveal all immediately
  if (reduceMotion) {
    document.querySelectorAll('.reveal, .card, .hero-text').forEach(el => el.classList.add('visible'));
    return;
  }

  // Create observer
  const observer = new IntersectionObserver(onIntersect, ioOptions);

  // Observe elements with .reveal
  document.addEventListener('DOMContentLoaded', function () {
    // hero text reveal (make it feel immediate)
    const heroText = document.querySelector('.hero-text');
    if (heroText) {
      setTimeout(() => heroText.classList.add('visible'), 120);
    }

    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach((el, idx) => {
      // stagger small amount by default if no data-delay
      if (!el.hasAttribute('data-delay')) {
        el.dataset.delay = (idx % 6) * 80; // small stagger 0,80,160...
      }
      observer.observe(el);
    });

    // small accessibility: allow keyboard users to see focus outlines
    document.body.addEventListener('keyup', function (e) {
      if (e.key === 'Tab') document.documentElement.classList.add('show-focus');
    }, { once: true });
  });
})();
