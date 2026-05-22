### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive KPI Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet architecture where a "Dashboard" presentation layer queries a hidden "Staging" data matrix using a Data Validation dropdown and `INDEX(MATCH())` combinations. Calculates prior periods natively by shifting the `MATCH` index by -1.
* **Applicability**: Perfect for high-level executive summaries, monthly reporting packages, or any scenario where you need to display "Big Number" metrics with variance to target and prior periods without relying on VBA or PivotTables.

### 2. Structural Breakdown

- **Data Layout**: Two-sheet system. A hidden `Staging` sheet holds targets and a matrix of time-series data. The `Dashboard` sheet acts as a grid of spatial "cards" separated by spacer columns.
- **Formula Logic**: Uses `=INDEX(Staging!$C$R:$F$R, MATCH(Selected_Month, Staging!$C$1:$F$1, 0))` to pull the current period value. Subtracting 1 from the `MATCH` result effortlessly grabs the prior period.
- **Visual Design**: Cards use an outer outline border, strong theme-driven header fills, and massive 20pt fonts for the primary metric.
- **Charts/Tables**: Employs spatial cell-merging to create a "Dashboard Tile" aesthetic rather than native charts.
- **Theme Hooks**: Consumes `primary` for section banners and active UI elements, `secondary` for card headers, and standard red/green semantics for conditional formatting based on target performance.

### 3. Reproduction Code

