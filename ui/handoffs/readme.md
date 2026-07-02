# Sekai Design System

A design system for **Sekai** — an app for recording, managing, and realizing the dreams you want to achieve in life. Users register up to **100 dreams**, each with a short description and up to **4 images**, and can share any dream to **X**.

The visual language is **Notion-style minimal**: a white canvas, subtle warm-gray borders, a single restrained blue accent, and hierarchy built from spacing and typography rather than decoration. It is calm, readable, and quiet so the user's dreams — not the UI — carry the emotion.

---

## Sources

This system was built from the company's own design-system repository. The reader is encouraged to explore it directly for deeper fidelity:

- **GitHub — design system:** https://github.com/kojiito-sekaiinc/sekai-ui-system
  - `design/tokens.json` — canonical color / type / spacing / radius / shadow values (mirrored into `tokens/*.css` here)
  - `design/design-principles.md` — the full Notion-minimal philosophy
  - `AI_RULES.md` — rules for AI agents generating UI in the system
  - `components/`, `layouts/`, `examples/` — the original Tailwind + Django template implementations

The source repo ships UI as **Django templates styled with Tailwind** using `sekai-*` color utilities. This design system re-expresses those same tokens as **CSS custom properties + self-contained React components** so they can be composed in prototypes and mocks here, while staying value-for-value faithful to the originals.

---

## Content Fundamentals

The product surface is **Japanese**; system/foundation docs are bilingual. Copy is **warm, quiet, and second-person-implicit** — it speaks softly to the user without barking commands.

- **Language & person:** Japanese product copy. Addresses the user gently as *あなた* ("あなたが人生で叶えたい夢") but usually drops the pronoun. First-person appears only inside user-authored content (e.g. a share card: "私の夢").
- **Tone:** aspirational but understated. "夢を、現実に。" / "もう叶えた夢。おめでとう。" Encouraging, never hype-y or salesy. No exclamation-stacking.
- **Casing (Latin):** the wordmark and UI labels use sentence case or simple capitalization ("Dreams, one at a time."). No ALL-CAPS shouting; uppercase is reserved for small tracked section labels in the sidebar.
- **Verbs/labels:** short imperative nouns+する on actions — 夢を追加 / 保存 / 編集 / シェア / キャンセル. Status is a single word: 下書き・進行中・実現済み.
- **Numbers:** progress is framed as a journey, not a KPI — "37 / 100 実現", "人生の進捗". Tabular numerals, no decorative stats.
- **Emoji:** **none.** The brand never uses emoji in UI. State is shown with a small colored dot + word, never an emoji.
- **Vibe:** a quiet personal notebook for your life's ambitions. Think Notion's calm, not a gamified habit tracker.

---

## Visual Foundations

- **Color:** white base (`--color-bg` `#FFFFFF`). Secondary surfaces and the sidebar use warm off-white `--color-bg-subtle` `#F7F7F5`. A **single** blue accent `--color-primary` `#2F6FEB` is used sparingly — primary buttons and active nav only. Text is near-black `#191919`, muted `#6B7280`, subtle `#9CA3AF`. Status colors (green/amber/red) appear **only** to communicate state, always paired with text. **No gradients. No second accent. No neon.**
- **Type:** **Inter** for Latin/numerals, **Noto Sans JP** for Japanese (see Substitutions). Scale: 24 / 20 / 16 / 14 / 12 px. Weights 400 / 500 / 600 only — 600 for titles, 500 for labels & emphasis, 400 for body. Hierarchy comes from size + weight, not color or decoration. Line height 1.3 (titles) → 1.6 (body).
- **Spacing:** 8px base scale (8/12/16/20/24/32/40/48). Spacing does the work of separation, **reducing the need for borders and shadows**. Larger gaps between sections, tight gaps within compact components.
- **Borders:** subtle 1px `--color-border` `#E7E5E4` everywhere; `--color-border-strong` `#D6D3D1` only for emphasis or hover. Borders, not shadows, define cards.
- **Shadow:** **minimal by design.** `--shadow-none` is the default for almost everything; `--shadow-sm` (`0 1px 2px rgba(0,0,0,.04)`) is permitted only for floating elements — modals, the auth card. No layered or large drop shadows.
- **Radius:** 6px (inputs, tags, badges), 8px (buttons, cards, dropdowns), 10px (modals, large panels). Never mixed arbitrarily within one component.
- **Backgrounds:** flat white / off-white. **No** background images, textures, patterns, or gradients in chrome. Imagery appears **only** as user-supplied dream photos — full-color, full-bleed inside cards, never tinted or filtered by the system.
- **Imagery treatment:** dream photos are shown true-to-color (no duotone, no grain, no forced warm/cool grade). One image fills the card; 2–4 images form a 1 + 3 mosaic with a `+N` overlay for extras. Cover aspect ~16:10 in cards, 4:3 on the detail page.
- **Cards:** white surface, 1px border, 8px radius, **no shadow**. Interactive cards darken their border to `border-strong` on hover — nothing else moves.
- **Hover states:** background shifts to `--color-surface-hover` `#F5F5F4`; primary buttons darken to `--color-primary-hover`; ghost text darkens muted→text. Color-only, fast.
- **Press / focus:** focus shows a 3px subtle ring (`--color-primary-subtle` / `--color-danger-subtle`) plus a solid border in the accent color. No shrink/scale animations.
- **Motion:** fast and subtle — 100–150ms color/border transitions only. **No** bounce, no decorative loops, no transitions over 150ms. Reduced-motion-safe by default (motion is incidental).
- **Transparency / blur:** used sparingly — the status badge over a photo sits on `rgba(255,255,255,.92)` with a light backdrop blur; the modal scrim is `rgba(25,25,25,.4)`. Not used as decoration.
- **Layout:** fixed three-part app shell — 56px topbar, 240px sidebar (on `--color-bg-subtle`), content capped at 1200px. Auth pages center a narrow card on the subtle background.

