"""生成首页横幅背景：深海青色 + 云雾 + 细雨。"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
rng = np.random.default_rng(20261029)


def smooth_noise(h, w, cells):
    """低频随机噪声：小图放大 + 平滑。"""
    small = rng.random((cells, cells)).astype(np.float32)
    img = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32) / 255.0


def fbm(h, w, octaves=(2, 4, 9, 20, 45), weights=(0.5, 0.25, 0.14, 0.08, 0.03)):
    total = np.zeros((h, w), dtype=np.float32)
    for cells, wt in zip(octaves, weights):
        total += smooth_noise(h, w, cells) * wt
    total -= total.min()
    total /= total.max()
    return total


# 1. 纵向渐变底色：顶部深墨绿 -> 中部海青 -> 底部更深
y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
top = np.array([13, 45, 43], dtype=np.float32)
mid = np.array([26, 80, 74], dtype=np.float32)
bot = np.array([12, 42, 44], dtype=np.float32)
t = y * 2
base = np.where(t < 1, top + (mid - top) * t, mid + (bot - mid) * (t - 1))
base = np.repeat(base[:, None, :], W, axis=1)

# 2. 多层云雾
clouds = fbm(H, W, octaves=(3, 6, 12, 26, 55), weights=(0.45, 0.24, 0.15, 0.1, 0.06))
clouds = np.clip((clouds - 0.30) * 1.8, 0, 1) ** 1.15

# 3. 远处的亮雾带（贴着地平线，制造"云海"感）
horizon = np.exp(-((y[:, 0] - 0.76) ** 2) / 0.010)[:, None]
far = np.clip(clouds * 0.85 + horizon * 0.35, 0, 1)

# 4. 上色：暗部偏青，亮部偏灰绿
dark = np.array([13, 47, 44], dtype=np.float32)
light = np.array([150, 190, 178], dtype=np.float32)
color = base + (light - base) * (far ** 1.5)[..., None] * 0.9

# 5. 顶部再压暗一点，突出标题
top_dim = np.clip(1.0 - 0.20 * np.exp(-y * 3.2), 0, 1)[..., None]
color *= top_dim

# 6. 细微雨丝
rain = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(rain)
for _ in range(700):
    x = rng.integers(0, W)
    y0 = rng.integers(-100, H)
    ln = rng.integers(30, 150)
    d.line([(x, y0), (x - 12, y0 + ln)], fill=int(rng.integers(18, 55)), width=1)
rain = rain.filter(ImageFilter.GaussianBlur(0.6))
rain_a = (np.asarray(rain, dtype=np.float32) / 255.0) * 0.5
color += (np.array([200, 230, 220], dtype=np.float32) - color) * rain_a[..., None]

# 7. 暗角
xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
vig = np.clip(1.0 - 0.55 * np.sqrt((xx ** 2) * 0.7 + (yy ** 2) * 1.0), 0.15, 1.0)[..., None]
color *= vig

# 8. 颗粒感
color += rng.normal(0, 3.2, (H, W, 3)).astype(np.float32)

img = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save(r"source/img/banner.jpg", quality=92, optimize=True, progressive=True)
print("saved source/img/banner.jpg", img.size)
