# -*- coding: utf-8 -*-
"""Generates the favicon set for china-flag.cn.

A favicon is square but the flag is 3:2, so we render the square left
region of the flag's construction grid (x 0..20, y 0..20 on the 30x20
grid) — a red field carrying the large star and all four small stars,
the most recognisable crop at 16 px. Everything is rendered 4x
supersampled from the official star geometry, then downscaled.

Outputs (in the repo root): favicon.ico (16/32/48), favicon-16x16.png,
favicon-32x32.png, apple-touch-icon.png (180, with padding so iOS
rounded corners don't clip a star), android-chrome-192x192.png,
android-chrome-512x512.png. Run: python scripts/make_favicons.py
"""
import math
import os

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RED = (222, 41, 16)
GOLD = (255, 222, 0)
INNER_OVER_OUTER = 0.381966
SS = 4  # supersampling


def star_points(cx, cy, r_outer, angle_deg):
    r_inner = r_outer * INNER_OVER_OUTER
    pts = []
    for i in range(5):
        a_out = math.radians(angle_deg + i * 72)
        pts.append((cx + r_outer * math.sin(a_out), cy - r_outer * math.cos(a_out)))
        a_in = math.radians(angle_deg + i * 72 + 36)
        pts.append((cx + r_inner * math.sin(a_in), cy - r_inner * math.cos(a_in)))
    return pts


def angle_to(cx, cy, tx, ty):
    return math.degrees(math.atan2(tx - cx, -(ty - cy)))


def render(size, pad_ratio=0.0, rounded=False):
    """size = target px. pad_ratio shrinks the red field inside a
    transparent square (used for apple-touch-icon breathing room)."""
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(big * pad_ratio)
    field = big - 2 * pad
    if rounded:
        draw.rounded_rectangle([pad, pad, pad + field, pad + field],
                               radius=int(field * 0.18), fill=RED)
    else:
        draw.rectangle([pad, pad, pad + field, pad + field], fill=RED)

    # Map the flag's left 20x20 grid region onto the red field.
    unit = field / 20.0

    def to_px(pts):
        return [(pad + x * unit, pad + y * unit) for x, y in pts]

    draw.polygon(to_px(star_points(5, 5, 3, 0)), fill=GOLD)
    for sx, sy in [(10, 2), (12, 4), (12, 7), (10, 9)]:
        draw.polygon(to_px(star_points(sx, sy, 1, angle_to(sx, sy, 5, 5))), fill=GOLD)

    return img.resize((size, size), Image.LANCZOS)


def save(img, name):
    img.save(os.path.join(BASE, name))
    print(f"wrote {name} ({os.path.getsize(os.path.join(BASE, name))} bytes)")


def main():
    save(render(16), "favicon-16x16.png")
    save(render(32), "favicon-32x32.png")
    save(render(192), "android-chrome-192x192.png")
    save(render(512), "android-chrome-512x512.png")
    # Apple: slight padding so a star isn't clipped by iOS rounded mask.
    save(render(180, pad_ratio=0.08), "apple-touch-icon.png")
    # Multi-size .ico
    ico = render(48)
    ico.save(os.path.join(BASE, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote favicon.ico (16/32/48)")


if __name__ == "__main__":
    main()
