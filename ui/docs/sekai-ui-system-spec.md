# Sekai UI System v1
## Design & Implementation Specification

Version: 1.0  
Design Style: Notion-style Minimal UI  
Target Stack: Django Templates + Tailwind CSS  

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

The UI system should follow this repository structure.

```
sekai-ui-system/
├ README.md
│
├ design/
│   ├ tokens.json
│   └ design-principles.md
│
├ prompts/
│   ├ claude-system-prompt.md
│   ├ component-generation-prompt.md
│   └ page-generation-prompt.md
│
├ components/
│   ├ button.html
│   ├ input.html
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
├ figma/
│   └ figma-structure.md
│
└ docs/
    ├ sekai-ui-system-spec.md
    ├ COMPONENT_SPEC.md
    ├ usage.md
    ├ django-integration.md
    └ figma-to-code.md
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
    "success": "#15803D",
    "warning": "#B45309",
    "danger": "#B91C1C"
  },
  "font": {
    "family": "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "size_xs": "12px",
    "size_sm": "14px",
    "size_md": "16px",
    "size_lg": "20px",
    "size_xl": "24px",
    "line_height_sm": "1.4",
    "line_height_md": "1.6",
    "line_height_lg": "1.3"
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
    "sm": "0 1px 2px rgba(0,0,0,0.04)"
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

Create reusable UI components.

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
- right-aligned actions

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

Create:

```
prompts/claude-system-prompt.md
```

Content:

```
You are implementing UI using Sekai UI System.

Rules:

- Always reference design/tokens.json
- Reuse existing components whenever possible
- Maintain Notion-style minimal UI
- Avoid flashy visual design
- Avoid heavy shadows
- Maintain consistent spacing
- Use Tailwind CSS
- Structure templates for Django reuse
```

---

# 10. Figma Structure

Define the Figma file structure in:

```
figma/figma-structure.md
```

Pages:

```
00 Foundations
01 Components
02 Layouts
03 Screens
```

Foundations include:

- colors
- typography
- spacing
- radius
- shadows

Components include:

- buttons
- inputs
- cards
- tables
- sidebar

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
