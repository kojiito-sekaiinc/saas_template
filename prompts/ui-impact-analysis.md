# Sekai UI System Impact Analysis Prompt

You are reviewing a Django project that uses the Sekai UI System.

The UI system has recently been updated and the entire `ui/` directory
has been replaced with the latest version.

Your task is to perform an **IMPACT ANALYSIS ONLY**.

## IMPORTANT RULES

-   Do NOT modify any code
-   Do NOT rewrite templates
-   Do NOT propose redesigns
-   This task is analysis only

Your goal is to identify which existing Django templates may break or
require updates due to the UI system changes.

------------------------------------------------------------------------

# Project Structure

The project contains:

    ui/
      design/
      components/
      layouts/
      examples/

    templates/
      (actual Django templates)

Templates typically use the UI system via:

    {% extends "layouts/..." %}
    {% include "components/..." %}

------------------------------------------------------------------------

# What to Analyze

## 1. Layout Changes

Check if any layouts changed:

    layouts/app_shell.html
    layouts/base.html

Verify if block names changed:

    title
    topbar_brand
    topbar_center
    topbar_actions
    sidebar_nav
    sidebar_footer
    page_content
    scripts

------------------------------------------------------------------------

## 2. Component API Changes

Check components used by templates:

    components/button.html
    components/input.html
    components/table.html
    components/page_header.html
    components/sidebar.html

Detect:

-   parameter changes
-   required argument changes
-   expected data structure changes

------------------------------------------------------------------------

## 3. Design Token Changes

Check:

    ui/design/tokens.json

Identify token changes affecting:

-   spacing
-   typography
-   colors

------------------------------------------------------------------------

## 4. Template Usage

Scan `templates/` and list:

-   templates extending layouts/app_shell.html
-   templates including components/\*
-   templates using tables
-   templates using pagination

------------------------------------------------------------------------

# Output Format

Provide a structured report:

1.  Layout changes
2.  Component API changes
3.  Token changes
4.  Potential template break points
5.  Recommended minimal updates

Do NOT modify files.
