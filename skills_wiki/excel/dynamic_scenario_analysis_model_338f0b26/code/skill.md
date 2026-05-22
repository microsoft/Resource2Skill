### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Analysis Model

* **Tier**: sheet_shell
* **Core Mechanism**: Construct a live financial model driven by a scenario selector cell. The `CHOOSE` function links a "Live Assumptions" block to distinct scenario data blocks (e.g., Optimistic vs. Pessimistic). A Data Validation dropdown controls the active scenario index, updating the entire downstream model dynamically.
* **Applicability**: Highly useful for financial modeling, budgeting, forecasting, and sensitivity analysis where multiple discrete scenarios need to be evaluated without changing the core model calculations. Follows the financial modeling convention of blue fonts for hardcoded inputs and black fonts for dynamic formulas.

### 2. Structural Breakdown

- **Data Layout**: 
  - Top section: Core Financial Model calculations.
  - Middle section: "Live Assumptions" acting as the variable router.
  - Bottom sections: Hardcoded scenario blocks (Scenario 1, Scenario 2).
- **Formula Logic**: `=CHOOSE($F$2, B16, B22)` routes the correct scenario data into the Live Assumptions based on the toggle index. Downstream metrics multiply values strictly from the Live block.
- **Visual Design**: Themed header backgrounds. Formula outputs use black text, while hard-coded scenario inputs use blue text (`#0000FF`). The scenario selector is visually offset with a background fill and a border.
- **Charts/Tables**: Standard spreadsheet projection spanning multiple forward years, utilizing specific accounting number formats (`$#,##0.00` and `#,##0`).
- **Theme Hooks**: Uses `header_bg`, `header_fg`, and `accent` to style the shell cleanly.

### 3. Reproduction Code

