### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Three-Panel Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Generates a professional dashboard interface by disabling standard Excel UI elements (gridlines, row/col headers), establishing a prominent themed title banner, and orchestrating a multi-chart layout (one primary stacked column, two secondary trend lines) driven by a hidden backend data sheet.
* **Applicability**: Ideal for executive summaries and performance overviews where a primary categorical breakdown needs to be displayed alongside supporting time-series metrics without distracting spreadsheet grid elements.

### 2. Structural Breakdown

- **Data Layout**: Summarized tabular data placed on a separate, hidden `Data` sheet to keep the presentation layer clean.
- **Formula Logic**: None (relies on direct chart data references to the backend sheet).
- **Visual Design**: 
  - `sheet_view.showGridLines = False` and `sheet_view.showRowColHeaders = False` create a blank canvas effect.
  - Large merged banner (B2:M4) for the title with centered alignment and solid fill.
- **Charts/Tables**: 
  - Main Chart (Left): Stacked Column Chart for categorical composition.
  - Secondary Charts (Right): Two Line Charts stacked vertically for time-series trends. Legends removed to maximize plot area.
- **Theme Hooks**: Consumes `bg` and `fg` from the active theme to style the header banner.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Theme Setup
    themes = {
        "corporate_blue": {"bg": "1F4E78", "fg": "FFFFFF"},
        "executive_dark": {"bg": "262626", "fg": "FFFFFF"},
        "emerald_green": {"bg": "005A36", "fg": "FFFFFF"}
    }
    t_colors = themes.get(theme, themes["corporate_blue"])

    # 2. Setup Dashboard Sheet
    dash_ws = wb.active
    dash_ws.title = "Dashboard"
    
    # The crucial steps for a "Dashboard" look: disable gridlines and headers
    dash_ws.sheet_view.showGridLines = False
    dash_ws.sheet_view.showRowColHeaders = False

    # Add Title Banner
    dash_ws.merge_cells("B2:M4")
    title_cell = dash_ws["B2"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=t_colors["fg"])
    title_cell.fill = PatternFill(start_color=t_colors["bg"], end_color=t_colors["bg"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Setup Backend Data Sheet
    data_ws = wb.create_sheet(title="Backend Data")

    # Mock Data: Profit by Market & Product
    markets = ["India", "Philippines", "United Kingdom", "Malaysia", "United States"]
    products = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"]
    market_data = [
        ["Market"] + products,
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["Malaysia", 46587, 5537, 17536, 20555],
        ["United States", 36657, 6368, 22260, 9937]
    ]
    for row in market_data:
        data_ws.append(row)

    # Mock Data: Monthly Trends
    month_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    start_row_trends = len(market_data) + 3
    for i, row in enumerate(month_data):
        for j, val in enumerate(row):
            data_ws.cell(row=start_row_trends + i, column=j + 1, value=val)

    # 4. Create and Position Charts
    
    # Chart A: Stacked Column (Left Panel)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.style = 11

    bar_data = Reference(data_ws, min_col=2, min_row=1, max_col=len(products)+1, max_row=len(markets)+1)
    bar_cats = Reference(data_ws, min_col=1, min_row=2, max_row=len(markets)+1)
    bar_chart.add_data(bar_data, titles_from_data=True)
    bar_chart.set_categories(bar_cats)

    dash_ws.add_chart(bar_chart, "B6")
    bar_chart.width = 16
    bar_chart.height = 14

    # Chart B: Line Chart - Units Sold (Top Right Panel)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.style = 12
    line1.legend = None # Remove legend for cleaner look as per video
    
    trend_cats = Reference(data_ws, min_col=1, min_row=start_row_trends+1, max_row=start_row_trends+4)
    line1_data = Reference(data_ws, min_col=2, min_row=start_row_trends, max_row=start_row_trends+4)
    line1.add_data(line1_data, titles_from_data=True)
    line1.set_categories(trend_cats)

    dash_ws.add_chart(line1, "I6")
    line1.width = 14
    line1.height = 7

    # Chart C: Line Chart - Profit (Bottom Right Panel)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.style = 12
    line2.legend = None
    
    line2_data = Reference(data_ws, min_col=3, min_row=start_row_trends, max_row=start_row_trends+4)
    line2.add_data(line2_data, titles_from_data=True)
    line2.set_categories(trend_cats)

    dash_ws.add_chart(line2, "I13")
    line2.width = 14
    line2.height = 7

    # 5. Hide the Backend Data Sheet
    data_ws.sheet_state = 'hidden'
```