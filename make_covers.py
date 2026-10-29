"""把两张竖版插画裁成 8:5 的文章封面。"""
from PIL import Image


def make(src, box, out, size=(800, 500)):
    im = Image.open(src).convert("RGB").crop(box)
    im = im.resize(size, Image.LANCZOS)
    im.save(out, quality=88, optimize=True)
    print("saved", out, im.size)


# 第一张：星空 + 人物上半身
make("cover-src-1.jpg", (0, 230, 1320, 1055), "../shots/cover1-preview.jpg")

# 第二张：蓝衣女孩，取头部到腰部
make("cover-src-2.jpg", (150, 140, 1170, 777), "../shots/cover2-preview.jpg")
