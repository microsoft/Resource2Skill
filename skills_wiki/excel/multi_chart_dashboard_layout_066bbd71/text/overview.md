### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Separates the data layer from the presentation layer. Disables gridlines on a presentation sheet and populates it with multiple charts sourced from a hidden backend data sheet, creating a clean, report-style visual dashboard.
* **Applicability**: Best for high-level management reports or automated KPI dashboards where a clean, non-spreadsheet visual layout is desired. While Excel-native slicers cannot be generated via standard Python libraries, this structural pattern effectively builds the static foundation for any standard dashboard.

### 2. Structural Breakdown

- **Data Layout**: Raw or aggregated metric blocks are housed on a dedicated `Data` sheet, which is then hidden (`ws.sheet_state = "hidden"`) to keep the user focused entirely on the frontend.
- **Formula Logic**: N/A
- **Visual Design**: Gridlines are disabled on the frontend dashboard sheet (`showGridLines = False`). A merged cell block acts as an oversized report header.
- **Charts/Tables**: Combines a large Stacked Column chart for categorical breakdowns alongside vertically stacked Line charts for time-series trends.
- **Theme Hooks**: The title foreground color and chart style IDs (`style=10`, `style=13`) dictate the visual aesthetic of the layout.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    
    # 1. Setup Frontend Dashboard Sheet
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False
    
    # Dashboard Header
    ws_dash["A1"] = title
    ws_dash["A1"].font = Font(size=24, bold=True, color="2F5496") # Typically pulled from theme.title_fg
    ws_dash.merge_cells("A1:R2")
    ws_dash["A1"].alignment = Alignment(vertical="center")
    
    # 2. Setup Backend Hidden Data Sheet
    ws_data = wb.create_sheet("Data")
    ws_data.sheet_state = "hidden"
    
    # Block 1: Data for Stacked Column Chart
    data_stacked = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 60000, 20000, 25000],
        ["United States", 35000, 10000, 15000],
        ["United Kingdom", 45000, 15000, 20000],
    ]
    for row in data_stacked:
        ws_data.append(row)
        
    # Block 2: Data for Line Chart 1 (Units)
    data_units = [
        ["Month", "Units Sold"],
        ["Sep", 50000],
        ["Oct", 95000],
        ["Nov", 65000],
        ["Dec", 52000],
    ]
    for i, row in enumerate(data_units, start=10):
        for j, val in enumerate(row, start=1):
            ws_data.cell(row=i, column=j, value=val)
            
    # Block 3: Data for Line Chart 2 (Profit)
    data_profit = [
        ["Month", "Profit"],
        ["Sep", 124000],
        ["Oct", 228000],
        ["Nov", 160000],
        ["Dec", 136000],
    ]
    for i, row in enumerate(data_profit, start=20):
        for j, val in enumerate(row, start=1):
            ws_data.cell(row=i, column=j, value=val)
            
    # 3. Create Stacked Column Chart
    chart_stacked = BarChart()
    chart_stacked.type = "col"
    chart_stacked.grouping = "stacked"
    chart_stacked.overlap = 100
    chart_stacked.title = "Profit by Market & Cookie Type"
    chart_stacked.style = 10
    
    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=4)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=4)
    chart_stacked.add_data(data_ref, titles_from_data=True)
    chart_stacked.set_categories(cats_ref)
    chart_stacked.height = 14
    chart_stacked.width = 16
    ws_dash.add_chart(chart_stacked, "B4")
    
    # 4. Create Top Line Chart
    chart_units = LineChart()
    chart_units.title = "Units sold each month"
    chart_units.style = 13
    chart_units.legend = None # Remove legend for single-series line charts
    
    data_ref_u = Reference(ws_data, min_col=2, min_row=10, max_row=14)
    cats_ref_u = Reference(ws_data, min_col=1, min_row=11, max_row=14)
    chart_units.add_data(data_ref_u, titles_from_data=True)
    chart_units.set_categories(cats_ref_u)
    chart_units.height = 7
    chart_units.width = 12
    ws_dash.add_chart(chart_units, "K4")
    
    # 5. Create Bottom Line Chart
    chart_profit = LineChart()
    chart_profit.title = "Profit by month"
    chart_profit.style = 13
    chart_profit.legend = None
    
    data_ref_p = Reference(ws_data, min_col=2, min_row=20, max_row=24)
    cats_ref_p = Reference(ws_data, min_col=1, min_row=21, max_row=24)
    chart_profit.add_data(data_ref_p, titles_from_data=True)
    chart_profit.set_categories(cats_ref_p)
    chart_profit.height = 7
    chart_profit.width = 12
    ws_dash.add_chart(chart_profit, "K18")
```