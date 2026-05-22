### 1. High-level Skill Pattern Extraction

> **Skill Name**: Static Chart Dashboard 

* **Tier**: archetype
* **Core Mechanism**: Builds a visually clean presentation dashboard by decoupling the data into a hidden "summary" calculation sheet. Projects standard openpyxl charts (Stacked Column and Line) onto a gridline-free layout layer, avoiding the need for interactive Pivot Tables/Slicers which openpyxl cannot fully render.
* **Applicability**: Best used when you need to programmatically generate an end-to-end multi-chart KPI dashboard. Perfect for weekly or monthly automated reports where the data is static upon generation.

### 2. Structural Breakdown

- **Data Layout**: Places aggregated data into a hidden `Summary Data` sheet, grouped into separate contiguous tables (e.g., Stacked Bar matrix, Monthly Line series).
- **Formula Logic**: Purely static in this archetype, but typically this pattern pairs with `SUMIFS` or `COUNTIFS` in the hidden summary sheet pointing back to a raw data dump.
- **Visual Design**: Turns off gridlines on the dashboard sheet (`showGridLines = False`), uses a large merged header for the title, and strictly controls chart anchors (e.g., `B5`, `K5`, `K14`) to build a predictable UI grid.
- **Charts/Tables**: 
  - `BarChart` (`grouping="stacked"`, `overlap=100`) for categorical breakdown.
  - Two `LineChart`s stacked vertically for trend analysis.
- **Theme Hooks**: Uses a primary theme color for the title text and relies on openpyxl's built-in chart `.style` indices to provide cohesive charting palettes.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, Alignment

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a multi-chart dashboard archetype.
    """
    # 1. Setup sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False
    
    ws_sum = wb.create_sheet("Summary Data")
    
    # 2. Populate Summary Data (Hidden Calculation Layer)
    # Stacked Bar data (Profit by Market & Cookie)
    ws_sum.append(["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"])
    ws_sum.append(["India", 62349, 23621, 21028])
    ws_sum.append(["Philippines", 54618, 24567, 22005])
    ws_sum.append(["United Kingdom", 46530, 26731, 11497])
    ws_sum.append(["United States", 36657, 32910, 9938])
    
    # Line chart data (Units Sold by Month)
    ws_sum.append([]) # Row 6 empty
    ws_sum.append(["Month", "Units Sold"]) # Row 7
    ws_sum.append(["Sep", 50601]) # Row 8
    ws_sum.append(["Oct", 95622]) # Row 9
    ws_sum.append(["Nov", 65481]) # Row 10
    ws_sum.append(["Dec", 52970]) # Row 11
    
    # Line chart data (Profit by Month)
    ws_sum.append([]) # Row 12 empty
    ws_sum.append(["Month", "Profit"]) # Row 13
    ws_sum.append(["Sep", 124812]) # Row 14
    ws_sum.append(["Oct", 228275]) # Row 15
    ws_sum.append(["Nov", 160228]) # Row 16
    ws_sum.append(["Dec", 136337]) # Row 17
    
    # 3. Build Dashboard Header
    ws_dash.merge_cells("B2:P3")
    header_cell = ws_dash["B2"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="2F5597")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Create Stacked Bar Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 11  # Built-in theme style index
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    
    data1 = Reference(ws_sum, min_col=2, max_col=4, min_row=1, max_row=5)
    cats1 = Reference(ws_sum, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    chart1.width = 18
    chart1.height = 14
    ws_dash.add_chart(chart1, "B5")
    
    # 5. Create Line Chart (Units Sold)
    chart2 = LineChart()
    chart2.style = 13
    chart2.title = "Units sold each month"
    
    data2 = Reference(ws_sum, min_col=2, min_row=7, max_row=11)
    cats2 = Reference(ws_sum, min_col=1, min_row=8, max_row=11)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    
    chart2.width = 13
    chart2.height = 7
    ws_dash.add_chart(chart2, "K5")
    
    # 6. Create Line Chart (Profit by Month)
    chart3 = LineChart()
    chart3.style = 13
    chart3.title = "Profit by month"
    
    data3 = Reference(ws_sum, min_col=2, min_row=13, max_row=17)
    cats3 = Reference(ws_sum, min_col=1, min_row=14, max_row=17)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    
    chart3.width = 13
    chart3.height = 7
    ws_dash.add_chart(chart3, "K12")
    
    # 7. Hide summary calculation sheet for clean UX
    ws_sum.sheet_state = 'hidden'
```