# Sekai UI System Final Review Prompt

You are performing a **final safety review** of a Django project after
UI compatibility fixes were applied.

Your goal is to detect remaining risks.

This task is **review only**.

Do NOT rewrite code. Do NOT apply refactors.

------------------------------------------------------------------------

# What to Verify

## Template Integrity

Check for:

    TemplateSyntaxError
    missing variables
    invalid include paths

------------------------------------------------------------------------

## Component Compatibility

Verify components:

    components/button.html
    components/table.html
    components/input.html

Ensure required parameters are passed.

------------------------------------------------------------------------

## Layout Compatibility

Check templates extending:

    layouts/app_shell.html
    layouts/base.html

Ensure block names still match.

------------------------------------------------------------------------

## Pagination Safety

Prefer view-generated URLs instead of fragile template URL building.

------------------------------------------------------------------------

# Output

Provide:

Safe Areas Potential Issues Optional Improvements
