### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Static Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet reporting workbook that strictly separates aggregated calculation data from presentation. It configures a central "Dashboard" sheet with hidden gridlines, customized chart dimensions, and aligned anchors to create an interactive, application-like visual report layout.
* **Applicability**: Best for generating polished, static executive dashboards programmatically (where interactive Slicers and PivotTables cannot be created from scratch via standard libraries). Ideal for clean PDF exports or flat Excel reports.

### 2. Structural Breakdown

- **Data Layout**: Employs a multi-sheet structure (`Dashboard` and `Calculations`). Aggregated summary tables are generated on the `Calculations` sheet, which can optionally be hidden from the end user.
- **Formula Logic**: Pure data binding via `openpyxl.chart.Reference` to link front-end charts to the background `Calculations` sheet.
- **Visual Design**: The presentation sheet has `showGridLines = False`. The dashboard title is merged across the top rows with a large, themed font.
- **Charts/Tables**: Includes a Stacked Column chart (`type="col", grouping="stacked"`) for cross-sectional data and Line charts (`type="line"`) for time-series trends. 
- **Theme Hooks**: Primary font colors are driven by the theme configuration to allow easy switching between light/dark or corporate styling.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Font, Alignment, PatternFill
    
    # Theme palette fallback resolution
    colors = {
        "corporate_blue": {"primary": "4F81BD", "text": "333333", "bg": "FFFFFF"},
        "dark_mode": {"primary": "4472C4", "text": "FFFFFF", "bg": "262626"}
    }.get(theme, {"primary": "4F81BD", "text": "333333", "bg": "FFFFFF"})

    # 1. Setup Presentation Dashboard Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False
    
    if colors["bg"] != "FFFFFF":
        # Apply background color to visible range if dark mode
        for row in ws_dash.iter_rows(min_row=1, max_row=40, min_col=1, max_col=20):
            for cell in row:
                cell.fill = PatternFill(start_color=colors["bg"], end_color=colors["bg"], fill_type="solid")
    
    # Dashboard Header Area
    ws_dash.merge_cells("B2:N4")
    title_cell = ws_dash["B2"]
    title_cell.value = title
    title_cell.font = Font(size=26, bold=True, color=colors["text"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # 2. Setup Background Calculations Sheet
    ws_calc = wb.create_sheet("Calculations")
    ws_calc.sheet_state = 'hidden' # Hides the raw aggregated data from the viewer
    
    # Table 1: Profit by Market & Product Category
    calc_data_1 = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62000, 23000, 21000, 25000],
        ["Philippines", 54000, 24000, 22000, 8000],
        ["United Kingdom", 46000, 26000, 11000, 14000],
        ["United States", 36000, 32000, 9000, 20000],
    ]
    for r in calc_data_1:
        ws_calc.append(r)
        
    # Table 2: Units sold over time
    ws_calc.append([])
    calc_data_2 = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970],
    ]
    row_offset_2 = ws_calc.max_row + 1
    for r in calc_data_2:
        ws_calc.append(r)
        
    # Table 3: Profit over time
    ws_calc.append([])
    calc_data_3 = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337],
    ]
    row_offset_3 = ws_calc.max_row + 1
    for r in calc_data_3:
        ws_calc.append(r)

    # 3. Instantiate & Anchor Charts
    
    # Chart 1: Stacked Column (Market Breakdown)
    c1 = BarChart()
    c1.type = "col"
    c1.style = 10
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.width = 16.0
    c1.height = 10.0
    
    data_ref_1 = Reference(ws_calc, min_col=2, min_row=1, max_col=5, max_row=5)
    cats_ref_1 = Reference(ws_calc, min_col=1, min_row=2, max_row=5)
    c1.add_data(data_ref_1, titles_from_data=True)
    c1.set_categories(cats_ref_1)
    c1.legend.position = 'r'
    
    ws_dash.add_chart(c1, "B6")
    
    # Chart 2: Line Chart (Units Trend)
    c2 = LineChart()
    c2.style = 13
    c2.title = "Units sold each month"
    c2.width = 14.0
    c2.height = 7.0
    
    data_ref_2 = Reference(ws_calc, min_col=2, min_row=row_offset_2, max_col=2, max_row=row_offset_2+4)
    cats_ref_2 = Reference(ws_calc, min_col=1, min_row=row_offset_2+1, max_row=row_offset_2+4)
    c2.add_data(data_ref_2, titles_from_data=True)
    c2.set_categories(cats_ref_2)
    c2.legend = None
    
    ws_dash.add_chart(c2, "J6")
    
    # Chart 3: Line Chart (Profit Trend)
    c3 = LineChart()
    c3.style = 13
    c3.title = "Profit by month"
    c3.width = 14.0
    c3.height = 7.0
    
    data_ref_3 = Reference(ws_calc, min_col=2, min_row=row_offset_3, max_col=2, max_row=row_offset_3+4)
    cats_ref_3 = Reference(ws_calc, min_col=1, min_row=row_offset_3+1, max_row=row_offset_3+4)
    c3.add_data(data_ref_3, titles_from_data=True)
    c3.set_categories(cats_ref_3)
    c3.legend = None
    
    ws_dash.add_chart(c3, "J21")
```