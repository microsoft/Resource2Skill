### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Dashboard Layout Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Creates a polished presentation layer by disabling gridlines, adding a dominant merged header banner, generating supporting data on a hidden backing worksheet, and meticulously aligning multiple charts (stacked columns and lines) onto the blank canvas to simulate an app-like dashboard view.
* **Applicability**: Best used when generating executive summaries or final KPI dashboards where raw data and pivot tables should be hidden, leaving only an organized, visually clean chart grid.

### 2. Structural Breakdown

- **Data Layout**: The target worksheet acts purely as a UI canvas. All supporting chart data is segregated into a dynamically created hidden sheet (`{sheet_name}_Data`), preventing accidental tampering and keeping the view pristine.
- **Formula Logic**: N/A (Data is modeled as static aggregations to simulate the PivotTable outputs from the original technique).
- **Visual Design**: Gridlines disabled (`showGridLines = False`). The top 3 rows are merged (`A1:N3`) into a single, large header block driven by theme colors, using vertically and horizontally centered large, bold text.
- **Charts/Tables**: Employs an asymmetrical dashboard layout—a large Stacked Column chart on the left, flanked by two smaller Line charts stacked vertically on the right. Legends are selectively disabled on trend charts to save space.
- **Theme Hooks**: Consumes `header_bg` and `header_fg` to style the dashboard title bar.

### 3. Reproduction Code

