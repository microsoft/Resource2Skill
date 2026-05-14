### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier Dynamic KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Separates report architecture into three distinct layers (Data, Staging, Dashboard). A dropdown on the Dashboard sheet controls interactive `INDEX/MATCH` formulas that pull calculated metrics from Staging, while conditional formatting paints entire merged "cards" based on target rules.
* **Applicability**: Perfect for monthly reporting packs, financial scorecards, and executive summaries where raw data needs to be aggregated and then cleanly presented as large KPI tiles for a specific period.

### 2. Structural Breakdown

- **Data Layout**: 
  - `Data` tab: Raw input values (Sales, COGS, Balances) horizontally by month.
  - `Staging` tab: Calculations (Margins, DSO) and Targets horizontally by month.
  - `Dashboard` tab: Pure presentation layer. No raw data, just layout structures.
- **Formula Logic**: 
  - `=INDEX(Staging!$B$2:$G$2, MATCH($C$4, Staging!$B$1:$G$1, 0))` pulls the specific row metric matching the dropdown's month.
- **Visual Design**: 
  - KPI Cards span 3 columns and 4 rows.
  - Value cell is merged and utilizes a 22pt font for high legibility.
  - Full-card background colors switch dynamically (Green/Pink) using `CellIsRule`.
- **Charts/Tables**: Dropped in favor of pure typography-driven KPI tiles.
- **Theme Hooks**: Utilizes `primary` for headers, `text_light` for contrast, and semantic colors (`success_bg`, `danger_bg`) for the conditional rules.

### 3. Reproduction Code

