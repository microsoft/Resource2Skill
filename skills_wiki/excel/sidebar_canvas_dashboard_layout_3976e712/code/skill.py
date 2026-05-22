### 1. High-level Skill Pattern Extraction

> **Skill Name**: Sidebar Canvas Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Uses cell background colors and borders to simulate floating "layout cards" on a light canvas, combined with a dark vertical sidebar for navigation. Bypasses the need for brittle floating shape rectangles, making the layout fully programmatic, grid-aligned, and easily targetable by charts.
* **Applicability**: When building an interactive, top-level executive dashboard that needs to look like a modern web app but stay entirely within native Excel grid features.

### 2. Structural Breakdown

- **Data Layout**: Uses slim spacer columns (B, F, J, N) and spacer rows (4, 9, 16) to create visual gutters between the white "card" regions.
- **Formula Logic**: Purely structural layout shell; designed to accept values or formulas dynamically in the KPI value cells.
- **Visual Design**: Gridlines are hidden. The canvas uses a light gray fill (`F2F2F2`), the sidebar uses a primary dark fill (`1F4E78`), and the cards use a solid white fill (`FFFFFF`) with a thin gray (`D9D9D9`) perimeter border to simulate a drop shadow / elevation effect.
- **Charts/Tables**: Provides designated cell ranges (cards) acting as anchoring zones for line charts, donut charts, or maps.
- **Theme Hooks**: Consumes `primary` for the sidebar background and main header text, a light `canvas_bg` for the worksheet, and `card_bg` for the content blocks.

### 3. Reproduction Code

