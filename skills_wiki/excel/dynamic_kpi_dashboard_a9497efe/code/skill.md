### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Combines a backend `Data` sheet with a frontend `Dashboard` sheet. Uses a Data Validation dropdown to select a time period, feeding an `INDEX/MATCH` formula to dynamically populate large KPI "cards". Employs `CellIsRule` conditional formatting to color-code values against performance targets while preserving the large typography.
* **Applicability**: Best for executive summaries, financial overviews, and operational metric reporting where users need to quickly toggle between time periods (e.g., months, quarters) and instantly see if KPIs are hitting targets.

### 2. Structural Breakdown

- **Data Layout**: 
  - `Data` tab: Time-series layout (Metrics in rows, Time periods in columns).
  - `Dashboard` tab: Grid-based KPI cards separated by empty buffer columns.
- **Formula Logic**: `=INDEX(Data!$B$2:$D$2, MATCH($C$4, Data!$B$1:$D$1, 0))`
- **Visual Design**: 
  - Cards are constructed using three merged rows: Header (gray background), Value (large size 24 font), and Footer (small italic target label).
  - Conditional Formatting (CF) rules apply to the value row. CF fonts explicitly re-declare `size=24` and `bold=True` so they don't overwrite the base typography when triggered.
- **Charts/Tables**: None (purely typography and cell-fill driven).
- **Theme Hooks**: Primary backgrounds for section headers, light gray for card headers, and semantic green/red for success/fail states.

### 3. Reproduction Code

