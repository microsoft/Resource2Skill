### 1. High-level Skill Pattern Extraction

> **Skill Name**: Static Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Generates a presentation-ready dashboard layout. Since `openpyxl` cannot create live PivotTables or interactive Slicers, this pattern routes pre-aggregated data to a hidden calculation sheet, binds `BarChart` and `LineChart` objects to it, and styles the active sheet as a software interface by disabling gridlines/headers, rendering a header banner, and constructing a mockup control panel. 
* **Applicability**: Best used when generating management reports where data aggregation is handled upstream (e.g., in `pandas`). It produces an elegant, locked-down dashboard view matching the visual layout of advanced Excel interactive dashboards.

### 2. Structural Breakdown

- **Data Layout**: Summary data is written to a dedicated sheet (`CalcData`) which is subsequently hidden from the user (`sheet_state = 'hidden'`).
- **Formula Logic**: No direct formulas are used; relies entirely on upstream data aggregation before charting.
- **Visual Design**: Uses `ws.sheet_view.showGridLines = False` and `ws.sheet_view.showRowColHeaders = False` for a clean canvas. Left column simulates interactive slicers via light gray fills and thin borders. Top row merges horizontally for a prominent theme-colored banner.
- **Charts/Tables**: Employs a 100% Stacked Column Chart for comparative dimensions (Profit by Market & Cookie Type) and a Line Chart for time-series trends (Units Sold). Legends are stripped where unnecessary to maximize plot area.
- **Theme Hooks**: Consumes `primary` for the banner background, `text_light` for banner text, and `bg_light` / `border` for the slicer panel mockups.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

def get_theme(theme_name: str) -> dict:
    """Fallback theme loader."""
    themes = {
        "corporate_blue": {
            "primary": "203764",
            "secondary": "4F81BD",
            "bg_light": "F2F2F2",
            "text_light": "FFFFFF",
            "border": "D9D9D9"
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = get_theme(theme)
    
    # 1. Setup Data Sheet (Hidden) - Pre-aggregated data injected here
    calc_ws = wb.active
    calc_ws.title = "CalcData"
    
    summary_data = [
        ["Month", "Fortune Cookie", "Sugar", "Chocolate Chip", "Total Units"],
        ["Sep", 4872, 8313, 23621, 50601],
        ["Oct", 7026, 14947, 24567, 95622],
        ["Nov", 5538, 19446, 26731, 65481],
        ["Dec", 6369, 10633, 32910, 52970],
    ]
    for row in summary_data:
        calc_ws.append(row)
    
    # Hide the calculation sheet to maintain the illusion of a standalone dashboard
    calc_ws.sheet_state = 'hidden'
    
    # 2. Setup Dashboard Sheet
    ws = wb.create_sheet("Dashboard", 0)
    wb.active = ws
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    
    # 3. Header Banner
    ws.merge_cells("A1:M3")
    header = ws["A1"]
    header.value = title
    header.font = Font(color=palette["text_light"], size=24, bold=True)
    header.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    header.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    
    # 4. Slicer / Control Mockup Panel (Left Column)
    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 2
    
    thin_border = Border(
        top=Side(style="thin", color=palette["border"]),
        left=Side(style="thin", color=palette["border"]),
        right=Side(style="thin", color=palette["border"]),
        bottom=Side(style="thin", color=palette["border"])
    )
    gray_fill = PatternFill(start_color=palette["bg_light"], end_color=palette["bg_light"], fill_type="solid")
    
    # Mocking Slicer elements for layout completeness
    ws["A5"] = "Date Filters"
    ws["A5"].font = Font(bold=True)
    ws["A6"] = "All Periods"
    ws["A6"].fill = gray_fill
    ws["A6"].border = thin_border
    
    ws["A9"] = "Market"
    ws["A9"].font = Font(bold=True)
    markets = ["India", "Malaysia", "Philippines", "United Kingdom", "United States"]
    for i, m in enumerate(markets):
        cell = ws.cell(row=10+i, column=1, value=m)
        cell.fill = gray_fill
        cell.border = thin_border
        
    ws["A16"] = "Product"
    ws["A16"].font = Font(bold=True)
    products = ["Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"]
    for i, p in enumerate(products):
        cell = ws.cell(row=17+i, column=1, value=p)
        cell.fill = gray_fill
        cell.border = thin_border
        
    # 5. Insert Charts
    # Chart A: Stacked Column Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.style = 10 
    
    data_ref = Reference(calc_ws, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref = Reference(calc_ws, min_col=1, min_row=2, max_row=5)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    
    bar_chart.width = 16
    bar_chart.height = 8.5
    ws.add_chart(bar_chart, "C5")
    
    # Chart B: Line Chart
    line_chart = LineChart()
    line_chart.title = "Units sold each month"
    line_chart.style = 13
    
    line_data = Reference(calc_ws, min_col=5, min_row=1, max_row=5)
    line_chart.add_data(line_data, titles_from_data=True)
    line_chart.set_categories(cats_ref)
    line_chart.legend = None  # Remove legend for single-series charts
    
    line_chart.width = 16
    line_chart.height = 8.5
    ws.add_chart(line_chart, "H5")
    
    # 6. Adjust central layout columns for chart breathing room
    for col in range(3, 14):
        ws.column_dimensions[get_column_letter(col)].width = 10
```