### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Performance Dashboard

* **Tier**: archetype
* **Core Mechanism**: Transforms raw analytical data into a unified, interactive-feeling dashboard. Since openpyxl does not natively evaluate Pivot Tables or Slicers, this archetype aggregates summary data via Python into a hidden "Calculations" sheet, then constructs a clean "Dashboard" sheet (with gridlines disabled) populated by aligned Stacked Column and Line charts to replicate the visual layout.
* **Applicability**: Executive summaries, monthly reporting, and KPI overviews where multiple visual dimensions (e.g., categorical breakdown + time-series trends) need to be presented on a single, print-ready page.

### 2. Structural Breakdown

- **Data Layout**: Splits the workbook into separation of concerns: "Dashboard" (Visuals), "Calculations" (Aggregated chart source data), and "Data" (Raw records - omitted in code for brevity but assumed present).
- **Formula Logic**: Python performs the aggregations that Pivot Tables normally would, hard-coding the summary matrix into the `Calculations` sheet to ensure charts render properly upon opening.
- **Visual Design**: Turns off `showGridLines` on the Dashboard sheet. Employs a bold, colored spanning header (A1:P2) to frame the dashboard.
- **Charts/Tables**: 
  1. `BarChart` (type="col", grouping="stacked") to show Profit by Market & Cookie Type.
  2. Two `LineChart` objects to display monthly trends (Units and Profit), with legends disabled for cleaner aesthetics.
- **Theme Hooks**: Uses the primary theme color for the dashboard title background, providing a cohesive brand feel.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Font, PatternFill, Alignment

    # --- Setup Sheets ---
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_calc = wb.create_sheet("Calculations")
    
    # Hide gridlines for a clean "App/Dashboard" aesthetic
    ws_dash.sheet_view.showGridLines = False

    # --- Dashboard Header ---
    ws_dash.merge_cells("A1:O2")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color="FFFFFF")
    # In a real app, this hex comes from the theme dictionary
    title_cell.fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # --- Populate Calculation Sheet (Simulating Pivot Table Outputs) ---
    
    # Table 1: Profit by Country & Product
    calc_data_1 = [
        ["Country", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62349, 4872, 21028],
        ["Philippines", 54618, 7026, 22005],
        ["United Kingdom", 46530, 5220, 11497],
        ["United States", 36657, 6368, 22260]
    ]
    for r_idx, row in enumerate(calc_data_1, 1):
        for c_idx, val in enumerate(row, 1):
            ws_calc.cell(row=r_idx, column=c_idx, value=val)

    # Table 2: Units Sold by Month
    calc_data_2 = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    for r_idx, row in enumerate(calc_data_2, 8):
        for c_idx, val in enumerate(row, 1):
            ws_calc.cell(row=r_idx, column=c_idx, value=val)

    # Table 3: Profit by Month
    calc_data_3 = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    for r_idx, row in enumerate(calc_data_3, 15):
        for c_idx, val in enumerate(row, 1):
            ws_calc.cell(row=r_idx, column=c_idx, value=val)

    # --- Generate & Position Charts ---

    # Chart 1: Stacked Column (Profit by Market & Cookie)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.style = 10  # Standard Excel chart style preset
    
    data1 = Reference(ws_calc, min_col=2, min_row=1, max_col=4, max_row=5)
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=5)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    
    ws_dash.add_chart(c1, "B4")
    c1.width = 16
    c1.height = 11

    # Chart 2: Line Chart (Units sold each month)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.style = 10
    
    data2 = Reference(ws_calc, min_col=2, min_row=8, max_col=2, max_row=12)
    cats2 = Reference(ws_calc, min_col=1, min_row=9, max_row=12)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    c2.legend = None # Remove legend for cleaner look
    
    ws_dash.add_chart(c2, "J4")
    c2.width = 13
    c2.height = 7.5

    # Chart 3: Line Chart (Profit by month)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.style = 10
    
    data3 = Reference(ws_calc, min_col=2, min_row=15, max_col=2, max_row=19)
    cats3 = Reference(ws_calc, min_col=1, min_row=16, max_row=19)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats3)
    c3.legend = None
    
    ws_dash.add_chart(c3, "J12")
    c3.width = 13
    c3.height = 7.5
```