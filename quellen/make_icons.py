"""Erzeugt PNG-Icons fuer den Homebildschirm aus der Geometrie von icon.svg (Volleyball)."""
import re
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BG = (255, 248, 238)
svg = (ROOT / "icon.svg").read_text(encoding="utf-8")
STROKES = re.findall(r'<path d="([^"]+)"[^>]*stroke="(#[0-9a-fA-F]{6})"', svg)


def cubic(p0, p1, p2, p3, steps=400):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        pts.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                         for a, b, c, d in zip(p0, p1, p2, p3)))
    return pts


def parse(d):
    nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", d)]
    pts, cur, i = [], (nums[0], nums[1]), 2
    while i + 5 < len(nums) + 0 and i + 5 <= len(nums) - 1 + 0:
        p1, p2, p3 = (nums[i], nums[i + 1]), (nums[i + 2], nums[i + 3]), (nums[i + 4], nums[i + 5])
        pts += cubic(cur, p1, p2, p3)
        cur, i = p3, i + 6
    return pts


def render(size):
    s = 4
    n = size * s
    k = n * 0.80 / 64          # Ball fuellt 80 % der Flaeche
    off = n * 0.10
    tf = lambda p: (off + p[0] * k, off + p[1] * k)
    ball = Image.new("RGB", (n, n), (255, 255, 255))
    d = ImageDraw.Draw(ball)
    for path, col in STROKES:
        pts = [tf(p) for p in parse(path)]
        r = 2.5 * k
        for x, y in pts:
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    mask = Image.new("L", (n, n), 0)
    cx, r = tf((32, 32)), 30 * k
    ImageDraw.Draw(mask).ellipse([cx[0] - r, cx[1] - r, cx[0] + r, cx[1] + r], fill=255)
    img = Image.new("RGB", (n, n), BG)
    img.paste(ball, (0, 0), mask)
    ImageDraw.Draw(img).ellipse([cx[0] - r, cx[1] - r, cx[0] + r, cx[1] + r],
                                outline=(27, 36, 51), width=int(3 * k))
    return img.resize((size, size), Image.LANCZOS)


for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
    render(size).save(ROOT / name, optimize=True)