```python
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Theme Palette
    theme_colors = {
        "corporate_blue": {"primary": "4F81BD", "text_light": "FFFFFF", "text_dark": "000000", "success_bg": "C6EFCE", "danger_bg": "FFC7CE"},
        "modern_dark": {"primary": "202020", "text_light": "FFFFFF", "text_dark": "FFFFFF", "success_bg": "43A047", "danger_bg": "E53935"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])

    # 2. Setup Sheets (Data -> Staging -> Dashboard)
    if "Sheet" in wb.sheetnames:
        dash_ws = wb["Sheet"]
        dash_ws.title = "Dashboard"
    else:
        dash_ws = wb.create_sheet("Dashboard")
        
    staging_ws = wb.create_sheet("Staging")
    data_ws = wb.create_sheet("Data")

    # 3. Populate Raw Data (Layer 1)
    months = ["Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20"]
    data_ws.append(["Category"] + months)
    data_ws.append(["Sales", 1500000, 1590000, 1685400, 1786524, 1893715, 2007338])
    data_ws.append(["COGS", 900000, 954000, 1030320, 1102442, 1168589, 1276000])
    data_ws.append(["AR Balance", 2800000, 2940000, 3087000, 3241350, 3403418, 3573588])

    for col in range(1, 2 + len(months)):
        data_ws.column_dimensions[get_column_letter(col)].width = 15

    # 4. Populate Staging Sheet calculations (Layer 2)
    staging_ws.append(["Category"] + months)
    for i, month in enumerate(months):
        col_idx = i + 2
        col_ltr = get_column_letter(col_idx)
        # Sales
        staging_ws.cell(row=2, column=col_idx, value=f"=Data!{col_ltr}2")
        # Sales Target
        staging_ws.cell(row=3, column=col_idx, value=1600000)
        # Gross Margin %
        staging_ws.cell(row=4, column=col_idx, value=f"=(Data!{col_ltr}2-Data!{col_ltr}3)/Data!{col_ltr}2")
        # GM Target
        staging_ws.cell(row=5, column=col_idx, value=0.40)
        # DSO (Proxy metric: AR / Sales * 30 days)
        staging_ws.cell(row=6, column=col_idx, value=f"=(Data!{col_ltr}4/Data!{col_ltr}2)*30")
        # DSO Target
        staging_ws.cell(row=7, column=col_idx, value=45)

    staging_labels = ["Sales", "Sales Target", "Gross Margin", "GM Target", "DSO", "DSO Target"]
    for row_idx, label in enumerate(staging_labels, start=2):
        staging_ws.cell(row=row_idx, column=1, value=label)
    staging_ws.column_dimensions["A"].width = 20

    # 5. Build Dashboard Presentation (Layer 3)
    dash_ws.sheet_view.showGridLines = False
    
    # Main Header
    dash_ws.merge_cells("B2:J2")
    dash_ws["B2"] = title
    dash_ws["B2"].font = Font(size=20, bold=True, color=palette["text_light"])
    dash_ws["B2"].fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    dash_ws["B2"].alignment = Alignment(horizontal="center", vertical="center")
    
    # Interactive Date Selector
    dash_ws["B4"] = "For the month of:"
    dash_ws["B4"].font = Font(bold=True)
    dash_ws["B4"].alignment = Alignment(horizontal="right", vertical="center")
    
    col_range = get_column_letter(1 + len(months))
    dv = DataValidation(type="list", formula1=f"Staging!$B$1:${col_range}$1", allow_blank=False)
    dash_ws.add_data_validation(dv)
    dv.add("C4")
    dash_ws["C4"] = months[-1] # Default value
    dash_ws["C4"].fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    dash_ws["C4"].border = Border(bottom=Side(style="medium", color=palette["primary"]))
    dash_ws["C4"].alignment = Alignment(horizontal="center", vertical="center")

    # Section Banner
    dash_ws.merge_cells("B6:J6")
    dash_ws["B6"] = "Key Performance Indicators"
    dash_ws["B6"].font = Font(size=14, bold=True, color=palette["text_dark"])
    dash_ws["B6"].fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    dash_ws["B6"].alignment = Alignment(horizontal="center", vertical="center")

    # 6. Reusable helper to draw index-matched KPI Cards
    def draw_kpi_card(start_row, start_col, kpi_title, val_row, is_lower_better, format_str):
        # Card Header
        dash_ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+2)
        h_cell = dash_ws.cell(row=start_row, column=start_col, value=kpi_title)
        h_cell.font = Font(bold=True, color=palette["text_light"])
        h_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
        h_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Primary Value (Dynamically pulls from staging via month dropdown)
        dash_ws.merge_cells(start_row=start_row+1, start_column=start_col, end_row=start_row+2, end_column=start_col+2)
        v_form = f"=INDEX(Staging!$B${val_row}:${col_range}${val_row}, MATCH($C$4, Staging!$B$1:${col_range}$1, 0))"
        v_cell = dash_ws.cell(row=start_row+1, column=start_col, value=v_form)
        v_cell.font = Font(size=22, bold=True)
        v_cell.alignment = Alignment(horizontal="center", vertical="center")
        v_cell.number_format = format_str
        
        # Comparison Labels
        dash_ws.cell(row=start_row+3, column=start_col, value="Vs. Target").font = Font(size=9, italic=True)
        dash_ws.merge_cells(start_row=start_row+3, start_column=start_col+1, end_row=start_row+3, end_column=start_col+2)
        
        t_form = f"=INDEX(Staging!$B${val_row+1}:${col_range}${val_row+1}, MATCH($C$4, Staging!$B$1:${col_range}$1, 0))"
        t_cell = dash_ws.cell(row=start_row+3, column=start_col+1, value=t_form)
        t_cell.font = Font(size=9)
        t_cell.number_format = format_str
        t_cell.alignment = Alignment(horizontal="right", vertical="center")
        
        # Setup Conditional Formatting matching the Target
        cf_range = f"{v_cell.coordinate}:{get_column_letter(start_col+2)}{start_row+2}"
        tgt_ref = f"${t_cell.column_letter}${t_cell.row}"
        
        good_fill = PatternFill(start_color=palette["success_bg"], end_color=palette["success_bg"], fill_type="solid")
        bad_fill = PatternFill(start_color=palette["danger_bg"], end_color=palette["danger_bg"], fill_type="solid")
        
        if is_lower_better:
            dash_ws.conditional_formatting.add(cf_range, CellIsRule(operator="lessThanOrEqual", formula=[tgt_ref], fill=good_fill))
            dash_ws.conditional_formatting.add(cf_range, CellIsRule(operator="greaterThan", formula=[tgt_ref], fill=bad_fill))
        else:
            dash_ws.conditional_formatting.add(cf_range, CellIsRule(operator="greaterThanOrEqual", formula=[tgt_ref], fill=good_fill))
            dash_ws.conditional_formatting.add(cf_range, CellIsRule(operator="lessThan", formula=[tgt_ref], fill=bad_fill))
            
        # Standardize borders around the card
        thin = Side(border_style="thin", color="BFBFBF")
        for r in range(start_row, start_row+4):
            for c in range(start_col, start_col+3):
                dash_ws.cell(row=r, column=c).border = Border(top=thin, bottom=thin, left=thin, right=thin)

    # 7. Render Example Specific Cards
    draw_kpi_card(start_row=8, start_col=2, kpi_title="Sales Revenue", val_row=2, is_lower_better=False, format_str="$#,##0")
    draw_kpi_card(start_row=8, start_col=5, kpi_title="Gross Margin %", val_row=4, is_lower_better=False, format_str="0.0%")
    draw_kpi_card(start_row=8, start_col=8, kpi_title="DSO (Days)", val_row=6, is_lower_better=True, format_str="0")

    # Expand presentation column widths across the board
    for col in range(2, 11):
        dash_ws.column_dimensions[get_column_letter(col)].width = 12
```