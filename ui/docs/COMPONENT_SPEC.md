# Component Specification for Sekai UI System

Version: 1.0  
Design Style: Notion-style Minimal UI  

This document defines how UI components must be designed and implemented in Sekai UI System.

The goal is to ensure that both humans and AI agents generate **consistent, reusable, minimal UI components**.

---

# 1. Purpose

Components in Sekai UI System exist to:

- standardize UI elements
- improve reusability
- maintain visual consistency
- simplify AI-generated UI
- reduce design decisions during development

All components must follow the design philosophy described in `design/design-principles.md`.

---

# 2. Component Design Principles

All components must follow these principles.

## Simplicity

Components should remain simple.

Avoid:

- complex nested logic
- excessive configuration
- unnecessary variants

Prefer smaller reusable components.

---

## Reusability

Components should be reusable across:

- dashboards
- list pages
- forms
- configuration panels
- analytics views

Before creating a new component, check the `components` directory for an existing one.

---

## Consistency

All components must follow:

- `design/tokens.json`
- spacing rules
- typography rules
- color rules

Hardcoded values must be avoided whenever possible.

---

# 3. Component Directory Structure

All UI components must be placed inside the `components` directory.

Example structure:

components/  
button.html  
input.html  
card.html  
table.html  
sidebar.html  
page_header.html  

Each file should contain one primary component.

---

# 4. Component Naming Rules

Component filenames should follow simple lowercase naming.

Examples:

button.html  
input.html  
card.html  
table.html  

Avoid complex names such as:

primaryButtonComponent.html

Use clear and descriptive names instead.

---

# 5. Component Layout Rules

Each component should follow a predictable structure.

Typical structure:

container  
content  
optional actions  

Example structure for a card component:

card container  
card header  
card body  
card footer  

Components should avoid deeply nested HTML structures.

---

# 6. Styling Rules

All styling must use Tailwind CSS.

Avoid:

- inline style attributes
- custom CSS when unnecessary

Styling must respect the values defined in `design/tokens.json`.

Example:

Use spacing classes aligned with the token spacing scale.

Avoid arbitrary spacing values.

---

# 7. Button Component Specification

Button components must support the following variants:

primary  
secondary  
ghost  
danger  

Rules:

- consistent height
- rounded corners
- subtle hover feedback
- minimal shadow usage

Primary buttons should be used sparingly.

Avoid placing multiple primary buttons close together.

---

# 8. Input Component Specification

Input components must support:

- text input
- password input
- optional error state
- optional help text

Rules:

- white background
- border-based design
- subtle focus ring
- readable placeholder text

Error states must be visually clear.

---

# 9. Card Component Specification

Card components are used for grouping content.

Typical usage:

- dashboard widgets
- settings sections
- content blocks

Rules:

- white background
- subtle border
- minimal shadow
- adequate padding

Cards should not include excessive visual decoration.

---

# 10. Table Component Specification

Tables are used for displaying structured data.

Rules:

- soft row separators
- hover highlight
- readable header row
- right-aligned action columns

Avoid heavy grid lines.

Tables should remain visually light.

---

# 11. Sidebar Component Specification

The sidebar is used for application navigation.

Rules:

- fixed width
- vertical layout
- subtle active state
- icons optional

The sidebar must remain visually minimal.

Avoid excessive nesting of navigation items.

---

# 12. Page Header Component Specification

The page header provides context for each page.

Structure:

title  
description  
primary action  

The page header must appear at the top of most pages.

It should clearly communicate the page purpose.

---

# 13. Component Variants

Variants should be limited.

If a component requires too many variants, it should be split into separate components.

Example:

Instead of a single complex card component, consider:

stat_card  
info_card  
settings_card  

---

# 14. Accessibility Considerations

Components must maintain basic accessibility principles.

Important considerations:

- readable font sizes
- visible focus states
- clickable targets large enough for interaction
- sufficient contrast

Accessibility should not rely on color alone.

---

# 15. AI Development Workflow

When generating components with AI:

Step 1  
Read `docs/sekai-ui-system-spec.md`.

Step 2  
Read `design/design-principles.md`.

Step 3  
Read `design/tokens.json`.

Step 4  
Check existing components.

Step 5  
Reuse components whenever possible.

Step 6  
Create new components only when necessary.

---

# 16. Expected Component Qualities

Every component in Sekai UI System should be:

- minimal
- reusable
- readable
- consistent
- predictable

Components should support AI-assisted UI development without introducing unnecessary complexity.

---

# End of Component Specification