---

## Iconography

- **System:** **Heroicons (outline)** style — 24px grid, **1.5–2px** stroke, `currentColor`, round caps/joins. The source repo hand-inlines these exact paths (hamburger, bell, chevron); this system follows suit. Icons are line/outline, never filled, except brand glyphs.
- **Delivery:** inline `<svg>` with `stroke="currentColor"` so icons inherit text color and size via `width/height`. **No icon font, no sprite, no PNG icons.** If you need the full set, load Heroicons from CDN (https://heroicons.com) at the same stroke weight.
- **The one filled glyph:** the **X (Twitter)** logo for the Share action — solid `fill="currentColor"`, since the brand requires its official mark.
- **Emoji / unicode-as-icon:** **never.** Status uses a colored dot + word, not an emoji or symbol.
- **Substitution flag:** the icon paths used in cards and the UI kit are Heroicons-outline equivalents chosen to match the repo's inlined SVGs. Swap for the canonical Heroicons package when integrating into production.

> **Note — no logo file in the source repo.** The brand identity is a **text wordmark** ("Sekai", semibold, −0.02em tracking), optionally with a small blue dot mark. There is no raster/vector logo asset to copy; the wordmark in `assets/brand-wordmark.card.html` reproduces the repo's `topbar_brand` treatment. Provide an official logo if one exists.

---

## Font substitution

The source repo specifies **Inter** with system-ui fallbacks but ships **no font binaries**. This system loads Inter from Google Fonts and **adds Noto Sans JP** (also Google Fonts) because the product copy is Japanese and Inter has no Japanese glyphs. **Please confirm the intended Japanese typeface and supply licensed/self-hosted binaries if Google Fonts is not acceptable.**

---

## Index / Manifest

**Foundations**
- `styles.css` — global entry point (imports only). Consumers link this one file.
- `tokens/colors.css` · `tokens/typography.css` · `tokens/spacing.css` · `tokens/fonts.css` · `tokens/base.css`
- `guidelines/*.card.html` — specimen cards (colors, type, spacing, radius/shadow)
- `assets/brand-wordmark.card.html` · `assets/iconography.card.html`

**Components** (`window.SekaiDesignSystem_2572f3.*`)
- `components/core/` — **Button**, **Card**, **Badge**, **Avatar**
- `components/forms/` — **Input**, **Textarea**, **Select**
- `components/feedback/` — **ProgressBar**
- `components/product/` — **DreamCard** (the core unit of the app)

Each component directory has `<Name>.jsx`, `<Name>.d.ts`, `<Name>.prompt.md`, and a `*.card.html` specimen.

**UI kit**
- `ui_kits/dreams/` — interactive recreation of the Sekai Dreams app: dream grid + life-progress, dream detail with image gallery, add/edit form (title, description, 4 image slots, status), and the Share-to-X modal. Entry: `ui_kits/dreams/index.html`.

**Other**
- `SKILL.md` — Agent-Skill manifest for using this system in Claude Code.
- `AI_RULES.md`, `design/`, `docs/` — imported reference docs from the source repo.

---

*Built from `kojiito-sekaiinc/sekai-ui-system`. Explore that repo for the authoritative Django/Tailwind implementations.*
