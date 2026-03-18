# Sekai UI System Minimal Fix Prompt

You are applying a **minimal compatibility update** to a Django project
after a Sekai UI System update.

An impact analysis has already been performed.

Your task is to apply ONLY the required minimal fixes.

------------------------------------------------------------------------

# Important Rules

-   Do NOT redesign pages
-   Do NOT rewrite templates
-   Do NOT change unrelated logic
-   Do NOT rename variables unless required
-   Preserve Django template structure
-   Apply the smallest possible change

------------------------------------------------------------------------

# Context

Changes may exist in:

    ui/components
    ui/layouts
    ui/design/tokens.json

Existing templates under:

    templates/

may require compatibility updates.

------------------------------------------------------------------------

# Your Task

Apply only minimal fixes such as:

    - adding show_actions=True
    - adjusting include parameters
    - updating component arguments
    - adapting block names

Do NOT perform:

    - layout rewrites
    - component replacements
    - visual redesign

------------------------------------------------------------------------

# Output

Return:

1.  Summary of changes
2.  Updated template(s)
