/* 相册灯箱：点击图片放大查看 */
(function () {
  function init() {
    var grid = document.querySelector('.album-grid');
    if (!grid || grid.dataset.lbInit) return;
    grid.dataset.lbInit = '1';

    var box = document.createElement('div');
    box.className = 'album-lightbox';
    box.innerHTML = '<img alt=""><button class="album-lightbox-close" aria-label="关闭">×</button>';
    document.body.appendChild(box);

    var img = box.querySelector('img');

    function open(href, alt) {
      img.src = href;
      img.alt = alt || '';
      box.classList.add('is-open');
      document.documentElement.style.overflow = 'hidden';
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

  // 兼容 pjax 局部刷新
  document.addEventListener('pjax:complete', init);
})();
