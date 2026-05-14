### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Builds a modular 3-sheet architecture (Data, Staging, Dashboard) to separate raw data from metric calculations and presentation. Uses a Data Validation dropdown tied to `INDEX`/`MATCH` formulas to dynamically swap out the active month across multiple KPI cards, using `CellIsRule` conditional formatting to highlight performance against targets.
* **Applicability**: Best for executive summaries, monthly reporting packages, or any scenario where you need to distill complex time-series data into a clean, highly readable, interactive presentation layer.

### 2. Structural Breakdown

- **Data Layout**: 3 sheets. `Data` holds raw GL outputs. `Staging` calculates the specific metrics row-by-row (Actual, Target, Prior Month). `Dashboard` is a clean presentation grid (gridlines disabled).
- **Formula Logic**: `=INDEX(Staging!$B$2:$D$2, MATCH($C$5, Staging!$B$1:$D$1, 0))` used in each KPI value box to retrieve the correct metric based on the dropdown selector in `$C$5`.
- **Visual Design**: Gridlines off. Extra large fonts for KPI values (Size 24). Distinct solid color headers for sections and individual cards. Light grey borders to delineate cards.
- **Charts/Tables**: No native charts; relies on "big number" typography and color coding (green=good, red=bad).
- **Theme Hooks**: Uses `primary` for main section headers, `card_header` for individual KPI titles, `good_bg`/`good_text` for exceeding targets, and `bad_bg`/`bad_text` for missing targets.

### 3. Reproduction Code

