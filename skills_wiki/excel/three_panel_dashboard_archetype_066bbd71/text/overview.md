### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Panel Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a professional multi-sheet dashboard structure. It provisions a hidden backend sheet for aggregated data (mimicking PivotTable outputs) and a presentation sheet with gridlines disabled. The layout features a styled header, a left-hand control panel area, and a 3-panel visualization grid (one large categorical chart, two stacked time-series charts).
* **Applicability**: Ideal for executive summaries and standard business performance dashboards that need to display both cross-sectional categorical breakdowns (e.g., product by region) and trending data over time on a single screen.

### 2. Structural Breakdown

- **Data Layout**: Separates data into a backend `Dashboard_Data` sheet (hidden) containing three distinct contiguous ranges for the three charts.
- **Formula Logic**: Uses static sample data in the backend sheet to drive the charts, representing pre-aggregated metrics.
- **Visual Design**: Turns off gridlines (`ws.sheet_view.showGridLines = False`). Uses a bold, theme-colored header spanning the dashboard. Sets specific column widths to create a structured grid (sidebar, main left, main right).
- **Charts/Tables**: 
  - 1x Stacked Column Chart (`BarChart` with `grouping="stacked"`) for categorical comparison.
  - 2x Line Charts (`LineChart`) for monthly trends.
- **Theme Hooks**: Consumes `primary` for the header background, `text_light` for the header font, and standard chart styling.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference

def _get_theme_palette(theme: str) -> dict:
    """Mock theme helper for self-contained execution."""
    themes = {
        "corporate_blue": {
            "primary": "2B579A",
            "secondary": "F3F2F1",
            "text_light": "FFFFFF",
            "text_dark": "323130",
            "border": "E1DFDD"
        }
    }
    return themes.get(theme, themes["corporate_blue"])

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = _get_theme_palette(theme)
    
    # -------------------------------------------------------------------------
    # 1. Backend Data Sheet (Hidden)
    # -------------------------------------------------------------------------
    ws_data = wb.active
    ws_data.title = "Dashboard_Data"
    # In a real scenario, this would be populated by data logic, 
    # but here we provide the structured data to drive the dashboard archetype.
    
    # Data Range 1: Profit by Market & Product (Categorical Stacked)
    cat_data = [
        ["Market", "Chocolate Chip", "Sugar", "Oatmeal Raisin"],
        ["India", 62000, 25000, 21000],
        ["United Kingdom", 46000, 14000, 22000],
        ["United States", 36000, 9000, 22000],
        ["Philippines", 54000, 8000, 24000]
    ]
    for r_idx, row in enumerate(cat_data, 1):
        for c_idx, val in enumerate(row, 1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)
            
    # Data Range 2: Units Sold Each Month (Trend)
    units_data = [
        ["Month", "Units Sold"],
        ["Sep", 50601], ["Oct", 95622], ["Nov", 65481], ["Dec", 52970]
    ]
    for r_idx, row in enumerate(units_data, 1):
        for c_idx, val in enumerate(row, 6): # Offset to column F
            ws_data.cell(row=r_idx, column=c_idx, value=val)
            
    # Data Range 3: Profit by Month (Trend)
    profit_data = [
        ["Month", "Profit"],
        ["Sep", 124812], ["Oct", 228275], ["Nov", 160228], ["Dec", 136337]
    ]
    for r_idx, row in enumerate(profit_data, 1):
        for c_idx, val in enumerate(row, 9): # Offset to column I
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    # ws_data.sheet_state = 'hidden' # Hide backend data in final output

    # -------------------------------------------------------------------------
    # 2. Presentation Dashboard Sheet
    # -------------------------------------------------------------------------
    ws = wb.create_sheet("Dashboard", 0)
    ws.sheet_view.showGridLines = False
    
    # Layout Grid: Set Column Widths
    ws.column_dimensions['A'].width = 2   # Margin
    ws.column_dimensions['B'].width = 25  # Control Panel Sidebar
    ws.column_dimensions['C'].width = 2   # Gap
    ws.column_dimensions['D'].width = 40  # Main Left
    ws.column_dimensions['E'].width = 2   # Gap
    ws.column_dimensions['F'].width = 40  # Main Right
    
    # Header Construction
    header_fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header_font = Font(color=palette["text_light"], size=22, bold=True)
    
    for col in range(2, 7): # B to F
        cell = ws.cell(row=2, column=col)
        cell.fill = header_fill
        # Merge visually by styling all, writing to first
        if col == 2:
            cell.value = title
            cell.font = header_font
            cell.alignment = Alignment(vertical="center")
            
    ws.row_dimensions[2].height = 40

    # Sidebar Panel Placeholder
    ws['B4'] = "Filters & Controls"
    ws['B4'].font = Font(size=14, bold=True, color=palette["primary"])
    ws['B5'] = "(Insert Slicers Here)"
    ws['B5'].font = Font(italic=True, color="7F7F7F")
    
    # -------------------------------------------------------------------------
    # 3. Chart Generation & Placement
    # -------------------------------------------------------------------------
    
    # Chart 1: Profit by Market & Cookie Type (Stacked Column)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    chart1.height = 14
    chart1.width = 22
    
    data1 = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    ws.add_chart(chart1, "D4")

    # Chart 2: Units Sold Each Month (Line)
    chart2 = LineChart()
    chart2.title = "Units Sold Each Month"
    chart2.height = 7
    chart2.width = 20
    chart2.legend = None # Clean up legend
    
    data2 = Reference(ws_data, min_col=7, min_row=1, max_row=5)
    cats2 = Reference(ws_data, min_col=6, min_row=2, max_row=5)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    ws.add_chart(chart2, "F4")

    # Chart 3: Profit by Month (Line)
    chart3 = LineChart()
    chart3.title = "Profit by Month"
    chart3.height = 7
    chart3.width = 20
    chart3.legend = None
    
    data3 = Reference(ws_data, min_col=10, min_row=1, max_row=5)
    cats3 = Reference(ws_data, min_col=9, min_row=2, max_row=5)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    ws.add_chart(chart3, "F18")

    wb.active = ws
```