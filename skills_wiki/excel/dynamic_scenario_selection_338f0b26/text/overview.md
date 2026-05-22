### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Selection

*   **Tier**: snippet
*   **Core Mechanism**: Utilizes the `CHOOSE` Excel function to dynamically retrieve values from multiple predefined assumption sets (scenarios) based on a single numerical index. This index is typically controlled by a Data Validation dropdown, allowing users to switch between scenarios instantly.
*   **Applicability**: Essential for financial models, business forecasts, or any Excel-based analysis that requires comparing different 'what-if' scenarios (e.g., optimistic, base, pessimistic). It requires pre-structured blocks of assumptions for each scenario to function effectively.

### 2. Structural Breakdown

-   **Data Layout**:
    *   **Scenario Selector Cell**: A single cell (e.g., J4 in the video) designated for user input, containing a numerical index (e.g., '1' or '2') for the active scenario. This cell is configured with Data Validation of type 'List', allowing only predefined scenario indices (e.g., '1,2').
    *   **'Live Case' Assumptions Block**: A block of cells (e.g., D30:H44 in the video) that acts as the active set of assumptions. Each cell in this block contains the `CHOOSE` formula, pulling values from the respective scenario blocks. This block directly feeds into the main financial model.
    *   **Scenario Assumption Blocks**: Separate, static blocks of cells (e.g., 'Upper Case (Scenario 1)' starting at D48 and 'Lower Case (Scenario 2)' starting at D66 in the video) that hold the complete set of assumption values for each specific scenario. These blocks are referenced by the `CHOOSE` formulas.
-   **Formula Logic**:
    *   The core formula applied to each cell within the 'Live Case' assumptions block is in the format: `=CHOOSE({scenario_selector_cell_abs}, {scenario_1_value_cell_rel}, {scenario_2_value_cell_rel})`.
        *   `{scenario_selector_cell_abs}`: An absolute reference (e.g., `$J$4`) to the Scenario Selector Cell. This ensures the reference remains fixed when the formula is copied.
        *   `{scenario_1_value_cell_rel}`: A relative reference (e.g., `D48`) to the corresponding assumption value in the first scenario block.
        *   `{scenario_2_value_cell_rel}`: A relative reference (e.g., `D66`) to the corresponding assumption value in the second scenario block.
    *   When this formula is copied across and down the 'Live Case' assumptions block, the relative references for `scenario_1_value_cell_rel` and `scenario_2_value_cell_rel` automatically adjust to pull the correct values from the respective scenario blocks.
-   **Visual Design**:
    *   **Scenario Selector Cell**: Typically formatted with a distinctive background fill (e.g., yellow) and bold, centered text to highlight its function as an interactive control. Borders are usually applied.
    *   **Hard-coded Scenario Assumption Values**: Often styled with a unique font color (e.g., blue) to visually differentiate them as direct inputs.
    *   **Formula-driven 'Live Case' Assumption Values**: Usually displayed with a standard font color (e.g., black) to indicate they are derived from formulas.
    *   (Other standard formatting for headers, borders, and overall table presentation is typically applied to enhance readability and structure.)
-   **Charts/Tables**: This skill dynamically updates the input data for any charts or tables linked to the 'Live Case' assumptions or the derived financial statements, allowing for real-time visualization of different scenarios.
-   **Theme Hooks**: This skill could leverage theme tokens such as `header_bg` and `header_fg` for section headers, `accent_fill_1` for the scenario selector's background, `text_color_normal` for formula-driven text, and a custom `link_color` for hard-coded input values to ensure consistent styling.

### 3. Reproduction Code

```json
{
  "name": "Dynamic Scenario Selector (CHOOSE Formula)",
  "description": "Uses the CHOOSE function to dynamically select values from different scenario blocks based on a user-controlled index. This snippet provides the core formula string.",
  "formula_string": "=CHOOSE({scenario_selector_cell_abs}, {scenario_1_value_cell_rel}, {scenario_2_value_cell_rel})",
  "placeholders": {
    "scenario_selector_cell_abs": {
      "description": "Absolute reference to the cell containing the chosen scenario number (e.g., $J$4). This cell should typically have a Data Validation dropdown.",
      "example": "$J$4"
    },
    "scenario_1_value_cell_rel": {
      "description": "Relative reference to the corresponding assumption value in the first scenario block (e.g., D48).",
      "example": "D48"
    },
    "scenario_2_value_cell_rel": {
      "description": "Relative reference to the corresponding assumption value in the second scenario block (e.g., D66).",
      "example": "D66"
    }
  },
  "usage_notes": "To implement this skill, first define your scenario assumption blocks (e.g., Scenario 1 and Scenario 2 with their respective values). Then, create a scenario selector cell (e.g., J4) and apply Data Validation (List type, Source: '1,2'). Finally, apply this formula to the top-left cell of your 'Live Case' assumptions block (e.g., D30) and drag it across and down to dynamically populate the entire block. The example formula assumes two scenarios; extend with additional '{scenario_N_value_cell_rel}' arguments for more scenarios."
}
```