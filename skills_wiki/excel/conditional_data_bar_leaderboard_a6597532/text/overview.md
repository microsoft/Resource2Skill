### 1. High-level Skill Pattern Extraction

> **Skill Name**: Conditional Data Bar Leaderboard

* **Tier**: component
* **Core Mechanism**: Builds a structured table from a list of dictionaries and applies `DataBarRule` conditional formatting to numerical columns. This creates horizontal, in-cell bar charts that overlay the cell values, turning a dense grid of numbers into an easily scannable visual ranking. 
* **Applicability**: Excellent for sales dashboards, performance scorecards, or any report where ranking entities (like sales reps, products, or regions) across multiple numeric metrics is required. Best used when you need to convey both precise figures and relative magnitude without consuming the space of a standalone chart.

### 2. Structural Breakdown

- **Data Layout**: Standard table structure with a merged, oversized title row placed directly above the column headers.
- **Formula Logic**: No complex formulas are required; raw aggregated values are written directly to the cells to keep the sheet lightweight.
- **Visual Design**: Uses a dark theme color for the header background with white text. Applies subtle alternating row banding, and sets thin bottom borders to anchor the data.
- **Charts/Tables**: Bypasses heavy PivotTables and traditional charts in favor of Conditional Formatting (`DataBarRule`), mapping distinct hex colors to each metric's bar.
- **Theme Hooks**: Consumes `primary` for the main title and header fills, `text_light` for header fonts, and `bg_light` for alternating row bands. 

### 3. Reproduction Code

```python
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule

def render(ws, anchor: str, *, data: list[dict] = None, columns: list[dict] = None, title: str = "Sales Agent Leaderboard", theme: str = "purple_aspect", **kwargs) -> None:
    """
    Renders a leaderboard table with in-cell data bars for visual ranking.
    """
    
    # 1. Setup default mock data if none provided
    if not data:
        data = [
            {"name": "Alice", "calls": 1031, "reached": 56, "closed": 27, "value": 13519},
            {"name": "Bob", "calls": 661, "reached": 73, "closed": 28, "value": 40092},
            {"name": "Charlie", "calls": 610, "reached": 86, "closed": 67, "value": 45236},
            {"name": "Diana", "calls": 566, "reached": 163, "closed": 26, "value": 38593},
            {"name": "Evan", "calls": 722, "reached": 168, "closed": 91, "value": 11093},
            {"name": "Fiona", "calls": 840, "reached": 190, "closed": 28, "value": 27234},
        ]
        # Sort by value descending to simulate a true leaderboard ranking
        data = sorted(data, key=lambda x: x["value"], reverse=True)
        
    if not columns:
        columns = [
            {"key": "name", "label": "Agent", "type": "text"},
            {"key": "calls", "label": "Total Calls", "type": "number", "format": "#,##0", "bar_color": "FFB4A7D6"}, # Light Purple
            {"key": "reached", "label": "Calls Reached", "type": "number", "format": "#,##0", "bar_color": "FFFFC000"}, # Gold
            {"key": "closed", "label": "Deals Closed", "type": "number", "format": "#,##0", "bar_color": "FF9BC2E6"}, # Light Blue
            {"key": "value", "label": "Deal Value", "type": "number", "format": "$#,##0", "bar_color": "FF4A235A"}, # Dark Purple
        ]

    # 2. Theme setup (simulating standard theme loader)
    theme_colors = {
        "corporate_blue": {"primary": "FF2F5597", "bg_light": "FFD9E1F2", "text_light": "FFFFFFFF"},
        "purple_aspect": {"primary": "FF4A235A", "bg_light": "FFF2EFF5", "text_light": "FFFFFFFF"},
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])

    # Parse anchor
    col_str, row_str = coordinate_from_string(anchor)
    start_col = column_index_from_string(col_str)
    start_row = int(row_str)

    # 3. Render Title
    end_col = start_col + len(columns) - 1
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)
    title_cell = ws.cell(row=start_row, column=start_col, value=title)
    title_cell.font = Font(size=16, bold=True, color=palette["primary"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[start_row].height = 25

    # 4. Render Headers
    header_row = start_row + 1
    thin_border = Border(bottom=Side(style='thin', color="FFCCCCCC"))
    
    for c_idx, col_def in enumerate(columns):
        cell = ws.cell(row=header_row, column=start_col + c_idx, value=col_def["label"])
        cell.font = Font(bold=True, color=palette["text_light"])
        cell.fill = PatternFill(solid=True, fgColor=palette["primary"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Set a generous column width so data bars display clearly alongside text
        col_letter = get_column_letter(start_col + c_idx)
        ws.column_dimensions[col_letter].width = 18 if col_def.get("type") == "number" else 15

    # 5. Render Data & Banding
    data_start_row = header_row + 1
    for r_idx, row_data in enumerate(data):
        current_row = data_start_row + r_idx
        for c_idx, col_def in enumerate(columns):
            val = row_data.get(col_def["key"], "")
            cell = ws.cell(row=current_row, column=start_col + c_idx, value=val)
            
            if col_def.get("type") == "number":
                cell.number_format = col_def.get("format", "General")
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
            cell.border = thin_border
            
            # Apply subtle background banding to alternating rows
            if r_idx % 2 == 1:
                cell.fill = PatternFill(solid=True, fgColor=palette["bg_light"])

    # 6. Apply Data Bars (Conditional Formatting)
    data_end_row = data_start_row + len(data) - 1
    for c_idx, col_def in enumerate(columns):
        if col_def.get("bar_color"):
            col_letter = get_column_letter(start_col + c_idx)
            cell_range = f"{col_letter}{data_start_row}:{col_letter}{data_end_row}"
            
            # Creates the in-cell bar chart dynamically scaled to the column's min/max
            rule = DataBarRule(
                start_type='min', 
                end_type='max', 
                color=col_def["bar_color"]
            )
            ws.conditional_formatting.add(cell_range, rule)
```