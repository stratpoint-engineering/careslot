"""Design fidelity guards: tokens.css matches the design system, and templates use tokens only."""

import colorsys
import re
from pathlib import Path

from django.conf import settings

ROOT = Path(settings.BASE_DIR)
HEX = re.compile(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})")
HSL = re.compile(r"(--[\w-]+):\s*hsl\(([\d.]+) ([\d.]+)% ([\d.]+)%\)")


def _hsl_to_hex(h: float, s: float, light: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h / 360, light / 100, s / 100)
    return "#{:02x}{:02x}{:02x}".format(*(round(c * 255) for c in (r, g, b)))


def _hsl_blocks(text: str) -> dict[str, dict[str, str]]:
    light, _, dark = text.partition(".dark")
    out = {}
    for name, part in (("light", light), ("dark", dark)):
        out[name] = {
            k: _hsl_to_hex(float(h), float(s), float(lum)) for k, h, s, lum in HSL.findall(part)
        }
    return out


def _close(a: str, b: str) -> bool:
    return all(abs(int(a[i : i + 2], 16) - int(b[i : i + 2], 16)) <= 1 for i in (1, 3, 5))


def test_tokens_match_design_system() -> None:
    source = (ROOT / "docs/designs/design-system/tokens.css").read_text()
    light, _, dark = source.partition(".dark")
    expected = {"light": dict(HEX.findall(light)), "dark": dict(HEX.findall(dark))}
    actual = _hsl_blocks((ROOT / "static/css/tokens.css").read_text())
    assert actual.keys() == expected.keys()
    for mode in expected:
        assert actual[mode].keys() == expected[mode].keys(), mode
        for key, hex_value in expected[mode].items():
            assert _close(actual[mode][key], hex_value.lower()), (mode, key)


def test_no_raw_colours_outside_tokens() -> None:
    raw = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(")
    offenders = []
    for path in [*(ROOT / "templates").rglob("*.html"), ROOT / "static/css/components.css"]:
        if raw.search(path.read_text()):
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_no_inline_style_attributes() -> None:
    # The CSP allows styles from our own files only; an inline style="" would be blocked.
    offenders = [
        str(p.relative_to(ROOT))
        for p in (ROOT / "templates").rglob("*.html")
        if "email" not in p.parts and re.search(r"\sstyle=", p.read_text())
    ]
    assert offenders == []
