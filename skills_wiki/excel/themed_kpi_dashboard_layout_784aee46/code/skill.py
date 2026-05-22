### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Sets up a clean presentation canvas by turning off gridlines, merging cells for a prominent themed header, building a left-hand contextual filter pane, and arranging charts loaded from a hidden background data sheet into a structured grid.
* **Applicability**: Use when aggregating multiple charts into a complete, standalone visual dashboard interface intended for management review or presentations. 

### 2. Structural Breakdown

- **Data Layout**: Dashboard source metrics are centralized on a dedicated "DashboardData" sheet which is then hidden (`ws.sheet_state = "hidden"`) to keep the user focused entirely on the visual canvas.
- **Formula Logic**: Replaces tabular data layouts with `openpyxl.chart.Reference` ranges pulling directly from the hidden backend sheet.
- **Visual Design**: Gridlines disabled (`showGridLines = False`). A bold primary-colored header banner spans across the top (`A1:M3`). A secondary-colored left sidebar (`A5:B27`) emulates the spacing and context of interactive slicers.
- **Charts/Tables**: Employs a hero Line Chart (full width) over two supporting Clustered Bar Charts (half width each), forming a classic dashboard hierarchy. Single-series legends are removed to maximize data-ink ratio.
- **Theme Hooks**: Consumes `primary`, `secondary`, and `bg` token colors to ensure the dashboard instantly adapts to branding palettes without manual adjustments.

### 3. Reproduction Code

