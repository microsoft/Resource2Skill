### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Tone Sidebar Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a navigation/KPI sidebar by widening a left-side column and applying a dark theme fill, contrasted against a light-filled main canvas area. Disables native gridlines to enforce a clean, application-like aesthetic. (Adapts the video's manual shape-based background approach into an Openpyxl-native cell-fill grid approach for robust layout automation).
* **Applicability**: Best for landing pages of reports or high-level dashboards where global metrics (KPIs) and slicers need a dedicated visual zone separated from the primary data visualizations.

### 2. Structural Breakdown

- **Data Layout**: 
  - Column A: Narrow outer left margin (width 2.0).
  - Column B: Wide Sidebar for KPIs/Slicers (width 28.0).
  - Column C: Narrow inner gutter (width 2.0).
  - Columns D-R: Main canvas area for charts/tables (width 14.0).
- **Formula Logic**: N/A for the shell itself, but acts as the destination for linked values calculated on backend pivot sheets.
- **Visual Design**: Hides native gridlines (`showGridLines = False`). Uses a high-contrast theme where the sidebar takes a dark, heavy fill and the main canvas takes a soft, pastel fill.
- **Charts/Tables**: Leaves the main canvas area structurally open for downstream chart components.
- **Theme Hooks**: Consumes `sidebar_bg` (dark), `sidebar_fg` (light/white), and `canvas_bg` (light/soft).

### 3. Reproduction Code

