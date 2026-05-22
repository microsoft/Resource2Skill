# Spilled Array Reference Operator

## Applicability

Essential for aggregating, summarizing, or chaining dynamic arrays (e.g., `=COUNTA(F7#)`) and for defining dynamic named ranges used in chart series or data validation dropdowns where the data length is variable.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Spilled Array Reference Operator

* **Tier**: snippet
* **Core Mechanism**: By appending a hash (`#`) to a cell reference containing a dynamic array formula (e.g., `UNIQUE` or `FILTER`), Excel dynamically captures the entire spilled range. As the underlying data updates and the array resizes, the reference automatically expands or shrinks without requiring manual adjustment.
* **Applicability**: Essential for aggregating, summarizing, or chaining dynamic arrays (e.g., `=COUNTA(F7#)`) and for defining dynamic named ranges used in chart series or data validation dropdowns where the data length is variable.

### 2. Structural Breakdown

- **Data Layout**: A dynamic array formula (like `=UNIQUE(SalesData[Category])`) is placed in a single anchor cell (e.g., `F7`), spilling its results into the adjacent cells below it.
- **Formula Logic**: `={function}({anchor_cell}#)` — The `#` operator instructs Excel to resolve the anchor cell to its full spilled array dimensions rather than a single static cell.
- **Visual Design**: N/A
- **Charts/Tables**: Can be used inside the Name Manager to create dynamic, auto-expanding ranges that feed into Dashboard charts.
- **Theme Hooks**: N/A

### 3. Reproduction Code

```json
{
  "name": "spilled_array_reference",
  "description": "Reference an entire dynamic array spill range by appending a hash (#) to the top-left anchor cell.",
  "formula": "={function}({anchor_cell}#)",
  "placeholders": {
    "function": "Any Excel function that accepts a range or array (e.g., COUNTA, SUM, SORT, TEXTJOIN)",
    "anchor_cell": "The single cell containing the parent dynamic array formula (e.g., F7)"
  },
  "example": "=COUNTA(F7#)"
}
```