### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic KPI Dashboard Workbook

* **Tier**: archetype
* **Core Mechanism**: A three-sheet architecture separating raw inputs ("Data"), derived metrics/targets ("Staging"), and presentation ("Dashboard"). The dashboard uses `INDEX/MATCH` bound to a data validation dropdown to dynamically fetch metrics for a selected month, applying large typography and dynamic conditional formatting based on target thresholds.
* **Applicability**: Best used for recurring monthly/quarterly financial or operational reporting. This pattern cleanly abstracts calculation logic away from the end-user, providing a clean, interactive executive summary.

### 2. Structural Breakdown

- **Data Layout**: A 3-sheet structure:
  1. `1) Data`: Raw matrix of accounts/metrics (rows) by period (columns).
  2. `2) Staging`: Calculation layer computing final KPIs and mapping targets per period.
  3. `3) Dashboard`: Presentation layer with hidden gridlines and KPI "cards".
- **Formula Logic**: 
  - `INDEX/MATCH` looks up the selected month: `=INDEX('2) Staging'!$B$2:$D$2, 1, MATCH($C$4, '2) Staging'!$B$1:$D$1, 0))`
  - IFERROR wrappers on the staging layer handle zero-division for early months.
- **Visual Design**: 
  - Clean card design with merged title headers.
  - Oversized font (size 24) for primary metrics to ensure readability.
  - `CellIsRule` Conditional Formatting dynamically applies green/red fills and fonts depending on whether the metric beats or misses the target.
- **Charts/Tables**: Not chart-based; relies entirely on localized KPI card clusters with inline conditional styling.
- **Theme Hooks**: Uses neutral borders and background fills for structure, but relies heavily on semantic green (`C6EFCE`) and red (`FFC7CE`) for performance indication.

### 3. Reproduction Code

