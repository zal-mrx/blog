/**
 * 相册生成器：扫描 source/img/gallery/ 下的图片，自动生成 /gallery/ 页面。
 * 你只需要往那个文件夹里丢照片，重新构建就会自动出现。
 */
const fs = require('fs');
const path = require('path');

hexo.extend.generator.register('gallery', function (locals) {
  const dir = path.join(hexo.source_dir, 'img', 'gallery');
  if (!fs.existsSync(dir)) return [];

  const exts = /\.(jpe?g|png|webp|gif)$/i;
  const files = fs.readdirSync(dir)
    .filter(f => exts.test(f))
    .sort((a, b) => a.localeCompare(b, 'zh'));

  if (!files.length) return [];

  const items = files.map(f => {
    const url = '/img/gallery/' + encodeURIComponent(f);
    const name = path.basename(f, path.extname(f));
    return `<a class="album-item" href="${url}" data-caption="${name}">
      <img src="${url}" alt="${name}" loading="lazy">
      <span class="album-caption">${name}</span>
    </a>`;
  }).join('\n');

  const content = `<div class="album-grid">\n${items}\n</div>`;

  return {
    path: 'gallery/index.html',
    layout: ['page'],
    data: {
      title: '相册',
      type: 'page',
      date: new Date(),
      top_img: '/img/banner.jpg',
      comments: false,
      content
    }
  };
});
