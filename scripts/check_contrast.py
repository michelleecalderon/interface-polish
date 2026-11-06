#!/usr/bin/env python3
"""Check WCAG contrast for two hexadecimal CSS colors.

The script accepts #RGB, #RGBA, #RRGGBB, and #RRGGBBAA. Transparent colors are
composited in sRGB: background over --canvas, then foreground over background.
"""

from __future__ import annotations

import argparse
import re
import sys


COLOR_PATTERN = re.compile(r"^#(?:(?P<short>[0-9a-fA-F]{3,4})|(?P<long>[0-9a-fA-F]{6,8}))$")


def parse_color(value: str) -> tuple[float, float, float, float]:
    match = COLOR_PATTERN.fullmatch(value)
    if not match:
        raise ValueError("use #RGB, #RGBA, #RRGGBB, or #RRGGBBAA")

    digits = match.group("short") or match.group("long")
    if len(digits) in (3, 4):
        digits = "".join(channel * 2 for channel in digits)
    if len(digits) == 6:
        digits += "ff"

    return tuple(int(digits[index : index + 2], 16) / 255 for index in range(0, 8, 2))


def composite(
    foreground: tuple[float, float, float, float],
    background: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    alpha = foreground[3] + background[3] * (1 - foreground[3])
    if alpha == 0:
        return (0, 0, 0, 0)
    channels = tuple(
        (foreground[index] * foreground[3] + background[index] * background[3] * (1 - foreground[3])) / alpha
        for index in range(3)
    )
    return (*channels, alpha)


def linearize(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(color: tuple[float, float, float, float]) -> float:
    red, green, blue = (linearize(channel) for channel in color[:3])
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: tuple[float, float, float, float], background: tuple[float, float, float, float]) -> float:
    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def threshold(kind: str, level: str) -> tuple[float, str]:
    if kind == "ui":
        return 3.0, "WCAG 2.2 SC 1.4.11 AA non-text contrast"
    values = {
        ("text", "AA"): 4.5,
        ("large-text", "AA"): 3.0,
        ("text", "AAA"): 7.0,
        ("large-text", "AAA"): 4.5,
    }
    return values[(kind, level)], f"WCAG 2.2 {level} {kind.replace('-', ' ')} contrast"


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate WCAG contrast for two hex colors.")
    parser.add_argument("foreground", help="foreground hex color")
    parser.add_argument("background", help="background hex color")
    parser.add_argument("--canvas", default="#ffffff", help="opaque layer behind transparent colors (default: #ffffff)")
    parser.add_argument("--kind", choices=("text", "large-text", "ui"), default="text")
    parser.add_argument("--level", choices=("AA", "AAA"), default="AA", help="text level; UI uses SC 1.4.11 AA")
    arguments = parser.parse_args()

    try:
        canvas = parse_color(arguments.canvas)
        if canvas[3] != 1:
            raise ValueError("--canvas must be opaque")
        background = composite(parse_color(arguments.background), canvas)
        foreground = composite(parse_color(arguments.foreground), background)
    except ValueError as error:
        parser.error(str(error))

    ratio = contrast_ratio(foreground, background)
    required, criterion = threshold(arguments.kind, arguments.level)
    passed = ratio >= required

    print(f"Contrast ratio: {ratio:.3f}:1")
    print(f"Requirement: {required:g}:1 ({criterion})")
    print("Result: PASS" if passed else "Result: FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
