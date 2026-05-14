### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Sales Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a full dashboard canvas by manipulating cell fills and hiding gridlines to create a two-tone layout (dark header, light content area). It simulates floating KPI cards using merged cells with thick outer borders, and builds a summary Excel Table augmented with in-cell conditional formatting Data Bars.
* **Applicability**: Ideal for executive overviews and reporting dashboards. Use this when you need to combine high-level metric callouts (KPIs) with a sortable, visually dense summary table on a single, professional-looking pane.

### 2. Structural Breakdown

- **Data Layout**: Places dashboard titles in the upper left, KPI strips across the right side of the header (using spacing arrays to place "cards"), and a summary table anchored below the header on the light canvas.
- **Formula Logic**: Simulated KPI cards use simple static values here, but in practice anchor to external summary calculations. The table dynamically adapts to data length.
- **Visual Design**: Uses a custom two-tone layout (`primary` for the top 8 rows, `bg_light` for the rest). KPI cards use white fills with `accent`-colored borders. 
- **Charts/Tables**: Replaces basic table numbers with gradient Data Bars via `DataBarRule` for columns requiring rapid visual scanning (e.g., volume and revenue metrics).
- **Theme Hooks**: Consumes `primary` (header block, primary data bar), `accent` (subtitle, KPI borders, secondary data bar), `bg_light` (canvas background), and `text_light`/`text_dark` (fonts).

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, 
                 title: str = "Sales Dashboard", 
                 subtitle: str = "Evaluating Agent Performance", 
                 kpi_data: list = None, 
                 table_data: list = None, 
                 theme: str = "dashboard_purple", 
                 **kwargs) -> None:
    """
    Renders a complete dashboard canvas featuring a bold header, mock KPI cards, 
    and a conditionally formatted data bar summary table.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Fallback default data
    if kpi_data is None:
        kpi_data = [
            {"label": "TOTAL CALLS", "value": "16,749"},
            {"label": "REACHED", "value": "3,328"},
            {"label": "CLOSED", "value": "1,203"},
            {"label": "DEAL VALUE", "value": "$646,979"}
        ]

    if table_data is None:
        table_data = [
            ["Agent Name", "Total Calls", "Calls Reached", "Deals Closed", "Deal Value"],
            ["Alice", 1031, 128, 49, 41200],
            ["Bob", 661, 73, 28, 40092],
            ["Charlie", 610, 86, 67, 45236],
            ["Diana", 566, 163, 26, 38593],
            ["Evan", 722, 168, 70, 44841],
        ]

    # 2. Theme definitions
    themes = {
        "corporate_blue": {"primary": "2F5597", "accent": "FFC000", "bg_light": "F2F5FA", "text_light": "FFFFFF", "text_dark": "000000"},
        "dashboard_purple": {"primary": "5C3A92", "accent": "FFD966", "bg_light": "F2EFF5", "text_light": "FFFFFF", "text_dark": "333333"}
    }
    t = themes.get(theme, themes["dashboard_purple"])

    fill_primary = PatternFill("solid", fgColor=t["primary"])
    fill_light = PatternFill("solid", fgColor=t["bg_light"])
    fill_white = PatternFill("solid", fgColor="FFFFFF")

    # 3. Canvas Background 
    # Header zone (Rows 1-8)
    for row in range(1, 9):
        ws.row_dimensions[row].height = 25
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = fill_primary

    # Content zone (Rows 9-40)
    for row in range(9, 40):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = fill_light

    # 4. Dashboard Typography
    ws.row_dimensions[2].height = 40
    c_title = ws.cell(row=2, column=2, value=title)
    c_title.font = Font(size=32, color=t["text_light"], bold=True)

    c_subtitle = ws.cell(row=3, column=2, value=subtitle)
    c_subtitle.font = Font(size=14, color=t["accent"])

    # 5. KPI Cards (Mocked as bordered cell regions)
    col_offsets = [6, 9, 12, 15] # Placing cards in cols F, I, L, O
    for i, kpi in enumerate(kpi_data[:4]):
        start_col = col_offsets[i]
        
        # Merge Top (Value)
        ws.merge_cells(start_row=4, start_column=start_col, end_row=5, end_column=start_col+1)
        val_cell = ws.cell(row=4, column=start_col, value=kpi["value"])
        val_cell.font = Font(size=20, bold=True, color=t["primary"])
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Merge Bottom (Label)
        ws.merge_cells(start_row=6, start_column=start_col, end_row=6, end_column=start_col+1)
        lbl_cell = ws.cell(row=6, column=start_col, value=kpi["label"])
        lbl_cell.font = Font(size=11, color=t["text_dark"], bold=True)
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Apply Fill & Outer Borders
        for r in range(4, 7):
            for c in range(start_col, start_col+2):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_white
                
                b_top = Side(style='medium', color=t["accent"]) if r == 4 else None
                b_bottom = Side(style='medium', color=t["accent"]) if r == 6 else None
                b_left = Side(style='medium', color=t["accent"]) if c == start_col else None
                b_right = Side(style='medium', color=t["accent"]) if c == start_col+1 else None
                
                cell.border = Border(top=b_top, bottom=b_bottom, left=b_left, right=b_right)

    # 6. Data Bar Summary Table
    start_row = 10
    start_col = 2
    for r_idx, row_data in enumerate(table_data):
        for c_idx, val in enumerate(row_data):
            cell = ws.cell(row=start_row + r_idx, column=start_col + c_idx, value=val)
            if r_idx > 0 and c_idx == 4:
                cell.number_format = '"$"#,##0'

    end_row = start_row + len(table_data) - 1
    end_col = start_col + len(table_data[0]) - 1

    # Excel Table Implementation
    ref = f"{get_column_letter(start_col)}{start_row}:{get_column_letter(end_col)}{end_row}"
    tab = Table(displayName="AgentKPIs", ref=ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, 
                                        showLastColumn=False, showRowStripes=True)
    ws.add_table(tab)

    # Conditional Formatting: In-Cell Data Bars
    # Metric 1: Calls Reached (Column D / Index 2)
    d_col = get_column_letter(start_col + 2)
    ws.conditional_formatting.add(
        f"{d_col}{start_row+1}:{d_col}{end_row}", 
        DataBarRule(start_type='min', end_type='max', color="FF" + t["accent"])
    )

    # Metric 2: Deal Value (Column F / Index 4)
    f_col = get_column_letter(start_col + 4)
    ws.conditional_formatting.add(
        f"{f_col}{start_row+1}:{f_col}{end_row}", 
        DataBarRule(start_type='min', end_type='max', color="FF" + t["primary"])
    )

    # Clean up column spacing
    for c in range(start_col, end_col + 1):
        ws.column_dimensions[get_column_letter(c)].width = 15
    ws.column_dimensions["A"].width = 2
```