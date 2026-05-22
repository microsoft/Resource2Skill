### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Panel Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Creates an app-like dashboard layout by disabling gridlines, building a dark-themed banner header, reserving a left-hand column for filters (slicers), and orchestrating three distinct charts (Line for trends, Column for comparisons, Bar for rankings) driven by a hidden background data sheet.
* **Applicability**: Best used for executive summaries or KPI reporting. Transforms flat data into a professional, presentation-ready layout that mimics business intelligence software directly within Excel. 

### 2. Structural Breakdown

- **Data Layout**: A separate, hidden `Data` sheet stores aggregated summary tables. The main `Dashboard` sheet contains no raw data grids, only visual elements.
- **Formula Logic**: (Not applicable for the shell itself, relies on pre-aggregated data).
- **Visual Design**: Gridlines are disabled (`showGridLines = False`). A continuous top banner is created via merged cells, filled with the primary theme color and large, white text. A dedicated sidebar area is shaded lightly to house interactive controls.
- **Charts/Tables**: 
  - Top: Line Chart spanning the full width (Monthly Revenue Trend).
  - Bottom Left: Clustered Column Chart (Product Category Comparison).
  - Bottom Right: Clustered Bar Chart (Top 5 States by Profit).
- **Theme Hooks**: Utilizes `primary` for the header banner, `bg` for the filter sidebar, and `text_light` for header text.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a professional 3-panel dashboard shell with a left-side filter pane.
    Generates hidden sample data to power the charts.
    """
    # 1. Theme Palette Fallback
    palette = {
        "primary": "003366",     # Dark blue banner
        "secondary": "4F81BD",   # Lighter blue
        "bg": "F2F2F2",          # Light gray sidebar
        "border": "D9D9D9",      # Soft borders
        "text_light": "FFFFFF",  # White text
        "text_dark": "000000"    # Black text
    }
    try:
        from skills_library.excel.components._helpers import get_theme_palette
        theme_colors = get_theme_palette(theme)
        palette.update(theme_colors)
    except ImportError:
        pass

    # 2. Setup Hidden Data Sheet
    ws_data = wb.create_sheet(f"{sheet_name}_Data")
    ws_data.sheet_state = 'hidden'

    # Trend Data (A1:B13)
    trend_data = [
        ["Month", "Revenue"],
        ["Jan", 15200], ["Feb", 18100], ["Mar", 16500], ["Apr", 21000],
        ["May", 22500], ["Jun", 24000], ["Jul", 23100], ["Aug", 26400],
        ["Sep", 25800], ["Oct", 28000], ["Nov", 31200], ["Dec", 35000]
    ]
    for row in trend_data:
        ws_data.append(row)

    # Category Data (D1:F3)
    cat_data = [
        ["Category", "2023", "2024"],
        ["Hoodies", 75000, 92000],
        ["T-shirts", 81000, 105000]
    ]
    for i, row in enumerate(cat_data, start=1):
        for j, val in enumerate(row, start=4):
            ws_data.cell(row=i, column=j, value=val)

    # Top Ranking Data (H1:I6)
    top_data = [
        ["State", "Profit"],
        ["California", 45200],
        ["New York", 38100],
        ["Texas", 34500],
        ["Florida", 29800],
        ["Illinois", 26400]
    ]
    for i, row in enumerate(top_data, start=1):
        for j, val in enumerate(row, start=8):
            ws_data.cell(row=i, column=j, value=val)

    # 3. Setup Dashboard Sheet
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 4. Create Header Banner
    header_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header_font = Font(name="Calibri", size=24, bold=True, color=palette["text_light"])
    header_align = Alignment(horizontal="left", vertical="center", indent=1)
    
    ws.merge_cells("D2:S4")
    header_cell = ws["D2"]
    header_cell.value = title
    header_cell.fill = header_fill
    header_cell.font = header_font
    header_cell.alignment = header_align

    # Fill remaining header space to keep the colored band continuous
    for col in range(2, 20):  # B to S
        if col < 4:
            ws.cell(row=2, column=col).fill = header_fill
            ws.merge_cells(start_row=2, start_column=col, end_row=4, end_column=col)

    # 5. Sidebar Pane (Mocking Slicer Area)
    sidebar_fill = PatternFill(start_color=palette["bg"], end_color=palette["bg"], fill_type="solid")
    sidebar_border = Border(right=Side(style="thin", color=palette["border"]))
    
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 12

    for row in range(5, 35):
        for col in [2, 3]:
            cell = ws.cell(row=row, column=col)
            cell.fill = sidebar_fill
            if col == 3:
                cell.border = sidebar_border

    # Mock Slicer Label
    ws.merge_cells("B6:C6")
    filter_title = ws["B6"]
    filter_title.value = "FILTERS"
    filter_title.font = Font(bold=True, color=palette["primary"])
    filter_title.alignment = Alignment(horizontal="center")

    # 6. Chart 1: Monthly Trend (Line)
    chart_trend = LineChart()
    chart_trend.title = "Monthly Revenue Trend"
    chart_trend.style = 13
    chart_trend.y_axis.title = "Revenue (USD)"
    chart_trend.width = 24
    chart_trend.height = 8

    data_trend = Reference(ws_data, min_col=2, min_row=1, max_row=13)
    cats_trend = Reference(ws_data, min_col=1, min_row=2, max_row=13)
    chart_trend.add_data(data_trend, titles_from_data=True)
    chart_trend.set_categories(cats_trend)
    ws.add_chart(chart_trend, "D6")

    # 7. Chart 2: Category Comparison (Column)
    chart_cat = BarChart()
    chart_cat.type = "col"
    chart_cat.style = 10
    chart_cat.title = "Units Sold: T-Shirts vs Hoodies"
    chart_cat.width = 11.5
    chart_cat.height = 9

    data_cat = Reference(ws_data, min_col=5, max_col=6, min_row=1, max_row=3)
    cats_cat = Reference(ws_data, min_col=4, min_row=2, max_row=3)
    chart_cat.add_data(data_cat, titles_from_data=True)
    chart_cat.set_categories(cats_cat)
    chart_cat.shape = 4
    ws.add_chart(chart_cat, "D19")

    # 8. Chart 3: Top States (Bar)
    chart_top = BarChart()
    chart_top.type = "bar"
    chart_top.style = 10
    chart_top.title = "Top 5 States by Profit"
    chart_top.width = 11.5
    chart_top.height = 9
    chart_top.legend = None

    data_top = Reference(ws_data, min_col=9, min_row=1, max_row=6)
    cats_top = Reference(ws_data, min_col=8, min_row=2, max_row=6)
    chart_top.add_data(data_top, titles_from_data=True)
    chart_top.set_categories(cats_top)
    ws.add_chart(chart_top, "K19")
```