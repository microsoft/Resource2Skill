```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Tier Dynamic KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Separates the workbook into 3 distinct sheets: Data (raw inputs), Staging (KPI calculations by period), and Dashboard (presentation). Uses an interactive Data Validation dropdown tied to `VLOOKUP` and `MATCH` formulas to dynamically render KPIs with conditional big-font status formatting.
* **Applicability**: Best used for executive reports tracking multiple performance metrics over time, where you want to allow the user to easily toggle the reporting period without cluttering the visual layer with underlying data.

### 2. Structural Breakdown

- **Data Layout**: 
  - `1) Data`: Appended raw extracts (e.g., Accounts Receivable, COGS).
  - `2) Staging`: Row-wise KPIs (DSO, DPO, Gross Margin) with columns acting as time periods, plus a static Target column.
  - `3) Dashboard`: Presentation layer with hidden gridlines, group headers, and modular KPI "cards" occupying a 2x3 grid.
- **Formula Logic**: `=VLOOKUP(metric_name, Staging_Range, MATCH(selected_month, Staging_Headers, 0), FALSE)` retrieves dynamic values based on the month dropdown. 
- **Visual Design**: Uses merged cells for KPI group headers with solid fills. Main numbers use a prominent 24pt font and feature dynamic background fills (green/red) leveraging conditional formatting rules against the adjacent target value.
- **Charts/Tables**: Standalone big-number cells instead of charts.
- **Theme Hooks**: Hardcoded fallback values (`4F81BD` for headers, `DCE6F1` for metric titles) are included, but in a full system, these should map to `theme.primary_bg`, `theme.secondary_bg`, and standard success/danger semantic colors.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup 3-Tier Architecture
    ws_data = wb.active
    ws_data.title = "1) Data"
    ws_staging = wb.create_sheet("2) Staging")
    ws_dash = wb.create_sheet("3) Dashboard")
    
    # --- Tier 1: Data Sheet ---
    data_headers = ["Category", "Jan-20", "Feb-20", "Mar-20"]
    data_rows = [
        ["Account Receivables", 2800000, 2940000, 3087000],
        ["Credit Sales", 1500000, 1590000, 1685000],
        ["Accounts Payable", 3100000, 3255000, 3417000],
        ["COGS", 900000, 954000, 1030000],
        ["Gross Profit", 600000, 636000, 655000]
    ]
    ws_data.append(data_headers)
    for row in data_rows:
        ws_data.append(row)
        
    # --- Tier 2: Staging Sheet ---
    staging_headers = ["KPI", "Target", "Jan-20", "Feb-20", "Mar-20"]
    staging_rows = [
        ["DSO", 45, 58, 54, 57],
        ["DPO", 90, 107, 99, 103],
        ["Gross Margin", 0.38, 0.40, 0.40, 0.38]
    ]
    ws_staging.append(staging_headers)
    for row in staging_rows:
        ws_staging.append(row)
        
    # --- Tier 3: Dashboard Sheet ---
    ws_dash.sheet_view.showGridLines = False
    
    # Month Selector
    ws_dash["B4"] = "For the month of"
    ws_dash["B4"].font = Font(bold=True)
    ws_dash["C4"] = "Feb-20"
    
    dv = DataValidation(type="list", formula1="='2) Staging'!$C$1:$E$1", allow_blank=False)
    ws_dash.add_data_validation(dv)
    dv.add(ws_dash["C4"])
    ws_dash["C4"].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    ws_dash["C4"].border = Border(bottom=Side(style="thin"))
    
    # Theme/Styling Setup
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=14)
    kpi_title_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    kpi_title_font = Font(bold=True, size=12)
    val_font = Font(bold=True, size=24)
    
    good_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    bad_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    
    def render_kpi_card(ws, start_col_idx, start_row, kpi_name, format_code, is_lower_better=True):
        col_letter1 = get_column_letter(start_col_idx)
        col_letter2 = get_column_letter(start_col_idx + 1)
        
        # 1. KPI Title Cell
        ws.merge_cells(f"{col_letter1}{start_row}:{col_letter2}{start_row}")
        title_cell = ws[f"{col_letter1}{start_row}"]
        title_cell.value = kpi_name
        title_cell.fill = kpi_title_fill
        title_cell.font = kpi_title_font
        title_cell.alignment = Alignment(horizontal="center")
        
        # 2. Main KPI Value (Dynamic via Dropdown)
        val_cell_ref = f"{col_letter1}{start_row + 1}"
        ws.merge_cells(f"{col_letter1}{start_row + 1}:{col_letter2}{start_row + 1}")
        val_cell = ws[val_cell_ref]
        # Core dynamic VLOOKUP/MATCH formula linked to staging
        val_cell.value = f'=VLOOKUP("{kpi_name}", \'2) Staging\'!$A$1:$E$10, MATCH($C$4, \'2) Staging\'!$A$1:$E$1, 0), FALSE)'
        val_cell.font = val_font
        val_cell.alignment = Alignment(horizontal="center")
        val_cell.number_format = format_code
        
        # 3. Static Target Reference
        ws[f"{col_letter1}{start_row + 2}"] = "Vs. Target"
        ws[f"{col_letter1}{start_row + 2}"].font = Font(size=10, color="595959")
        target_cell_ref = f"{col_letter2}{start_row + 2}"
        target_cell = ws[target_cell_ref]
        target_cell.value = f'=VLOOKUP("{kpi_name}", \'2) Staging\'!$A$1:$E$10, 2, FALSE)'
        target_cell.number_format = format_code
        target_cell.font = Font(size=10, bold=True)
        target_cell.alignment = Alignment(horizontal="right")
        
        # 4. Target-driven Conditional Formatting
        target_val_ref = f"${col_letter2}${start_row + 2}"
        if is_lower_better:
            ws.conditional_formatting.add(val_cell_ref, CellIsRule(operator='lessThanOrEqual', formula=[target_val_ref], fill=good_fill))
            ws.conditional_formatting.add(val_cell_ref, CellIsRule(operator='greaterThan', formula=[target_val_ref], fill=bad_fill))
        else:
            ws.conditional_formatting.add(val_cell_ref, CellIsRule(operator='greaterThanOrEqual', formula=[target_val_ref], fill=good_fill))
            ws.conditional_formatting.add(val_cell_ref, CellIsRule(operator='lessThan', formula=[target_val_ref], fill=bad_fill))
            
    # --- Layout Construction ---
    
    # Group 1: Working Capital Efficiency
    ws_dash.merge_cells("B6:E6")
    ws_dash["B6"] = "Working Capital Efficiency"
    ws_dash["B6"].fill = header_fill
    ws_dash["B6"].font = header_font
    ws_dash["B6"].alignment = Alignment(horizontal="center")
    
    render_kpi_card(ws_dash, 2, 7, "DSO", "0", is_lower_better=True)
    render_kpi_card(ws_dash, 4, 7, "DPO", "0", is_lower_better=False)
    
    # Group 2: Sales KPIs
    ws_dash.merge_cells("B11:E11")
    ws_dash["B11"] = "Sales KPIs"
    ws_dash["B11"].fill = header_fill
    ws_dash["B11"].font = header_font
    ws_dash["B11"].alignment = Alignment(horizontal="center")
    
    render_kpi_card(ws_dash, 2, 12, "Gross Margin", "0%", is_lower_better=False)
    
    # General Sizing
    ws_dash.column_dimensions['A'].width = 3
    for col in ['B', 'C', 'D', 'E']:
        ws_dash.column_dimensions[col].width = 15
```
```