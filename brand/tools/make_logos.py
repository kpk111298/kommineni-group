"""Draws the Pkomm Group logos: a fine double-ring seal plus a serif wordmark."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT_DIR = os.environ.get("FONT_DIR", "fonts")
OUT = os.environ.get("OUT", "..")
SERIF = TTFont(f"{FONT_DIR}/cormorant-garamond-latin-500-normal.woff2")
SERIF_BOLD = TTFont(f"{FONT_DIR}/cormorant-garamond-latin-600-normal.woff2")
SANS = TTFont(f"{FONT_DIR}/jost-latin-400-normal.woff2")

NAVY, IVORY = "#0A0D16", "#F4F1EA"
GOLD, GOLD_TEXT = "#C9AE72", "#8A7344"

ENTITIES = {
    "pkomm-group": ("PKOMM GROUP", "A FICTIONAL COMPANY", GOLD),
    "pkomm-motors": ("PKOMM MOTORS", "A PKOMM GROUP COMPANY", "#7A2E2A"),
    "pkomm-cart": ("PKOMM CART", "A PKOMM GROUP COMPANY", "#8C5A1E"),
    # Planned businesses. Add them to ACTIVE when they launch.
    "pkomm-health": ("PKOMM HEALTH", "A PKOMM GROUP COMPANY", "#2F5D46"),
    "pkomm-freight": ("PKOMM FREIGHT", "A PKOMM GROUP COMPANY", "#2A4A73"),
    "pkomm-capital": ("PKOMM CAPITAL", "A PKOMM GROUP COMPANY", "#4E3A6B"),
    "pkomm-media": ("PKOMM MEDIA", "A PKOMM GROUP COMPANY", "#8A3A52"),
    "pkomm-hq": ("PKOMM HQ", "A PKOMM GROUP COMPANY", "#4A4F58"),
}
ACTIVE = ["pkomm-group", "pkomm-motors", "pkomm-cart"]

LINE = 'fill="none" stroke="{c}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'
GLYPHS = {
    "pkomm-motors": '<circle {l} cx="60" cy="60" r="22"/><circle {l} cx="60" cy="60" r="5"/>'
                   '<path {l} d="M60 65 V82 M55.5 58 L39 52 M64.5 58 L81 52"/>',
    "pkomm-cart": '<path {l} d="M44 52 H76 L73 82 H47 Z M52 52 V47 A8 8 0 0 1 68 47 V52"/>',
    "pkomm-health": '<path {l} d="M55 41 H65 V55 H79 V65 H65 V79 H55 V65 H41 V55 H55 Z"/>',
    "pkomm-freight": '<path {l} d="M38 60 H81 M71 50 L81 60 L71 70 M38 52 V68"/>',
    "pkomm-capital": '<path {l} d="M48 44 H72 L82 56 L60 82 L38 56 Z M38 56 H82 M53 44 L50 56 L60 82 L70 56 L67 44"/>',
    "pkomm-media": '<path {l} d="M60 37 L64.5 55.5 L83 60 L64.5 64.5 L60 83 L55.5 64.5 L37 60 L55.5 55.5 Z"/>',
    "pkomm-hq": '<path {l} d="M40 50 L60 38 L80 50 Z M46 55 V76 M55 55 V76 M65 55 V76 M74 55 V76 M38 81 H82"/>',
}


def text_path(font, text, size, x, y, tracking, fill, center=False):
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    advances = [font["hmtx"][cmap[ord(ch)]][0] * scale for ch in text]
    width = sum(advances) + tracking * size * (len(text) - 1)
    cx = x - width / 2 if center else x
    parts = []
    for ch, adv in zip(text, advances):
        pen = SVGPathPen(gs)
        gs[cmap[ord(ch)]].draw(TransformPen(pen, (scale, 0, 0, -scale, cx, y)))
        if pen.getCommands():
            parts.append(pen.getCommands())
        cx += adv + tracking * size
    return f'<path fill="{fill}" d="{" ".join(parts)}"/>', width


def seal(key, accent, dark):
    ring = GOLD if dark else accent
    ink = GOLD if dark else accent
    out = (f'<circle fill="none" stroke="{ring}" stroke-width="1.25" cx="60" cy="60" r="56"/>'
           f'<circle fill="none" stroke="{ring}" stroke-width="0.6" cx="60" cy="60" r="51"/>')
    if key == "pkomm-group":
        k, _ = text_path(SERIF_BOLD, "P", 62, 60, 81, 0, IVORY if dark else NAVY, center=True)
        return out + k
    return out + GLYPHS[key].replace("{l}", LINE).replace("{c}", ink)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def lockup(key, name, line, accent, dark):
    word, ww = text_path(SERIF, name, 36, 146, 66, 0.16, IVORY if dark else NAVY)
    rule = f'<path stroke="{GOLD}" stroke-width="0.8" d="M147 79.5 H{147 + 28}"/>'
    tag, tw = text_path(SANS, line, 10.5, 147, 98, 0.3, GOLD if dark else GOLD_TEXT)
    w = 146 + max(ww, tw) + 12
    bg = f'<rect width="{w:.0f}" height="120" fill="{NAVY}"/>' if dark else ""
    return svg(w, 120, bg + seal(key, accent, dark) + word + rule + tag, f"{name.title()} logo")


for key in ACTIVE:
    name, line, accent = ENTITIES[key]
    d = os.path.join(OUT, key)
    os.makedirs(d, exist_ok=True)
    open(f"{d}/mark.svg", "w").write(svg(120, 120, seal(key, accent, False), f"{name.title()} seal"))
    open(f"{d}/mark-dark.svg", "w").write(
        svg(120, 120, f'<rect width="120" height="120" rx="60" fill="{NAVY}"/>' + seal(key, accent, True), f"{name.title()} seal"))
    open(f"{d}/lockup-light.svg", "w").write(lockup(key, name, line, accent, False))
    open(f"{d}/lockup-dark.svg", "w").write(lockup(key, name, line, accent, True))
print("done")
