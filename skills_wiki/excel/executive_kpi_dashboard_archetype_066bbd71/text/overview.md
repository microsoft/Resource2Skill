### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive KPI Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Builds a clean, interactive-feeling presentation layer by disabling gridlines, establishing a bold merged header strip, and orchestrating a multi-chart layout (a primary stacked bar chart alongside vertically stacked trend lines). Abstracting the chart data to a separate backend worksheet keeps the presentation layer pristine.
* **Applicability**: Best for high-level management reports or automated dashboards where aggregated metrics need to be presented side-by-side without the visual noise of raw tables.

### 2. Structural Breakdown

- **Data Layout**: Pre-aggregated data blocks are constructed on a dedicated `Chart Data` worksheet. Each block is spaced out to define clear `openpyxl.chart.Reference` boundaries.
- **Formula Logic**: N/A for this presentation-focused layout (relies on pre-calculated/aggregated data inputs).
- **Visual Design**: The `Dashboard` sheet hides gridlines (`sheet_view.showGridLines = False`). A prominent banner title is created via merged cells with a solid background fill and bold, contrasting text.
- **Charts/Tables**: Utilizes a `BarChart` (`type="col"`, `grouping="stacked"`) for categorical breakdowns, and two `LineChart` objects for time-series trends. Legends are selectively disabled to reduce clutter.
- **Theme Hooks**: The title banner's background color consumes the primary theme color.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a multi-chart dashboard presentation layer powered by a hidden data sheet.
    Mimics the clean, gridless layout of an interactive Excel dashboard.
    """
    # 1. Setup Theme Fallbacks
    theme_colors = {
        "corporate_blue": "4F81BD",
        "midnight": "2C3E50",
        "forest": "27AE60"
    }
    primary_color = theme_colors.get(theme, "4F81BD")

    # 2. Initialize Dashboard Sheet
    dash_ws = wb.active
    dash_ws.title = "Dashboard"
    dash_ws.sheet_view.showGridLines = False

    # 3. Create Data Backend Sheet
    data_ws = wb.create_sheet(title="Chart Data")
    
    # --- Populate Data Sheet ---
    
    # Data Block 1: Stacked Bar (Profit by Market and Cookie)
    markets = ["India", "Philippines", "UK", "USA"]
    cookies = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"]
    data_ws.append(["Market"] + cookies)
    data_ws.append([markets[0], 62349, 23621, 21028, 25085])
    data_ws.append([markets[1], 54618, 24567, 22005, 8313])
    data_ws.append([markets[2], 46530, 26731, 11497, 14620])
    data_ws.append([markets[3], 36657, 32910, 22260, 9938])

    # Data Block 2: Line Chart 1 (Units Sold by Month)
    months = ["Sep", "Oct", "Nov", "Dec"]
    units = [50601, 95622, 65481, 52970]
    data_ws.append([]) # Spacer row
    line1_start_row = data_ws.max_row + 1
    data_ws.append(["Month", "Units Sold"])
    for m, u in zip(months, units):
        data_ws.append([m, u])

    # Data Block 3: Line Chart 2 (Profit by Month)
    profit = [124812, 228275, 160228, 136337]
    data_ws.append([]) # Spacer row
    line2_start_row = data_ws.max_row + 1
    data_ws.append(["Month", "Profit"])
    for m, p in zip(months, profit):
        data_ws.append([m, p])

    # --- Style Dashboard Header ---
    dash_ws.merge_cells("B2:Q4")
    header_cell = dash_ws["B2"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color="FFFFFF")
    header_cell.fill = PatternFill(start_color=primary_color, fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # --- Create Main Stacked Bar Chart ---
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.height = 14
    bar_chart.width = 16

    bar_data = Reference(data_ws, min_col=2, min_row=1, max_col=5, max_row=5)
    bar_cats = Reference(data_ws, min_col=1, min_row=2, max_row=5)
    bar_chart.add_data(bar_data, titles_from_data=True)
    bar_chart.set_categories(bar_cats)
    dash_ws.add_chart(bar_chart, "B6")

    # --- Create Top Line Chart (Units) ---
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.height = 7
    line1.width = 14
    line1.legend = None

    l1_data = Reference(data_ws, min_col=2, min_row=line1_start_row, max_row=line1_start_row+4)
    l1_cats = Reference(data_ws, min_col=1, min_row=line1_start_row+1, max_row=line1_start_row+4)
    line1.add_data(l1_data, titles_from_data=True)
    line1.set_categories(l1_cats)
    dash_ws.add_chart(line1, "J6")

    # --- Create Bottom Line Chart (Profit) ---
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.height = 7
    line2.width = 14
    line2.legend = None

    l2_data = Reference(data_ws, min_col=2, min_row=line2_start_row, max_row=line2_start_row+4)
    l2_cats = Reference(data_ws, min_col=1, min_row=line2_start_row+1, max_row=line2_start_row+4)
    line2.add_data(l2_data, titles_from_data=True)
    line2.set_categories(l2_cats)
    dash_ws.add_chart(line2, "J18")
```