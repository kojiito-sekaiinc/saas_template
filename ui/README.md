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
- **AI rules** — rules and guidelines for AI agents generating UI in this system (`AI_RULES.md`)

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
├── AI_RULES.md                      # Rules for AI agents generating UI in this system
│
├── design/
│   ├── tokens.json                  # Design tokens (colors, spacing, typography, etc.)
│   └── design-principles.md         # Design philosophy and usage rules
│
├── docs/
│   ├── sekai-ui-system-spec.md      # Full system specification
│   ├── COMPONENT_SPEC.md            # Component design and implementation rules
│   └── UI_EXAMPLES.md               # UI pattern examples and guidelines
│
├── components/
│   ├── button.html                  # Button variants (primary, secondary, ghost, danger)
│   ├── input.html                   # Text input with optional error state
│   ├── select.html                  # Select dropdown with optional error state
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
└── examples/
    ├── dashboard.html               # Dashboard with stat cards and activity table
    ├── list.html                    # List page with search, table, and pagination
    └── form.html                    # Form page with inputs and submit actions
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
- `components/select.html`
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

1. `ui/` ディレクトリをプロジェクトルートに配置し、`settings.py` の `TEMPLATES["DIRS"]` に追加します。
   ファイルのコピーは不要です。`ui/` を独立したディレクトリとして直接参照してください。

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "ui"],
        ...
    }
]
```

この設定により `{% extends "layouts/app_shell.html" %}` や `{% include "components/button.html" %}` が
`ui/` 以下のファイルを参照します。

2. **開発時**: `layouts/base.html` の Tailwind Play CDN (`cdn.tailwindcss.com`) をそのまま使用できます。
   **本番前**: `tailwindcss` CLI で CSS をビルドし、CDN を `<link rel="stylesheet">` に置き換えてください。
   CDN のまま本番稼働させると、CSP 制限・外部通信制限がある環境でスタイルが消失します。

### Extending Layouts

Extend `app_shell.html` for authenticated pages:

```django
{% extends "layouts/app_shell.html" %}

{% block title %}Dashboard — MyApp{% endblock %}

{% block topbar_brand %}<span>MyApp</span>{% endblock %}
{% block sidebar_nav %}{% include "components/sidebar.html" with items=nav_items %}{% endblock %}

{% block page_content %}
  {% include "components/page_header.html" with title="Dashboard" %}
  {# page content #}
{% endblock %}
```

Available blocks in `app_shell.html`: `title`, `topbar_brand`, `topbar_center` (hidden on mobile — do not place mobile-required content here), `topbar_actions`, `sidebar_nav`, `sidebar_footer`, `page_content`, `scripts`.

Extend `auth.html` for login and registration pages:

```django
{% extends "layouts/auth.html" %}

{% block title %}Sign in — MyApp{% endblock %}

{% block brand %}<span>MyApp</span>{% endblock %}

{% block auth_content %}
  <h1>Sign in</h1>
  {# auth form #}
{% endblock %}

{% block auth_footer %}
  {# e.g. "Don't have an account? Sign up" #}
{% endblock %}
```

Available blocks in `auth.html`: `title`, `brand`, `auth_content`, `auth_footer`, `scripts`.

> **このプロジェクトの現状**: `templates/accounts/login.html` および `signup.html` は現時点で
> 旧 `base.html` を継承しており、`layouts/auth.html` への移行は未実施です。
> auth ページを Sekai UI に統一する場合は、これらのテンプレートを `layouts/auth.html` ベースに
> 書き直してください。

### Using Components

Include components with `{% include %}` and pass context variables:

```django
{% include "components/card.html" with card_title="Total Users" stat_value="1,204" stat_label="↑ 12% from last month" %}

{% include "components/button.html" with label="Save" variant="primary" %}
```

The table component requires `show_actions=True` to display the actions column. The column is hidden by default regardless of whether row data contains action links:

```django
{# Actions column hidden (default) #}
{% include "components/table.html" with headers=table_headers rows=table_rows %}

{# Actions column visible #}
{% include "components/table.html" with headers=table_headers rows=table_rows show_actions=True %}
```

### Design Token Reference

All visual values are defined in `design/tokens.json`. When writing custom Tailwind classes, align values with the token scale. Do not introduce arbitrary color or spacing values outside the defined tokens.

For component API details, refer to the inline documentation at the top of each template file.

---

## このプロジェクトでの現状（混在構成）

このリポジトリでは Sekai UI への移行が進行中であり、現在 2 系統が混在しています：

- **旧系統**（accounts・billing・home・dashboard）: `templates/base.html` を使用。WhiteNoise が配信するローカル CSS に依存。
- **Sekai UI 系**（customers 以降）: `ui/layouts/base.html` を使用。Google Fonts CDN と Tailwind CDN に依存（開発用）。

新規ページは Sekai UI 系で実装してください。旧系統は将来の移行対象です。

本番デプロイ前に必ず Tailwind CDN を静的ファイルに置き換えてください（詳細は `../README.md` の Known Limitations を参照）。

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
