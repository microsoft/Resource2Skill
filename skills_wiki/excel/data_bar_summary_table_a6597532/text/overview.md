### 1. High-level Skill Pattern Extraction

> **Skill Name**: Data Bar Summary Table

* **Tier**: component
* **Core Mechanism**: Transforms a standard data grid into an "in-cell dashboard" by applying Conditional Formatting Data Bars across multiple metrics simultaneously. Combines this with an Excel Table object to automatically handle row striping and formatting. 
* **Applicability**: Ideal for leaderboard dashboards, ranking tables, or executive summaries. Use this when you want to display exact values for multiple entities (e.g., sales reps, products) while also visually comparing their magnitudes without cluttering the canvas with standalone charts.

### 2. Structural Breakdown

- **Data Layout**: A 2D grid where the first column is a categorical label (e.g., Name) and subsequent columns contain numeric metrics. Placed below an optional title header.
- **Formula Logic**: Relies on relative magnitudes within the column; no external formulas are required as the `DataBarRule` implicitly evaluates the `min` and `max` of each range.
- **Visual Design**: Uses explicitly themed header row fills. Number formatting is applied directly (`"$"#,##0` for currency, `#,##0` for standard integers). Values are center-aligned over the data bars for readability.
- **Charts/Tables**: Binds the data area into an `openpyxl.worksheet.table.Table` with `TableStyleLight1` to automatically add subtle alternating row stripes. Replaces standard charts with in-cell `DataBarRule` overlays.
- **Theme Hooks**: Consumes `primary` for the header and top-level metric data bar, `secondary` for the mid-level metric, and `accent` for the secondary metric. `header_text` defines contrast for the table header font.

### 3. Reproduction Code

```python
from openpyxl.utils import get_column_letter, column_index_from_string, coordinate_from_string
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import DataBarRule
from openpyxl.worksheet.table import Table, TableStyleInfo

def render(ws, anchor: str, *, title: str = "Sales Agent KPIs", data: list[list] = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a styled summary table with embedded conditional formatting data bars for visual comparison.
    """
    # 1. Theme setup
    colors = {
        "corporate_blue": {"primary": "FF2F5597", "secondary": "FF8FAADC", "accent": "FFFFC000", "header_text": "FFFFFFFF", "text": "FF000000"},
        "purple_gold": {"primary": "FF604A7B", "secondary": "FFB1A0C7", "accent": "FFFFC000", "header_text": "FFFFFFFF", "text": "FF000000"}
    }
    palette = colors.get(theme, colors["corporate_blue"])
    
    if not data:
        data = [
            ["Alice", 1031, 56, 37, 13519.04],
            ["Bob", 661, 73, 28, 40092.43],
            ["Charlie", 610, 86, 67, 45236.03],
            ["Diana", 566, 163, 26, 38593.93],
            ["Evan", 722, 168, 91, 11093.02],
            ["Fiona", 414, 169, 85, 41186.17]
        ]
        
    headers = ["Name", "Total Calls", "Calls Reached", "Deals Closed", "Deal Value ($)"]
    
    start_col_str, start_row_str = coordinate_from_string(anchor)
    start_col = column_index_from_string(start_col_str)
    start_row = int(start_row_str)
    
    # 2. Render Title
    title_cell = ws.cell(row=start_row, column=start_col)
    title_cell.value = title
    title_cell.font = Font(size=14, bold=True, color=palette["text"])
    
    header_row = start_row + 2
    
    # 3. Write and format headers
    for col_idx, header in enumerate(headers, start=start_col):
        cell = ws.cell(row=header_row, column=col_idx, value=header)
        cell.font = Font(bold=True, color=palette["header_text"])
        cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = max(len(header) + 4, 14)
        
    # 4. Write data payload
    for r_idx, row_data in enumerate(data, start=header_row + 1):
        for c_idx, val in enumerate(row_data, start=start_col):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            
            # Format Deal Value as currency, others as standard numbers
            if c_idx == start_col + 4: 
                cell.number_format = '"$"#,##0'
            elif isinstance(val, (int, float)):
                cell.number_format = '#,##0'
            
            # Left align textual entities, center align numbers over data bars
            align = "left" if c_idx == start_col else "center"
            cell.alignment = Alignment(horizontal=align, vertical="center")
            
    last_row = header_row + len(data)
    
    # 5. Apply In-Cell Data Bars
    def add_databar(col_offset, color_hex):
        col_letter = get_column_letter(start_col + col_offset)
        cell_range = f"{col_letter}{header_row + 1}:{col_letter}{last_row}"
        rule = DataBarRule(start_type="min", end_type="max", color=color_hex)
        ws.conditional_formatting.add(cell_range, rule)
        
    add_databar(2, palette["accent"])     # Calls Reached 
    add_databar(3, palette["secondary"])  # Deals Closed
    add_databar(4, palette["primary"])    # Deal Value
    
    # 6. Wrap in Excel Table for automatic striping and structure
    end_col_letter = get_column_letter(start_col + len(headers) - 1)
    tab_ref = f"{start_col_str}{header_row}:{end_col_letter}{last_row}"
    
    # Ensure table name is clean and unique per anchor
    clean_sheet_name = "".join(c for c in ws.title if c.isalnum())
    tab_name = f"KPITable_{clean_sheet_name}_{anchor}"
    
    tab = Table(displayName=tab_name, ref=tab_ref)
    style = TableStyleInfo(
        name="TableStyleLight1", 
        showFirstColumn=False,
        showLastColumn=False, 
        showRowStripes=True, 
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)
```