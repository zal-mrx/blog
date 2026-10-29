"""生成头像与文章封面。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

rng = np.random.default_rng(11)


def gradient(w, h, c1, c2):
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.array(c1, dtype=np.float32)
    b = np.array(c2, dtype=np.float32)
    img = a + (b - a) * y
    return np.repeat(img, w, axis=1)


def add_blobs(arr, n, color, rmin, rmax, alpha):
    h, w, _ = arr.shape
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        cx, cy = rng.integers(0, w), rng.integers(0, h)
        r = rng.integers(rmin, rmax)
        d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=int(alpha * 255))
    layer = layer.filter(ImageFilter.GaussianBlur(rmin * 0.9))
    m = np.asarray(layer, dtype=np.float32)[..., None] / 255.0
    col = np.array(color, dtype=np.float32)
    return arr + (col - arr) * m * alpha


# ---------- 头像 ----------
S = 240
bg = gradient(S, S, (46, 122, 112), (10, 44, 42))
bg = add_blobs(bg, 12, (120, 190, 175), 20, 60, 0.25)
av = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")

cloud = Image.new("RGBA", (S, S), (0, 0, 0, 0))
cd = ImageDraw.Draw(cloud)
cd.rounded_rectangle([58, 118, 182, 158], radius=20, fill=(248, 252, 251, 240))
cd.ellipse([70, 96, 130, 152], fill=(248, 252, 251, 240))
cd.ellipse([106, 78, 176, 148], fill=(248, 252, 251, 240))
cd.ellipse([146, 104, 190, 150], fill=(248, 252, 251, 240))
cloud = cloud.filter(ImageFilter.GaussianBlur(0.8))
av = Image.alpha_composite(av, cloud)

mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
av.putalpha(mask)
av.save(r"source/img/avatar.png")
print("avatar ok")

# ---------- 文章封面 ----------
def cover(path, seed, c1, c2, accent):
    r = np.random.default_rng(seed)
    w, h = 800, 500
    arr = gradient(w, h, c1, c2)
    arr = add_blobs(arr, 9, accent, 60, 180, 0.3)
    arr += r.normal(0, 2.5, (h, w, 3)).astype(np.float32)
    # 右下角一点柔光
    yy, xx = np.mgrid[0:h, 0:w]
    glow = np.exp(-(((xx - w * 0.78) ** 2 + (yy - h * 0.72) ** 2) / (2 * (h * 0.42) ** 2)))[..., None]
    arr = arr + (np.array([200, 235, 225], dtype=np.float32) - arr) * glow * 0.28
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path, quality=90, optimize=True)
    print("saved", path)


cover(r"source/img/cover-1.jpg", 3, (18, 62, 58), (8, 30, 34), (90, 160, 145))
cover(r"source/img/cover-2.jpg", 9, (30, 52, 72), (10, 22, 34), (110, 150, 190))
