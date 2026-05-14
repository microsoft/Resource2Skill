```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Tier KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Builds a modular 3-sheet architecture (Data, Staging, Dashboard) to separate raw data from metric calculations and presentation. Uses a Data Validation dropdown tied to `INDEX`/`MATCH` formulas to dynamically swap out the active month across multiple KPI cards, using `CellIsRule` conditional formatting to highlight performance against targets.
* **Applicability**: Best for executive summaries, monthly reporting packages, or any scenario where you need to distill complex time-series data into a clean, highly readable, interactive presentation layer.

### 2. Structural Breakdown

- **Data Layout**: 3 sheets. `Data` holds raw GL outputs. `Staging` calculates the specific metrics row-by-row (Actual, Target, Prior Month). `Dashboard` is a clean presentation grid (gridlines disabled).
- **Formula Logic**: `=INDEX(Staging!$B$2:$D$2, MATCH($C$5, Staging!$B$1:$D$1, 0))` used in each KPI value box to retrieve the correct metric based on the dropdown selector in `$C$5`.
- **Visual Design**: Gridlines off. Extra large fonts for KPI values (Size 24). Distinct solid color headers for sections and individual cards. Light grey borders to delineate cards.
- **Charts/Tables**: No native charts; relies on "big number" typography and color coding (green=good, red=bad).
- **Theme Hooks**: Uses `primary` for main section headers, `card_header` for individual KPI titles, `good_bg`/`good_text` for exceeding targets, and `bad_bg`/`bad_text` for missing targets.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup Theme
    themes = {
        "corporate_blue": {
            "primary": "2F5597",
            "primary_text": "FFFFFF",
            "card_header": "D9E1F2",
            "card_header_text": "000000",
            "good_bg": "C6EFCE",
            "good_text": "006100",
            "bad_bg": "FFC7CE",
            "bad_text": "9C0006",
        }
    }
    t = themes.get(theme, themes["corporate_blue"])

    # Basic reusable styles
    title_font = Font(name="Calibri", size=18, bold=True, color=t["primary_text"])
    section_font = Font(name="Calibri", size=14, bold=True, color=t["primary_text"])
    card_header_font = Font(name="Calibri", size=12, bold=True, color=t["card_header_text"])
    kpi_value_font = Font(name="Calibri", size=24, bold=True)
    label_font = Font(name="Calibri", size=11, color="595959")
    
    fill_primary = PatternFill(start_color=t["primary"], end_color=t["primary"], fill_type="solid")
    fill_card_header = PatternFill(start_color=t["card_header"], end_color=t["card_header"], fill_type="solid")
    
    border_thin = Border(
        left=Side(style='thin', color='BFBFBF'),
        right=Side(style='thin', color='BFBFBF'),
        top=Side(style='thin', color='BFBFBF'),
        bottom=Side(style='thin', color='BFBFBF')
    )
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # 2. Setup Architecture (3 Sheets)
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
        
    ws_data = wb.create_sheet("Data")
    ws_staging = wb.create_sheet("Staging")
    ws_dash = wb.create_sheet("Dashboard")

    # 3. Populate Data Sheet
    data_rows = [
        ["Metric", "Jan-20", "Feb-20", "Mar-20"],
        ["Revenue", 1500000, 1590000, 1685400],
        ["COGS", 900000, 954000, 1030320],
        ["Receivables", 2800000, 2940000, 3087000],
        ["Payables", 3100000, 3255000, 3417750]
    ]
    for row in data_rows:
        ws_data.append(row)
        
    # 4. Populate Staging Sheet (Metrics calculated from Data)
    staging_rows = [
        ["Metric", "Jan-20", "Feb-20", "Mar-20"],
        ["DSO Actual", 56, 54, 55],
        ["DSO Target", 45, 45, 45],
        ["DSO Prior Month", 58, 56, 54],
        ["DPO Actual", 103, 100, 99],
        ["DPO Target", 90, 90, 90],
        ["DPO Prior Month", 107, 103, 100],
        ["Gross Margin Actual", 0.40, 0.40, 0.38],
        ["Gross Margin Target", 0.38, 0.38, 0.38],
        ["Gross Margin Prior", 0.41, 0.40, 0.40]
    ]
    for row in staging_rows:
        ws_staging.append(row)

    # 5. Build Dashboard Presentation Layer
    ws_dash.sheet_view.showGridLines = False
    
    # Grid proportions
    cols = {'A': 2, 'B': 22, 'C': 15, 'D': 2, 'E': 22, 'F': 15, 'G': 2}
    for col, width in cols.items():
        ws_dash.column_dimensions[col].width = width

    # Dashboard Title
    ws_dash.merge_cells('B2:F3')
    ws_dash['B2'] = title
    ws_dash['B2'].font = title_font
    ws_dash['B2'].fill = fill_primary
    ws_dash['B2'].alignment = align_center

    # Month Dropdown Selector
    ws_dash['B5'] = "For the month of:"
    ws_dash['B5'].font = Font(name="Calibri", size=12, bold=True)
    ws_dash['B5'].alignment = align_right
    
    ws_dash['C5'] = "Feb-20"  # Default
    ws_dash['C5'].font = Font(name="Calibri", size=12, bold=True)
    ws_dash['C5'].alignment = align_center
    ws_dash['C5'].border = border_thin
    ws_dash['C5'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # subtle highlight

    # Bind Validation
    dv = DataValidation(type="list", formula1="Staging!$B$1:$D$1", allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash['C5'])

    # Reusable function to stamp a KPI Card onto the grid
    def render_kpi_card(start_col, start_row, title_text, row_offset, number_format, lower_is_better=True):
        # Header
        header_cell = ws_dash.cell(row=start_row, column=start_col)
        ws_dash.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col+1)
        header_cell.value = title_text
        header_cell.font = card_header_font
        header_cell.fill = fill_card_header
        header_cell.alignment = align_center
        
        # Apply borders to both cells in merge
        header_cell.border = border_thin
        ws_dash.cell(row=start_row, column=start_col+1).border = border_thin

        # Big Value (Dynamic Index/Match)
        val_row = start_row + 1
        val_cell = ws_dash.cell(row=val_row, column=start_col)
        ws_dash.merge_cells(start_row=val_row, start_column=start_col, end_row=val_row, end_column=start_col+1)
        
        val_cell.value = f'=INDEX(Staging!$B${row_offset}:$D${row_offset}, MATCH($C$5, Staging!$B$1:$D$1, 0))'
        val_cell.font = kpi_value_font
        val_cell.alignment = align_center
        val_cell.number_format = number_format
        val_cell.border = border_thin
        ws_dash.cell(row=val_row, column=start_col+1).border = border_thin

        # Target 
        sub_row = start_row + 2
        ws_dash.cell(row=sub_row, column=start_col, value="Vs. Target:").font = label_font
        ws_dash.cell(row=sub_row, column=start_col).alignment = align_left
        ws_dash.cell(row=sub_row, column=start_col).border = border_thin
        
        tgt_cell = ws_dash.cell(row=sub_row, column=start_col+1)
        tgt_cell.value = f'=INDEX(Staging!$B${row_offset+1}:$D${row_offset+1}, MATCH($C$5, Staging!$B$1:$D$1, 0))'
        tgt_cell.font = label_font
        tgt_cell.alignment = align_right
        tgt_cell.number_format = number_format
        tgt_cell.border = border_thin

        # Prior Month
        ws_dash.cell(row=sub_row+1, column=start_col, value="Vs. Prior Month:").font = label_font
        ws_dash.cell(row=sub_row+1, column=start_col).alignment = align_left
        ws_dash.cell(row=sub_row+1, column=start_col).border = border_thin
        
        prior_cell = ws_dash.cell(row=sub_row+1, column=start_col+1)
        prior_cell.value = f'=INDEX(Staging!$B${row_offset+2}:$D${row_offset+2}, MATCH($C$5, Staging!$B$1:$D$1, 0))'
        prior_cell.font = label_font
        prior_cell.alignment = align_right
        prior_cell.number_format = number_format
        prior_cell.border = border_thin

        # Conditional Formatting based on Target
        green_fill = PatternFill(start_color=t["good_bg"], end_color=t["good_bg"], fill_type="solid")
        green_font = Font(color=t["good_text"], size=24, bold=True)
        red_fill = PatternFill(start_color=t["bad_bg"], end_color=t["bad_bg"], fill_type="solid")
        red_font = Font(color=t["bad_text"], size=24, bold=True)

        tgt_coord = f"${tgt_cell.column_letter}${tgt_cell.row}"
        val_coord = val_cell.coordinate

        if lower_is_better:
            ws_dash.conditional_formatting.add(val_coord, CellIsRule(operator='lessThanOrEqual', formula=[tgt_coord], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_coord, CellIsRule(operator='greaterThan', formula=[tgt_coord], fill=red_fill, font=red_font))
        else:
            ws_dash.conditional_formatting.add(val_coord, CellIsRule(operator='greaterThanOrEqual', formula=[tgt_coord], fill=green_fill, font=green_font))
            ws_dash.conditional_formatting.add(val_coord, CellIsRule(operator='lessThan', formula=[tgt_coord], fill=red_fill, font=red_font))

    # Section 1: Working Capital
    ws_dash.merge_cells('B7:F7')
    ws_dash['B7'] = "Working Capital Efficiency"
    ws_dash['B7'].font = section_font
    ws_dash['B7'].fill = fill_primary
    ws_dash['B7'].alignment = align_center

    render_kpi_card(start_col=2, start_row=9, title_text="DSO (Days Sales Outstanding)", row_offset=2, number_format="0", lower_is_better=True)
    render_kpi_card(start_col=5, start_row=9, title_text="DPO (Days Payables Outstanding)", row_offset=5, number_format="0", lower_is_better=False)

    # Section 2: Sales
    ws_dash.merge_cells('B15:F15')
    ws_dash['B15'] = "Sales KPIs"
    ws_dash['B15'].font = section_font
    ws_dash['B15'].fill = fill_primary
    ws_dash['B15'].alignment = align_center

    render_kpi_card(start_col=2, start_row=17, title_text="Gross Margin", row_offset=8, number_format="0%", lower_is_better=False)
```
```