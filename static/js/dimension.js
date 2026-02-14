/**
 * Adds visual dimension across all pages: scroll-based depth and layered feel.
 * Runs once on DOMContentLoaded and updates on scroll (throttled).
 */
(function() {
  var ticking = false;
  var lastScrollY = 0;
  var scrollThreshold = 24;

  function updateDimension() {
    var scrollY = window.scrollY || window.pageYOffset;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var ratio = docHeight > 0 ? Math.min(1, scrollY / (docHeight * 0.5)) : 0;

    document.body.classList.toggle('is-scrolled', scrollY > scrollThreshold);
    document.documentElement.style.setProperty('--scroll-y', scrollY + 'px');
    document.documentElement.style.setProperty('--scroll-ratio', ratio);

    lastScrollY = scrollY;
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(updateDimension);
      ticking = true;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      updateDimension();
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
    });
  } else {
    updateDimension();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }
})();
