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

  /* Mobile nav: hamburger toggles nav drawer */
  function initNavToggle() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('main-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function() {
      var expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !expanded);
      nav.classList.toggle('nav--open');
      document.body.classList.toggle('nav-open');
    });
    nav.querySelectorAll('.nav-link, .btn-header, .nav-dropdown-link, .nav-profile-icon').forEach(function(link) {
      link.addEventListener('click', function() {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('nav--open');
        document.body.classList.remove('nav-open');
      });
    });
  }

  function init() {
    updateDimension();
    initReveal();
    initNavToggle();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
