### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Employs a "4-column split and merge" layout pattern to build structured KPI cards. The top rows of each card (Title and large Value) are merged across 4 columns to permit oversized fonts and spacious color blocks. The bottom row uses the 4 unmerged columns to align detailed comparative metrics ("Vs. Target" and "Vs. Prior") without forcing unnatural column widths on the rest of the sheet. `CellIsRule` conditional formatting is applied to the merged value area to indicate performance.
* **Applicability**: Best used for executive summaries or high-level status reports where you need to display dense comparative metrics (actuals vs targets/priors) in a highly readable, card-based visual format.

### 2. Structural Breakdown

- **Data Layout**: 4 columns allocated per KPI. Row 1 (Section Title) merges across all KPIs in the group. Row 2 (KPI Name) and Row 3 (KPI Value) merge across the 4 allocated columns. Row 4 splits into 4 individual cells for comparison labels and values.
- **Formula Logic**: Relative evaluation within Conditional Formatting (`CellIsRule`), comparing the merged value block against an absolute reference to the adjacent target cell.
- **Visual Design**: Gridlines disabled. Section headers use theme primary background with bold white text. KPI Names use theme secondary background. Value cells use a large font (size 24) and conditional fills (Light Green for favorable, Light Red for unfavorable).
- **Charts/Tables**: Pure cell-based card layout simulating visual "blocks" with uniform thin grey outer borders.
- **Theme Hooks**: Consumes `primary` (section headers, main title), `secondary` (sub-headers, active filters), and `text` (labels).

### 3. Reproduction Code

