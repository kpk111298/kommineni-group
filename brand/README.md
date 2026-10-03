# Brand

Every Kommineni Group business shares one look, so they read as one company.

## The system

- **Tile.** Every mark sits on the same rounded square.
- **Gold corner.** Every division tile has a small antique gold corner. It marks a Kommineni Group company. The group's own tile has a gold edge and a gold K instead.
- **Symbol.** One simple white symbol per business.
- **Wordmark.** Jost Medium in capitals, widely spaced. The line under it reads A Kommineni Group company.

## Colors

| Business | Color | Symbol |
|---|---|---|
| Kommineni Group | Navy `#0A0D16` with gold `#D9C08A` | K |
| Meel Motors | Brick `#A63A2B` | Wheel in motion |
| Meel Cart | Amber `#A85F0C` | Shopping bag |
| Meel Care | Green `#2F7A55` | Plus |
| Meel Move | Blue `#1F5FA8` | Forward arrows |
| Meel Pay | Violet `#4C3FA0` | Card |
| Meel Reach | Rose `#B23A68` | Broadcast signal |
| Kommineni HQ | Graphite `#3A3F4B` | Headquarters building |

Gold text on white uses `#8A7344` so it stays readable.

## Files

Each folder has:
- `mark.svg` and `mark.png` (512 px): the tile alone. Use for app icons, favicons and Streamlit `page_icon`.
- `lockup-light.svg`: tile and name for white backgrounds.
- `lockup-dark.svg`: tile and name on navy.

All text is already converted to shapes, so the logos look the same on any machine.

## Rebuilding

The logos are drawn by `tools/make_logos.py`. To change one, edit the script and run it from `brand/tools/` after putting the Jost font files (`jost-latin-400-normal.woff2`, `jost-latin-500-normal.woff2`, from the `@fontsource/jost` npm package) in `brand/tools/fonts/`. Jost is free under the SIL Open Font License.
