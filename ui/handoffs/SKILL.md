---
name: sekai-design
description: Use this skill to generate well-branded interfaces and assets for Sekai (a Japanese app for recording and realizing life dreams), either for production or throwaway prototypes/mocks. Contains Sekai's design guidelines, colors, type, fonts, icon approach, reusable components, and the Dreams app UI kit. Notion-style minimal: white canvas, subtle gray borders, one blue accent, calm.
user-invocable: true
---

Read the `readme.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Where things are
- `styles.css` — link this one file to inherit every token (colors, type, spacing, radius, fonts). Imports `tokens/*.css`.
- `tokens/` — CSS custom properties (`--color-*`, `--text-*`, `--space-*`, `--radius-*`). Never hardcode values; use the tokens.
- `components/` — self-contained React primitives: Button, Card, Badge, Avatar (core); Input, Textarea, Select (forms); ProgressBar (feedback); DreamCard (product). Each has a `.prompt.md` with usage.
- `ui_kits/dreams/` — a full interactive recreation of the Sekai Dreams app; copy its patterns for product screens.
- `readme.md` — Content Fundamentals, Visual Foundations, Iconography. Read before designing.

## Non-negotiables (Notion-minimal)
- White base, warm off-white (`#F7F7F5`) for sidebars/secondary surfaces. One blue accent (`#2F6FEB`), used sparingly — at most one primary button per view.
- Hierarchy from spacing + typography, not decoration. Inter (Latin) + Noto Sans JP (日本語). Weights 400/500/600 only.
- Borders define cards (1px `#E7E5E4`), not shadows. Shadow is near-absent (`shadow-sm` only for modals/floating).
- Radii 6/8/10px. Motion is 100–150ms color/border only — no bounce, no decorative animation.
- Heroicons outline (1.5–2px stroke, currentColor), inline SVG. The only filled glyph is the X share logo. **No emoji, ever.** Status = colored dot + word.
- Japanese product copy: warm, quiet, understated. Short noun+する action labels (夢を追加 / 保存 / シェア).
