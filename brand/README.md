# Brand

Every Kommineni Group business shares one look, so they read as one company. The style is classic and quiet: fine lines, a serif name, navy and antique gold.

## The system

- **Seal.** Every mark is a fine double ring: an outer line and a thinner inner line.
- **Symbol.** One simple line drawing inside the seal, drawn with a thin round stroke. The group's seal holds a serif K instead.
- **Accent.** Each division draws its seal in its own deep accent color. The group's seal is gold.
- **Wordmark.** Cormorant Garamond Medium in capitals, widely spaced, in navy.
- **Gold rule and endorsement.** A short gold line under the name, then A KOMMINENI GROUP COMPANY in Jost, small and widely spaced. The group reads ILLINOIS · EST. 2026.
- **On navy.** Every seal turns gold and the name turns ivory.

## Colors

| Business | Accent | Symbol |
|---|---|---|
| Kommineni Group | Gold `#C9AE72` on navy `#0A0D16` | Serif K |
| Meel Motors | Oxblood `#7A2E2A` | Steering wheel |
| Meel Cart | Ochre `#8C5A1E` | Shopping bag |
| Meel Care | Forest `#2F5D46` | Cross |
| Meel Move | Ink blue `#2A4A73` | Arrow |
| Meel Pay | Plum `#4E3A6B` | Cut gem |
| Meel Reach | Rosewood `#8A3A52` | Guiding star |
| Kommineni HQ | Slate `#4A4F58` | Columned building |

Gold text on white uses `#8A7344` so it stays readable. Ivory on navy is `#F4F1EA`.

## Files

Each folder has:
- `mark.svg` and `mark.png` (512 px): the seal on a clear background. Favicons, dashboard page icons, avatars.
- `mark-dark.svg`: the gold seal on a navy disc.
- `lockup-light.svg`: seal and name for white backgrounds.
- `lockup-dark.svg`: seal and name on navy.

All text is already drawn as shapes, so the logos look the same on any machine.

## Rules

- Keep clear space around a logo equal to a quarter of the seal.
- Smallest seal: 32px. Below that the fine lines get too faint.
- Don't fill the seal, thicken the lines, add shadows, or swap a division's accent or symbol.

## Rebuilding

The logos are drawn by `tools/make_logos.py`. To change one, edit the script and run it from `brand/tools/` after putting these font files in `brand/tools/fonts/`:
- `cormorant-garamond-latin-500-normal.woff2` and `cormorant-garamond-latin-600-normal.woff2` from the `@fontsource/cormorant-garamond` npm package
- `jost-latin-400-normal.woff2` from the `@fontsource/jost` npm package

Both fonts are free under the SIL Open Font License.
