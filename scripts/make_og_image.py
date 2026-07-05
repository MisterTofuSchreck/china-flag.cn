# -*- coding: utf-8 -*-
"""Renders assets/og-image.png (1200x630), the social-media preview image.

The flag is drawn from the same official construction grid as
assets/flag.svg (30x20 units, large star at (5,5) r=3, small stars
r=1 at (10,2), (12,4), (12,7), (10,9), each rotated toward the large
star's center). Rendered 4x supersampled for clean anti-aliased edges,
then downscaled. Run once via `python scripts/make_og_image.py`
whenever the design changes; the PNG is committed as a static asset.
"""
import math
import os

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1200, 630
SS = 4  # supersampling factor

PAPER = (253, 251, 246)
RED = (222, 41, 16)
GOLD = (255, 222, 0)
BORDER = (232, 227, 214)

# Flag placement on the canvas (3:2, centered)
FLAG_W, FLAG_H = 870, 580
FLAG_X = (W - FLAG_W) // 2
FLAG_Y = (H - FLAG_H) // 2
CORNER_RADIUS = 18

INNER_OVER_OUTER = 0.381966


def star_points(cx, cy, r_outer, angle_deg):
    """Vertices of a 5-pointed star; angle_deg = direction of the first
    point, measured clockwise from 'up' in y-down screen coordinates."""
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


def main():
    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    draw = ImageDraw.Draw(img)

    fx, fy, fw, fh = FLAG_X * SS, FLAG_Y * SS, FLAG_W * SS, FLAG_H * SS
    draw.rounded_rectangle(
        [fx - 2 * SS, fy - 2 * SS, fx + fw + 2 * SS, fy + fh + 2 * SS],
        radius=(CORNER_RADIUS + 2) * SS, fill=BORDER,
    )
    draw.rounded_rectangle(
        [fx, fy, fx + fw, fy + fh], radius=CORNER_RADIUS * SS, fill=RED,
    )

    unit = fw / 30.0  # construction grid unit

    def to_px(pts):
        return [(fx + x * unit, fy + y * unit) for x, y in pts]

    draw.polygon(to_px(star_points(5, 5, 3, 0)), fill=GOLD)
    for sx, sy in [(10, 2), (12, 4), (12, 7), (10, 9)]:
        ang = angle_to(sx, sy, 5, 5)
        draw.polygon(to_px(star_points(sx, sy, 1, ang)), fill=GOLD)

    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(BASE, "assets", "og-image.png")
    img.save(out, optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
