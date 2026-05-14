### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Interactive Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Constructs a polished, application-like dashboard interface by disabling worksheet gridlines, creating a prominent top title banner, allocating a dedicated left sidebar for controls (slicers/timelines), and organizing a structured grid of charts.
* **Applicability**: Best used when building executive summaries or KPI dashboards that require multiple visual metrics (e.g., categorical breakdown alongside trend lines) and a dedicated area for user interactions.

### 2. Structural Breakdown

- **Data Layout**: Separates the presentation logic from the data by utilizing a dedicated "Data" sheet for aggregated chart data (e.g., categorical breakdowns and time-series trends), keeping the "Dashboard" sheet clean.
- **Formula Logic**: None required; relies on chart data references.
- **Visual Design**: Hides gridlines (`showGridLines = False`). Merges a large header row block filled with the theme's primary color and white text. Merges a left-side column block with a subtle light background to act as a placeholder/drop-zone for interactive slicers.
- **Charts/Tables**: Includes a Stacked Column chart (`type="col"`, `grouping="stacked"`) for categorical composition, and two Line charts (`LineChart`) for time-series trends. Line chart legends are removed to maximize the plot area.
- **Theme Hooks**: Consumes `primary` for the header banner background, `text_light` for the header text, and `bg_light`/`text_muted` for the left sidebar placeholder area.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def load_theme(theme_name: str) -> dict:
    themes = {
        "corporate_blue": {
            "primary": "003366",
            "secondary": "4F81BD",
            "bg_light": "F2F2F2",
            "text_light": "FFFFFF",
            "text_muted": "808080"
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = load_theme(theme)
    
    # 1. Setup sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet("Data")
    
    # 2. Write Data
    stacked_data = [
        ["Market", "Chocolate Chip", "Sugar", "Fortune Cookie"],
        ["India", 62349, 25085, 4872],
        ["Philippines", 54618, 8313, 7026],
        ["United Kingdom", 46530, 14620, 5220],
        ["United States", 36657, 9938, 6369]
    ]
    
    trend_data = [
        ["Month", "Units Sold", "Profit"],
        ["Jan", 50601, 124812],
        ["Feb", 65481, 228275],
        ["Mar", 52970, 160228],
        ["Apr", 54000, 136337],
        ["May", 75000, 185000],
        ["Jun", 82000, 205000],
        ["Jul", 79000, 195000],
        ["Aug", 71000, 178000],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337]
    ]
    
    for row in stacked_data:
        ws_data.append(row)
        
    ws_data.append([]) # Empty spacer row
    trend_start_row = ws_data.max_row + 1
    
    for row in trend_data:
        ws_data.append(row)
        
    # 3. Create Charts
    # Chart 1: Stacked Column (Main breakdown)
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "stacked"
    bar.overlap = 100
    bar.title = "Profit by Market & Cookie Type"
    bar.style = 11
    
    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=4, max_row=5)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    bar.add_data(data_ref, titles_from_data=True)
    bar.set_categories(cats_ref)
    bar.height = 14
    bar.width = 16
    ws_dash.add_chart(bar, "E5")
    
    # Chart 2: Line Chart (Top right trend)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.style = 12
    data_ref1 = Reference(ws_data, min_col=2, min_row=trend_start_row, max_row=ws_data.max_row)
    cats_ref_line = Reference(ws_data, min_col=1, min_row=trend_start_row+1, max_row=ws_data.max_row)
    line1.add_data(data_ref1, titles_from_data=True)
    line1.set_categories(cats_ref_line)
    line1.height = 7
    line1.width = 14
    line1.legend = None  # Free up space
    ws_dash.add_chart(line1, "O5")
    
    # Chart 3: Line Chart (Bottom right trend)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.style = 12
    data_ref2 = Reference(ws_data, min_col=3, min_row=trend_start_row, max_row=ws_data.max_row)
    line2.add_data(data_ref2, titles_from_data=True)
    line2.set_categories(cats_ref_line)
    line2.height = 7
    line2.width = 14
    line2.legend = None  # Free up space
    ws_dash.add_chart(line2, "O17")
    
    # 4. Dashboard Layout & Formatting
    ws_dash.sheet_view.showGridLines = False
    
    # Title Banner
    ws_dash.merge_cells("A1:AB3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text_light"])
    title_cell.fill = PatternFill("solid", fgColor=palette["primary"])
    title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    
    # Left sidebar for slicers (simulated drop-zone)
    ws_dash.merge_cells("A5:C28")
    slicer_area = ws_dash["A5"]
    slicer_area.fill = PatternFill("solid", fgColor=palette["bg_light"])
    slicer_area.value = "Slicer / Filters Area\n(Insert Slicers Here)"
    slicer_area.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    slicer_area.font = Font(color=palette["text_muted"], italic=True)
    
    # Adjust column widths for structural spacing
    for col in ["A", "B", "C"]:
        ws_dash.column_dimensions[col].width = 10
    ws_dash.column_dimensions["D"].width = 2
    ws_dash.column_dimensions["N"].width = 2
```