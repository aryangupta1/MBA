(function () {
  var root = document.documentElement;
  var key = 'dmba-blog-theme';
  var saved = localStorage.getItem(key);
  if (saved === 'dark' || saved === 'light') {
    root.setAttribute('data-theme', saved);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    root.setAttribute('data-theme', 'dark');
  }

  function bind(btn) {
    if (!btn) return;
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem(key, next);
      btn.setAttribute('aria-label', next === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      btn.textContent = next === 'dark' ? 'Light' : 'Dark';
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      var t = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      btn.textContent = t === 'dark' ? 'Light' : 'Dark';
      btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    }
    bind(btn);
  });
})();
