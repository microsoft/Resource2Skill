# Budget Vs Actuals Doughnut Dashboard

## Applicability

Best for performance dashboards, financial reporting, and budget variance sheets where visual indicators need to automatically flip states based on target thresholds.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Budget Vs Actuals Doughnut Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Standardizes financial variance direction by flipping the subtraction logic for revenue vs. expenses (so a positive variance % always means a "hit"). Uses a clever 4-slice conditional data table to drive KPI doughnut charts that dynamically color themselves green (hit) or red (miss) without needing VBA. 
* **Applicability**: Best for performance dashboards, financial reporting, and budget variance sheets where visual indicators need to automatically flip states based on target thresholds. 

### 2. Structural Breakdown

- **Data Layout**: 
  - Standard P&L vertically spanning rows 4-12. 
  - Main columns: Account, Budget, Actual, Var $, Var %.
  - A hidden "chart staging" area (Columns H:K) calculates the 4-slice logic (`Pos_Hit`, `Pos_Remainder`, `Neg_Miss`, `Neg_Remainder`).
- **Formula Logic**: 
  - Variance $: `Actual - Budget` (Revenue/Income), `Budget - Actual` (Expenses).
  - Variance %: `IFERROR(Var$ / ABS(Budget), 0)`.
  - Chart slice conditional logic uses `MIN(Var%, 1)` to prevent over-100% variances from rendering negative pie slices.
