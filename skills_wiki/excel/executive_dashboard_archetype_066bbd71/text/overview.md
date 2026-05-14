### 1. High-level Skill Pattern Extraction

> **Skill Name**: Executive Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Generates a clean, presentation-ready dashboard by disabling gridlines, constructing a branded header banner, and anchoring multiple stylized charts (Stacked Column, Line) to specific cell coordinates to simulate `Alt`-snapped grid alignment. Uses a hidden or separate data sheet for pre-aggregated chart sources.
* **Applicability**: Best for automated reporting pipelines (e.g., from `pandas`) where data is already aggregated and needs to be presented in a static, highly-polished executive view without requiring the end-user to manipulate Pivot Tables or Slicers.

### 2. Structural Breakdown

- **Data Layout**: A background "Data" sheet stores simple tabular summaries (e.g., Category x Metric). The "Dashboard" sheet acts purely as a canvas.
- **Formula Logic**: None required; this pattern relies on pre-calculated summary data written directly to the data sheet.
- **Visual Design**: Gridlines are disabled (`sheet.sheet_view.showGridLines = False`). A merged cell banner at the top uses theme-driven background fills and contrasting, large font sizes for the title.
- **Charts/Tables**: 
  - Chart 1: `BarChart` (`grouping="stacked"`, `overlap=100`) anchored for primary KPIs.
  - Chart 2 & 3: `LineChart` stacked vertically for trend analysis.
  - Anchors (e.g., `"B5"`, `"L5"`) simulate manual grid-snapping for perfect alignment.
- **Theme Hooks**: Consumes `primary` (header background) and `text` (header text) from the standard palette.

### 3. Reproduction Code

```python
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import PatternFill, Font, Alignment

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a clean, presentation-ready dashboard with multiple charts snapped to a grid layout.
    """
    # 1. Theme Configuration
    themes = {
        "corporate_blue": {"primary": "003366", "secondary": "4F81BD", "text": "FFFFFF"},
        "emerald_green": {"primary": "006633", "secondary": "339966", "text": "FFFFFF"},
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet(title="Data")
    
    # Clean the dashboard canvas
    ws_dash.sheet_view.showGridLines = False

    # 3. Create Dashboard Header Banner
    ws_dash.merge_cells("A1:Q3")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=palette["text"])
    header_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 4. Populate Background Data
    # Dataset 1: Market by Product (For Stacked Bar)
    table1_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin"],
        ["India", 62349, 23621, 21028],
        ["Philippines", 54618, 24567, 22005],
        ["United Kingdom", 46530, 26731, 11497],
        ["United States", 36657, 32910, 9938]
    ]
    for r in table1_data:
        ws_data.append(r)

    ws_data.append([]) # Spacer row
    start_row_t2 = ws_data.max_row + 1

    # Dataset 2: Trends over Time (For Line Charts)
    table2_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    for r in table2_data:
        ws_data.append(r)

    # 5. Build and Anchor Charts
    # Chart 1: Stacked Bar Chart (Main KPI)
    bc = BarChart()
    bc.type = "col"
    bc.style = 10
    bc.grouping = "stacked"
    bc.overlap = 100
    bc.title = "Profit by Market & Cookie Type"
    bc.height = 12
    bc.width = 18

    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    bc.add_data(data_ref, titles_from_data=True)
    bc.set_categories(cats_ref)
    
    # Anchor to cell to simulate Alt-snapping
    ws_dash.add_chart(bc, "B5")

    # Chart 2: Top Line Chart (Secondary KPI)
    lc1 = LineChart()
    lc1.title = "Units sold each month"
    lc1.style = 13
    lc1.height = 6
    lc1.width = 12
    
    lc1_data = Reference(ws_data, min_col=2, min_row=start_row_t2, max_row=start_row_t2+4)
    lc1_cats = Reference(ws_data, min_col=1, min_row=start_row_t2+1, max_row=start_row_t2+4)
    lc1.add_data(lc1_data, titles_from_data=True)
    lc1.set_categories(lc1_cats)
    
    ws_dash.add_chart(lc1, "K5")

    # Chart 3: Bottom Line Chart (Secondary KPI)
    lc2 = LineChart()
    lc2.title = "Profit by month"
    lc2.style = 13
    lc2.height = 6
    lc2.width = 12
    
    lc2_data = Reference(ws_data, min_col=3, min_row=start_row_t2, max_row=start_row_t2+4)
    lc2.add_data(lc2_data, titles_from_data=True)
    lc2.set_categories(lc1_cats)
    
    ws_dash.add_chart(lc2, "K17")
```