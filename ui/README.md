# Sekai UI System

A reusable, minimal UI framework for building SaaS applications with Django and Tailwind CSS.

---

## What is Sekai UI System?

Sekai UI System is a design system and component library built for rapid, consistent UI development across multiple Django-based applications.

It provides:

- **Design tokens** — a single source of truth for all visual values (colors, spacing, typography, radius, shadows)
- **Layout templates** — reusable Django template shells for authenticated app pages and auth flows
- **UI components** — minimal, composable HTML components styled with Tailwind CSS
- **Example screens** — reference pages for dashboards, list views, and forms
- **AI prompts** — system prompts and generation prompts for Claude and other AI agents

The system is optimized for:

- dashboards
- analytics tools
- CRUD admin interfaces
- SaaS application panels
- AI-powered productivity tools

---

## Design Philosophy

Sekai UI System follows a **Notion-style minimal interface philosophy**.

The UI is designed to feel calm, readable, and professional. Visual hierarchy is established through spacing and typography rather than decoration, color, or shadows.

Key characteristics:

- white base background
- subtle gray borders and separators
- typography-driven layout hierarchy
- generous, consistent whitespace
- minimal decoration and almost no shadows
- low visual noise

What to avoid:

- gradients or heavy background fills
- bright or saturated accent colors
- large drop shadows
- unnecessary animations
- skeuomorphic or overly decorative UI patterns

All visual values are defined in `design/tokens.json` and must never be hardcoded elsewhere.

For full details, see [design/design-principles.md](design/design-principles.md).

---

## Repository Structure

```
sekai-ui-system/
├── README.md                        # This file
│
├── design/
│   ├── tokens.json                  # Design tokens (colors, spacing, typography, etc.)
│   └── design-principles.md         # Design philosophy and usage rules
│
├── docs/
│   ├── sekai-ui-system-spec.md      # Full system specification
│   ├── COMPONENT_SPEC.md            # Component design and implementation rules
│   ├── usage.md                     # General usage guide
│   ├── django-integration.md        # Django-specific integration guide
│   └── figma-to-code.md             # Figma to code workflow
│
├── prompts/
│   ├── claude-system-prompt.md      # System prompt for AI-assisted development
│   ├── component-generation-prompt.md
│   └── page-generation-prompt.md
│
├── components/
│   ├── button.html                  # Button variants (primary, secondary, ghost, danger)
│   ├── input.html                   # Text input with optional error state
│   ├── card.html                    # Content grouping card
│   ├── table.html                   # Data table with hover and action columns
│   ├── sidebar.html                 # Vertical navigation sidebar
│   └── page_header.html             # Page title, description, and action area
│
├── layouts/
│   ├── base.html                    # Base HTML shell with Tailwind CSS
│   ├── app_shell.html               # Authenticated app layout (topbar + sidebar + content)
│   └── auth.html                    # Centered auth layout (login, register, reset)
│
├── examples/
│   ├── dashboard.html               # Dashboard with stat cards and activity table
│   ├── list.html                    # List page with search, table, and pagination
│   └── form.html                    # Form page with inputs and submit actions
│
├── figma/
│   └── figma-structure.md           # Figma file organization guide
│
└── AI_RULES.md                      # Rules for AI agents generating UI in this system
```

---

## Implementation Phases

The system is built incrementally across four phases.

### Phase 1 — Foundations

Establishes the design foundation.

Files:
- `design/tokens.json`
- `design/design-principles.md`
- `README.md`

### Phase 2 — Layouts

Creates the structural HTML shells for all page types.

Files:
- `layouts/base.html`
- `layouts/app_shell.html`
- `layouts/auth.html`

### Phase 3 — Components

Implements the core reusable UI components.

Files:
- `components/button.html`
- `components/input.html`
- `components/card.html`
- `components/table.html`
- `components/sidebar.html`
- `components/page_header.html`

### Phase 4 — Example Screens

Demonstrates the system with complete reference pages.

Files:
- `examples/dashboard.html`
- `examples/list.html`
- `examples/form.html`

---

## Django Integration

Sekai UI System is built for Django Templates and Tailwind CSS.

### Setup

1. Copy the `layouts/` and `components/` directories into your Django project's templates directory.
2. Register the template directories in `settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        ...
    }
]
```

3. Install Tailwind CSS via the CDN or the `django-tailwind` package. Reference the CDN in `layouts/base.html`.

### Extending Layouts

Extend `app_shell.html` for authenticated pages:

```django
{% extends "layouts/app_shell.html" %}

{% block page_title %}Dashboard{% endblock %}

{% block content %}
  {% include "components/page_header.html" with title="Dashboard" %}
  {# page content #}
{% endblock %}
```

Extend `auth.html` for login and registration pages:

```django
{% extends "layouts/auth.html" %}

{% block content %}
  <h1>Sign in</h1>
  {# auth form #}
{% endblock %}
```

### Using Components

Include components with `{% include %}` and pass context variables:

```django
{% include "components/card.html" with title="Total Users" value="1,204" %}

{% include "components/button.html" with label="Save" variant="primary" %}
```

### Design Token Reference

All visual values are defined in `design/tokens.json`. When writing custom Tailwind classes, align values with the token scale. Do not introduce arbitrary color or spacing values outside the defined tokens.

For a full integration walkthrough, see [docs/django-integration.md](docs/django-integration.md).

---

## AI Development

Sekai UI System is designed for AI-assisted development with tools like Claude Code.

When generating or modifying UI, AI agents must:

1. Read `docs/sekai-ui-system-spec.md`
2. Read `design/design-principles.md`
3. Read `design/tokens.json`
4. Check existing components before creating new ones
5. Follow the Notion-style minimal design philosophy

See [AI_RULES.md](AI_RULES.md) for the full set of rules.
