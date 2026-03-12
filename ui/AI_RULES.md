# AI Rules for Sekai UI System

This file defines rules that AI agents (Claude, Codex, Cursor, etc.) must follow when modifying or generating UI code in this repository.

The goal is to maintain a **consistent Notion-style minimal interface**.

---

# 1. Design Philosophy

Sekai UI System follows a **Notion-style minimal UI philosophy**.

Characteristics:

- white background
- subtle borders
- generous whitespace
- typography-first layout
- minimal visual noise

The UI must feel:

- calm
- readable
- professional
- distraction-free

Avoid:

- strong gradients
- neon colors
- large shadows
- excessive UI decoration
- inconsistent spacing

---

# 2. Always Use Design Tokens

AI must always reference the file:

design/tokens.json

Never hardcode colors or spacing values.

Tokens must be used for:

- colors
- spacing
- radius
- layout constants

Example:

Incorrect usage:

class="bg-blue-500"

Correct usage:

Use the primary color defined in design/tokens.json.

---

# 3. Reuse Components First

Before creating a new UI element, check the directory:

components/

If a similar component exists, reuse or extend it.

Never duplicate UI logic unnecessarily.

Preferred order:

1. reuse existing component
2. extend component
3. create new component only if necessary

---

# 4. Layout Consistency

Application layouts must follow:

layouts/app_shell.html

Standard layout structure:

Topbar  
Sidebar  
Main Content

Do not invent new layout structures unless absolutely necessary.

---

# 5. Minimal Shadow Usage

Shadow must be minimal.

Allowed usage:

- small shadow for floating cards
- modal dialogs

Avoid:

- large drop shadows
- stacked shadow layers

Default rule:

no shadow unless necessary

---

# 6. Spacing Rules

Spacing must follow token definitions.

Typical spacing scale:

8px
12px
16px
20px
24px
32px
40px
48px

Spacing should create hierarchy instead of heavy borders.

---

# 7. Typography Rules

Typography hierarchy must remain simple.

Standard hierarchy:

Title  
Subtitle  
Body  
Caption  

Avoid excessive font sizes.

Text must remain readable and calm.

---

# 8. Component Simplicity

Each component should:

- have a clear purpose
- remain small
- be reusable
- avoid unnecessary variants

Complex components should be split into smaller ones.

## Button Usage Rule

Primary buttons must be used sparingly.

- Use at most one primary button per page section or view
- Never place multiple primary buttons adjacent to each other
- Secondary, ghost, or danger variants must be used for all other actions

---

# 9. File Organization Rules

New components must be placed in:

components/

New layouts must be placed in:

layouts/

Example pages must be placed in:

examples/

Do not mix responsibilities between folders.

---

# 10. AI Development Workflow

When implementing features, follow this workflow.

Step 1
Read the specification file:

docs/sekai-ui-system-spec.md

Step 2
Read the design principles file:

design/design-principles.md

Step 3
Read the design tokens file:

design/tokens.json

Step 4
Check existing components in:

components/

Step 5
Reuse or extend existing components if possible.

Step 6
Create a new component only when no existing component can be reused.

Step 7
Maintain minimal UI philosophy throughout.

---

# 11. Output Expectations

Generated UI must be:

- clean
- readable
- minimal
- reusable
- consistent with tokens

The UI system should support:

- dashboards
- CRUD interfaces
- analytics tools
- admin panels
- AI applications

---

# End of AI Rules