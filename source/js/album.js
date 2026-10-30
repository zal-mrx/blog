/* 相册灯箱：点开图片放大，并可对每张照片评论（Giscus，按图片路径区分） */
(function () {
  var GISCUS = {
    repo: 'zal-mrx/blog',
    repoId: 'R_kgDOVbv6Hg',
    categoryId: 'DIC_kwDOVbv6Hs4DJ6qB',
    src: 'https://giscus.app/client.js'
  };

  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function init() {
    var grid = document.querySelector('.album-grid');
    if (!grid || grid.dataset.lbInit) return;
    grid.dataset.lbInit = '1';

    var box = document.createElement('div');
    box.className = 'album-lightbox';
    box.innerHTML =
      '<button class="album-lightbox-close" aria-label="关闭">×</button>' +
      '<div class="album-stage"><img alt=""></div>' +
      '<div class="album-comments"><div class="album-comments-head">这张照片的评论</div><div class="giscus-host"></div></div>';
    document.body.appendChild(box);

    var img = box.querySelector('.album-stage img');
    var host = box.querySelector('.giscus-host');
    var lastTerm = null;

    function loadComments(term) {
      if (lastTerm === term) return;
      lastTerm = term;
      host.innerHTML = '<div class="giscus-loading">评论加载中…</div>';

      var obs = new MutationObserver(function () {
        if (host.querySelector('iframe')) {
          var tip = host.querySelector('.giscus-loading');
          if (tip) tip.remove();
          obs.disconnect();
        }
      });
      obs.observe(host, { childList: true, subtree: true });

      var s = document.createElement('script');
      s.src = GISCUS.src;
      s.setAttribute('data-repo', GISCUS.repo);
      s.setAttribute('data-repo-id', GISCUS.repoId);
      s.setAttribute('data-category-id', GISCUS.categoryId);
      s.setAttribute('data-mapping', 'specific');
      s.setAttribute('data-term', term);
      s.setAttribute('data-strict', '0');
      s.setAttribute('data-reactions-enabled', '1');
      s.setAttribute('data-emit-metadata', '0');
      s.setAttribute('data-input-position', 'top');
      s.setAttribute('data-theme', currentTheme());
      s.setAttribute('data-lang', 'zh-CN');
      s.setAttribute('crossorigin', 'anonymous');
      s.async = true;
      host.appendChild(s);
    }

    function open(href, alt) {
      img.src = href;
      img.alt = alt || '';
      box.classList.add('is-open');
      document.documentElement.style.overflow = 'hidden';
      loadComments(href);
    }

    function close() {
      box.classList.remove('is-open');
      img.removeAttribute('src');
      document.documentElement.style.overflow = '';
    }

    grid.addEventListener('click', function (e) {
      var a = e.target.closest('.album-item');
      if (!a) return;
      e.preventDefault();
      open(a.getAttribute('href'), a.dataset.caption);
    });

    box.addEventListener('click', function (e) {
      if (e.target === box || e.target.closest('.album-lightbox-close')) close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  document.addEventListener('pjax:complete', init);
})();