- **Visual Design**: Uses a custom number format `0%" hit";0%" miss";0%` on the variance percentage column. This drops the minus sign on misses and replaces it with descriptive text. 
- **Charts/Tables**: Clean `DoughnutChart` instances with no border/background, 70% hole size, and disabled legends. Slices explicitly mapped to Theme Success and Theme Danger colors.
- **Theme Hooks**: Consumes `header`, `text`, `success`, and `danger` palette colors. 

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Budget vs Actuals", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Base Theme Palette
    theme_colors = {
        "corporate_blue": {"header": "1F4E78", "text": "FFFFFF", "success": "2CA02C", "danger": "D62728", "bg": "F2F2F2"},
        "midnight_accent": {"header": "2C3E50", "text": "FFFFFF", "success": "27AE60", "danger": "C0392B", "bg": "ECF0F1"}
    }.get(theme, {"header": "1F4E78", "text": "FFFFFF", "success": "2CA02C", "danger": "D62728", "bg": "F2F2F2"})
    
    header_fill = PatternFill("solid", fgColor=theme_colors["header"])
    header_font = Font(color=theme_colors["text"], bold=True)
    bold_font = Font(bold=True)
    
    # Custom Format: Drops negative sign for misses and appends text
    pct_hit_miss_format = '0%" hit";0%" miss";"0%"'
    pct_format = "0%"
    num_format = "#,##0;[Red](#,##0)"
    
    # Title
    ws["A1"] = title
    ws["A1"].font = Font(size=16, bold=True, color=theme_colors["header"])
    
    # Column Headers
    headers = ["Account", "BUDGET", "ACTUAL", "VAR $", "VAR %"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=c, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        
    # Standard P&L Setup: (Account, Budget, Actual, Type [1=Rev, -1=Exp], IsSubtotal)
    data = [
        ("Revenue", 419829, 362649, 1, False),
        ("COGS", 8402, 73041, -1, False),
        ("Gross Profit", None, None, 1, True), 
        ("Gross Margin", None, None, 1, True), 
        ("Advertising & Marketing", 19381, 4658, -1, False),
        ("Other G&A", 22510, 23373, -1, False),
        ("Headcount", 28636, 14387, -1, False),
        ("Total Opex", None, None, -1, True),
        ("Net Operating Income", None, None, 1, True),
    ]
    
    row_idx = 4
    for item in data:
        acc, bud, act, sign, is_sub = item
        ws.cell(row=row_idx, column=1, value=acc)
        
        if is_sub:
            ws.cell(row=row_idx, column=1).font = bold_font
        else:
            ws.cell(row=row_idx, column=2, value=bud).number_format = num_format
            ws.cell(row=row_idx, column=3, value=act).number_format = num_format
            
            # Variance direction logic standardizes "Hits" as positive
            var_formula = f"=C{row_idx}-B{row_idx}" if sign == 1 else f"=B{row_idx}-C{row_idx}"
            ws.cell(row=row_idx, column=4, value=var_formula).number_format = num_format
            
            var_pct_formula = f"=IFERROR(D{row_idx}/ABS(B{row_idx}), 0)"
            ws.cell(row=row_idx, column=5, value=var_pct_formula).number_format = pct_hit_miss_format
            
        row_idx += 1
        
    # Inject Subtotal Formulas dynamically
    # 1. Gross Profit
    ws["B6"], ws["C6"] = "=B4-B5", "=C4-C5"
    ws["D6"], ws["E6"] = "=C6-B6", "=IFERROR(D6/ABS(B6), 0)"
    
    # 2. Gross Margin
    ws["B7"], ws["C7"] = "=IFERROR(B6/B4, 0)", "=IFERROR(C6/C4, 0)"
    ws["D7"], ws["E7"] = "=C7-B7", "=IFERROR(D7/ABS(B7), 0)"
    for col in "BCDE":
        ws[f"{col}7"].number_format = pct_format
    
    # 3. Total Opex
    ws["B11"], ws["C11"] = "=SUM(B8:B10)", "=SUM(C8:C10)"
    ws["D11"], ws["E11"] = "=B11-C11", "=IFERROR(D11/ABS(B11), 0)"
    
    # 4. Net Operating Income
    ws["B12"], ws["C12"] = "=B6-B11", "=C6-C11"
    ws["D12"], ws["E12"] = "=C12-B12", "=IFERROR(D12/ABS(B12), 0)"
    
    # Apply subtotal styles
    top_bottom_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    for r in [6, 11, 12]:
        for c in range(1, 6):
            cell = ws.cell(row=r, column=c)
            cell.font, cell.border = bold_font, top_bottom_border
            if c > 1:
                cell.number_format = num_format if c < 5 else pct_hit_miss_format

    # Set up conditional 4-Slice Chart Data Table
    chart_kpis = [
        ("Revenue", 4), 
        ("Gross Profit", 6),
        ("Total Opex", 11),
        ("Net Op Income", 12)
    ]
    
    c_start = 15
    ws.cell(row=c_start, column=7, value="Chart Data").font = bold_font
    labels = ["Pos Var (A)", "Pos Var (B)", "Neg Var (A)", "Neg Var (B)"]
    for i, lbl in enumerate(labels):
        ws.cell(row=c_start + 1 + i, column=7, value=lbl)
        
    for i, (kpi_name, d_row) in enumerate(chart_kpis):
        col = 8 + i
        col_ltr = get_column_letter(col)
        var_cell = f"E{d_row}"
        
        ws.cell(row=c_start, column=col, value=kpi_name).font = bold_font
        
        # Slices conditionally populate. Using MIN prevents >100% variance from corrupting the pie.
        ws.cell(row=c_start+1, column=col, value=f"=IF({var_cell}>0, MIN({var_cell}, 1), 0)")
        ws.cell(row=c_start+2, column=col, value=f"=IF({var_cell}>0, 1-{col_ltr}{c_start+1}, 0)")
        ws.cell(row=c_start+3, column=col, value=f"=IF({var_cell}<0, MIN(ABS({var_cell}), 1), 0)")
        ws.cell(row=c_start+4, column=col, value=f"=IF({var_cell}<0, 1-{col_ltr}{c_start+3}, 0)")
        
        for r in range(1, 5):
            ws.cell(row=c_start+r, column=col).number_format = pct_format
            
        # Initialize KPIs Doughnut
        chart = DoughnutChart()
        chart.title, chart.width, chart.height = kpi_name, 3.5, 3.5
        
        c_data = Reference(ws, min_col=col, min_row=c_start+1, max_row=c_start+4)
        chart.add_data(c_data, titles_from_data=False)
        
        # Color mapping trick: Point 0 (Pos Hit), Point 1 (Pos Empty), Point 2 (Neg Miss), Point 3 (Neg Empty)
        slice_colors = [theme_colors["success"], "E0E0E0", theme_colors["danger"], "E0E0E0"]
        for idx, color in enumerate(slice_colors):
            pt = DataPoint(idx=idx)
            pt.graphicalProperties.solidFill = color
            chart.series[0].dPt.append(pt)
            
        chart.holeSize = 70
        chart.legend = None 
        chart.graphicalProperties.line.noFill = True  # Removes chart border
        
        # Layout charts across the top right
        ws.add_chart(chart, f"{get_column_letter(7 + (i * 4))}2")

    # Dimensions cleanup
    ws.column_dimensions['A'].width = 28
    for col in "BCDE":
        ws.column_dimensions[col].width = 13
```