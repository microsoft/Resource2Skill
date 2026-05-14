### 1. High-level Skill Pattern Extraction

> **Skill Name**: Financial Model Format Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Sets up a classic financial model layout with standard Wall Street conventions: disabled gridlines, narrow column A as a spacer, semantic font colors (blue for hardcoded inputs, black for calculations), and row grouping for collapsible sections.
* **Applicability**: Ideal for standardizing P&L statements, DCF models, and assumption schedules where clear distinction between inputs and outputs is required.

### 2. Structural Breakdown

- **Data Layout**: Column A is narrowed (width 2) as a visual spacer. Column B contains wide line-item labels. Columns C onwards contain time-series data (years). Row dimensions are grouped to allow collapsing assumption sections.
- **Formula Logic**: (Demonstrated via dummy calculations) In practice, calculations use relative/anchored references, while inputs are static values.
- **Visual Design**: Gridlines are disabled for a clean look. Time headers are bolded, centered, and have a bottom border. Inputs use blue fonts (`#0000FF`) to indicate they are editable, while formulas remain black. Totals feature top and bottom borders.
- **Charts/Tables**: Standard unstructured ranges (not Excel Tables) to allow maximum formatting flexibility and formula copying across rows.
- **Theme Hooks**: While this uses standard financial color codes (Blue/Black), it accepts a `theme` parameter to allow integration with larger reporting workbooks.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a standard financial model worksheet applying classic IB formatting conventions.
    """
    ws = wb.create_sheet(sheet_name)
    
    # 1. Remove Gridlines for clean presentation
    ws.sheet_view.showGridLines = False
    
    # Standard Wall Street color coding (typically overrides standard themes)
    color_input = "0000FF" # Blue for hardcoded inputs
    color_calc = "000000"  # Black for formulas/calculations
    
    font_title = Font(size=16, bold=True, color=color_calc)
    font_header = Font(bold=True, color=color_calc)
    font_input = Font(color=color_input)
    font_calc = Font(color=color_calc)
    
    border_bottom = Border(bottom=Side(style='thin'))
    border_top_bottom = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    
    # 2. Adjust Column Widths
    ws.column_dimensions['A'].width = 2   # Spacer column
    ws.column_dimensions['B'].width = 25  # Line item labels
    for col in range(3, 10):
        ws.column_dimensions[get_column_letter(col)].width = 12
        
    # Title
    ws['B2'] = title
    ws['B2'].font = font_title
    
    # 3. Time Series Headers
    years = [2023, 2024, 2025, 2026, 2027, 2028, 2029]
    for i, year in enumerate(years):
        col_letter = get_column_letter(i + 3)
        cell = ws[f'{col_letter}4']
        cell.value = year
        cell.font = font_header
        cell.alignment = Alignment(horizontal='center')
        cell.border = border_bottom
        
    # 4. Section: Assumptions (Inputs in Blue)
    ws['B5'] = "Assumptions"
    ws['B5'].font = font_header
    
    assumptions = [
        ("Revenue Growth", 0.15, '0.0%'),
        ("EBIT Margin", 0.20, '0.0%'),
        ("Tax Rate", 0.25, '0.0%')
    ]
    
    for row_idx, (label, val, fmt) in enumerate(assumptions, start=6):
        ws[f'B{row_idx}'] = label
        for col_idx in range(3, 10):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.value = val
            cell.number_format = fmt
            cell.font = font_input  # Semantic blue font
            
    # Group Assumptions rows for collapsibility
    ws.row_dimensions.group(6, 8, hidden=False)
            
    # 5. Section: Income Statement (Calculations in Black)
    ws['B10'] = "Income Statement"
    ws['B10'].font = font_header
    
    base_rev = 100000
    for col_idx in range(3, 10):
        # Dummy calculations simulating formula results propagating across columns
        rev = base_rev * (1 + 0.15)**(col_idx - 3)
        ebit = rev * 0.20
        taxes = ebit * 0.25
        net_income = ebit - taxes
        
        # Revenue
        ws.cell(row=11, column=2, value="Revenue")
        c_rev = ws.cell(row=11, column=col_idx, value=rev)
        c_rev.number_format = '#,##0'
        c_rev.font = font_calc
        
        # EBIT
        ws.cell(row=12, column=2, value="EBIT")
        c_ebit = ws.cell(row=12, column=col_idx, value=ebit)
        c_ebit.number_format = '#,##0'
        c_ebit.font = font_calc
        
        # Taxes
        ws.cell(row=13, column=2, value="Taxes")
        c_tax = ws.cell(row=13, column=col_idx, value=taxes)
        c_tax.number_format = '#,##0'
        c_tax.font = font_calc
        
        # Net Income Total
        ws.cell(row=14, column=2, value="Net Income")
        c_ni = ws.cell(row=14, column=col_idx, value=net_income)
        c_ni.number_format = '#,##0'
        c_ni.font = font_calc
        c_ni.border = border_top_bottom
```