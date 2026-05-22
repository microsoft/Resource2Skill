# Two-Dimensional XLOOKUP

## Applicability

Highly effective for retrieving data from a two-way table or grid where you need to match both a row condition (e.g., Country, Product) and a column condition (e.g., Year, Month).

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Dimensional XLOOKUP

* **Tier**: snippet
* **Core Mechanism**: Nests an `XLOOKUP` inside another `XLOOKUP`'s `return_array` argument to perform a matrix lookup. The inner lookup finds the matching column and returns that entire column as an array; the outer lookup then searches vertically to find the intersection point.
* **Applicability**: Highly effective for retrieving data from a two-way table or grid where you need to match both a row condition (e.g., Country, Product) and a column condition (e.g., Year, Month). 

### 2. Structural Breakdown

- **Data Layout**: A continuous matrix of data surrounded by a 1D array of row headers on the left and a 1D array of column headers on the top.
- **Formula Logic**: `=XLOOKUP({row_lookup_value}, {row_lookup_array}, XLOOKUP({col_lookup_value}, {col_lookup_array}, {data_matrix}))`
- **Visual Design**: N/A (Formula logic only)
- **Charts/Tables**: N/A
- **Theme Hooks**: N/A

### 3. Reproduction Code

```json
{
  "name": "two_dimensional_xlookup",
  "description": "Performs a two-way matrix lookup by nesting XLOOKUPs. The inner XLOOKUP evaluates the column criteria and passes the resulting vertical array to the outer XLOOKUP to evaluate the row criteria.",
  "formula": "=XLOOKUP({row_lookup_value}, {row_lookup_array}, XLOOKUP({column_lookup_value}, {column_lookup_array}, {data_matrix}))"
}
```