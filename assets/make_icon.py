"""Draw the kstack icon: three isometric slabs stacked on a rounded-square background.

Run: python3 assets/make_icon.py   (needs Pillow; overwrites assets/icon.png)
"""
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 1024
SCALE = 4  # draw large, then downscale for smooth edges
S = SIZE * SCALE

BG_TOP = (30, 27, 75)
BG_BOTTOM = (49, 46, 129)
# Bottom to top: two base slabs and an accent slab on top.
LAYERS = [
    ((99, 102, 241), (67, 56, 202)),
    ((139, 92, 246), (109, 40, 217)),
    ((251, 191, 36), (217, 119, 6)),
]


def background() -> Image.Image:
    grad = Image.new("RGB", (S, S))
    px = grad.load()
    for y in range(S):
        t = y / (S - 1)
        row = tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM))
        for x in range(S):
            px[x, y] = row
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * 0.22), fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(grad, mask=mask)
    return out


def slab(draw: ImageDraw.ImageDraw, cx: float, cy: float, top, side) -> None:
    w, h, depth = S * 0.30, S * 0.15, S * 0.055  # half-width and half-height of the top face, thickness
    north, east, south, west = (cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)
    draw.polygon([west, south, (south[0], south[1] + depth), (west[0], west[1] + depth)], fill=side)
    draw.polygon([south, east, (east[0], east[1] + depth), (south[0], south[1] + depth)], fill=tuple(max(c - 30, 0) for c in side))
    draw.polygon([north, east, south, west], fill=top)


def main() -> None:
    img = background()
    draw = ImageDraw.Draw(img)
    step = S * 0.15
    base_y = S * 0.66
    for i, (top, side) in enumerate(LAYERS):
        slab(draw, S / 2, base_y - i * step, top, side)
    out = Path(__file__).with_name("icon.png")
    img.resize((SIZE, SIZE), Image.LANCZOS).save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
