### 1. High-level Skill Pattern Extraction

> **Skill Name**: In-Cell Data Bar KPI Table

* **Tier**: component
* **Core Mechanism**: Converts a raw dataset into a structured Excel Table and applies column-specific `DataBarRule` conditional formats to numeric fields. This creates in-cell bar charts that scale relatively within their column, transforming a standard grid into a compact multi-metric visual ranking leaderboard.
* **Applicability**: Ideal for ranking categorical entities (like sales reps, products, or regions) across multiple distinct numeric metrics simultaneously, without cluttering the report with multiple separate charts.

### 2. Structural Breakdown

- **Data Layout**: A continuous tabular block with headers. Categorical entity names in the leftmost column, and numeric metrics in the subsequent columns.
- **Formula Logic**: Uses static numeric values; the visual scaling is handled entirely by the Excel rendering engine evaluating the min/max of each column dynamically.
- **Visual Design**: Columns are widened to provide physical space for the data bars. Numbers remain visible overlaid on the bars, formatted with comma separators and currency symbols where appropriate.
- **Charts/Tables**: An official Excel `Table` object (`ListObject`) is used for robust structured references and auto-banding, coupled with `conditional_formatting.add` using `DataBarRule`.
- **Theme Hooks**: The table style and data bar colors map to a theme's categorical palette (e.g., primary, secondary, accent colors) to visually differentiate the metrics.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, data: list[dict] = None, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter
    from openpyxl.worksheet.table import Table, TableStyleInfo
    from openpyxl.formatting.rule import DataBarRule
    from openpyxl.styles import Font

    # Default dataset if none provided
    if data is None:
        raw_data = [
            {"Rep": "Alice", "Calls": 827, "Reached": 128, "Closed": 49, "Value": 41200},
            {"Rep": "Bob", "Calls": 661, "Reached": 73, "Closed": 28, "Value": 40092},
            {"Rep": "Charlie", "Calls": 610, "Reached": 86, "Closed": 67, "Value": 45236},
            {"Rep": "David", "Calls": 375, "Reached": 120, "Closed": 48, "Value": 2590},
            {"Rep": "Emma", "Calls": 1057, "Reached": 63, "Closed": 17, "Value": 37876},
            {"Rep": "Frank", "Calls": 737, "Reached": 168, "Closed": 91, "Value": 11093},
        ]
        # Pre-sort to create a leaderboard effect based on the primary metric
        data = sorted(raw_data, key=lambda x: x["Value"], reverse=True)

    start_row, start_col = coordinate_to_tuple(anchor)
    headers = list(data[0].keys())

    # Write Headers
    for col_idx, header in enumerate(headers):
        cell = ws.cell(row=start_row, column=start_col + col_idx, value=header)
        cell.font = Font(bold=True)
        # Widen columns to give data bars physical room to render effectively
        ws.column_dimensions[get_column_letter(start_col + col_idx)].width = 16

    # Write Data & Format Numbers
    for row_idx, row_data in enumerate(data):
        for col_idx, key in enumerate(headers):
            val = row_data[key]
            cell = ws.cell(row=start_row + 1 + row_idx, column=start_col + col_idx, value=val)
            
            if isinstance(val, (int, float)):
                if "Value" in key or "Revenue" in key or "Sales" in key:
                    cell.number_format = "$#,##0"
                else:
                    cell.number_format = "#,##0"

    end_row = start_row + len(data)
    end_col = start_col + len(headers) - 1

    # Apply Structured Table
    ref = f"{get_column_letter(start_col)}{start_row}:{get_column_letter(end_col)}{end_row}"
    
    # Table names must be strictly unique in the workbook
    tab_name = f"KPI_Table_{ws.title.replace(' ', '_')}_{start_row}_{start_col}"
    tab = Table(displayName=tab_name, ref=ref)
    
    # Use a neutral table style so the bright data bars stand out
    style = TableStyleInfo(
        name="TableStyleLight1", 
        showFirstColumn=False, 
        showLastColumn=False, 
        showRowStripes=True, 
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)

    # Apply Conditional Formatting Data Bars to Numeric Columns
    # These hex values can be wired to a dynamically loaded theme dictionary
    bar_colors = ["FF4F81BD", "FFC0504D", "FF9BBB59", "FF8064A2", "FF4BACC6"]
    
    color_idx = 0
    for col_idx, key in enumerate(headers):
        # Skip categorical/string columns (heuristic: check first row's data type)
        if isinstance(data[0][key], (int, float)):
            col_letter = get_column_letter(start_col + col_idx)
            data_range = f"{col_letter}{start_row + 1}:{col_letter}{end_row}"
            
            selected_color = bar_colors[color_idx % len(bar_colors)]
            color_idx += 1
            
            # Create and add the data bar rule
            rule = DataBarRule(
                start_type='min', 
                end_type='max', 
                color=selected_color
            )
            ws.conditional_formatting.add(data_range, rule)
```