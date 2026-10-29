"""把插画抠出来，分别合成桌面横图与手机竖图。"""
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

SRC = r"source/img/_hero-source.jpg"


def cutout(art):
    """从四边泛洪去掉白纸，返回 0~1 的 alpha。"""
    scale = 3
    small = art.resize((art.width // scale, art.height // scale), Image.BILINEAR)
    arr = np.asarray(small).astype(np.int16)
    near_white = arr.min(axis=2) >= 234

    h, w = near_white.shape
    visited = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near_white[y, x] and not visited[y, x]:
                visited[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near_white[y, x] and not visited[y, x]:
                visited[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and near_white[ny, nx] and not visited[ny, nx]:
                visited[ny, nx] = True
                dq.append((ny, nx))

    mask = Image.fromarray((visited * 255).astype(np.uint8)).resize(art.size, Image.BILINEAR)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    a = 1.0 - np.asarray(mask, dtype=np.float32) / 255.0
    return np.clip((a - 0.12) / 0.88, 0, 1) ** 0.9


def backdrop(w, h, cx, cy, glow_x, glow_y):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - cx) / (w * 0.80)) ** 2 + ((yy - cy) / (h * 0.95)) ** 2)
    r = np.clip(r, 0, 1)
    inner = np.array([24, 34, 62], dtype=np.float32)
    outer = np.array([5, 7, 15], dtype=np.float32)
    bg = inner + (outer - inner) * (r ** 1.25)[..., None]
    glow = np.exp(-(((xx - glow_x) ** 2) / (2 * (w * 0.24) ** 2) + ((yy - glow_y) ** 2) / (2 * (h * 0.5) ** 2)))
    bg = bg + (np.array([48, 72, 128], dtype=np.float32) - bg) * glow[..., None] * 0.6
    return bg, xx, yy


def compose(w, h, art, alpha, fg_h, x0, y0, cx, cy, glow_x, glow_y, out_path, fade=0.20):
    bg, xx, yy = backdrop(w, h, cx, cy, glow_x, glow_y)

    fg_w = int(art.width * fg_h / art.height)
    fg = art.resize((fg_w, fg_h), Image.LANCZOS)
    fg_arr = np.asarray(fg, dtype=np.float32) * np.array([0.88, 0.92, 1.02], dtype=np.float32)
    fg_a = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((fg_w, fg_h), Image.LANCZOS),
                      dtype=np.float32) / 255.0

    # 底部淡出，避免画稿自身的笔刷断边露出来
    ramp = np.clip((fg_h - np.arange(fg_h, dtype=np.float32)) / (fg_h * fade), 0, 1)[:, None]
    fg_a = fg_a * (ramp ** 1.2)

    ys, ye = max(0, y0), min(h, y0 + fg_h)
    xs, xe = max(0, x0), min(w, x0 + fg_w)
    sub = fg_arr[ys - y0:ye - y0, xs - x0:xe - x0]
    a = fg_a[ys - y0:ye - y0, xs - x0:xe - x0][..., None]

    canvas = bg.copy()
    canvas[ys:ye, xs:xe] = canvas[ys:ye, xs:xe] * (1 - a) + np.clip(sub, 0, 255) * a

    grad = np.clip(xx / (w * 0.60), 0, 1)[..., None] ** 1.15
    canvas *= (0.32 + 0.68 * grad)
    vig = np.clip(1.0 - 0.5 * np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) ** 2, 0.3, 1.0)[..., None]
    canvas *= vig
    canvas += np.random.default_rng(7).normal(0, 2.4, (h, w, 3)).astype(np.float32)

    Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)) \
        .filter(ImageFilter.GaussianBlur(0.3)) \
        .save(out_path, quality=92, optimize=True)
    print("saved", out_path)


art = Image.open(SRC).convert("RGB").crop((0, 0, 1180, 1340))
alpha = cutout(art)

# 桌面 1920x1080：人物靠右
compose(1920, 1080, art, alpha, fg_h=1170, x0=1920 - int(1180 * 1170 / 1340) + 70, y0=-35,
        cx=1920 * 0.70, cy=1080 * 0.40, glow_x=1420, glow_y=470,
        out_path=r"../shots/hero-preview.jpg")

# 手机 1080x1620：人物居中偏下，上方留白给标题
compose(1080, 1620, art, alpha, fg_h=1200, x0=10, y0=520,
        cx=1080 * 0.55, cy=1620 * 0.55, glow_x=600, glow_y=980,
        out_path=r"../shots/hero-mobile-preview.jpg", fade=0.06)

