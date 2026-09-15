#!/usr/bin/env python3
"""Convert colors between formats and check accessible contrast."""

import argparse
import re
import sys

__version__ = "0.1.0"

HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_CALL = re.compile(r"^rgba?\(([^)]+)\)$", re.I)
HSL_CALL = re.compile(r"^hsla?\(([^)]+)\)$", re.I)


def parse_hex(text):
    match = HEX.match(text.strip())
    if not match:
        raise ValueError("not a hex color: %r" % text)
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, c)))) for c in rgb)


def rgb_to_hsl(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    high, low = max(r, g, b), min(r, g, b)
    lightness = (high + low) / 2
    if high == low:
        return (0.0, 0.0, lightness * 100)
    delta = high - low
    saturation = delta / (2 - high - low) if lightness > 0.5 else delta / (high + low)
    if high == r:
        hue = ((g - b) / delta) % 6
    elif high == g:
        hue = (b - r) / delta + 2
    else:
        hue = (r - g) / delta + 4
    return (hue * 60 % 360, saturation * 100, lightness * 100)


def hsl_to_rgb(hsl):
    h, s, l = hsl[0] % 360, hsl[1] / 100.0, hsl[2] / 100.0
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    table = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]
    r, g, b = table[int(h // 60) % 6]
    return tuple(round((v + m) * 255) for v in (r, g, b))


def parse(text):
    """Accept #hex, rgb(...), hsl(...) and return an (r, g, b) tuple."""
    text = text.strip()
    match = RGB_CALL.match(text)
    if match:
        parts = [float(p.strip().rstrip("%")) for p in re.split(r"[,\s/]+", match.group(1)) if p.strip()]
        return tuple(int(round(p)) for p in parts[:3])
    match = HSL_CALL.match(text)
    if match:
        parts = [float(p.strip().rstrip("%")) for p in re.split(r"[,\s/]+", match.group(1)) if p.strip()]
        return hsl_to_rgb(parts[:3])
    return parse_hex(text)


def relative_luminance(rgb):
    channels = []
    for value in rgb:
        v = value / 255.0
        channels.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = relative_luminance(a), relative_luminance(b)
    high, low = max(la, lb), min(la, lb)
    return (high + 0.05) / (low + 0.05)


def wcag_grade(ratio):
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA large text only"
    return "fail"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("color", help="#hex, rgb(r,g,b) or hsl(h,s%,l%)")
    ap.add_argument("--contrast", help="second color to compare against")
    args = ap.parse_args(argv)

    try:
        rgb = parse(args.color)
    except ValueError as exc:
        print("colorconv: %s" % exc, file=sys.stderr)
        return 2
    h, s, l = rgb_to_hsl(rgb)
    print("hex  %s" % to_hex(rgb))
    print("rgb  rgb(%d, %d, %d)" % rgb)
    print("hsl  hsl(%.0f, %.0f%%, %.0f%%)" % (h, s, l))

    if args.contrast:
        try:
            other = parse(args.contrast)
        except ValueError as exc:
            print("colorconv: %s" % exc, file=sys.stderr)
            return 2
        ratio = contrast_ratio(rgb, other)
        print("\ncontrast with %s" % to_hex(other))
        print("ratio %.2f:1  -> %s" % (ratio, wcag_grade(ratio)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
