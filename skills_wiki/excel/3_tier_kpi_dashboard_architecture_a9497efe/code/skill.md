### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier KPI Dashboard Architecture

* **Tier**: archetype
* **Core Mechanism**: Separates the workbook into three interconnected sheets: Raw Data (inputs), Staging (calculation formulas like Gross Margin or DSO), and Dashboard (presentation). Uses a dynamic Data Validation dropdown alongside `INDEX/MATCH` to filter metrics for the selected month, applying `CellIsRule` conditional formatting to highlight performance against targets.
* **Applicability**: Highly applicable to monthly periodic reporting packages or executive summaries. Use this architecture when you have expanding time-series raw data but need a pristine, single-page interactive view of the most important metrics that doesn't break as new months are added.

### 2. Structural Breakdown

- **Data Layout**: 
  - `1) Data`: Raw input metrics (Sales, COGS, AR) rows by Month columns.
  - `2) Staging`: Calculated metrics (Margins, Ratios, Targets) rows by Month columns.
  - `3) Dashboard`: Grid of visual "Cards", bounded by empty spacer rows/columns.
- **Formula Logic**: `=INDEX('2) Staging'!$B$2:$G$2, MATCH($C$3, '2) Staging'!$B$1:$G$1, 0))` grabs the staging value matching the dropdown's month in `C3`.
- **Visual Design**: Themed dark header background (`header_fill`) with gray card body (`card_fill`). Large KPI font sizes. Red/Green conditional formatting driven by the adjacent dynamic target cell.
- **Charts/Tables**: Pure cell-based card layout utilizing merged ranges (e.g., 3 columns wide x 3 rows high) with uniform borders.
- **Theme Hooks**: Utilizes `header_fill` (Primary Color) and standard traffic light colors (Red/Green) for indicator state.

### 3. Reproduction Code

