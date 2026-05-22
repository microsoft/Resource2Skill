### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Canvas Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Generates a professional dashboard interface by turning off the worksheet's gridlines and row/column headers. Populates the "clean canvas" with neatly aligned charts (with removed major gridlines) that read from a hidden background calculation sheet to mimic an interactive Pivot Dashboard. 
* **Applicability**: Best used for generating static, visually appealing reporting dashboards. Ideal for high-level management reports where you want the Excel file to feel like a bespoke application rather than a raw spreadsheet.

### 2. Structural Breakdown

- **Data Layout**: Consists of two sheets. The `Dashboard` sheet acts as the presentation layer, while a hidden `Calc` sheet stores the pre-summarized reporting data.
- **Formula Logic**: Purely structural mapping; references the hidden `Calc` sheet data ranges to feed the openpyxl chart elements.
- **Visual Design**: The `showGridLines` and `showRowColHeaders` worksheet view properties are set to `False`. A prominent, merged title banner spans the top of the canvas, utilizing a solid theme color and white bold text.
- **Charts/Tables**: Employs a Stacked Bar chart on the left, sized large, alongside two vertically stacked Line charts on the right. All charts have their `majorGridlines` disabled to maintain a clean aesthetic.
- **Theme Hooks**: Consumes a standard `header_bg` style from the theme token to dynamically style the dashboard's main title banner. 

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Font, Alignment, PatternFill
    
    # 1. Setup Hidden Calc Sheet for Chart Data
    ws_calc = wb.create_sheet("Calc")
    ws_calc.sheet_state = "hidden"
    
    # Dummy data simulating summarized PivotTable outputs
    calc_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Sugar"],
        ["India", 62349, 4872, 18560],
        ["United Kingdom", 46530, 5220, 14946],
        ["United States", 36657, 6368, 9938],
    ]
    for r in calc_data:
        ws_calc.append(r)
        
    monthly_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337],
    ]
    start_row = len(calc_data) + 3
    for r in monthly_data:
        ws_calc.append(r)
        
    # 2. Setup Clean Canvas Dashboard
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    
    # Core Mechanism: Hide Excel UI elements for a "software" feel
    ws_dash.sheet_view.showGridLines = False
    ws_dash.sheet_view.showRowColHeaders = False
    
    # 3. Create Dashboard Header
    theme_colors = {"corporate_blue": "4F81BD", "modern_dark": "2E2E2E", "forest_green": "4F6228"}
    header_bg = theme_colors.get(theme, "4F81BD")
    
    ws_dash.merge_cells("B1:N2")
    header_cell = ws_dash["B1"]
    header_cell.value = title
    header_cell.font = Font(size=22, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(solid=True, start_color=header_bg)
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Generate Main Stacked Bar Chart (Left Side)
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "stacked"
    bar.overlap = 100
    bar.title = "Profit by Market & Cookie Type"
    
    data = Reference(ws_calc, min_col=2, min_row=1, max_col=4, max_row=4)
    cats = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    bar.y_axis.majorGridlines = None  # Remove chart gridlines for cleanliness
    bar.width = 16
    bar.height = 14
    ws_dash.add_chart(bar, "B4")
    
    # 5. Generate Line Chart 1: Units Sold (Top Right)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.legend = None  # Hide legend to save space
    
    data1 = Reference(ws_calc, min_col=2, min_row=start_row, max_row=start_row+4)
    cats1 = Reference(ws_calc, min_col=1, min_row=start_row+1, max_row=start_row+4)
    line1.add_data(data1, titles_from_data=True)
    line1.set_categories(cats1)
    line1.y_axis.majorGridlines = None
    line1.width = 12
    line1.height = 6.5
    ws_dash.add_chart(line1, "I4")
    
    # 6. Generate Line Chart 2: Profit by Month (Bottom Right)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.legend = None
    
    data2 = Reference(ws_calc, min_col=3, min_row=start_row, max_row=start_row+4)
    cats2 = Reference(ws_calc, min_col=1, min_row=start_row+1, max_row=start_row+4)
    line2.add_data(data2, titles_from_data=True)
    line2.set_categories(cats2)
    line2.y_axis.majorGridlines = None
    line2.width = 12
    line2.height = 6.5
    ws_dash.add_chart(line2, "I15")
```