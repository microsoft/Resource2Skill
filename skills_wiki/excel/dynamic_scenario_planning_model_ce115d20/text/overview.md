### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic Scenario Planning Model

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet financial model separating static inputs from time-series logic. The first sheet captures driving variables (AOV, growth rates, margins) as absolute references, while the second sheet builds a 24-month forecast using relative period-over-period growth formulas. It automatically aggregates totals, calculates blended margins, runs an inline parity check, and plots the results.
* **Applicability**: Ideal for FP&A forecasting, business casing, and what-if analysis where product/service drivers need to be quickly toggled to instantly see downstream margin impacts and P&L trends.

### 2. Structural Breakdown

- **Data Layout**: Splits the workbook into `Assumptions` (column A for labels, B for inputs) and `Model` (column A for line items, B-Y for Months 1-24). Product lines are compartmentalized with aggregated totals at the bottom.
- **Formula Logic**: Relies on Absolute Referencing (`Assumptions!$B$10`) for fixed inputs and Relative Referencing (`=C5*(1+...)`) for compounding monthly growth. Incorporates a sanity check logic row using `=IF(ROUND(B22,2)=ROUND(B15,2), "✓ Match", "✗ Error")`.
- **Visual Design**: Uses a solid header color for time periods. Visually isolates inputs, totals, and sanity checks with standard grey background fills and bold fonts to clarify where user interaction is expected versus calculated output.
- **Charts/Tables**: A 3-series Line Chart dynamically reading from the disjointed `Revenue` and `Contribution Margin` calculation rows, anchoring cleanly beneath the model block.
- **Theme Hooks**: Utilizes `header_fill` (defaulting to dark blue) and `header_font` for the main structural timeline row, allowing easy integration with global palette tokens.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.series import Series
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "Scenario Planning Model", theme: str = "corporate_blue", **kwargs) -> None:
    # Clean default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
        
    # Create sheets
    ws_assump = wb.create_sheet("Assumptions")
    ws_model = wb.create_sheet("Model")
    
    # Theme definition fallback
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    bold_font = Font(bold=True)
    grey_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    
    # --- ASSUMPTIONS SHEET ---
    ws_assump["A1"] = f"{title} - Assumptions"
    ws_assump["A1"].font = Font(size=14, bold=True)
    
    data_map = {
        "A3": ("General", bold_font, grey_fill),
        "A4": ("Model Start Date", None, None), "B4": ("Month 1", None, None),
        
        "A6": ("Product Line Assumptions", bold_font, grey_fill),
        "A7": ("Accessories", bold_font, None),
        "A8": ("Average Order Value ($)", None, None), "B8": (45, None, None),
        "A9": ("Starting Monthly Orders", None, None), "B9": (2000, None, None),
        "A10": ("Monthly Growth (%)", None, None), "B10": (0.06, None, None),
        "A11": ("Gross Margin (%)", None, None), "B11": (0.35, None, None),
        
        "A13": ("Devices", bold_font, None),
        "A14": ("Average Order Value ($)", None, None), "B14": (280, None, None),
        "A15": ("Starting Monthly Orders", None, None), "B15": (500, None, None),
        "A16": ("Monthly Growth (%)", None, None), "B16": (0.04, None, None),
        "A17": ("Gross Margin (%)", None, None), "B17": (0.22, None, None),
        
        "A19": ("Marketing Spend (% of Total Revenue)", bold_font, grey_fill), "B19": (0.12, None, grey_fill)
    }
    
    for cell_ref, (val, font, fill) in data_map.items():
        cell = ws_assump[cell_ref]
        cell.value = val
        if font:
            cell.font = font
        if fill:
            cell.fill = fill
            
    # Input Number Formatting
    ws_assump["B8"].number_format = "$#,##0"
    ws_assump["B9"].number_format = "#,##0"
    ws_assump["B10"].number_format = "0.0%"
    ws_assump["B11"].number_format = "0.0%"
    ws_assump["B14"].number_format = "$#,##0"
    ws_assump["B15"].number_format = "#,##0"
    ws_assump["B16"].number_format = "0.0%"
    ws_assump["B17"].number_format = "0.0%"
    ws_assump["B19"].number_format = "0.0%"
    
    ws_assump.column_dimensions["A"].width = 40
    ws_assump.column_dimensions["B"].width = 15
    
    # --- MODEL SHEET ---
    ws_model["A1"] = f"{title} - 24-Month Forecast"
    ws_model["A1"].font = Font(size=14, bold=True)
    
    # Timeline Headers
    for c in range(2, 26):
        col_letter = get_column_letter(c)
        cell = ws_model[f"{col_letter}2"]
        cell.value = f"Month {c-1}"
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
        ws_model.column_dimensions[col_letter].width = 13
        
    ws_model.column_dimensions["A"].width = 32
    
    # Row Labels
    labels = [
        (4, "Accessories", bold_font, False),
        (5, "Orders", None, False),
        (6, "Revenue", None, False),
        (7, "Gross Profit", None, False),
        (9, "Devices", bold_font, False),
        (10, "Orders", None, False),
        (11, "Revenue", None, False),
        (12, "Gross Profit", None, False),
        (14, "COMBINED TOTALS", bold_font, True),
        (15, "Total Revenue", bold_font, False),
        (16, "Total Gross Profit", bold_font, False),
        (17, "Blended Gross Margin %", None, False),
        (18, "Marketing Spend ($)", None, False),
        (19, "Contribution Margin ($)", bold_font, False),
        (21, "SANITY CHECK", bold_font, True),
        (22, "Accessories Rev + Devices Rev ($)", None, False),
        (23, "Matches Total Revenue?", None, False)
    ]
    
    for r, label, font, is_section in labels:
        cell = ws_model.cell(row=r, column=1, value=label)
        if font:
            cell.font = font
        if is_section:
            cell.fill = grey_fill
            for c in range(2, 26):
                ws_model.cell(row=r, column=c).fill = grey_fill
                
    # Logic Generation
    for c in range(2, 26):
        col = get_column_letter(c)
        prev_col = get_column_letter(c-1) if c > 2 else ""
        
        # Accessories block
        ws_model[f"{col}5"] = "=Assumptions!B9" if c == 2 else f"={prev_col}5*(1+Assumptions!$B$10)"
        ws_model[f"{col}6"] = f"={col}5*Assumptions!$B$8"
        ws_model[f"{col}7"] = f"={col}6*Assumptions!$B$11"
        
        # Devices block
        ws_model[f"{col}10"] = "=Assumptions!B15" if c == 2 else f"={prev_col}10*(1+Assumptions!$B$16)"
        ws_model[f"{col}11"] = f"={col}10*Assumptions!$B$14"
        ws_model[f"{col}12"] = f"={col}11*Assumptions!$B$17"
        
        # Aggregations & Margins
        ws_model[f"{col}15"] = f"={col}6+{col}11"
        ws_model[f"{col}16"] = f"={col}7+{col}12"
        ws_model[f"{col}17"] = f"=IFERROR({col}16/{col}15, 0)"
        ws_model[f"{col}18"] = f"={col}15*Assumptions!$B$19"
        ws_model[f"{col}19"] = f"={col}16-{col}18"
        
        # Sanity Check formulas
        ws_model[f"{col}22"] = f"={col}6+{col}11"
        ws_model[f"{col}23"] = f'=IF(ROUND({col}22,2)=ROUND({col}15,2), "✓ Match", "✗ Error")'
        
        # Formatting formats
        ws_model[f"{col}5"].number_format = "#,##0"
        ws_model[f"{col}6"].number_format = "$#,##0"
        ws_model[f"{col}7"].number_format = "$#,##0"
        ws_model[f"{col}10"].number_format = "#,##0"
        ws_model[f"{col}11"].number_format = "$#,##0"
        ws_model[f"{col}12"].number_format = "$#,##0"
        ws_model[f"{col}15"].number_format = "$#,##0"
        ws_model[f"{col}16"].number_format = "$#,##0"
        ws_model[f"{col}17"].number_format = "0.0%"
        ws_model[f"{col}18"].number_format = "$#,##0"
        ws_model[f"{col}19"].number_format = "$#,##0"
        ws_model[f"{col}22"].number_format = "$#,##0"

    # --- FORECAST LINE CHART ---
    chart = LineChart()
    chart.title = "Monthly Revenue & Contribution Margin by Product Line"
    chart.style = 13
    chart.y_axis.title = "Revenue / Margin ($)"
    chart.x_axis.title = "Month"
    chart.width = 30
    chart.height = 10
    
    # Define X-axis
    cats = Reference(ws_model, min_col=2, min_row=2, max_col=25, max_row=2)
    chart.set_categories(cats)
    
    # Append separated series rows
    chart.series.append(Series(Reference(ws_model, min_col=2, min_row=6, max_col=25, max_row=6), title="Accessories Revenue"))
    chart.series.append(Series(Reference(ws_model, min_col=2, min_row=11, max_col=25, max_row=11), title="Devices Revenue"))
    chart.series.append(Series(Reference(ws_model, min_col=2, min_row=19, max_col=25, max_row=19), title="Contribution Margin"))
    
    ws_model.add_chart(chart, "A26")
```