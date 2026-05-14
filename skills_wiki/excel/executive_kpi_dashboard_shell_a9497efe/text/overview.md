### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive KPI Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Generates a modular dashboard layout using wide merged regions for large typography, standardizing metrics into 4-column "KPI Cards". Applies dynamic `CellIsRule` conditional formatting to the primary values, evaluating them against their adjacent target cells to color-code performance (green/red) based on target directionality.
* **Applicability**: Ideal for high-level financial, operational, or sales summary sheets. Best used when tracking top-tier metrics across time periods where executives need immediate, glanceable status indicators.

### 2. Structural Breakdown

- **Data Layout**: Utilizes a grid system where each KPI card spans 4 columns and 3 rows. A spacer column separates horizontally adjacent cards.
- **Formula Logic**: (Mocked dynamically in layout) Primary values are evaluated directly against the localized "Target" cell within the same card.
- **Visual Design**: 
  - Section headers use a dark background with bold white text.
  - KPI Card values use highly scaled fonts (size 24+).
  - Positive performance triggers light green fills and dark green text; negative performance triggers pink fills and dark red text.
- **Charts/Tables**: Replaces traditional charts with high-contrast alphanumeric status cards.
- **Theme Hooks**: Utilizes `header_bg` and `header_fg` for section dividers, and standard semantic colors (good/bad) for conditional formatting.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

def render_sheet(wb, sheet_name: str, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a standalone KPI Dashboard with modular KPI cards and semantic conditional formatting.
    """
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)

    # Basic Theme Fallback
    themes = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF", "card_bg": "E7E6E6"},
        "executive_gray": {"header_bg": "404040", "header_fg": "FFFFFF", "card_bg": "F2F2F2"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # Semantic Colors for CF
    fill_good = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    font_good = Font(color="006100", size=24, bold=True)
    fill_bad = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    font_bad = Font(color="9C0006", size=24, bold=True)

    # Border style
    thin = Side(border_style="thin", color="BFBFBF")

    # Set Column Widths for the Card Grid
    col_widths = {
        "A": 2, "B": 14, "C": 12, "D": 16, "E": 12, # Card 1
        "F": 3,                                     # Spacer
        "G": 14, "H": 12, "I": 16, "J": 12          # Card 2
    }
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Dashboard Title
    ws["B2"] = "For the month of:"
    ws["B2"].font = Font(bold=True)
    ws["B2"].alignment = Alignment(horizontal="right", vertical="center")
    
    # Month Dropdown
    ws["C2"] = "Jul-20"
    ws["C2"].fill = PatternFill("solid", fgColor="FFF2CC")
    ws["C2"].border = Border(top=thin, left=thin, right=thin, bottom=thin)
    ws["C2"].alignment = Alignment(horizontal="center", vertical="center")
    
    dv = DataValidation(type="list", formula1='"Jan-20,Feb-20,Mar-20,Apr-20,May-20,Jun-20,Jul-20"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("C2")

    def draw_section_header(row, text):
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=10)
        cell = ws.cell(row=row, column=2, value=text)
        cell.fill = PatternFill("solid", fgColor=palette["header_bg"])
        cell.font = Font(color=palette["header_fg"], bold=True, size=14)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row].height = 25

    def draw_kpi_card(r, c, title, val, target, prior, num_format, good_direction="down"):
        # Card Title
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+3)
        t_cell = ws.cell(row=r, column=c, value=title)
        t_cell.fill = PatternFill("solid", fgColor=palette["card_bg"])
        t_cell.font = Font(bold=True, size=11)
        t_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[r].height = 20

        # Main Value
        ws.merge_cells(start_row=r+1, start_column=c, end_row=r+1, end_column=c+3)
        v_cell = ws.cell(row=r+1, column=c, value=val)
        v_cell.font = Font(size=24, bold=True)
        v_cell.alignment = Alignment(horizontal="center", vertical="center")
        v_cell.number_format = num_format
        ws.row_dimensions[r+1].height = 40

        # Sub-metrics
        ws.cell(row=r+2, column=c, value="Vs. Target").font = Font(bold=True, size=9)
        tgt_cell = ws.cell(row=r+2, column=c+1, value=target)
        tgt_cell.number_format = num_format
        
        ws.cell(row=r+2, column=c+2, value="Vs. Prior Month").font = Font(bold=True, size=9)
        p_cell = ws.cell(row=r+2, column=c+3, value=prior)
        p_cell.number_format = num_format
        ws.row_dimensions[r+2].height = 18

        # Borders & Alignments
        for row in range(r, r+3):
            for col in range(c, c+4):
                ws.cell(row=row, column=col).border = Border(top=thin, left=thin, right=thin, bottom=thin)
                if row == r+2:
                    ws.cell(row=row, column=col).alignment = Alignment(horizontal="center", vertical="center")

        # Conditional Formatting based on adjacent Target Cell
        target_ref = f"{tgt_cell.column_letter}{tgt_cell.row}"
        
        if good_direction == "down": # Lower is better (e.g., DSO, Costs)
            rule_green = CellIsRule(operator='lessThan', formula=[target_ref], fill=fill_good, font=font_good)
            rule_red = CellIsRule(operator='greaterThanOrEqual', formula=[target_ref], fill=fill_bad, font=font_bad)
        else: # Higher is better (e.g., Margins, Revenue)
            rule_green = CellIsRule(operator='greaterThanOrEqual', formula=[target_ref], fill=fill_good, font=font_good)
            rule_red = CellIsRule(operator='lessThan', formula=[target_ref], fill=fill_bad, font=font_bad)

        val_coord = f"{v_cell.column_letter}{v_cell.row}"
        ws.conditional_formatting.add(val_coord, rule_green)
        ws.conditional_formatting.add(val_coord, rule_red)

    # --- Render Dashboard Sections ---
    
    # Section 1: Working Capital
    draw_section_header(4, "Working Capital Efficiency")
    draw_kpi_card(5, 2, "DSO (Days Sales Outstanding)", 41, 45, 53, "0", good_direction="down")
    draw_kpi_card(5, 7, "DPO (Days Payables Outstanding)", 90, 90, 89, "0", good_direction="up")

    # Section 2: Sales
    draw_section_header(9, "Sales KPIs")
    draw_kpi_card(10, 2, "CAC (Customer Acquisition Cost)", 17725, 15000, 18236, "$#,##0", good_direction="down")
    draw_kpi_card(10, 7, "Gross Margin", 0.26, 0.38, 0.33, "0%", good_direction="up")
    
    # Clean Gridlines
    ws.sheet_view.showGridLines = False
```