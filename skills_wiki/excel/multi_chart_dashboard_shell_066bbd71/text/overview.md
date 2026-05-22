### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Configures a clean, presentation-ready dashboard worksheet by disabling gridlines, applying a bold centralized title, and anchoring multiple generated charts (a stacked bar and dual line charts) into a carefully aligned grid layout.
* **Applicability**: Best used for presenting key performance indicators and aggregated metrics visually. Because openpyxl cannot generate live PivotCaches or interactive Slicers from scratch, this pattern is ideal for rendering a static, aligned "dashboard view" over pre-aggregated backend data.

### 2. Structural Breakdown

- **Data Layout**: Stores the underlying aggregated chart data in off-screen columns (e.g., Column `AA` onwards) to keep the main view clean.
- **Formula Logic**: Relies on pre-calculated absolute values pushed directly into the hidden data ranges.
- **Visual Design**: The sheet view is scrubbed of default gridlines (`ws.sheet_view.showGridLines = False`), and a prominent main header is merged across the top of the dashboard.
- **Charts/Tables**: Utilizes a Stacked Column Chart (`type="col"`, `grouping="stacked"`) for categorical compositions, and two Line Charts stacked vertically for time-series trends.
- **Theme Hooks**: The title font color and the built-in chart color styles (integer ID mapping) adapt based on the injected `theme` name.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, Alignment

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a clean, multi-chart dashboard shell using pre-aggregated mock data.
    Aligns a stacked bar chart on the left, and two line charts on the right.
    """
    ws = wb.create_sheet(sheet_name)
    
    # 1. Clean up visual layout
    ws.sheet_view.showGridLines = False

    # Theme mapping for chart styles and title
    theme_map = {
        "corporate_blue": {"style": 2, "title_color": "002060"},
        "warm_earth": {"style": 14, "title_color": "5c3a21"},
        "vibrant": {"style": 11, "title_color": "000000"}
    }
    t = theme_map.get(theme, {"style": 2, "title_color": "000000"})

    # 2. Main Title
    ws["B2"] = title
    ws["B2"].font = Font(size=24, bold=True, color=t["title_color"])
    ws.merge_cells("B2:P2")
    ws["B2"].alignment = Alignment(horizontal="center", vertical="center")

    # 3. Write Pre-Aggregated Data to an off-screen area (Column AA onwards)
    # Chart 1 Data: Profit by Market & Product (Stacked Bar)
    c1_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62349, 4872, 21028],
        ["Philippines", 54618, 7026, 22005],
        ["United Kingdom", 46530, 5220, 11497],
        ["United States", 36657, 6369, 22260]
    ]
    for r_idx, row in enumerate(c1_data, start=1):
        for c_idx, val in enumerate(row, start=27): # AA
            ws.cell(row=r_idx, column=c_idx, value=val)

    # Chart 2 Data: Units sold each month (Line)
    c2_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    for r_idx, row in enumerate(c2_data, start=10):
        for c_idx, val in enumerate(row, start=27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # Chart 3 Data: Profit by month (Line)
    c3_data = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    for r_idx, row in enumerate(c3_data, start=20):
        for c_idx, val in enumerate(row, start=27):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 4. Create and Anchor Charts
    
    # Left Stacked Bar Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.style = t["style"]
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    
    data_c1 = Reference(ws, min_col=28, min_row=1, max_col=30, max_row=5)
    cats_c1 = Reference(ws, min_col=27, min_row=2, max_row=5)
    bar_chart.add_data(data_c1, titles_from_data=True)
    bar_chart.set_categories(cats_c1)
    bar_chart.height = 14
    bar_chart.width = 16
    ws.add_chart(bar_chart, "B4")

    # Top Right Line Chart
    line1 = LineChart()
    line1.style = t["style"]
    line1.title = "Units sold each month"
    line1.legend = None
    data_c2 = Reference(ws, min_col=28, min_row=10, max_row=14)
    cats_c2 = Reference(ws, min_col=27, min_row=11, max_row=14)
    line1.add_data(data_c2, titles_from_data=True)
    line1.set_categories(cats_c2)
    line1.height = 7
    line1.width = 14
    ws.add_chart(line1, "J4")

    # Bottom Right Line Chart
    line2 = LineChart()
    line2.style = t["style"]
    line2.title = "Profit by month"
    line2.legend = None
    data_c3 = Reference(ws, min_col=28, min_row=20, max_row=24)
    cats_c3 = Reference(ws, min_col=27, min_row=21, max_row=24)
    line2.add_data(data_c3, titles_from_data=True)
    line2.set_categories(cats_c3)
    line2.height = 7
    line2.width = 14
    ws.add_chart(line2, "J11")
```