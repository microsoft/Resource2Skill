# Dynamic Array Calculated Fields (GROUPBY)

## Applicability

Essential for creating modern, single-formula summary reports comparing metrics (Budget vs. Actual, YoY, Forecast vs. Actual) where you need calculated variance columns attached to grouped data, overcoming the limitation that `GROUPBY` doesn't natively support calculated fields like PivotTables do.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Array Calculated Fields (GROUPBY)

* **Tier**: snippet
* **Core Mechanism**: Uses the `LET` function to execute and store a base `GROUPBY` (or `PIVOTBY`) array result. It then utilizes `CHOOSECOLS` to extract the aggregated metric columns, performs row-by-row arithmetic to generate new "Calculated Fields" (like Variance and % Variance), and uses `HSTACK` to append these new columns to the original summary table. 
* **Applicability**: Essential for creating modern, single-formula summary reports comparing metrics (Budget vs. Actual, YoY, Forecast vs. Actual) where you need calculated variance columns attached to grouped data, overcoming the limitation that `GROUPBY` doesn't natively support calculated fields like PivotTables do.

### 2. Structural Breakdown

- **Data Layout**: Requires a tabular source with at least one categorical column (for row grouping) and two aligned numeric columns representing the metrics to compare (e.g., a Budget column and an Actual column).
- **Formula Logic**: 
  - `calc`: Calculates the base summary using `GROUPBY({row_categories}, HSTACK({budget}, {actual}), SUM)`.
  - `variance`: Extracts actuals `CHOOSECOLS(calc, 3)` and subtracts budget `CHOOSECOLS(calc, 2)`.
  - `pct_variance`: Divides the computed `variance` by the budget column.
  - Final output stacks everything horizontally: `HSTACK(calc, variance, pct_variance)`.
- **Visual Design**: N/A (Formula snippet)
- **Charts/Tables**: N/A (Formula snippet)
- **Theme Hooks**: N/A (Formula snippet)

### 3. Reproduction Code

```json
{
  "name": "groupby_variance_calculated_fields",
  "description": "Dynamic array formula extending GROUPBY with calculated Variance and % Variance columns using LET and HSTACK.",
  "formula": "=LET(calc, GROUPBY({row_category_range}, HSTACK({baseline_range}, {actual_range}), SUM), variance, CHOOSECOLS(calc, 3) - CHOOSECOLS(calc, 2), pct_variance, variance / CHOOSECOLS(calc, 2), HSTACK(calc, variance, pct_variance))",
  "placeholders": {
    "row_category_range": "Range containing the categorical values to group by (e.g., Table1[Product])",
    "baseline_range": "Range containing the budget/target values (e.g., Table1[Budget])",
    "actual_range": "Range containing the actual values (e.g., Table1[Actual])"
  }
}
```