### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Dashboard Layout

* **Tier**: sheet_shell
* **Core Mechanism**: Configures worksheet view properties to hide gridlines and row/column headers, converting a typical spreadsheet into a blank presentation canvas. Adds a full-width themed banner for the title and positions charts into a dimensionally aligned grid, utilizing hidden calculation sheets for the data.
* **Applicability**: Best used as the final presentation layer of a report workbook where charts, KPIs, and controls (like Slicers) are consolidated, and standard Excel grid elements would be visually distracting.

### 2. Structural Breakdown

- **Data Layout**: Top rows (1-3) merged and filled to act as a permanent header banner. Remaining rows left completely blank for positioning floating charts and shapes.
- **Formula Logic**: None. (Presentation layer is cleanly separated from logic; data is sourced from hidden background sheets).
- **Visual Design**: Gridlines disabled (`showGridLines = False`), row and column headers disabled (`showRowColHeaders = False`).
- **Charts/Tables**: Demonstrates a primary stacked column chart and a secondary line chart grouped on the canvas with gutters left intentionally empty for visual breathing room and UI controls.
- **Theme Hooks**: Primary background color used for the header banner, contrasting white text for the dashboard title.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # 1. Canvas Setup: Hide gridlines and headers to create a software-like dashboard feel
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    
    # 2. Header Banner: Create a full-width title band
    # Hardcoded fallback colors (normally injected via standard _helpers theme palette)
    banner_color = "1F4E78" # Corporate Blue
    banner_fill = PatternFill(start_color=banner_color, end_color=banner_color, fill_type="solid")
    banner_font = Font(name="Calibri", size=24, bold=True, color="FFFFFF")
    
    # Merge cells for the title and style it
    ws.merge_cells("A1:Q3")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.fill = banner_fill
    title_cell.font = banner_font
    title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    
    # Apply fill to the rest of the merged area to ensure the background color covers the full horizontal span
    for col in range(1, 18):
        for row in range(1, 4):
            ws.cell(row=row, column=col).fill = banner_fill

    # 3. Hidden Data: Create a calculation sheet for dashboard visuals
    data_ws = wb.create_sheet(f"{sheet_name}_Data")
    data_ws.sheet_state = 'hidden'
    
    data = [
        ["Month", "Chocolate Chip", "Sugar", "Oatmeal Raisin"],
        ["Jan", 15000, 12000, 8000],
        ["Feb", 22000, 18000, 10000],
        ["Mar", 18000, 15000, 12000],
        ["Apr", 25000, 20000, 16000],
        ["May", 28000, 22000, 15000],
        ["Jun", 30000, 25000, 18000]
    ]
    for row in data:
        data_ws.append(row)
        
    # 4. Chart 1: Main visual (Stacked Bar)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.style = 10
    bar_chart.title = "Profit by Market & Cookie Type"
    
    data_ref = Reference(data_ws, min_col=2, min_row=1, max_row=7, max_col=4)
    cats_ref = Reference(data_ws, min_col=1, min_row=2, max_row=7)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    
    # Dimensions roughly match the video's layout proportions
    bar_chart.height = 11.5
    bar_chart.width = 18
    
    # Place main chart leaving columns A & B empty as a gutter for Slicers/Controls
    ws.add_chart(bar_chart, "C5")
    
    # 5. Chart 2: Secondary visual (Line Trend)
    line_chart = LineChart()
    line_chart.style = 13
    line_chart.title = "Units Sold Each Month"
    
    # Trend for total units (plotting Chocolate Chip for illustration)
    line_data_ref = Reference(data_ws, min_col=2, min_row=1, max_row=7, max_col=2)
    line_chart.add_data(line_data_ref, titles_from_data=True)
    line_chart.set_categories(cats_ref)
    
    line_chart.height = 7.5
    line_chart.width = 15
    line_chart.legend = None # Remove legend to save space
    
    ws.add_chart(line_chart, "M5")
```