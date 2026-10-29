"""把上传的图片做成圆形头像（240x240）。"""
from PIL import Image, ImageDraw

SRC = "avatar-src.jpg"
SIZE = 240

im = Image.open(SRC).convert("RGB")
w, h = im.size

# 取中心偏上一点的方形区域，让人脸占满
side = int(min(w, h) * 0.74)
cx, cy = w // 2, int(h * 0.44)
box = (cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)
im = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)

# 圆形遮罩（边缘抗锯齿）
mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, SIZE * 4 - 1, SIZE * 4 - 1], fill=255)
mask = mask.resize((SIZE, SIZE), Image.LANCZOS)

out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
out.paste(im, (0, 0), mask)
out.save("source/img/avatar.png")
print("saved avatar.png", out.size)
