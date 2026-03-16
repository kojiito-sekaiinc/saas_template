# Sekai UI System v1
## Design & Implementation Specification

Version: 1.0
Design Style: Notion-style Minimal UI
Target Stack: Django Templates + Tailwind CSS

> **Document scope:** This file is the build specification from which the system was constructed.
> It describes both implemented features and future plans; each section is labelled accordingly.
> For current component APIs, refer to the inline documentation at the top of each template file.

---

# 1. Overview

Sekai UI System is a reusable UI framework designed for building multiple SaaS-style applications quickly and consistently.

The goal is to create a UI system that:

- maintains consistent visual design
- is easy for AI agents to understand
- is reusable across multiple projects
- minimizes UI design decisions
- produces clean, calm interfaces similar to Notion

The system will be used in:

- dashboards
- analytics tools
- CRUD interfaces
- SaaS admin panels
- AI tools
- productivity applications

---

# 2. Design Philosophy

Sekai UI System follows **Notion-style minimalism**.

Key characteristics:

- white base UI
- subtle gray separators
- typography-driven layout
- generous whitespace
- minimal decoration
- low visual noise

The UI should feel:

- calm
- readable
- professional
- stable
- timeless

---

## Avoid

The following must be avoided:

- heavy shadows
- bright gradients
- neon colors
- overly colorful UI
- unnecessary animations
- skeuomorphic designs
- inconsistent spacing

---

# 3. Technology Requirements

The system must be implemented using:

- HTML
- Tailwind CSS
- Django Templates

JavaScript should be minimal.

Components must be structured so that AI agents such as ClaudeCode can easily reuse them.

---

# 4. Repository Structure

**Status: Implemented** (reflects current state of the repository)

```
sekai-ui-system/
├ README.md
├ AI_RULES.md
│
├ design/
│   ├ tokens.json
│   └ design-principles.md
│
├ components/
│   ├ button.html
│   ├ input.html
│   ├ select.html
│   ├ card.html
│   ├ table.html
│   ├ sidebar.html
│   └ page_header.html
│
├ layouts/
│   ├ base.html
│   ├ app_shell.html
│   └ auth.html
│
├ examples/
│   ├ dashboard.html
│   ├ list.html
│   └ form.html
│
└ docs/
    ├ sekai-ui-system-spec.md
    ├ COMPONENT_SPEC.md
    └ UI_EXAMPLES.md
```

---

# 5. Design Tokens

Create the file:

```
design/tokens.json
```

with the following content:

```json
{
  "color": {
    "bg": "#FFFFFF",
    "bg_subtle": "#F7F7F5",
    "surface": "#FFFFFF",
    "surface_hover": "#F5F5F4",
    "border": "#E7E5E4",
    "border_strong": "#D6D3D1",
    "text": "#191919",
    "text_muted": "#6B7280",
    "text_subtle": "#9CA3AF",
    "primary": "#2F6FEB",
    "primary_hover": "#1D4ED8",
    "primary_subtle": "#EEF4FF",
    "success": "#15803D",
    "warning": "#B45309",
    "danger": "#B91C1C",
    "danger_subtle": "#FEF2F2",
    "success_subtle": "#F0FDF4",
    "warning_subtle": "#FFFBEB"
  },
  "font": {
    "family": "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "size_xs": "12px",
    "size_sm": "14px",
    "size_md": "16px",
    "size_lg": "20px",
    "size_xl": "24px",
    "line_height_tight": "1.3",
    "line_height_normal": "1.4",
    "line_height_relaxed": "1.6",
    "weight_normal": "400",
    "weight_medium": "500",
    "weight_semibold": "600"
  },
  "radius": {
    "sm": "6px",
    "md": "8px",
    "lg": "10px"
  },
  "spacing": {
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px"
  },
  "shadow": {
    "none": "none",
    "sm": "0 1px 2px rgba(0, 0, 0, 0.04)"
  },
  "layout": {
    "content_max_width": "1200px",
    "sidebar_width": "240px",
    "header_height": "56px"
  }
}
```

---

# 6. Layout Templates

Create the following layout templates.

---

## base.html

