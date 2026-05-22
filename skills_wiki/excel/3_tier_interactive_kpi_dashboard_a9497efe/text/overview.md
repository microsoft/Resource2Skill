### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier Interactive KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Separates data, calculations, and presentation across three tabs (Data, Staging, Dashboard). Uses a Data Validation dropdown to select a reporting period, and dynamic `INDEX(MATCH())` formulas to populate a clean, grid-based dashboard of KPI cards with conditional formatting.
* **Applicability**: Best used for monthly or weekly executive reporting packages where raw data is updated periodically, keeping the presentation layer clean, dynamic, and strictly separated from calculations.

### 2. Structural Breakdown

- **Data Layout**: 
  - **1) Data**: Raw metrics (AR Balance, Sales, Days) organized with dates in row 1.
  - **2) Staging**: Formula-driven calculations computing derived metrics (DSO, Gross Margin) and holding targets.
  - **3) Dashboard**: Presentation layer mapping to the Staging tab.
- **Formula Logic**: Uses full-row array lookups to ensure dynamic column extraction: `=INDEX('2) Staging'!2:2, MATCH($C$4, '2) Staging'!$1:$1, 0))`
- **Visual Design**: Uses merged card headers, large bold text (size 24) for primary metrics, and eliminates gridlines.
- **Charts/Tables**: Implements visual variance indicators via Conditional Formatting (Green for favorable to target, Red for unfavorable).
- **Theme Hooks**: Uses a simple dict mapping to define `header` and `card_bg` colors, defaulting to `corporate_blue`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Palette & Styles
    themes = {
        "corporate_blue": {"header": "4F81BD", "card_bg": "DCE6F1", "text": "1F497D"},
        "executive_dark": {"header": "2B2B2B", "card_bg": "EFEFEF", "text": "000000"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    header_fill = PatternFill("solid", fgColor=palette["header"])
    card_header_fill = PatternFill("solid", fgColor=palette["card_bg"])
    white_font = Font(color="FFFFFF", bold=True)
    title_font = Font(size=20, bold=True, color=palette["text"])
    kpi_font = Font(size=24, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    
    # 2. Setup Sheets
    for sheet in wb.sheetnames:
        del wb[sheet]
            
    ws_data = wb.create_sheet("1) Data")
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")

    # -------------------------
    # 3. Data Sheet (Raw Inputs)
    # -------------------------
    headers = ["Metric", "Jan-20", "Feb-20", "Mar-20"]
    ws_data.append(headers)
    for cell in ws_data[1]:
        cell.font = white_font
        cell.fill = header_fill
        
    data_rows = [
        ["AR Balance", 2800, 2940, 3087],
        ["Credit Sales", 1500, 1590, 1685],
        ["Days in Month", 31, 29, 31],
        ["Gross Profit", 600, 636, 684],
        ["Revenue", 1500, 1590, 1685]
    ]
    for row in data_rows:
        ws_data.append(row)
        
    for col in ws_data.columns:
        ws_data.column_dimensions[col[0].column_letter].width = 15

    # -------------------------
    # 4. Staging Sheet (Calculations)
    # -------------------------
    ws_staging.append(["KPI", "Jan-20", "Feb-20", "Mar-20"])
    for cell in ws_staging[1]:
        cell.font = white_font
        cell.fill = header_fill
        
    ws_staging.append(["DSO", 
        "=('1) Data'!B2/'1) Data'!B3)*'1) Data'!B4",
        "=('1) Data'!C2/'1) Data'!C3)*'1) Data'!C4",
        "=('1) Data'!D2/'1) Data'!D3)*'1) Data'!D4"])
    ws_staging.append(["DSO Target", 45, 45, 45])
    
    ws_staging.append(["Gross Margin",
        "='1) Data'!B5/'1) Data'!B6",
        "='1) Data'!C5/'1) Data'!C6",
        "='1) Data'!D5/'1) Data'!D6"])
    ws_staging.append(["GM Target", 0.40, 0.40, 0.40])
    
    for col in ws_staging.columns:
        ws_staging.column_dimensions[col[0].column_letter].width = 15

    # -------------------------
    # 5. Dashboard Sheet (Presentation)
    # -------------------------
    ws_dash.sheet_view.showGridLines = False
    
    # Adjust column widths for card spacing
    col_widths = {'A': 2, 'B': 15, 'C': 15, 'D': 15, 'E': 5, 'F': 15, 'G': 15, 'H': 15}
    for col, width in col_widths.items():
        ws_dash.column_dimensions[col].width = width
    
    # Title & Interactive Selector
    ws_dash["B2"] = title
    ws_dash["B2"].font = title_font
    
    ws_dash["B4"] = "For the month of:"
    ws_dash["B4"].font = Font(bold=True)
    ws_dash["C4"] = "Jan-20"
    ws_dash["C4"].fill = PatternFill("solid", fgColor="FFF2CC")
    ws_dash["C4"].border = Border(bottom=Side(style='thin', color="000000"))
    
    dv = DataValidation(type="list", formula1="'1) Data'!$B$1:$D$1", allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C4"])

    # --- KPI Card 1: DSO (Lower is better) ---
    ws_dash.merge_cells("B6:D6")
    ws_dash["B6"] = "DSO (Days Sales Outstanding)"
    ws_dash["B6"].fill = card_header_fill
    ws_dash["B6"].font = Font(bold=True)
    ws_dash["B6"].alignment = center_align
    
    ws_dash.merge_cells("B7:D7")
    ws_dash["B7"] = "=INDEX('2) Staging'!2:2, MATCH($C$4, '2) Staging'!$1:$1, 0))"
    ws_dash["B7"].font = kpi_font
    ws_dash["B7"].alignment = center_align
    ws_dash["B7"].number_format = "0"
    
    ws_dash.merge_cells("C8:D8")
    ws_dash["B8"] = "Vs. Target:"
    ws_dash["B8"].font = Font(italic=True, size=10)
    ws_dash["C8"] = "=$B$7 - INDEX('2) Staging'!3:3, MATCH($C$4, '2) Staging'!$1:$1, 0))"
    ws_dash["C8"].number_format = "0"

    # --- KPI Card 2: Gross Margin (Higher is better) ---
    ws_dash.merge_cells("F6:H6")
    ws_dash["F6"] = "Gross Margin %"
    ws_dash["F6"].fill = card_header_fill
    ws_dash["F6"].font = Font(bold=True)
    ws_dash["F6"].alignment = center_align
    
    ws_dash.merge_cells("F7:H7")
    ws_dash["F7"] = "=INDEX('2) Staging'!4:4, MATCH($C$4, '2) Staging'!$1:$1, 0))"
    ws_dash["F7"].font = kpi_font
    ws_dash["F7"].alignment = center_align
    ws_dash["F7"].number_format = "0%"
    
    ws_dash.merge_cells("G8:H8")
    ws_dash["F8"] = "Vs. Target:"
    ws_dash["F8"].font = Font(italic=True, size=10)
    ws_dash["G8"] = "=$F$7 - INDEX('2) Staging'!5:5, MATCH($C$4, '2) Staging'!$1:$1, 0))"
    ws_dash["G8"].number_format = "0%"
    
    # --- Conditional Formatting for Variances ---
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    green_font = Font(color="006100")
    red_font = Font(color="9C0006")
    
    # DSO Variance (<=0 Green, >0 Red)
    ws_dash.conditional_formatting.add('C8', CellIsRule(operator='lessThanOrEqual', formula=['0'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add('C8', CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill, font=red_font))
    
    # GM Variance (>=0 Green, <0 Red)
    ws_dash.conditional_formatting.add('G8', CellIsRule(operator='greaterThanOrEqual', formula=['0'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add('G8', CellIsRule(operator='lessThan', formula=['0'], fill=red_fill, font=red_font))

    # --- Outline Styling ---
    thin_side = Side(style='thin', color="A6A6A6")
    
    def apply_card_outline(ws, range_str):
        cells = ws[range_str]
        for row_idx, row in enumerate(cells):
            for col_idx, cell in enumerate(row):
                cell.border = Border(
                    top=thin_side if row_idx == 0 else None,
                    bottom=thin_side if row_idx == len(cells) - 1 else None,
                    left=thin_side if col_idx == 0 else None,
                    right=thin_side if col_idx == len(row) - 1 else None
                )

    apply_card_outline(ws_dash, 'B6:D8')
    apply_card_outline(ws_dash, 'F6:H8')
```