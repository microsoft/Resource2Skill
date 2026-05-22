```markdown
### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Analysis Model

* **Tier**: sheet_shell
* **Core Mechanism**: Construct a live financial model driven by a scenario selector cell. The `CHOOSE` function links a "Live Assumptions" block to distinct scenario data blocks (e.g., Optimistic vs. Pessimistic). A Data Validation dropdown controls the active scenario index, updating the entire downstream model dynamically.
* **Applicability**: Highly useful for financial modeling, budgeting, forecasting, and sensitivity analysis where multiple discrete scenarios need to be evaluated without changing the core model calculations. Follows the financial modeling convention of blue fonts for hardcoded inputs and black fonts for dynamic formulas.

### 2. Structural Breakdown

- **Data Layout**: 
  - Top section: Core Financial Model calculations.
  - Middle section: "Live Assumptions" acting as the variable router.
  - Bottom sections: Hardcoded scenario blocks (Scenario 1, Scenario 2).
- **Formula Logic**: `=CHOOSE($F$2, B16, B22)` routes the correct scenario data into the Live Assumptions based on the toggle index. Downstream metrics multiply values strictly from the Live block.
- **Visual Design**: Themed header backgrounds. Formula outputs use black text, while hard-coded scenario inputs use blue text (`#0000FF`). The scenario selector is visually offset with a background fill and a border.
- **Charts/Tables**: Standard spreadsheet projection spanning multiple forward years, utilizing specific accounting number formats (`$#,##0.00` and `#,##0`).
- **Theme Hooks**: Uses `header_bg`, `header_fg`, and `accent` to style the shell cleanly.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Hardcoded theme for standalone execution (fallbacks)
    theme_colors = {
        "header_bg": "1F4E78", 
        "accent": "D9E1F2",
        "input_fg": "0000FF",  # Financial modeling standard: blue for hardcoded inputs
        "formula_fg": "000000" # Black for formulas
    }
    
    # 1. Report Header & Scenario Toggle
    ws["A1"] = title
    ws["A1"].font = Font(size=14, bold=True, color=theme_colors["header_bg"])
    
    ws["E2"] = "Active Scenario:"
    ws["E2"].font = Font(bold=True, color=theme_colors["header_bg"])
    ws["E2"].alignment = Alignment(horizontal="right")
    
    scen_cell = ws["F2"]
    scen_cell.value = 1
    scen_cell.font = Font(bold=True, color=theme_colors["input_fg"])
    scen_cell.fill = PatternFill(start_color=theme_colors["accent"], end_color=theme_colors["accent"], fill_type="solid")
    scen_cell.alignment = Alignment(horizontal="center")
    scen_cell.border = Border(
        left=Side(style="thin", color="000000"), right=Side(style="thin", color="000000"),
        top=Side(style="thin", color="000000"), bottom=Side(style="thin", color="000000")
    )
    
    dv = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(scen_cell)
    
    years = ["Year 1", "Year 2", "Year 3"]
    cols = ["B", "C", "D"]
    
    # Helper for rendering distinct section headers
    def render_headers(start_row, section_name):
        ws[f"A{start_row}"] = section_name
        ws[f"A{start_row}"].font = Font(bold=True, color=theme_colors["header_bg"])
        for c, yr in zip(cols, years):
            cell = ws[f"{c}{start_row}"]
            cell.value = yr
            cell.font = Font(bold=True, color=theme_colors["header_bg"])
            cell.border = Border(bottom=Side(style="thin", color=theme_colors["header_bg"]))
            cell.alignment = Alignment(horizontal="right")

    # 2. Financial Model (Driven strictly by Live Assumptions)
    render_headers(4, "Financial Model")
    
    ws["A5"] = "Revenue"
    ws["A6"] = "COGS"
    ws["A7"] = "Gross Profit"
    
    for c in cols:
        ws[f"{c}5"] = f"={c}10*{c}11"  # Volume * Price
        ws[f"{c}6"] = f"={c}10*{c}12"  # Volume * Unit Cost
        ws[f"{c}7"] = f"={c}5-{c}6"    # Revenue - COGS
        
        for r in [5, 6, 7]:
            ws[f"{c}{r}"].number_format = "$#,##0"
            ws[f"{c}{r}"].font = Font(color=theme_colors["formula_fg"])
            
        # Top border for profit sum row
        ws[f"{c}7"].border = Border(top=Side(style="thin", color="000000"))

    # 3. Live Assumptions (Dynamic CHOOSE formulas routing the data)
    render_headers(9, "Live Assumptions")
    assumptions = ["Volume (Orders)", "Price (AOV)", "Unit Cost (COGS)"]
    
    for i, label in enumerate(assumptions, start=10):
        ws[f"A{i}"] = label
        for c in cols:
            s1_row = i + 6  # Offset to Scenario 1 row
            s2_row = i + 12 # Offset to Scenario 2 row
            
            # The core mechanism: CHOOSE switches between S1 and S2 blocks based on cell F2
            ws[f"{c}{i}"] = f"=CHOOSE($F$2, {c}{s1_row}, {c}{s2_row})"
            ws[f"{c}{i}"].font = Font(color=theme_colors["formula_fg"])
            
            if i == 10:
                ws[f"{c}{i}"].number_format = "#,##0"
            else:
                ws[f"{c}{i}"].number_format = "$#,##0.00"

    # 4. Scenario 1 (Optimistic Inputs)
    render_headers(15, "Scenario 1: Optimistic")
    s1_data = [
        [1000, 1200, 1500],    # Volume
        [50.00, 50.00, 52.00], # Price
        [20.00, 19.00, 18.00]  # Unit Cost
    ]
    
    for r_idx, row_data in enumerate(s1_data, start=16):
        ws[f"A{r_idx}"] = assumptions[r_idx - 16]
        for c_idx, val in enumerate(row_data):
            cell = ws[f"{cols[c_idx]}{r_idx}"]
            cell.value = val
            cell.font = Font(color=theme_colors["input_fg"]) # Standard convention: Blue = hardcoded
            cell.number_format = "#,##0" if r_idx == 16 else "$#,##0.00"

    # 5. Scenario 2 (Pessimistic Inputs)
    render_headers(21, "Scenario 2: Pessimistic")
    s2_data = [
        [800, 850, 900],       # Volume
        [45.00, 45.00, 45.00], # Price
        [22.00, 23.00, 24.00]  # Unit Cost
    ]
    
    for r_idx, row_data in enumerate(s2_data, start=22):
        ws[f"A{r_idx}"] = assumptions[r_idx - 22]
        for c_idx, val in enumerate(row_data):
            cell = ws[f"{cols[c_idx]}{r_idx}"]
            cell.value = val
            cell.font = Font(color=theme_colors["input_fg"])
            cell.number_format = "#,##0" if r_idx == 22 else "$#,##0.00"

    # Polish column sizing
    ws.column_dimensions["A"].width = 25
    for c in cols:
        ws.column_dimensions[c].width = 14
    ws.column_dimensions["E"].width = 16
```
```