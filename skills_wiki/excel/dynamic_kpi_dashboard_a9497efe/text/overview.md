```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Combines a backend `Data` sheet with a frontend `Dashboard` sheet. Uses a Data Validation dropdown to select a time period, feeding an `INDEX/MATCH` formula to dynamically populate large KPI "cards". Employs `CellIsRule` conditional formatting to color-code values against performance targets while preserving the large typography.
* **Applicability**: Best for executive summaries, financial overviews, and operational metric reporting where users need to quickly toggle between time periods (e.g., months, quarters) and instantly see if KPIs are hitting targets.

### 2. Structural Breakdown

- **Data Layout**: 
  - `Data` tab: Time-series layout (Metrics in rows, Time periods in columns).
  - `Dashboard` tab: Grid-based KPI cards separated by empty buffer columns.
- **Formula Logic**: `=INDEX(Data!$B$2:$D$2, MATCH($C$4, Data!$B$1:$D$1, 0))`
- **Visual Design**: 
  - Cards are constructed using three merged rows: Header (gray background), Value (large size 24 font), and Footer (small italic target label).
  - Conditional Formatting (CF) rules apply to the value row. CF fonts explicitly re-declare `size=24` and `bold=True` so they don't overwrite the base typography when triggered.
- **Charts/Tables**: None (purely typography and cell-fill driven).
- **Theme Hooks**: Primary backgrounds for section headers, light gray for card headers, and semantic green/red for success/fail states.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.utils import get_column_letter
    
    # 1. Setup Theme Colors & Styles
    header_fill = PatternFill("solid", fgColor="2C3E50")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    
    card_header_fill = PatternFill("solid", fgColor="ECF0F1")
    card_header_font = Font(color="2C3E50", bold=True, size=11)
    card_footer_font = Font(color="7F8C8D", italic=True, size=10)
    
    # NOTE: Conditional formatting fonts override base fonts. 
    # Must explicitly re-declare size=24 and bold=True here.
    green_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
    green_font = Font(color="155724", bold=True, size=24)
    
    red_fill = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
    red_font = Font(color="721C24", bold=True, size=24)
    
    center_align = Alignment(horizontal="center", vertical="center")
    
    thin_border = Border(
        left=Side(style='thin', color='BDC3C7'),
        right=Side(style='thin', color='BDC3C7'),
        top=Side(style='thin', color='BDC3C7'),
        bottom=Side(style='thin', color='BDC3C7')
    )

    # 2. Setup Data Sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
        
    ws_data = wb.create_sheet("Data")
    data = [
        ["Metric", "Jan-2020", "Feb-2020", "Mar-2020"],
        ["DSO", 41, 56, 42],
        ["DPO", 89, 100, 85],
        ["Gross Margin", 0.38, 0.25, 0.40]
    ]
    for row in data:
        ws_data.append(row)
        
    for cell in ws_data[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="E0E0E0")
        
    # 3. Setup Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard", 0)
    ws_dash.sheet_view.showGridLines = False
    
    # Title & Controls
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=20, bold=True, color="2C3E50")
    
    ws_dash["B4"] = "For the month of:"
    ws_dash["B4"].font = Font(bold=True)
    ws_dash["B4"].alignment = Alignment(horizontal="right", vertical="center")
    
    ws_dash["C4"] = "Feb-2020"
    ws_dash["C4"].fill = PatternFill("solid", fgColor="FFF2CC")
    ws_dash["C4"].border = thin_border
    ws_dash["C4"].alignment = center_align
    
    dv = DataValidation(type="list", formula1='"Jan-2020,Feb-2020,Mar-2020"', allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C4"])
    
    # Section Header
    ws_dash.merge_cells("B6:L6")
    ws_dash["B6"] = "Working Capital & Profitability Efficiency"
    for row in ws_dash["B6:L6"]:
        for cell in row:
            cell.fill = header_fill
            cell.border = thin_border
    ws_dash["B6"].font = header_font
    ws_dash["B6"].alignment = center_align
    
    # Helper to construct a KPI Card
    def create_kpi_card(start_col, title_text, formula, target_text, num_format="0"):
        c1 = get_column_letter(start_col)
        c2 = get_column_letter(start_col + 2)
        
        header_range = f"{c1}8:{c2}8"
        value_range = f"{c1}9:{c2}9"
        footer_range = f"{c1}10:{c2}10"
        
        ws_dash.merge_cells(header_range)
        ws_dash.merge_cells(value_range)
        ws_dash.merge_cells(footer_range)
        
        ws_dash[f"{c1}8"] = title_text
        ws_dash[f"{c1}9"] = formula
        ws_dash[f"{c1}10"] = target_text
        
        # Apply borders and backgrounds across merged ranges
        for row in ws_dash[header_range]:
            for cell in row:
                cell.border = thin_border
                cell.fill = card_header_fill
        for row in ws_dash[value_range]:
            for cell in row:
                cell.border = thin_border
        for row in ws_dash[footer_range]:
            for cell in row:
                cell.border = thin_border
                
        # Primary cell typography
        ws_dash[f"{c1}8"].font = card_header_font
        ws_dash[f"{c1}8"].alignment = center_align
        
        ws_dash[f"{c1}9"].font = Font(size=24, bold=True)
        ws_dash[f"{c1}9"].alignment = center_align
        ws_dash[f"{c1}9"].number_format = num_format
        
        ws_dash[f"{c1}10"].font = card_footer_font
        ws_dash[f"{c1}10"].alignment = center_align
        
        return value_range

    # Build KPI Cards
    dso_range = create_kpi_card(
        2, 
        "DSO (Days Sales Outstanding)", 
        "=INDEX(Data!$B$2:$D$2, MATCH($C$4, Data!$B$1:$D$1, 0))",
        "Target: < 45 Days"
    )
    
    dpo_range = create_kpi_card(
        6, 
        "DPO (Days Payables Outstanding)", 
        "=INDEX(Data!$B$3:$D$3, MATCH($C$4, Data!$B$1:$D$1, 0))",
        "Target: > 90 Days"
    )
    
    gm_range = create_kpi_card(
        10, 
        "Gross Margin %", 
        "=INDEX(Data!$B$4:$D$4, MATCH($C$4, Data!$B$1:$D$1, 0))",
        "Target: > 30%",
        num_format="0%"
    )
    
    # Apply Semantic Conditional Formatting
    # DSO: Lower is better
    ws_dash.conditional_formatting.add(dso_range, CellIsRule(operator='lessThan', formula=['45'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add(dso_range, CellIsRule(operator='greaterThanOrEqual', formula=['45'], fill=red_fill, font=red_font))
    
    # DPO: Higher is better (holding onto cash longer)
    ws_dash.conditional_formatting.add(dpo_range, CellIsRule(operator='greaterThan', formula=['90'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add(dpo_range, CellIsRule(operator='lessThanOrEqual', formula=['90'], fill=red_fill, font=red_font))
    
    # Gross Margin: Higher is better
    ws_dash.conditional_formatting.add(gm_range, CellIsRule(operator='greaterThan', formula=['0.30'], fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add(gm_range, CellIsRule(operator='lessThanOrEqual', formula=['0.30'], fill=red_fill, font=red_font))
    
    # Set Column Layout
    ws_dash.column_dimensions['A'].width = 3
    for col in ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L']:
        ws_dash.column_dimensions[col].width = 12
    ws_dash.column_dimensions['E'].width = 3  # Gap between KPI 1 and 2
    ws_dash.column_dimensions['I'].width = 3  # Gap between KPI 2 and 3
```
```