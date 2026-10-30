/**
 * 相册索引生成器：扫描 source/img/gallery/，输出 /gallery/list.json。
 * 照片页（source/gallery/index.html）读取它来构建 3D 照片墙。
 */
const fs = require('fs');
const path = require('path');

hexo.extend.generator.register('gallery-list', function () {
  const dir = path.join(hexo.source_dir, 'img', 'gallery');
  if (!fs.existsSync(dir)) return [];

  const exts = /\.(jpe?g|png|webp|gif)$/i;
  const files = fs.readdirSync(dir)
    .filter(f => exts.test(f))
    .sort((a, b) => a.localeCompare(b, 'zh'));

  const items = files.map(f => ({
    src: '/img/gallery/' + encodeURIComponent(f),
    name: path.basename(f, path.extname(f))
  }));

  return {
    path: 'gallery/list.json',
    data: JSON.stringify(items),
    layout: false
  };
});
