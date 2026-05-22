### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Dashboard Archetype

* **Tier**: archetype
* **Core Mechanism**: Generates a standard, clean interactive-style dashboard layout by creating a "Data Backend" sheet and a presentation-layer "Dashboard" sheet. Hides gridlines on the dashboard, applies a unified title banner, and positions multiple distinct chart types (e.g., a large stacked bar chart alongside a vertical stack of trend lines) using precise cell anchoring and sizing. 
* **Applicability**: Best used when building automated reporting workbooks that require an executive summary page. It abstracts away the clutter of raw data, providing a clean "canvas" approach to chart layout.

### 2. Structural Breakdown

- **Data Layout**: Raw structured tables are isolated on a hidden or secondary `Data_Backend` sheet. Data is arranged in standard tabular format (Categories in rows, Series in columns) to easily feed `Reference` objects.
- **Formula Logic**: Purely data-driven for charting; relies on OpenPyXL's chart `Reference` boundaries rather than cell formulas.
- **Visual Design**: Turns off `showGridLines` on the dashboard sheet to create a blank canvas. Uses a merged, colored header block driven by the `theme` dictionary to establish brand identity.
- **Charts/Tables**: Implements a large `BarChart` (`grouping="stacked"`) for categorical comparison, and two smaller `LineChart` objects to show time-series trends. Removes legends on the line charts for cleaner presentation (matching the video's cleanup steps).
- **Theme Hooks**: Utilizes a standard fallback palette (`primary`, `bg`, `text`) to colorize the main header block, ensuring it integrates with external styling systems.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.chart import BarChart, LineChart, Reference

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    # 1. Standard Theme Loader Pattern
    themes = {
        "corporate_blue": {"primary": "003366", "secondary": "4F81BD", "bg": "F2F2F2", "text": "FFFFFF"},
        "dark_mode": {"primary": "222222", "secondary": "444444", "bg": "111111", "text": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Setup Sheets
    ws_data = wb.active
    ws_data.title = "Data_Backend"
    ws_dash = wb.create_sheet("Dashboard", 0)
    
    # Hide gridlines to create a clean "Dashboard Canvas"
    ws_dash.sheet_view.showGridLines = False

    # 3. Populate Backend Data
    # --- Market & Product Data (For Stacked Bar) ---
    market_data = [
        ["Market", "Chocolate Chip", "Fortune Cookie", "Oatmeal Raisin", "Sugar"],
        ["India", 62349, 4872, 21028, 25085],
        ["Philippines", 54618, 7026, 22005, 8313],
        ["United Kingdom", 46530, 5220, 11497, 14620],
        ["United States", 36657, 6368, 22260, 9937],
    ]
    for r_idx, row in enumerate(market_data, 1):
        for c_idx, val in enumerate(row, 1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    # --- Monthly Trend Data (For Line Charts) ---
    trend_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50601, 124812],
        ["Oct", 95622, 228275],
        ["Nov", 65481, 160228],
        ["Dec", 52970, 136337],
    ]
    for r_idx, row in enumerate(trend_data, 10):
        for c_idx, val in enumerate(row, 1):
            ws_data.cell(row=r_idx, column=c_idx, value=val)

    # 4. Construct Dashboard Header
    ws_dash.merge_cells("A1:P2")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=palette["text"])
    title_cell.fill = PatternFill(fill_type="solid", fgColor=palette["primary"])
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 5. Create and Position Charts
    # --- Chart 1: Stacked Bar (Profit by Market) ---
    c1 = BarChart()
    c1.type = "col"
    c1.style = 10
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.height = 11.5
    c1.width = 16

    data_c1 = Reference(ws_data, min_col=2, min_row=1, max_col=5, max_row=5)
    cats_c1 = Reference(ws_data, min_col=1, min_row=2, max_row=5)
    c1.add_data(data_c1, titles_from_data=True)
    c1.set_categories(cats_c1)
    ws_dash.add_chart(c1, "B4")

    # --- Chart 2: Line (Units Sold) ---
    c2 = LineChart()
    c2.style = 13
    c2.title = "Units sold each month"
    c2.height = 5.5
    c2.width = 12

    data_c2 = Reference(ws_data, min_col=2, min_row=10, max_col=2, max_row=14)
    cats_c2 = Reference(ws_data, min_col=1, min_row=11, max_row=14)
    c2.add_data(data_c2, titles_from_data=True)
    c2.set_categories(cats_c2)
    c2.legend = None  # Remove legend for cleaner look
    ws_dash.add_chart(c2, "J4")

    # --- Chart 3: Line (Profit Trend) ---
    c3 = LineChart()
    c3.style = 13
    c3.title = "Profit by month"
    c3.height = 5.5
    c3.width = 12

    data_c3 = Reference(ws_data, min_col=3, min_row=10, max_col=3, max_row=14)
    c3.add_data(data_c3, titles_from_data=True)
    c3.set_categories(cats_c2) # Share the same month categories
    c3.legend = None  # Remove legend for cleaner look
    ws_dash.add_chart(c3, "J13")
```