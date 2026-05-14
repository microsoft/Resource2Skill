### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Model Matrix

* **Tier**: sheet_shell
* **Core Mechanism**: Employs a data validation dropdown linked to `CHOOSE` formulas to dynamically switch an active "Live Case" assumptions block between multiple predefined scenario blocks (Base, Downside, etc.). The Live Case then natively drives the dependent calculations (e.g., an Income Statement).
* **Applicability**: Highly applicable for financial modeling, multi-year forecasting, budgeting, or any analytical spreadsheet requiring robust multi-scenario/sensitivity analysis without the use of complex macros or hidden sheets.

### 2. Structural Breakdown

- **Data Layout**: Built in vertical tiers. Top section: Core calculated output (Income Statement). Middle section: "Live Case" assumptions linking to the active scenario. Bottom section: Matrix of distinct, hardcoded scenario blocks (Scenario 1, Scenario 2).
- **Formula Logic**: Uses `=CHOOSE($toggle_cell, C21, C28)` populated across the entire Live Case block, redirecting the calculation pointer dynamically. Output section strictly references the Live Case cells.
- **Visual Design**: Uses conventional financial modeling formatting: Blue text (`0000FF`) for hardcoded assumptions, Black text for formulas, and Yellow fill (`FFF2CC`) for the primary user input/toggle cell to signal interactivity. 
- **Charts/Tables**: Standalone data grid design using themed header bands and selective double-bottom borders for margin totals.
- **Theme Hooks**: Consumes `header_bg` and `header_fg` for the master timeline header, and uses `accent` for the Live Assumptions subheader band.

### 3. Reproduction Code

