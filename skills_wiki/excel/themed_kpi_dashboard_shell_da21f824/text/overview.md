# Themed KPI Dashboard Shell

## Applicability

Ideal for high-level summary reports, executive dashboards, or visually driven KPI sheets. Use when you want to abstract away standard Excel grid mechanics and present polished charts and metrics in a web-like UI.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed KPI Dashboard Shell

* **Tier**: archetype
* **Core Mechanism**: Constructs a clean, application-like presentation layer by hiding worksheet gridlines and headers, establishing a dedicated layout grid (sidebar + main content), and embedding Openpyxl charts anchored to specific functional zones.
* **Applicability**: Ideal for high-level summary reports, executive dashboards, or visually driven KPI sheets. Use when you want to abstract away standard Excel grid mechanics and present polished charts and metrics in a web-like UI.

### 2. Structural Breakdown

- **Data Layout**: A hidden or backend "Data" sheet stores clean tabular summaries. The frontend "Dashboard" sheet uses structural column widths (e.g., narrow columns as visual padding/spacers) to arrange elements.
- **Formula Logic**: None natively required; relies on structured chart references to the backend data sheet. 
- **Visual Design**: Disables native Excel `showGridLines` and `showRowColHeaders` for a clean canvas. Uses merged cell regions to create a solid-fill top banner and a dedicated left-sidebar area (reserved for Slicers or instructional text).
- **Charts/Tables**: Implements a stacked column chart for compositional data and multiple line charts for trend data. Charts are strictly sized in cm and anchored to explicit cells (e.g., `E6`, `N6`) to mimic a CSS grid layout.
- **Theme Hooks**: Consumes `primary` for the top branding banner background and standard contrasting text (`text_light`). Uses `surface_alt` or a light gray (`#F2F2F2`) for the sidebar panel.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds an executive dashboard with a branded header, a left sidebar zone, 
    and a grid of KPI charts driven by a backend data sheet.
    """
    # 1. Clean up default sheets
    for sheet in wb.sheetnames:
        wb.remove(wb[sheet])
        
    # 2. Add backend Data Sheet
    ws_data = wb.create_sheet("Data")
    
    # Monthly trend data
    ws_data.append(["Month", "Units Sold", "Profit"])
    monthly_data = [
        ("Sep", 50601, 124812),
        ("Oct", 95622, 228275),
        ("Nov", 65481, 160228),
        ("Dec", 52970, 136337)
    ]
    for row in monthly_data:
        ws_data.append(row)
        
    ws_data.append([]) # Spacer row 6
    
    # Category composition data (Rows 7-11)
    ws_data.append(["Market", "Fortune Cookie", "Sugar", "Snickerdoodle", "Oatmeal Raisin", "Chocolate Chip"])
    market_data = [
        ("India", 4872, 18561, 25085, 21028, 62349),
        ("Philippines", 7026, 14947, 8313, 22005, 54618),
        ("United Kingdom", 1220, 124044, 5220, 11497, 46530),
        ("United States", 6369, 117319, 9938, 22260, 36657)
    ]
    for row in market_data:
        ws_data.append(row)
        
    # 3. Create Frontend Dashboard Sheet
    ws_dash = wb.create_sheet("Dashboard", 0) # Place at front
    ws_dash.sheet_view.showGridLines = False
    ws_dash.sheet_view.showRowColHeaders = False
    
    # Theme fallbacks
    primary_color = kwargs.get("primary_color", "203764")
    sidebar_color = kwargs.get("sidebar_color", "F2F2F2")
    
    # Build Top Title Banner
    ws_dash.merge_cells("A1:U4")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color=primary_color, end_color=primary_color, fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Build Sidebar Placeholder (Designated zone for Slicers in Excel UI)
    ws_dash.merge_cells("A6:C30")
    sidebar = ws_dash["A6"]
    sidebar.value = "Interactive Filters\n(Add Slicers Here)"
    sidebar.font = Font(italic=True, color="7F7F7F")
    sidebar.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    sidebar.fill = PatternFill(start_color=sidebar_color, end_color=sidebar_color, fill_type="solid")
    
    # Format structural column widths for padding
    ws_dash.column_dimensions['D'].width = 2
    ws_dash.column_dimensions['M'].width = 2
    
    # --- Chart 1: Stacked Bar Chart (Profit by Market) ---
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    
    data_ref = Reference(ws_data, min_col=2, min_row=7, max_col=6, max_row=11)
    cats_ref = Reference(ws_data, min_col=1, min_row=8, max_row=11)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    bar_chart.height = 13.5
    bar_chart.width = 16
    bar_chart.legend.position = "b" # Move legend to bottom for clean horizontal layout
    
    ws_dash.add_chart(bar_chart, "E6")
    
    # --- Chart 2: Line Chart 1 (Units Sold Trend) ---
    lc1 = LineChart()
    lc1.title = "Units sold each month"
    lc1.style = 13
    lc1_data = Reference(ws_data, min_col=2, min_row=1, max_col=2, max_row=5)
    lc1_cats = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    lc1.add_data(lc1_data, titles_from_data=True)
    lc1.set_categories(lc1_cats)
    lc1.height = 6.5
    lc1.width = 14
    lc1.legend = None # Hide legend for single-series
    
    ws_dash.add_chart(lc1, "N6")
    
    # --- Chart 3: Line Chart 2 (Profit Trend) ---
    lc2 = LineChart()
    lc2.title = "Profit by month"
    lc2.style = 13
    lc2_data = Reference(ws_data, min_col=3, min_row=1, max_col=3, max_row=5)
    lc2_cats = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    lc2.add_data(lc2_data, titles_from_data=True)
    lc2.set_categories(lc2_cats)
    lc2.height = 6.5
    lc2.width = 14
    lc2.legend = None 
    
    ws_dash.add_chart(lc2, "N19")
```