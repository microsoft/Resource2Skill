### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid KPI Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Lays out hierarchical KPI data into a dense, readable visual grid. Each KPI occupies a 4-column merged block featuring a 24pt metric value, flanked by smaller variance comparisons below it. Merged cells are styled dynamically via `FormulaRule` conditional formatting (comparing absolute cell references), tinting the background green or red based on performance vs target.
* **Applicability**: Perfect for executive summaries and top-level KPI tracking where the focus is on a few key metrics and their performance against targets in a single, clean view.

### 2. Structural Breakdown

- **Data Layout**: KPIs are arranged in a 3-column wrapping grid. Each KPI metric block takes 4 Excel columns, with 1 blank spacer column between blocks. Section headers merge across all 14 columns to anchor the sections.
- **Formula Logic**: Openpyxl conditional formatting `FormulaRule` uses absolute cell references (e.g., `formula=["$B$9<=$C$10"]`) so that the green/red fill applies uniformly across the entire merged cell block representing the KPI value.
- **Visual Design**: Gridlines are disabled. Section headers use theme colors, KPI names use a neutral dark gray background, and metric values use a very light gray default background that is overwritten by conditional formatting. Variance labels are right-aligned to sit flush against left-aligned variance values.
- **Charts/Tables**: N/A; purely cell-based dynamic typography and color visualization.
- **Theme Hooks**: Consumes the primary theme color for the main title and section header backgrounds.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "KPI Dashboard", theme: str = "corporate_blue", data: dict = None, **kwargs) -> None:
    """
    Renders a grid-based KPI Dashboard with conditionally formatted big-number metrics.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Default data matching the 3-across structural pattern
    if not data:
        data = {
            "month": "Jul-20",
            "sections": [
                {
                    "section": "Working Capital Efficiency",
                    "kpis": [
                        {"name": "DSO (Days Sales Outstanding)", "value": 41, "target": 45, "prior": 53, "lower_is_better": True},
                        {"name": "DPO (Days Payables)", "value": 90, "target": 90, "prior": 89, "lower_is_better": False},
                        {"name": "Non-Current AR %", "value": 0.12, "target": 0.03, "prior": 0.11, "lower_is_better": True, "format": "0%"}
                    ]
                },
                {
                    "section": "Sales KPIs",
                    "kpis": [
                        {"name": "CAC (Acquisition Cost)", "value": 17725, "target": 15000, "prior": 18236, "lower_is_better": True, "format": "$#,##0"},
                        {"name": "Sales vs. Budget %", "value": 1.27, "target": 1.00, "prior": 0.98, "lower_is_better": False, "format": "0%"},
                        {"name": "Gross Margin", "value": 0.26, "target": 0.38, "prior": 0.33, "lower_is_better": False, "format": "0%"}
                    ]
                }
            ]
        }
        
    # Theme handling
    theme_colors = {
        "corporate_blue": "4F81BD",
        "executive_dark": "333333",
        "vibrant_orange": "FF9900"
    }
    primary_color = theme_colors.get(theme, "4F81BD")
    
    # Pre-define styles
    section_fill = PatternFill("solid", fgColor=primary_color)
    header_fill = PatternFill("solid", fgColor="E7E6E6")
    neutral_fill = PatternFill("solid", fgColor="F2F2F2")
    good_fill = PatternFill("solid", fgColor="D9EAD3") # Light Green
    bad_fill = PatternFill("solid", fgColor="F4CCCC") # Light Red
    
    white_font = Font(color="FFFFFF", bold=True, size=14)
    kpi_name_font = Font(bold=True, color="333333")
    kpi_val_font = Font(size=24, bold=True, color="111111")
    label_font = Font(size=9, color="555555")
    val_font = Font(size=10, bold=True)
    
    center_align = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    
    # Configure precise column widths for the 3x grid (4 cols per KPI + 1 spacer)
    ws.column_dimensions['A'].width = 2
    for i in range(3):
        base = 2 + i * 5
        ws.column_dimensions[get_column_letter(base)].width = 14
        ws.column_dimensions[get_column_letter(base+1)].width = 10
        ws.column_dimensions[get_column_letter(base+2)].width = 16
        ws.column_dimensions[get_column_letter(base+3)].width = 10
        ws.column_dimensions[get_column_letter(base+4)].width = 2
        
    # Render Dashboard Title & Timeframe Selector
    ws.cell(row=2, column=2, value=title).font = Font(size=18, bold=True, color=primary_color)
    
    ws.cell(row=4, column=2, value="For the month of:").font = Font(bold=True)
    ws.cell(row=4, column=2).alignment = right_align
    
    month_cell = ws.cell(row=4, column=3, value=data.get("month", ""))
    month_cell.font = Font(bold=True)
    month_cell.alignment = left_align
    month_cell.fill = PatternFill("solid", fgColor="FFF2CC") # subtle drop-down highlight
    
    def style_range(row, start_col, end_col, fill, font=None, alignment=None):
        """Applies styles uniformly across a range so merged cells render cleanly in all viewers."""
        for col in range(start_col, end_col + 1):
            c = ws.cell(row=row, column=col)
            if fill: c.fill = fill
            if font: c.font = font
            if alignment: c.alignment = alignment
            
    row = 6
    for section in data.get("sections", []):
        # Anchor the Section Header across 14 columns
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=15)
        ws.cell(row=row, column=2, value=section["section"])
        style_range(row, 2, 15, fill=section_fill, font=white_font, alignment=center_align)
        row += 2
        
        kpis = section["kpis"]
        # Batch KPIs into groups of 3 to wrap down rows
        for i in range(0, len(kpis), 3):
            batch = kpis[i:i+3]
            
            for j, kpi in enumerate(batch):
                start_col = 2 + (j * 5)
                end_col = start_col + 3
                
                # 1. KPI Name Header
                ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
                ws.cell(row=row, column=start_col, value=kpi["name"])
                style_range(row, start_col, end_col, fill=header_fill, font=kpi_name_font, alignment=center_align)
                
                # 2. Big KPI Value (Merged)
                ws.merge_cells(start_row=row+1, start_column=start_col, end_row=row+1, end_column=end_col)
                v_cell = ws.cell(row=row+1, column=start_col, value=kpi["value"])
                style_range(row+1, start_col, end_col, fill=neutral_fill, font=kpi_val_font, alignment=center_align)
                
                # 3. Secondary Variance Details
                ws.cell(row=row+2, column=start_col, value="Vs. Target").font = label_font
                ws.cell(row=row+2, column=start_col).alignment = right_align
                
                t_cell = ws.cell(row=row+2, column=start_col+1, value=kpi["target"])
                t_cell.font = val_font
                t_cell.alignment = left_align
                
                ws.cell(row=row+2, column=start_col+2, value="Vs. Prior").font = label_font
                ws.cell(row=row+2, column=start_col+2).alignment = right_align
                
                p_cell = ws.cell(row=row+2, column=start_col+3, value=kpi["prior"])
                p_cell.font = val_font
                p_cell.alignment = left_align
                
                # Apply Formatting Overrides
                if "format" in kpi:
                    v_cell.number_format = kpi["format"]
                    t_cell.number_format = kpi["format"]
                    p_cell.number_format = kpi["format"]
                
                # 4. Attach Absolute Conditional Formatting to the Merged Block
                val_coord = v_cell.coordinate
                tgt_coord = t_cell.coordinate
                cf_range = f"{ws.cell(row=row+1, column=start_col).coordinate}:{ws.cell(row=row+1, column=end_col).coordinate}"
                
                # Standard threshold checking logic
                if kpi.get("lower_is_better", False):
                    good_formula = [f"${val_coord}<=${tgt_coord}"]
                    bad_formula = [f"${val_coord}>${tgt_coord}"]
                else:
                    good_formula = [f"${val_coord}>=${tgt_coord}"]
                    bad_formula = [f"${val_coord}<${tgt_coord}"]
                    
                ws.conditional_formatting.add(cf_range, FormulaRule(formula=good_formula, fill=good_fill))
                ws.conditional_formatting.add(cf_range, FormulaRule(formula=bad_formula, fill=bad_fill))
                
            row += 4  # Shift down 3 rows for data + 1 for padding
        row += 1      # Add a gap before the next section
```