# Data Summary with Top KPIs and Sparklines

## Applicability

Excellent for "raw data" tabs that need to be readable and presentable, acting as a mini-dashboard or high-level summary before feeding into more complex visual layers.

## Analysis

```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Data Summary with Top KPIs and Sparklines

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a structured data table with frozen header panes, creates dynamic top-level KPI summary cards using `TEXT` formulas to format aggregated data, and adds bottom-row sparklines for inline trend visualization.
* **Applicability**: Excellent for "raw data" tabs that need to be readable and presentable, acting as a mini-dashboard or high-level summary before feeding into more complex visual layers.

### 2. Structural Breakdown

- **Data Layout**: KPIs sit in Rows 1-2, aligned above their corresponding data columns. Table headers start at Row 5, followed by data rows. Totals and Trends sit immediately below the data.
- **Formula Logic**: Uses `=TEXT(SUM(range), "format")` to generate formatted string summaries in single cells, preventing the need for complex custom cell formatting on the KPI cards.
- **Visual Design**: Gridlines disabled. KPI cells use a distinct background fill to act as "cards". Row heights and column widths are expanded for breathing room.
- **Charts/Tables**: Utilizes `SparklineGroup` to insert inline miniature trend charts at the base of each numeric column.
- **Theme Hooks**: Uses `header` for table headers and KPI values, `bg` for KPI card backgrounds, and `text` for header fonts.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.sparkline import Sparkline, SparklineGroup
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.active if wb.active.title == "Sheet" else wb.create_sheet(sheet_name)
    if ws.title != sheet_name:
        ws.title = sheet_name
        
    # Clean canvas
    ws.sheet_view.showGridLines = False
    
    # Palette configuration
    palettes = {
        "corporate_blue": {"header": "203764", "accent": "3B82F6", "text": "FFFFFF", "bg": "F3F4F6"},
        "veridian": {"header": "1F3B4D", "accent": "C8A14D", "text": "FFFFFF", "bg": "E5E7EB"},
        "minimal_grey": {"header": "374151", "accent": "9CA3AF", "text": "FFFFFF", "bg": "F9FAFB"}
    }
    colors = palettes.get(theme, palettes["corporate_blue"])
    
    header_fill = PatternFill("solid", fgColor=colors["header"])
    header_font = Font(color=colors["text"], bold=True)
    kpi_font = Font(color=colors["header"], bold=True, size=16)
    kpi_label_font = Font(color="555555", bold=True, size=10)
    card_fill = PatternFill("solid", fgColor=colors["bg"])
    
    # Data Setup
    headers = ["Month", "Product A Units", "Product B Units", "Total Sales", "Profit Margin"]
    rows = [
        ["Jan", 1200, 800, 20000, 0.15],
        ["Feb", 1360, 880, 22400, 0.18],
        ["Mar", 1490, 860, 23500, 0.22],
        ["Apr", 1320, 900, 22200, 0.20],
        ["May", 1500, 870, 23700, 0.24],
        ["Jun", 1570, 840, 24100, 0.25],
        ["Jul", 1600, 890, 24900, 0.26],
        ["Aug", 1580, 850, 24300, 0.25],
    ]
    
    start_row = 5
    end_row = start_row + len(rows)
    
    # 1. Add KPI Region (Rows 1-2)
    # Maps column letters to their aggregation logic
    kpis = [
        {"col": "B", "label": "Prod A Volume", "func": "SUM", "format": "#,##0"},
        {"col": "C", "label": "Prod B Volume", "func": "SUM", "format": "#,##0"},
        {"col": "D", "label": "Total Revenue", "func": "SUM", "format": "$#,##0"},
        {"col": "E", "label": "Avg Margin", "func": "AVERAGE", "format": "0.0%"},
    ]
    
    for i, kpi in enumerate(kpis):
        col_let = kpi["col"]
        
        # Label cell
        lbl_cell = ws[f"{col_let}1"]
        lbl_cell.value = kpi["label"].upper()
        lbl_cell.font = kpi_label_font
        lbl_cell.alignment = Alignment(horizontal="center", vertical="bottom")
        lbl_cell.fill = card_fill
        
        # Value cell (Dynamic TEXT formula)
        val_cell = ws[f"{col_let}2"]
        data_range = f"{col_let}{start_row+1}:{col_let}{end_row}"
        val_cell.value = f'=TEXT({kpi["func"]}({data_range}), "{kpi["format"]}")'
        val_cell.font = kpi_font
        val_cell.alignment = Alignment(horizontal="center", vertical="top")
        val_cell.fill = card_fill

    # 2. Insert Data Table
    for c_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=c_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
    for r_idx, row_data in enumerate(rows, start_row + 1):
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            if c_idx in (2, 3):
                cell.number_format = '#,##0'
            elif c_idx == 4:
                cell.number_format = '$#,##0'
            elif c_idx == 5:
                cell.number_format = '0.0%'
                
    # 3. Add Totals Row
    total_row = end_row + 1
    ws.cell(row=total_row, column=1, value="Total / Avg").font = Font(bold=True)
    
    for c_idx, col_let in enumerate(["B", "C", "D", "E"], 2):
        cell = ws.cell(row=total_row, column=c_idx)
        cell.font = Font(bold=True)
        if col_let == "E":
            cell.value = f"=AVERAGE({col_let}{start_row+1}:{col_let}{end_row})"
            cell.number_format = '0.0%'
        else:
            cell.value = f"=SUM({col_let}{start_row+1}:{col_let}{end_row})"
            cell.number_format = '$#,##0' if col_let == "D" else '#,##0'
            
        cell.border = Border(top=Side(style="thin"), bottom=Side(style="double"))
        
    # 4. Add Trend Row (Sparklines)
    trend_row = total_row + 1
    ws.cell(row=trend_row, column=1, value="Trend").font = Font(bold=True, color="888888")
    
    sg = SparklineGroup(type="line", markers=True)
    for col_let in ["B", "C", "D", "E"]:
        data_ref = f"{col_let}{start_row+1}:{col_let}{end_row}"
        loc_ref = f"{col_let}{trend_row}"
        sg.sparklines.append(Sparkline(reference=data_ref, sqref=loc_ref))
        
    ws.sparkline_groups.append(sg)
    
    # 5. Sizing & UX Polish
    ws.freeze_panes = f"A{start_row+1}"
    ws.column_dimensions["A"].width = 12
    for col in ["B", "C", "D", "E"]:
        ws.column_dimensions[col].width = 18
        
    ws.row_dimensions[1].height = 20
    ws.row_dimensions[2].height = 28
    ws.row_dimensions[3].height = 10  # Gap between KPIs and Table
    ws.row_dimensions[trend_row].height = 25
```
```