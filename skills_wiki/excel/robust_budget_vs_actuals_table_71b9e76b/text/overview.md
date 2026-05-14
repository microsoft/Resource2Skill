# Robust Budget vs Actuals Table

## Applicability

Essential for P&L reporting, departmental variance tracking, and monthly financial roll-forwards where empty or negative budget figures might otherwise break standard division formulas.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Robust Budget vs Actuals Table

* **Tier**: component
* **Core Mechanism**: Generates a standard BvA comparison table using dynamic cell references. Reverses the variance math for income vs. expenses so that "Good" outcomes are always positive and "Bad" outcomes are negative. Employs an `IFERROR(Variance / ABS(Budget), 0)` formula to prevent `#DIV/0!` errors on missing budgets and avoid misleading inverted signs when dealing with negative budgets.
* **Applicability**: Essential for P&L reporting, departmental variance tracking, and monthly financial roll-forwards where empty or negative budget figures might otherwise break standard division formulas.

### 2. Structural Breakdown

- **Data Layout**: 5 columns (`Category`, `Budget`, `Actual`, `Variance`, `Var %`). Rows iterate dynamically based on an ingested `data` list of dictionaries containing category names, figures, and an `is_expense` flag.
- **Formula Logic**: 
  - Variance (Income): `=Actual - Budget`
  - Variance (Expense): `=Budget - Actual`
  - Variance %: `=IFERROR(Variance / ABS(Budget), 0)`
- **Visual Design**: Themed solid background for the header row with white bold text. Data rows have thin bottom borders for readability.
- **Charts/Tables**: Standard grid layout with dynamic column width sizing.
- **Theme Hooks**: Uses `primary_color` and `primary_text` for headers, and standard red/green highlight tokens for conditional formatting on the percentage column.

### 3. Reproduction Code

```python
from openpyxl.utils import coordinate_to_tuple, get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule

# Fallback theme loader if standard helper is unavailable
try:
    from skills_library.excel._helpers import get_theme_palette
except ImportError:
    def get_theme_palette(theme: str):
        return {
            "primary_color": "4F81BD", 
            "primary_text": "FFFFFF", 
            "good_bg": "C6EFCE", 
            "good_text": "006100", 
            "bad_bg": "FFC7CE", 
            "bad_text": "9C0006",
            "border": "D9D9D9"
        }

def render(ws, anchor: str, *, data: list = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a Budget vs Actuals summary table with intelligent variance formulas.
    """
    if data is None:
        data = [
            {"category": "Revenue", "budget": 419829, "actual": 362649, "is_expense": False},
            {"category": "COGS", "budget": 8402, "actual": 73041, "is_expense": True},
            {"category": "Advertising & Marketing", "budget": 19381, "actual": 4658, "is_expense": True},
            {"category": "Software & Tech", "budget": 22337, "actual": 23949, "is_expense": True},
            {"category": "New Product Line", "budget": 0, "actual": 15000, "is_expense": False},
        ]
        
    start_row, start_col = coordinate_to_tuple(anchor)
    palette = get_theme_palette(theme)
    
    headers = ["Category", "Budget", "Actual", "Variance", "Var %"]
    
    header_fill = PatternFill(start_color=palette.get("primary_color", "4F81BD"), fill_type="solid")
    header_font = Font(color=palette.get("primary_text", "FFFFFF"), bold=True)
    thin_border = Border(bottom=Side(style='thin', color=palette.get("border", "D9D9D9")))
    
    # Render Headers
    for i, h in enumerate(headers):
        cell = ws.cell(row=start_row, column=start_col + i, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(start_col + i)].width = 18 if i == 0 else 14
        
    # Render Data Rows
    for r_idx, row_data in enumerate(data, start=1):
        curr_row = start_row + r_idx
        
        cat = row_data.get("category", "")
        bud = row_data.get("budget", 0)
        act = row_data.get("actual", 0)
        is_exp = row_data.get("is_expense", False)
        
        c_cat = ws.cell(row=curr_row, column=start_col, value=cat)
        c_bud = ws.cell(row=curr_row, column=start_col + 1, value=bud)
        c_act = ws.cell(row=curr_row, column=start_col + 2, value=act)
        
        c_bud.number_format = '"$"#,##0_)'
        c_act.number_format = '"$"#,##0_)'
        
        col_bud = get_column_letter(start_col + 1)
        col_act = get_column_letter(start_col + 2)
        
        # Good variance = positive. Bad variance = negative.
        if is_exp:
            var_formula = f"={col_bud}{curr_row}-{col_act}{curr_row}"
        else:
            var_formula = f"={col_act}{curr_row}-{col_bud}{curr_row}"
            
        c_var = ws.cell(row=curr_row, column=start_col + 3, value=var_formula)
        c_var.number_format = '"$"#,##0_)'
        
        # Safe divide using IFERROR and ABS() to prevent flipped logic on negative budgets
        col_var = get_column_letter(start_col + 3)
        var_pct_formula = f"=IFERROR({col_var}{curr_row}/ABS({col_bud}{curr_row}), 0)"
        
        c_pct = ws.cell(row=curr_row, column=start_col + 4, value=var_pct_formula)
        c_pct.number_format = '0.0%'
        
        for c in range(5):
            ws.cell(row=curr_row, column=start_col + c).border = thin_border

    # Conditional formatting for Var %
    first_pct = f"{get_column_letter(start_col + 4)}{start_row + 1}"
    last_pct = f"{get_column_letter(start_col + 4)}{start_row + len(data)}"
    pct_range = f"{first_pct}:{last_pct}"
    
    green_font = Font(color=palette.get("good_text", "006100"))
    green_fill = PatternFill(start_color=palette.get("good_bg", "C6EFCE"), fill_type="solid")
    red_font = Font(color=palette.get("bad_text", "9C0006"))
    red_fill = PatternFill(start_color=palette.get("bad_bg", "FFC7CE"), fill_type="solid")
    
    ws.conditional_formatting.add(pct_range, CellIsRule(operator='greaterThan', formula=['0'], font=green_font, fill=green_fill))
    ws.conditional_formatting.add(pct_range, CellIsRule(operator='lessThan', formula=['0'], font=red_font, fill=red_fill))
```