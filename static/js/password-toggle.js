(function () {
  function initToggle(btn) {
    var wrap = btn.closest('.password-field-wrap');
    if (!wrap) return;
    var input = wrap.querySelector('input[type="password"], input[type="text"]');
    var showIcon = wrap.querySelector('.password-toggle-icon--show');
    var hideIcon = wrap.querySelector('.password-toggle-icon--hide');
    if (!input || !showIcon || !hideIcon) return;

    btn.addEventListener('click', function () {
      var willShow = input.type === 'password';
      input.type = willShow ? 'text' : 'password';
      btn.setAttribute('aria-pressed', willShow ? 'true' : 'false');
      btn.setAttribute('aria-label', willShow ? 'Hide password' : 'Show password');
      showIcon.hidden = willShow;
      hideIcon.hidden = !willShow;
    });
  }

  document.querySelectorAll('.password-toggle-btn').forEach(initToggle);
})();
