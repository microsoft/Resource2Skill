# Nested Filter 2D Aggregation

## Applicability

Best used for cross-tabular datasets (e.g., matrices with months on columns and product categories on rows) where you need to aggregate values based on both a row label (which may appear multiple times) and a column header. This technique cleanly overcomes the limitations of `SUMIFS`, which strictly requires 1D ranges of identical dimensions.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Nested Filter 2D Aggregation

* **Tier**: snippet
* **Core Mechanism**: Nests two `FILTER` functions to slice a 2D data matrix by both row criteria and column criteria. The inner filter isolates matching rows based on a vertical lookup, while the outer filter isolates matching columns based on a horizontal lookup. The result is then wrapped in a `SUM` function to aggregate the values at the intersection.
* **Applicability**: Best used for cross-tabular datasets (e.g., matrices with months on columns and product categories on rows) where you need to aggregate values based on both a row label (which may appear multiple times) and a column header. This technique cleanly overcomes the limitations of `SUMIFS`, which strictly requires 1D ranges of identical dimensions.

### 2. Structural Breakdown

- **Data Layout**: Requires a 2D grid of values (e.g., `C4:F25`), an adjacent vertical column of row labels (`B4:B25`), and an adjacent horizontal row of column headers (`C3:F3`). 
- **Formula Logic**: `=SUM(FILTER(FILTER({data_range}, {row_criteria_range}={row_criteria_value}), {col_criteria_range}={col_criteria_value}))`. The inner array filters vertically, outputting a smaller 2D array of rows; the outer array filters horizontally, yielding a 1D vertical array of values from the target column, which are then summed.
- **Visual Design**: N/A (Formula Logic)
- **Charts/Tables**: N/A (Formula Logic)
- **Theme Hooks**: N/A (Formula Logic)

### 3. Reproduction Code

```json
{
  "name": "nested_filter_2d_sum",
  "description": "Sum the intersection of a 2D array by filtering rows based on one criteria and columns based on another.",
  "formula": "=SUM(FILTER(FILTER({data_range}, {row_criteria_range}={row_criteria_value}), {col_criteria_range}={col_criteria_value}))"
}
```