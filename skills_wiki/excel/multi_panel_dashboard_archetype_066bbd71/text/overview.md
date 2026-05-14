### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Panel Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a multi-sheet architecture separating presentation from calculation. Renders a clean UI (gridlines disabled) with a three-panel dashboard layout: a primary categorical stacked chart on the left, and two vertical trend charts on the right, all driven by a hidden summary calculation sheet.
* **Applicability**: Best for building executive summaries and performance dashboards where you want to highlight categorical mix (e.g., market by product) alongside temporal trends (e.g., monthly profit and volume), preventing users from seeing raw data calculations.

### 2. Structural Breakdown

- **Data Layout**: Employs a separation-of-concerns pattern with a "Dashboard" sheet for visual components and a hidden "Calc" sheet for summarized plot data.
- **Formula Logic**: Static injection used in Python context, simulating dynamic PivotTable aggregations.
- **Visual Design**: The dashboard sheet disables native gridlines (`showGridLines = False`) for a white-canvas effect. The title utilizes the active theme's primary color with a size-24 bold font.
- **Charts/Tables**: 
  - Main Panel: Stacked column chart (`type="col"`, `grouping="stacked"`, `overlap=100`) for dimensional breakdown.
  - Secondary Panels: Two line charts utilizing built-in Excel style presets (`style=13`) with legends disabled for cleaner data-ink ratio.
- **Theme Hooks**: Derives title color from `theme.primary`.

### 3. Reproduction Code

```python
from openpyxl.styles import Font
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Generates a presentation-ready dashboard workbook separating charts from data.
    """
    # Attempt to load external theme palette, fallback to default hex colors
    try:
        from _helpers import get_theme_palette
        palette = get_theme_palette(theme)
        primary_color = palette.get("primary", "003366")
    except ImportError:
        primary_color = "003366" if theme == "corporate_blue" else "4472C4"

    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_calc = wb.create_sheet("Calc")

    # --- 1. Setup Dashboard UI Canvas ---
    ws_dash.sheet_view.showGridLines = False
    ws_dash["B2"] = title
    ws_dash["B2"].font = Font(size=24, bold=True, color=primary_color)

    # --- 2. Populate Calc Data (Simulating Pivot Caches) ---
    # Table 1: Data for Main Chart (Stacked Bar)
    ws_calc.append(["Market", "Product Alpha", "Product Beta", "Product Gamma"])
    t1_data = [
        ["Region North", 62000, 23000, 25000],
        ["Region South", 54000, 24000, 8000],
        ["Region East",  46000, 26000, 14000],
        ["Region West",  36000, 32000, 9000]
    ]
    for row in t1_data:
        ws_calc.append(row)

    # Table 2: Data for Trend Charts (Lines)
    calc_row = 10
    t2_headers = ["Month", "Units Sold", "Profit"]
    t2_data = [
        ["Q1", 50000, 124000],
        ["Q2", 95000, 228000],
        ["Q3", 65000, 160000],
        ["Q4", 52000, 136000]
    ]
    ws_calc.cell(row=calc_row, column=1, value=t2_headers[0])
    ws_calc.cell(row=calc_row, column=2, value=t2_headers[1])
    ws_calc.cell(row=calc_row, column=3, value=t2_headers[2])

    for i, row in enumerate(t2_data, 1):
        ws_calc.cell(row=calc_row + i, column=1, value=row[0])
        ws_calc.cell(row=calc_row + i, column=2, value=row[1])
        ws_calc.cell(row=calc_row + i, column=3, value=row[2])

    # --- 3. Construct Charts ---
    
    # Chart 1: Stacked Bar (Main Left Panel)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Category"
    data1 = Reference(ws_calc, min_col=2, min_row=1, max_col=4, max_row=5)
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=5)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    c1.width = 16
    c1.height = 12
    ws_dash.add_chart(c1, "B4")

    # Chart 2: Line Trend (Top Right Panel)
    c2 = LineChart()
    c2.title = "Units Sold Trend"
    c2.style = 13  # Clean built-in Excel line style preset
    data2 = Reference(ws_calc, min_col=2, min_row=calc_row, max_col=2, max_row=calc_row + 4)
    cats2 = Reference(ws_calc, min_col=1, min_row=calc_row + 1, max_row=calc_row + 4)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    c2.legend = None # Remove legend to maximize plot area
    c2.width = 14
    c2.height = 5.8
    ws_dash.add_chart(c2, "K4")

    # Chart 3: Line Trend (Bottom Right Panel)
    c3 = LineChart()
    c3.title = "Profit Trend"
    c3.style = 13
    data3 = Reference(ws_calc, min_col=3, min_row=calc_row, max_col=3, max_row=calc_row + 4)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats2)
    c3.legend = None
    c3.width = 14
    c3.height = 5.8
    ws_dash.add_chart(c3, "K15")

    # --- 4. Hide Calculation Logic ---
    ws_calc.sheet_state = "hidden"
```