### 1. High-level Skill Pattern Extraction

> **Skill Name**: Flat-Design Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Simulates floating UI shapes (KPI cards and seamless charts) using cell formatting. Uses `PatternFill` to create a two-tone background, merges cells with an accent-color column to create "cards", and strips borders/gridlines from charts so they blend directly into the background layer.
* **Applicability**: Best for executive summaries and static dashboards where you want a modern, web-like aesthetic without relying on fragile floating shape objects or text boxes.

### 2. Structural Breakdown

- **Data Layout**: Data for the charts is sequestered far below the visible dashboard area (e.g., row 35+) to keep the top view clean.
- **Formula Logic**: Static layout generation; no complex formulas required for the shell itself.
- **Visual Design**: Gridlines are disabled sheet-wide. Rows 1-4 use a dark primary fill, while rows 5+ use a light background fill. KPI cards use a white fill block flanked by a single-column accent fill to mimic a card border/ribbon. 
- **Charts/Tables**: `BarChart` configured with `overlap`, `gapWidth = 50`, legend repositioned to the top, and `graphical_properties.line.noFill = True` to remove the outer frame.
- **Theme Hooks**: `header_bg` (top banner), `body_bg` (main background), `card_bg` (KPI block), `accent1` (KPI ribbon), `text_light`, `text_dark`.

### 3. Reproduction Code

