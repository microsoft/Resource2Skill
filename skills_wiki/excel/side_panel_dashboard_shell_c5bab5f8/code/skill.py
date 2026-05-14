### 1. High-level Skill Pattern Extraction

> **Skill Name**: Side-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Divides a worksheet into two distinct visual zones using `PatternFill` across column ranges: a dark, narrow sidebar on the left and a light, wide main content area on the right. It injects high-contrast KPI metric blocks into the sidebar, hides gridlines, and renders clean, white "card" regions in the main area to neatly house charts or tables.
* **Applicability**: Ideal for executive summaries, KPI scorecards, or high-level overview dashboards where 4-6 crucial top-level metrics must remain permanently visible alongside detailed charts. 

### 2. Structural Breakdown

- **Data Layout**: Accepts a `kpis` list containing dictionaries with `label` and `value` keys. The sidebar operates on fixed rows/columns, stacking these KPIs vertically.
- **Formula Logic**: Primarily structural; relies on pre-calculated values passed into the rendering function rather than sheet-level formulas.
- **Visual Design**: Two-tone layout (dark sidebar Columns A-C, light main area Columns D-N). Hides standard Excel gridlines. KPI values use large (size 20), bold typography. Chart areas use a solid white fill with thin, light-gray borders to mimic web UI "cards".
- **Charts/Tables**: Generates merged, styled placeholder cards indicating exactly where openpyxl charts (like LineCharts or BarCharts) should be anchored later in the generation pipeline.
- **Theme Hooks**: Consumes `sidebar_bg`, `main_bg`, `text_inv` (inverse text for the dark sidebar), and `text_main` to ensure the dashboard seamlessly adapts to corporate branding.

### 3. Reproduction Code

