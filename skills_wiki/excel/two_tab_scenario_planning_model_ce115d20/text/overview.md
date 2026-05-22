### 1. High-level Skill Pattern Extraction

> **Skill Name**: Two-Tab Scenario Planning Model

* **Tier**: archetype
* **Core Mechanism**: Constructs a standard financial forecasting workbook separating input variables into an "Assumptions" sheet and time-series calculations into a "Model" sheet. Uses horizontal rolling formulas over 24 months that dynamically reference the assumptions, enabling instant scenario simulation when inputs change. 
* **Applicability**: Highly effective for business case modeling, multi-product revenue forecasting, and interactive financial templates where stakeholders need to toggle drivers (pricing, growth rates, margins) to view downstream impacts on a chart.

### 2. Structural Breakdown

- **Data Layout**: 
  - **Assumptions Sheet**: Vertical key-value pairs grouped by product line/category (Col A: Label, Col B: Input Value).
  - **Model Sheet**: Horizontal time-series layout (Cols C-Z represent Months 1-24). Rows are hierarchically structured by Product Line with a "Combined Totals" summary section at the bottom.
- **Formula Logic**: 
  - Rolling volume metrics (Month N = Month N-1 * (1 + Assumptions!Growth)).
  - Financial derivations (Revenue = Volume * Assumptions!AOV; Gross Profit = Revenue * Assumptions!Margin).
  - Cross-sheet absolute references for static rates (e.g., `Assumptions!$B$14`).
- **Visual Design**: Minimalist layout with section header rows using background fills, bold typography for categories, and distinct number formatting (percentages, currencies, comma separators) applied systematically by row/metric.
- **Charts/Tables**: A wide Line Chart appended below the model, tracking multi-series Revenue trends and Contribution Margin across the 24-month timeline.
- **Theme Hooks**: Utilizes `header_bg` and `header_fg` for the timeline header row, and a generic `bg` token for subtle category row dividers.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, numbers
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter

