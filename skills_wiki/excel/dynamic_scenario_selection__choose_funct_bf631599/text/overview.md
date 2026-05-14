### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Selection (CHOOSE function)

* **Tier**: snippet
* **Core Mechanism**: This skill utilizes Excel's `CHOOSE` function to dynamically select values from different predefined scenarios (e.g., Best Case, Base Case, Worst Case). The selection is controlled by a single numerical input cell (the scenario selector), allowing the entire financial model's forecasts to update instantly based on the chosen scenario's assumptions.
* **Applicability**: This pattern is crucial for building robust and interactive financial models, budget forecasts, or any analytical report where users need to evaluate multiple "what-if" scenarios without manually changing underlying data. It enhances model flexibility and usability for decision-making and presentations.

### 2. Structural Breakdown

- **Data Layout**:
    - **Scenario Selector Cell**: A single, hard-coded input cell on a control sheet (e.g., `Cover!C6`) to specify the desired scenario using a number (e.g., 1, 2, 3). This cell is typically blue font to indicate manual input and locked.
    - **Scenario Assumption Rows**: For each key financial driver (e.g., Revenue Growth Rate, COGS as % of Revenue), multiple rows are prepared in the 'Assumptions' section of the forecast sheet. Each row represents a specific scenario (e.g., Best Case, Base Case, Worst Case) with corresponding values for each forecasted year.
    - **Dynamic Assumption Rows**: A row directly above the scenario assumption rows, where the `CHOOSE` formula is placed. This row will pull values dynamically based on the scenario selector.
- **Formula Logic**:
    - The core formula uses `CHOOSE(index_num, value1, [value2], ...)`.
    - **`index_num`**: This refers to the locked scenario selector cell (e.g., `Cover!$C$6`). This cell should be made an absolute reference (`$C$6`) so it doesn't change when the formula is dragged.
    - **`value1`, `value2`, `value3`**: These refer to the cells containing the assumption values for each scenario for the current year (e.g., `Forecast!G26` for Best Case, `Forecast!G27` for Base Case, `Forecast!G28` for Worst Case). These references should typically be relative (e.g., `G26`) so they adjust when the formula is dragged across different forecasted years.
    - **Example**: In a cell like `Forecast!G17` (representing Revenue Growth Rate for 2026), the formula would be `=CHOOSE(Cover!$C$6, G26, G27, G28)`.
- **Visual Design**:
    - **Scenario Selector Cell**: Blue font, typically bordered, for manual input. A comment/note can be added to explain the scenario numbers (e.g., 1=Best Case, 2=Base Case, 3=Worst Case).
    - **Dynamic Assumption Rows**: Values displayed in black font, as they are formula-driven.
    - **Scenario Assumption Rows (e.g., Best/Base/Worst Case)**: Values displayed in blue font, indicating they are manual inputs for each scenario.
    - **Headers**: Consistent dark blue background with white, bold font.
    - **Forecasted Figures**: Blue font for calculated results.
- **Charts/Tables**: The dynamic nature allows any charts or tables linked to the forecasted financial statements to update automatically with scenario changes, providing instant visual feedback.
- **Theme Hooks**: `header_bg`, `header_fg`, `input_fg`, `formula_fg`, `accent_bg` (for Net Income highlight).

### 3. Reproduction Code

```json
{
  "name": "CHOOSE Formula for Dynamic Scenario Selection",
  "description": "Dynamically selects an assumption value based on a scenario index. This formula is typically placed in a dynamic assumption row.",
  "formula_string": "=CHOOSE(Cover!$C$6, G26, G27, G28)",
  "cell_references": {
    "Cover!$C$6": "The absolute reference to the scenario selector cell on the 'Cover' sheet (e.g., 1, 2, or 3).",
    "G26": "The relative reference to the assumption value for scenario 1 in the current forecast year.",
    "G27": "The relative reference to the assumption value for scenario 2 in the current forecast year.",
    "G28": "The relative reference to the assumption value for scenario 3 in the current forecast year."
  },
  "notes": "This formula should be entered into the first forecasted year's cell of the dynamic assumption row (e.g., G17 for Revenue Growth Rate). Ensure 'Cover!$C$6' is an absolute reference using F4. The scenario-specific values (G26, G27, G28) should be relative references to allow them to adjust when the formula is dragged horizontally across all forecasted years. This snippet assumes three scenarios, but can be extended for more values in the CHOOSE function."
}
```