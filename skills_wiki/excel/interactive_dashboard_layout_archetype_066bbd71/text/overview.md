### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Dashboard Layout Archetype

* **Tier**: archetype
* **Core Mechanism**: Constructs a standard multi-sheet dashboard structure separating raw data (Excel Tables), aggregated calculation data (Hidden Sheets), and presentation. Applies a clean, gridline-free layout with a stylized banner and aligns Stacked Column and Line charts to create a professional management summary view.
* **Applicability**: Best used when building top-level management or performance dashboards that require a polished, readable front-end backed by structured raw tabular data. 

### 2. Structural Breakdown

- **Data Layout**: Three distinct layers: A `Data` sheet containing the raw transactional table, a hidden `Calc_Hidden` sheet holding summarized matrices (acting as mock PivotTables), and a `Dashboard` sheet serving as the canvas.
- **Formula Logic**: (Simulated via static data generation in the snippet, but practically driven by PivotTables or `SUMIFS` targeting the raw data table).
- **Visual Design**: The `Dashboard` sheet hides all gridlines (`showGridLines = False`). A large merged block (A1:N3) acts as a high-contrast themed header banner with bold, vertically-centered text.
- **Charts/Tables**: Employs a primary `Stacked Column` chart (for multi-dimensional categorical data like Profit by Market & Product) and secondary `Line` charts (for time-series trends like Monthly Sales). Legends are removed from line charts to maximize data-ink ratio.
- **Theme Hooks**: Uses `primary` for the dashboard header background and standardizes chart styles. 

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a complete multi-sheet dashboard archetype separating raw data, 
    calculations, and a clean presentation layer.
    """
    # 1. Basic theme fallback
    colors = {
        "corporate_blue": {"primary": "002060", "secondary": "4F81BD", "bg": "FFFFFF", "text": "000000"},
        "dark_mode": {"primary": "202020", "secondary": "505050", "bg": "121212", "text": "FFFFFF"}
    }
    palette = colors.get(theme, colors["corporate_blue"])

    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet("Data")
    ws_calc = wb.create_sheet("Calc_Hidden")

    # --- 3. Populate Raw Data Layer ---
    headers = ["Date", "Market", "Product", "Units", "Profit"]
    raw_data = [
        ["2023-01-01", "India", "Chocolate Chip", 1500, 4500],
        ["2023-01-15", "USA", "Oatmeal Raisin", 800, 2400],
        ["2023-02-01", "India", "Sugar", 1200, 3000],
        ["2023-02-20", "UK", "Chocolate Chip", 900, 3600],
        ["2023-03-05", "USA", "Chocolate Chip", 2000, 8000],
        ["2023-03-10", "UK", "Oatmeal Raisin", 600, 1500],
    ]
    ws_data.append(headers)
    for row in raw_data:
        ws_data.append(row)

    tab = Table(displayName="RawData", ref=f"A1:E{len(raw_data)+1}")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # --- 4. Populate Calculation Layer (Simulated Pivot Tables) ---
    # Chart 1 Data: Profit by Market & Product (Stacked Bar)
    ws_calc.append(["Market", "Chocolate Chip", "Oatmeal Raisin", "Sugar"])
    ws_calc.append(["India", 4500, 0, 3000])
    ws_calc.append(["USA", 8000, 2400, 0])
    ws_calc.append(["UK", 3600, 1500, 0])

    # Chart 2 Data: Units by Month (Line)
    ws_calc.append([]) # Gap
    ws_calc.append(["Month", "Units Sold"])
    ws_calc.append(["Jan", 2300])
    ws_calc.append(["Feb", 2100])
    ws_calc.append(["Mar", 2600])

    # Chart 3 Data: Profit by Month (Line)
    ws_calc.append([]) # Gap
    ws_calc.append(["Month", "Profit"])
    ws_calc.append(["Jan", 6900])
    ws_calc.append(["Feb", 6600])
    ws_calc.append(["Mar", 9500])

    # Hide the calculation mechanics from the end-user
    ws_calc.sheet_state = 'hidden'

    # --- 5. Build Dashboard Presentation Layer ---
    ws_dash.sheet_view.showGridLines = False

    # Create Header Banner
    ws_dash.merge_cells("A1:N3")
    title_cell = ws_dash["A1"]
    title_cell.value = f"  {title}"
    title_cell.font = Font(size=28, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color=palette["primary"], end_color=palette["primary"], fill_type="solid")
    title_cell.alignment = Alignment(vertical="center", horizontal="left")

    # Chart 1: Profit by Market (Stacked Bar)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Cookie Type"
    c1.height = 12
    c1.width = 16

    data1 = Reference(ws_calc, min_col=2, min_row=1, max_col=4, max_row=4)
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=4)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    ws_dash.add_chart(c1, "B5")

    # Chart 2: Units by Month (Line Trend)
    c2 = LineChart()
    c2.title = "Units Sold Each Month"
    c2.style = 13
    c2.height = 5.5
    c2.width = 11
    c2.legend = None # Clean up chart clutter

    data2 = Reference(ws_calc, min_col=2, min_row=7, max_col=2, max_row=9)
    cats2 = Reference(ws_calc, min_col=1, min_row=8, max_row=9)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    ws_dash.add_chart(c2, "J5")

    # Chart 3: Profit by Month (Line Trend)
    c3 = LineChart()
    c3.title = "Profit By Month"
    c3.style = 13
    c3.height = 5.5
    c3.width = 11
    c3.legend = None

    data3 = Reference(ws_calc, min_col=2, min_row=12, max_col=2, max_row=14)
    cats3 = Reference(ws_calc, min_col=1, min_row=13, max_row=14)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats3)
    ws_dash.add_chart(c3, "J16")
```