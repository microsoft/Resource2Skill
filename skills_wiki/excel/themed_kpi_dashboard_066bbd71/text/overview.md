### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard

* **Tier**: archetype
* **Core Mechanism**: Construct a presentation-ready dashboard layer that hides a backend data sheet. Configures a grid layout featuring a designated filter control panel on the left, a large primary composition chart in the center, and vertically stacked secondary trend charts on the right, while turning off sheet gridlines for a clean canvas.
* **Applicability**: Use when building executive summaries or reporting portals. Designed for high-level aggregated metrics requiring a mixture of composition (stacked bar) and time-series (line) analysis on a single screen.

### 2. Structural Breakdown

- **Data Layout**: Backend `ChartData` sheet holds discrete tables for each chart (Category $\times$ Subcategory matrix, and two Date $\times$ Value tables). It is hidden from the end user.
- **Formula Logic**: N/A (Uses static summary data simulating Pivot Table/cache outputs).
- **Visual Design**: Borderless canvas (`showGridLines = False`), dark high-contrast merged header, and a subtle gray placeholder block reserved for Slicer widgets.
- **Charts/Tables**: One Stacked Column chart (`type="col"`, `grouping="stacked"`) and two Line charts. Legends are removed from the line charts to maximize the data-ink ratio.
- **Theme Hooks**: Consumes `header_bg` and `header_fg` for the title ribbon, and `panel_bg` for the control sidebar.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Setup sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet("ChartData")
    
    # Hide worksheet gridlines for a clean "dashboard" canvas look
    ws_dash.sheet_view.showGridLines = False
    
    # 2. Populate Chart Data
    data_stacked = [
        ["Country", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Snickerdoodle"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["United States", 36657, 6368, 22260, 9937],
    ]
    for row in data_stacked:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row 6
    
    trend1_start = ws_data.max_row + 1 # Row 7
    data_trend1 = [
        ["Month", "Units Sold"],
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970],
    ]
    for row in data_trend1:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row 12
    
    trend2_start = ws_data.max_row + 1 # Row 13
    data_trend2 = [
        ["Month", "Profit"],
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337],
    ]
    for row in data_trend2:
        ws_data.append(row)
        
    # Hide the backend data sheet
    ws_data.sheet_state = "hidden"
    
    # 3. Build Header
    themes = {
        "corporate_blue": {"header_bg": "203764", "header_fg": "FFFFFF", "panel_bg": "F2F2F2"},
        "emerald": {"header_bg": "005A36", "header_fg": "FFFFFF", "panel_bg": "E6F0EC"},
        "slate": {"header_bg": "3B3838", "header_fg": "FFFFFF", "panel_bg": "F2F2F2"},
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    ws_dash.merge_cells("A1:R2")
    header_cell = ws_dash["A1"]
    header_cell.value = title
    header_cell.font = Font(size=22, bold=True, color=palette["header_fg"])
    header_cell.fill = PatternFill(fill_type="solid", start_color=palette["header_bg"])
    header_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 4. Build Filter/Slicer Placeholder Panel
    ws_dash.merge_cells("A4:C10")
    panel_cell = ws_dash["A4"]
    panel_cell.value = "Interactive Filters\n(Insert Slicers Here)"
    panel_cell.font = Font(color="555555", italic=True)
    panel_cell.fill = PatternFill(fill_type="solid", start_color=palette["panel_bg"])
    panel_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    thin_border = Border(
        top=Side(border_style="thin", color="CCCCCC"),
        left=Side(border_style="thin", color="CCCCCC"),
        right=Side(border_style="thin", color="CCCCCC"),
        bottom=Side(border_style="thin", color="CCCCCC")
    )
    for row in ws_dash.iter_rows(min_row=4, max_row=10, min_col=1, max_col=3):
        for cell in row:
            cell.border = thin_border
            
    # 5. Add Stacked Column Chart (Composition)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Product"
    chart1.width = 16
    chart1.height = 10
    
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=5)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    ws_dash.add_chart(chart1, "E4")
    
    # 6. Add Units Sold Line Chart (Trend 1)
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.width = 11
    chart2.height = 7
    chart2.legend = None  # Clean look
    
    data2 = Reference(ws_data, min_col=2, min_row=trend1_start, max_col=2, max_row=trend1_start+4)
    cats2 = Reference(ws_data, min_col=1, min_row=trend1_start+1, max_row=trend1_start+4)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    ws_dash.add_chart(chart2, "N4")
    
    # 7. Add Profit Line Chart (Trend 2)
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.width = 11
    chart3.height = 7
    chart3.legend = None  # Clean look
    
    data3 = Reference(ws_data, min_col=2, min_row=trend2_start, max_col=2, max_row=trend2_start+4)
    cats3 = Reference(ws_data, min_col=1, min_row=trend2_start+1, max_row=trend2_start+4)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    ws_dash.add_chart(chart3, "N19")
```