def render_workbook(wb, *, title: str = "Scenario Planning Model", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme and formatting setup
    palettes = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF", "accent": "4F81BD", "bg": "F2F2F2"}
    }
    colors = palettes.get(theme, palettes["corporate_blue"])

    header_fill = PatternFill(start_color=colors["header_bg"], end_color=colors["header_bg"], fill_type="solid")
    header_font = Font(color=colors["header_fg"], bold=True)
    bold_font = Font(bold=True)
    section_fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    
    currency_format = '"$"#,##0'
    pct_format = '0.0%'
    num_format = '#,##0'

    # 2. Setup Assumptions Sheet
    ws_assump = wb.active
    ws_assump.title = "Assumptions"

    assumptions_data = [
        ("ACCESSORIES", ""),
        ("Average Order Value ($)", 45),
        ("Starting Monthly Orders", 2000),
        ("Monthly Order Growth", 0.06),
        ("Gross Margin %", 0.35),
        ("", ""),
        ("DEVICES", ""),
        ("Average Order Value ($)", 280),
        ("Starting Monthly Orders", 500),
        ("Monthly Order Growth", 0.04),
        ("Gross Margin %", 0.22),
        ("", ""),
        ("GENERAL", ""),
        ("Marketing Spend (% of Rev)", 0.12)
    ]

    for r_idx, row_data in enumerate(assumptions_data, 1):
        ws_assump.cell(row=r_idx, column=1, value=row_data[0])
        
        # Apply formatting based on content
        if row_data[1] != "":
            val_cell = ws_assump.cell(row=r_idx, column=2, value=row_data[1])
            if "%" in row_data[0] or "Growth" in row_data[0]:
                val_cell.number_format = pct_format
            elif "Value" in row_data[0]:
                val_cell.number_format = currency_format
            else:
                val_cell.number_format = num_format
        
        # Style section headers
        if row_data[0].isupper() and row_data[1] == "":
            ws_assump.cell(row=r_idx, column=1).font = bold_font
            ws_assump.cell(row=r_idx, column=1).fill = section_fill
            ws_assump.cell(row=r_idx, column=2).fill = section_fill

    ws_assump.column_dimensions['A'].width = 30
    ws_assump.column_dimensions['B'].width = 15

    # 3. Setup Model Sheet
    ws_model = wb.create_sheet("Model")

    # Build Header Timeline
    ws_model.cell(row=2, column=2, value="Forecast Timeline").font = bold_font
    for col in range(3, 27):
        c = ws_model.cell(row=2, column=col, value=f"Month {col-2}")
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center")

    # Define Rows Layout
    labels = {
        4: "ACCESSORIES",
        5: "Orders",
        6: "Revenue",
        7: "Gross Profit",
        9: "DEVICES",
        10: "Orders",
        11: "Revenue",
        12: "Gross Profit",
        14: "COMBINED TOTALS",
        15: "Total Revenue",
        16: "Total Gross Profit",
        17: "Marketing Spend",
        18: "Contribution Margin"
    }

    for r, label in labels.items():
        ws_model.cell(row=r, column=2, value=label)
        if label.isupper():
            ws_model.cell(row=r, column=2).font = bold_font
            for c_idx in range(2, 27):
                ws_model.cell(row=r, column=c_idx).fill = section_fill

    ws_model.column_dimensions['B'].width = 25

    # 4. Inject Dynamic Formulas over 24 columns
    for col in range(3, 27):
        curr_col = get_column_letter(col)
        prev_col = get_column_letter(col-1)

        # Accessories Block
        if col == 3: # Month 1 pulls directly from baseline assumption
            ws_model.cell(row=5, column=col, value="=Assumptions!$B$3")
        else: # Month N applies growth to N-1
            ws_model.cell(row=5, column=col, value=f"={prev_col}5*(1+Assumptions!$B$4)")
        ws_model.cell(row=6, column=col, value=f"={curr_col}5*Assumptions!$B$2")
        ws_model.cell(row=7, column=col, value=f"={curr_col}6*Assumptions!$B$5")

        # Devices Block
        if col == 3:
            ws_model.cell(row=10, column=col, value="=Assumptions!$B$9")
        else:
            ws_model.cell(row=10, column=col, value=f"={prev_col}10*(1+Assumptions!$B$10)")
        ws_model.cell(row=11, column=col, value=f"={curr_col}10*Assumptions!$B$8")
        ws_model.cell(row=12, column=col, value=f"={curr_col}11*Assumptions!$B$11")

        # Combined Totals
        ws_model.cell(row=15, column=col, value=f"={curr_col}6+{curr_col}11")
        ws_model.cell(row=16, column=col, value=f"={curr_col}7+{curr_col}12")
        ws_model.cell(row=17, column=col, value=f"={curr_col}15*Assumptions!$B$14")
        ws_model.cell(row=18, column=col, value=f"={curr_col}16-{curr_col}17")

        # Format number types for the column
        ws_model.cell(row=5, column=col).number_format = num_format
        ws_model.cell(row=10, column=col).number_format = num_format
        for row_idx in [6, 7, 11, 12, 15, 16, 17, 18]:
            ws_model.cell(row=row_idx, column=col).number_format = currency_format

    # 5. Append Line Chart for Revenue vs Margin
    chart = LineChart()
    chart.title = "24-Month Revenue & Contribution Margin Forecast"
    chart.style = 13
    chart.y_axis.title = "Amount ($)"
    chart.x_axis.title = "Timeline"
    chart.width = 30
    chart.height = 12

    # Map Chart X-Axis
    timeline_cats = Reference(ws_model, min_col=3, min_row=2, max_col=26)
    chart.set_categories(timeline_cats)

    # Map Series
    series_acc = Reference(ws_model, min_col=3, min_row=6, max_col=26)
    chart.add_data(series_acc, titles_from_data=False)
    chart.series[0].title = "Accessories Revenue"

    series_dev = Reference(ws_model, min_col=3, min_row=11, max_col=26)
    chart.add_data(series_dev, titles_from_data=False)
    chart.series[1].title = "Devices Revenue"

    series_cm = Reference(ws_model, min_col=3, min_row=18, max_col=26)
    chart.add_data(series_cm, titles_from_data=False)
    chart.series[2].title = "Total Contribution Margin"

    ws_model.add_chart(chart, "B21")
```