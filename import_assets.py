import os
from PIL import Image

BASE = r"C:\Users\LEGION\.dsh\attachments\v1\objects"
OUT = r"C:\Users\LEGION\Documents\deepseek-harness\default-workspace\myblog\source\img"

def src(h):
    return os.path.join(BASE, h[:2], h)

def save(img, path, max_side, quality=86):
    im = Image.open(img).convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(path, quality=quality, optimize=True)
    print(os.path.basename(path), im.size)

# 关于页背景（拥抱）
save(src("06fc4fb4373bdbdc206ab262fe21e64d1165bb6decd540b82192d9218128b1f6"),
     os.path.join(OUT, "about-bg.jpg"), 1800, 88)

# 相册背景（圣诞树）
save(src("0d9b8ef54f7c558b1d4b259014e2d3f14c1beba4958403a54547d297078847c8"),
     os.path.join(OUT, "gallery-bg.jpg"), 1600, 86)

# 抖音二维码
qr = Image.open(src("fcd1f0dbe097e9cda27d344d82b9601d18b48f6e55f8fdf9ba0a523f6af0b16c")).convert("RGB")
qr.thumbnail((600, 600), Image.LANCZOS)
qr.save(os.path.join(OUT, "douyin-qr.png"))
print("douyin-qr.png", qr.size)

# 相册图片（15 张）
hashes = [
    "60beb5f43cf76dfe1143094d47edfa68c6100c2398bbf1a4da631122fa9c9377",  # 雏田线稿
    "457765e2f2791910d007a6ca02ed514634752354ba5478604079e28bd5c87bc8",  # 鸣人线稿
    "d5dca82bdf7ec2fa8222c0c08ea0b670c5f30b154ad848a782816c23aadb1876",  # 红梅
    "47b0b0d68190799461fbf2a9c43a52a66c9499987b95a314af52753092d33837",  # 站台184
    "f2c9a336040b04302eeb1f6d6276352181c7f1b420dfa3670ce9ea65a8f19581",  # 屏幕佐助
    "73d011747f147196e7b71d00a6318d1bc196082e14310ca4efc4b0f9afb9dd8a",  # 漫画书
    "9de8c4de4ad919e68c36ec66825461b727565c5c6c2f8394c5f8d2b05a8395fe",  # 影院
    "94a0f4ca238f6c5d489c0a61eb97d8a9ebd26e2acaa4ff1bb22296764dea2491",  # 兔子甜点
    "486bfe41c693c6477d6dee068c27f0e7cc48acf295d43245df44c13c9a5d0aaa",  # 躲被子
    "69bd0a7f089442cf82d8cc3568c6795f9dfc2bd0e55f8cc9cbd0f1232f6e6866",  # 舷窗雨
    "a885827c5c4391f2755ba5468d558ba9099c2bc5f4fed1a3acd0a31a8905c3cd",  # 夜站台
    "16c48f178989d3e2ad88ef4fba09a95eedd0393aa9386a667a4e552991bd9678",  # 机场
    "eefa56a52619519737151636fa4f35481959aa7c1d6989121c0666de8ebd3cd3",  # 香炉
    "c78f3578d3a0be83e760945b84ae60cedc5a1f0445cd6ccdad1d380d1c705b2b",  # 寺庙
    "3a3ae2569dacdfb1ae22832a8d1b20597d3464d6571a92edd050d34f5888d8b7",  # 心经
]

gdir = os.path.join(OUT, "gallery")
os.makedirs(gdir, exist_ok=True)
for old in os.listdir(gdir):
    os.remove(os.path.join(gdir, old))

for i, h in enumerate(hashes, 1):
    save(src(h), os.path.join(gdir, f"photo-{i:02d}.jpg"), 1200, 84)
