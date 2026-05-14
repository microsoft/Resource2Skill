### 1. High-level Skill Pattern Extraction

> **Skill Name**: Clean Dashboard Canvas

* **Tier**: sheet_shell
* **Core Mechanism**: Transforms a standard worksheet into a presentation-ready dashboard canvas by disabling gridlines and row/column headers. It inserts a prominent, theme-colored title banner and orchestrates chart placements while keeping raw data segregated on a hidden calculation sheet.
* **Applicability**: Best used as the front-end reporting layer of a workbook. It provides users with a clean, application-like viewing experience without the clutter of standard spreadsheet elements (like row numbers, column letters, and gridlines).

### 2. Structural Breakdown

- **Data Layout**: Employs a secondary hidden sheet (`_Data`) to hold chart source data, keeping the main dashboard sheet completely clean of tabular data.
- **Formula Logic**: N/A for the layout itself, though charts cleanly reference the hidden background calculation sheet.
- **Visual Design**: Uses a deep, solid fill for the top title banner (rows 1-3) with large, bold, contrasting text. Turns off `showGridLines` and `showRowColHeaders` to create a blank canvas.
- **Charts/Tables**: Places a stacked column chart and a line chart onto the clean canvas to act as KPI visualizers.
- **Theme Hooks**: Consumes the `primary` theme color for the banner background and the `text` color (usually white) for the banner font.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.chart import BarChart, LineChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Creates a clean, gridless dashboard canvas with a title banner and placeholder charts.
    """
    ws = wb.create_sheet(sheet_name)
    
    # Clean canvas: Hide gridlines and row/col headers to create an app-like dashboard feel
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    
    # Define theme colors (fallback to corporate_blue)
    themes = {
        "corporate_blue": {"primary": "203764", "text": "FFFFFF"},
        "emerald": {"primary": "005A36", "text": "FFFFFF"},
        "slate": {"primary": "2F3542", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])
    
    # Create Title Banner (A1:Q3)
    ws.merge_cells("A1:Q3")
    title_cell = ws["A1"]
    title_cell.value = title
    title_cell.font = Font(name="Calibri", size=24, bold=True, color=palette["text"])
    title_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Create a hidden data sheet for the dashboard charts
    data_ws_name = f"{sheet_name}_Data"
    # Ensure sheet name length is valid (max 31 chars)
    data_ws = wb.create_sheet(data_ws_name[:31])
    data_ws.sheet_state = 'hidden'
    
    # Realistic dummy data for the dashboard visuals
    data = [
        ["Month", "Fortune Cookie", "Sugar Cookie", "Oatmeal Raisin"],
        ["Jan", 12000, 15000, 9000],
        ["Feb", 13500, 14000, 9500],
        ["Mar", 14000, 16000, 10500],
        ["Apr", 15000, 13000, 11000],
        ["May", 18000, 17000, 12500],
        ["Jun", 19000, 18000, 14000]
    ]
    for row in data:
        data_ws.append(row)
        
    # --- Chart 1: Stacked Column Chart ---
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Sales by Cookie Type"
    chart1.height = 10
    chart1.width = 15
    
    cats = Reference(data_ws, min_col=1, min_row=2, max_row=7)
    data_ref = Reference(data_ws, min_col=2, min_row=1, max_col=4, max_row=7)
    chart1.add_data(data_ref, titles_from_data=True)
    chart1.set_categories(cats)
    
    # Place on the clean dashboard canvas
    ws.add_chart(chart1, "C6")
    
    # --- Chart 2: Line Chart ---
    chart2 = LineChart()
    chart2.title = "Trend over Time"
    chart2.style = 13  # Built-in Excel style
    chart2.height = 10
    chart2.width = 15
    chart2.add_data(data_ref, titles_from_data=True)
    chart2.set_categories(cats)
    
    # Place on the clean dashboard canvas
    ws.add_chart(chart2, "K6")
```