Responsibilities:

- global HTML structure
- Tailwind CSS inclusion
- global message area
- page content container

---

## app_shell.html

Layout used for authenticated application pages.

Structure:

```
Topbar
Sidebar
Main Content
```

Rules:

- sidebar width fixed
- content max width from tokens
- header height from tokens

Responsive behavior:

- Minimum supported viewport: 360px.
- Below `md:` (768px): sidebar is hidden by default. A hamburger button in the topbar opens an offcanvas drawer that slides in from the left, overlaid on the page with a semi-transparent backdrop. Tapping the backdrop or pressing Esc closes the drawer. The main content area uses no left margin at this size.
- At `md:` and above: sidebar is permanently visible at 240px (`layout.sidebar_width`). The main content area is offset left by the sidebar width. The hamburger button is hidden.
- `topbar_center` block is always hidden below `sm:` (640px). The topbar has no horizontal room at narrow widths. Do not place mobile-required functionality in this block — use `topbar_actions` or the top of `page_content` instead.

---

## auth.html

Layout used for:

- login
- register
- password reset

Characteristics:

- centered layout
- narrow container
- minimal decoration

---

# 7. Core Components

**Status: Implemented**

---

## button.html

Variants:

- primary
- secondary
- ghost
- danger

Rules:

- consistent height
- rounded corners
- minimal shadow
- Tailwind CSS styling

---

## input.html

Characteristics:

- border-based field
- white background
- primary focus ring
- optional error state
- password input type support
- optional help text below the field

---

## select.html

Characteristics:

- matches input.html visual design and API
- choices provided as a list of dicts from view context
- optional error state and help text
- selected_value for pre-selection

---

## card.html

Usage:

- dashboard blocks
- content grouping
- settings panels

Rules:

- white background
- border
- minimal shadow

---

## table.html

Characteristics:

- soft row borders
- hover highlight
- minimal header styling
- right-aligned actions column — **requires `show_actions=True`** to appear; hidden by default
- outer wrapper carries `overflow-x-auto` on all breakpoints — table scrolls horizontally on narrow viewports; row data is not reflowed into cards

Note: the actions column is not shown automatically. Pass `show_actions=True` explicitly when including the component, or the actions column and its header will be omitted regardless of whether rows contain action data.

---

## sidebar.html

Characteristics:

- vertical navigation
- fixed width
- subtle active state
- icons optional

---

## page_header.html

Structure:

```
Title
Description
Action Button
```

Reusable across all pages.

---

# 8. Example Screens

Create the following example pages.

---

## dashboard.html

Structure:

- page header
- stat cards
- activity table

---

## list.html

Structure:

- page header
- search/filter bar
- data table
- pagination

---

## form.html

Structure:

- page header
- form container
- submit buttons

---

# 9. Claude System Prompt

**Status: Future plan — not yet implemented**

Planned location: `prompts/claude-system-prompt.md`

Intended content: a system prompt instructing AI agents to reference
design tokens, reuse existing components, and maintain the Notion-style
minimal design philosophy. Currently, `AI_RULES.md` serves this purpose.

---

# 10. Figma Structure

**Status: Future plan — not yet implemented**

Planned location: `figma/figma-structure.md`

Intended to define a Figma file with pages: Foundations, Components,
Layouts, and Screens — mirroring the repository structure.

---

# 11. Implementation Phases

Build the system incrementally.

---

## Phase 1

Foundation files:

- tokens.json
- design-principles.md
- README.md

---

## Phase 2

Core layouts:

- base.html
- app_shell.html
- auth.html

---

## Phase 3

Core components:

- button.html
- input.html
- select.html
- card.html
- table.html
- sidebar.html
- page_header.html

---

## Phase 4

Example screens:

- dashboard.html
- list.html
- form.html

---

# 12. Completion Criteria

The UI system is complete when:

- layouts render correctly
- components are reusable
- design tokens control visual style
- pages are readable and consistent
- new pages can be created quickly
- AI agents can reuse components easily

The UI must support:

- SaaS dashboards
- AI tools
- analytics apps
- CRUD admin panels

---

# End of Specification
