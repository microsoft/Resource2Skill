### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Switcher

* **Tier**: component
* **Core Mechanism**: Creates a Data Validation dropdown to select an active scenario by index (1, 2, 3...). A primary "Live Case" table uses the `CHOOSE` function to dynamically pull assumption values from multiple scenario tables below. It implements the standard financial modeling convention: blue font for hardcoded inputs, black font for formulas.
* **Applicability**: Highly applicable for financial models, forecasting, and budgeting where analysts need to quickly toggle between multiple sets of assumptions (e.g., "Base", "Upside", and "Downside" cases) without losing data.

### 2. Structural Breakdown

- **Data Layout**: A master dropdown cell (index) at the top. A "Live Case" table directly below it. Sequentially stacked scenario tables (Scenario 1, Scenario 2, etc.) at the bottom.
- **Formula Logic**: `=CHOOSE($dropdown_index, scenario_1_cell, scenario_2_cell, ...)` applied across the entire Live Case table grid.
- **Visual Design**: The dropdown selector uses a light yellow fill (`FFF2CC`) and a solid border to indicate an input control cell. Hardcoded inputs in scenario tables are styled with `0000FF` (blue), while the live dynamic cells are `000000` (black).
- **Charts/Tables**: Standard spreadsheet data layout with bottom-bordered column headers. 
- **Theme Hooks**: Default modeling conventions utilized over specific thematic colors to strictly enforce the "Blue = Hardcoded, Black = Formula" standard.

### 3. Reproduction Code

