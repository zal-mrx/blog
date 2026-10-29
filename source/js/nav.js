/* 导航栏点击的「放大再缩回」反馈 */
(function () {
  function bind() {
    var nav = document.getElementById('nav');
    if (!nav || nav.dataset.pulseInit) return;
    nav.dataset.pulseInit = '1';

    nav.addEventListener('click', function (e) {
      var el = e.target.closest('a, .site-page, #search-button, #toggle-menu');
      if (!el) return;

      el.classList.remove('nav-pulse');
      // 强制重排，保证连续点击也能重播动画
      void el.offsetWidth;
      el.classList.add('nav-pulse');

      el.addEventListener(
        'animationend',
        function handler() {
          el.classList.remove('nav-pulse');
          el.removeEventListener('animationend', handler);
        },
        { once: true }
      );
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }

  document.addEventListener('pjax:complete', bind);
})();
