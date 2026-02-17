/**
 * Adds visual dimension across all pages: scroll-based depth, layered feel, and reveal animations.
 */
(function() {
  var ticking = false;
  var scrollThreshold = 24;

  function updateDimension() {
    var scrollY = window.scrollY || window.pageYOffset;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var ratio = docHeight > 0 ? Math.min(1, scrollY / (docHeight * 0.5)) : 0;

    document.body.classList.toggle('is-scrolled', scrollY > scrollThreshold);
    document.documentElement.style.setProperty('--scroll-y', scrollY + 'px');
    document.documentElement.style.setProperty('--scroll-ratio', ratio);

    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(updateDimension);
      ticking = true;
    }
  }

  /* Scroll-reveal: elements with class .reveal fade in when they enter the viewport */
  function initReveal() {
    var reveals = document.querySelectorAll('.reveal:not(.is-visible)');
    if (!reveals.length) return;

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0 });

      reveals.forEach(function(el) { observer.observe(el); });
    } else {
      reveals.forEach(function(el) { el.classList.add('is-visible'); });
    }
  }

  /* Expose for pages that render content dynamically */
  window.initReveal = initReveal;

  function init() {
    updateDimension();
    initReveal();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
