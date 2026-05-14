### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Tier Dynamic KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Separates the workbook into 3 distinct sheets: Data (raw inputs), Staging (KPI calculations by period), and Dashboard (presentation). Uses an interactive Data Validation dropdown tied to `VLOOKUP` and `MATCH` formulas to dynamically render KPIs with conditional big-font status formatting.
* **Applicability**: Best used for executive reports tracking multiple performance metrics over time, where you want to allow the user to easily toggle the reporting period without cluttering the visual layer with underlying data.

### 2. Structural Breakdown

- **Data Layout**: 
  - `1) Data`: Appended raw extracts (e.g., Accounts Receivable, COGS).
  - `2) Staging`: Row-wise KPIs (DSO, DPO, Gross Margin) with columns acting as time periods, plus a static Target column.
  - `3) Dashboard`: Presentation layer with hidden gridlines, group headers, and modular KPI "cards" occupying a 2x3 grid.
- **Formula Logic**: `=VLOOKUP(metric_name, Staging_Range, MATCH(selected_month, Staging_Headers, 0), FALSE)` retrieves dynamic values based on the month dropdown. 
- **Visual Design**: Uses merged cells for KPI group headers with solid fills. Main numbers use a prominent 24pt font and feature dynamic background fills (green/red) leveraging conditional formatting rules against the adjacent target value.
- **Charts/Tables**: Standalone big-number cells instead of charts.
- **Theme Hooks**: Hardcoded fallback values (`4F81BD` for headers, `DCE6F1` for metric titles) are included, but in a full system, these should map to `theme.primary_bg`, `theme.secondary_bg`, and standard success/danger semantic colors.

### 3. Reproduction Code

