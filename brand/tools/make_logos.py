import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = {w: TTFont(f"fonts/jost-latin-{w}-normal.woff2") for w in (400, 500)}
OUT = ".."

NAVY, GOLD = "#0A0D16", "#D9C08A"
GOLD_ON_LIGHT = "#8A7344"
INK, PAPER = "#0A0D16", "#FFFFFF"

ENTITIES = {
    "kommineni-group": ("KOMMINENI GROUP", None, NAVY),
    "meel-motors": ("MEEL MOTORS", "Car dealership", "#A63A2B"),
    "meel-cart": ("MEEL CART", "Online store", "#A85F0C"),
    "meel-care": ("MEEL CARE", "Clinics and health plan", "#2F7A55"),
    "meel-move": ("MEEL MOVE", "Logistics", "#1F5FA8"),
    "meel-pay": ("MEEL PAY", "Loans and payments", "#4C3FA0"),
    "meel-reach": ("MEEL REACH", "Marketing", "#B23A68"),
    "kommineni-hq": ("KOMMINENI HQ", "HR, finance, support", "#3A3F4B"),
}

S = 'fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
GLYPHS = {
    "kommineni-group": '<path {s} d="M43 30 V90 M80 30 L44 64 M58 51 L82 90"/>',
    "meel-motors": '<circle {s} cx="68" cy="60" r="24"/><circle fill="{c}" cx="68" cy="60" r="6"/>'
                   '<path {s} d="M20 50 H34 M14 64 H32 M24 78 H38"/>',
    "meel-cart": '<path {s} d="M33 50 H87 L82 90 H38 Z M48 50 V44 A12 12 0 0 1 72 44 V50"/>',
    "meel-care": '<path fill="none" stroke="{c}" stroke-width="16" stroke-linecap="round" d="M60 34 V86 M34 60 H86"/>',
    "meel-move": '<path {s} d="M36 36 L58 60 L36 84 M62 36 L84 60 L62 84"/>',
    "meel-pay": '<rect {s} x="28" y="36" width="64" height="48" rx="9"/><path {s} d="M28 53 H92 M40 70 H56"/>',
    "meel-reach": '<circle fill="{c}" cx="60" cy="60" r="8"/>'
                  '<path {s} d="M45 45 A21 21 0 0 0 45 75 M75 45 A21 21 0 0 1 75 75 M33 33 A38 38 0 0 0 33 87 M87 33 A38 38 0 0 1 87 87"/>',
    "kommineni-hq": '<path {s} d="M32 46 L60 30 L88 46 Z M44 54 V82 M60 54 V82 M76 54 V82 M30 90 H90"/>',
}


def text_path(text, size, weight, x, y, tracking, fill):
    font = FONTS[weight]
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    upm = font["head"].unitsPerEm
    scale = size / upm
    parts, cx = [], x
    for ch in text:
        name = cmap.get(ord(ch))
        adv = font["hmtx"][name][0]
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cx, y)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        cx += adv * scale + tracking * size
    width = cx - x - tracking * size
    return f'<path fill="{fill}" d="{" ".join(parts)}"/>', width


def tile(key, color, ox=0, oy=0):
    uid = f"{key}-{ox}-{oy}"
    tile_fill = NAVY if key == "kommineni-group" else color
    glyph_color = GOLD if key == "kommineni-group" else "#FFFFFF"
    out = f'<g transform="translate({ox} {oy})"><clipPath id="t-{uid}"><rect width="120" height="120" rx="26"/></clipPath>'
    out += f'<rect width="120" height="120" rx="26" fill="{tile_fill}"/>'
    if key == "kommineni-group":
        out += f'<rect x="1.5" y="1.5" width="117" height="117" rx="24.5" fill="none" stroke="{GOLD}" stroke-opacity="0.55" stroke-width="3"/>'
    if key != "kommineni-group":
        out += f'<polygon clip-path="url(#t-{uid})" points="92,0 120,0 120,28" fill="{GOLD}"/>'
    out += GLYPHS[key].replace("{s}", S).replace("{c}", glyph_color) + "</g>"
    return out


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h}" width="{w:.0f}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def lockup(key, name, color, dark):
    ink = PAPER if dark else INK
    sub = GOLD if dark else GOLD_ON_LIGHT
    word, ww = text_path(name, 40, 500, 148, 66, 0.14, ink)
    line = "A KOMMINENI GROUP COMPANY" if key != "kommineni-group" else "DATA ENGINEERING SHOWCASE"
    tag, tw = text_path(line, 13, 400, 149, 96, 0.22, sub)
    w = 148 + max(ww, tw) + 8
    bg = f'<rect width="{w:.0f}" height="120" fill="{NAVY}"/>' if dark else ""
    return svg(w, 120, bg + tile(key, color) + word + tag, f"{name.title()} logo")


os.makedirs(OUT, exist_ok=True)
for key, (name, _, color) in ENTITIES.items():
    d = os.path.join(OUT, key)
    os.makedirs(d, exist_ok=True)
    open(f"{d}/mark.svg", "w").write(svg(120, 120, tile(key, color), f"{name.title()} mark"))
    open(f"{d}/lockup-light.svg", "w").write(lockup(key, name, color, False))
    open(f"{d}/lockup-dark.svg", "w").write(lockup(key, name, color, True))
print("done")
