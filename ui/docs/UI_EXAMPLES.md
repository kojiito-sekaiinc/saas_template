# UI Examples for Sekai UI System

Version: 1.0  
Style: Notion-style Minimal UI  

This document provides example UI patterns that represent the intended visual style of Sekai UI System.

These examples help both humans and AI agents understand how components should be composed into real interfaces.

The goal is not pixel-perfect layouts but **clear structural patterns**.

---

# 1. Dashboard Page

Typical dashboard layout.

Structure:

Topbar  
Sidebar  
Main Content  

Main content usually contains a grid of cards displaying key metrics.

Example structure:

Page Title  
Description text  

Metric Cards Row  
Metric Cards Row  

Data Table or Activity Feed

Guidelines:

- Use cards for each metric
- Maintain consistent spacing between cards
- Avoid placing too many cards in a single row
- Keep the dashboard visually calm

---

# 2. CRUD List Page

Used for managing records.

Typical examples:

Users  
Projects  
Transactions  
Files  

Structure:

Page Header  
Primary Action Button  

Filter Bar  

Data Table  

Pagination

Guidelines:

- Primary action button should appear in the header
- Table should remain visually light
- Avoid heavy grid lines
- Use subtle hover effects for rows

---

# 3. Form Page

Used for creating or editing records.

Structure:

Page Header  

Form Card  

Form Fields  

Submit Button

Guidelines:

- Forms should be grouped into logical sections
- Use clear labels above inputs
- Avoid overly dense layouts
- Error messages should appear below the input field

---

# 4. Settings Page

Settings pages often contain multiple configuration sections.

Structure:

Page Header  

Settings Card  
Settings Card  
Settings Card  

Each card contains:

Section Title  
Description  
Input Fields or Toggles  

Guidelines:

- Separate sections clearly using cards
- Provide short descriptions for settings
- Avoid overly complex forms

---

# 5. Analytics Page

Used for dashboards that include charts.

Structure:

Page Header  

Filters or Date Range Selector  

Chart Card  
Chart Card  

Data Table

Guidelines:

- Charts should be placed inside cards
- Provide clear titles for charts
- Avoid excessive color usage in charts
- Maintain readable spacing around visualizations

---

# 6. Modal Dialog

Used for confirmations and short forms.

Structure:

Modal Container  

Modal Title  
Modal Description  

Form Fields or Message  

Primary Action Button  
Secondary Cancel Button

Guidelines:

- Keep modal content short
- Avoid large forms in modals
- Primary action should appear on the right

---

# 7. Card Component Example

Typical card usage pattern.

Card structure:

Card Header  
Card Body  
Optional Card Footer  

Usage examples:

Metric display  
Form grouping  
Settings sections  
Chart containers

Guidelines:

- Maintain consistent padding
- Use subtle borders
- Avoid heavy shadows

---

# 8. Table Layout Example

Table structure:

Table Header  
Table Body  
Optional Actions Column  

Guidelines:

- Header should have slightly stronger text weight
- Rows should have hover feedback
- Avoid vertical grid lines when possible
- Actions column should be right-aligned

---

# 9. Navigation Example

Navigation should remain simple.

Sidebar structure:

Application Logo  

Navigation Items  

Optional Secondary Section

Guidelines:

- Highlight active item
- Avoid deeply nested navigation
- Keep labels short and clear

---

# 10. Page Header Pattern

Most pages begin with a header section.

Structure:

Page Title  
Optional Description  

Primary Action Button  

Guidelines:

- Title should clearly describe the page
- Description should remain short
- Avoid placing too many actions in the header

---

# 11. Empty State Example

When a page has no data.

Structure:

Icon or Illustration  

Short Message  

Primary Action Button

Guidelines:

- Explain what the user should do next
- Keep the message short
- Provide a clear action

---

# 12. AI Guidance

AI agents generating UI should follow these steps:

1. Identify the page type
2. Select the closest example pattern
3. Use existing components
4. Apply tokens from `design/tokens.json`
5. Follow rules from `design/design-principles.md`

AI should prefer **predictable layouts** over creative variations.

---

# End of UI Examples