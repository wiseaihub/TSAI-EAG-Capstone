"""Blur the signed-in email strip on README portal screenshots.

Targets the AccountHeader bar directly under the dark hero ("Signed in as" + email).
Uses layout heuristics tuned for ~1024px-wide captures of the WISE Clinical Portal.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


def _center_column_luminance_row(im: Image.Image, row: int, cx: int, half: int = 40) -> float:
    px = im.convert("RGB").load()
    w, h = im.size
    if row < 0 or row >= h:
        return 0.0
    x0 = max(0, cx - half)
    x1 = min(w, cx + half)
    n = 0
    total = 0.0
    for x in range(x0, x1):
        r, g, b = px[x, row]
        total += (r + g + b) / 3.0
        n += 1
    return total / max(n, 1)


def _detect_account_header_band(im: Image.Image) -> tuple[int, int]:
    """Return (y0, y1) for the pale AccountHeader bar below the dark hero."""
    w, h = im.size
    cx = w // 2

    # Last row still reading as hero interior darkness along the vertical center column.
    last_dark = 40
    scan_hi = min(int(h * 0.30), h)
    for i in range(40, scan_hi):
        if _center_column_luminance_row(im, i, cx) < 48.0:
            last_dark = i

    window = 5
    white_thr = 243.0
    start = None
    lower = last_dark + 1
    upper = min(h - window - 1, int(h * 0.45))
    for i in range(lower, upper):
        chunk_mean = sum(_center_column_luminance_row(im, i + k, cx) for k in range(window)) / window
        if chunk_mean >= white_thr:
            start = i
            break

    if start is None:
        start = min(h - 80, last_dark + max(48, int(h * 0.08)))

    end = min(h, start + max(56, int(h * 0.135)))
    return start, end


def blur_email_strip(
    src: Path,
    dst: Path,
    *,
    blur_radius: int = 12,
) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    y0, y1 = _detect_account_header_band(im)
    x0 = max(0, int(w * 0.015))
    x1 = min(w, int(w * 0.985))
    region = im.crop((x0, y0, x1, y1))
    blurred = region.filter(ImageFilter.GaussianBlur(blur_radius))
    im.paste(blurred, (x0, y0))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, optimize=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--src", type=Path, required=True)
    p.add_argument("--dst", type=Path, default=None)
    p.add_argument("--blur", type=int, default=12)
    args = p.parse_args()
    dst = args.dst or args.src
    blur_email_strip(args.src, dst, blur_radius=args.blur)


if __name__ == "__main__":
    main()
