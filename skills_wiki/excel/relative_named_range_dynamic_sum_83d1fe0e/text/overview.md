# Relative Named Range Dynamic Sum

## Applicability

Ideal for financial models, expense ledgers, or summary tables where users frequently insert new rows at the very bottom of the data set (right above the total row). Normally, inserting a row outside the boundaries of a standard `SUM(C4:C9)` range fails to include the new row; this technique solves that completely without volatile functions like `OFFSET`.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Relative Named Range Dynamic Sum

* **Tier**: snippet
* **Core Mechanism**: Creates a Named Range (e.g., `PrevCell`) that uses a relative row reference to always point to the cell immediately above the active cell. A `SUM` formula then anchors to the top of the data column and ends at `PrevCell`. If a user inserts a new row just above the total, the total expands automatically because `PrevCell` dynamically points to the newly inserted row.
* **Applicability**: Ideal for financial models, expense ledgers, or summary tables where users frequently insert new rows at the very bottom of the data set (right above the total row). Normally, inserting a row outside the boundaries of a standard `SUM(C4:C9)` range fails to include the new row; this technique solves that completely without volatile functions like `OFFSET`.

### 2. Structural Breakdown

- **Data Layout**: A continuous column of numeric data ending with a Total row.
- **Formula Logic**: 
  - *Name Manager*: Define `PrevCell` = `!G16` (Assuming the active cell during creation is G17. Do not use `$` for the row, ensuring it stays relative).
  - *Cell Formula*: `=SUM(C4:PrevCell)`.
- **Visual Design**: N/A
- **Charts/Tables**: N/A
- **Theme Hooks**: N/A

### 3. Reproduction Code

```json
{
  "name": "dynamic_sum_relative_name",
  "description": "A dynamic sum formula anchored to a relative named range that points to the cell immediately above the formula, allowing seamless row insertions directly above the total.",
  "setup_instructions": [
    "1. Select the cell where you want your total (e.g., G17).",
    "2. Open Formulas > Name Manager > New.",
    "3. Name it 'PrevCell'.",
    "4. Set 'Refers to:' as =!G16 (Reference the cell directly above, omitting absolute $ signs on the row. Use the ! prefix to allow it across sheets)."
  ],
  "formula": "=SUM({start_cell}:PrevCell)",
  "example": "=SUM(C4:PrevCell)"
}
```