### 1. High-level Skill Pattern Extraction

> **Skill Name**: 3-Pane Executive Dashboard Layout

* **Tier**: archetype
* **Core Mechanism**: Aggregates raw transactional data into structured summary tables on a hidden calculation sheet. Generates a main dashboard sheet featuring a styled corporate header, gridlines disabled, and a clean three-pane visual layout (one large stacked column chart on the left, two stacked line charts on the right) linked to the calculated data.
* **Applicability**: Ideal for executive summaries and KPI overviews where you need to display a primary categorical breakdown (e.g., Region x Product) alongside multiple time-series trends (e.g., Volume and Profit over time).

### 2. Structural Breakdown

- **Data Layout**: Raw data is processed in Python and written to a hidden `_Calc` sheet in three distinct table blocks (2D matrix for the stacked bar, 1D tables for the line charts).
- **Formula Logic**: Aggregation is handled in Python before writing to Excel to ensure chart data ranges are predictable and static.
- **Visual Design**: The `Dashboard` sheet hides standard Excel gridlines. A deep-colored header spanning `A1:Q2` establishes a professional report frame.
- **Charts/Tables**: 
  - Chart 1: `BarChart` (col, stacked), spanning rows 4-24 on the left.
  - Chart 2: `LineChart` (no legend), spanning rows 4-13 on the right.
  - Chart 3: `LineChart` (no legend), spanning rows 15-24 on the right.
- **Theme Hooks**: Uses `theme.primary_color` for the dashboard header background and `theme.primary_text` for the header text.

### 3. Reproduction Code

```python
def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, LineChart, Reference
    from collections import defaultdict
    import datetime

    # 1. Setup Theme Fallbacks
    palettes = {
        "corporate_blue": {"primary": "203764", "text": "FFFFFF"},
        "exec_dark": {"primary": "1F1F1F", "text": "FFFFFF"},
    }
    colors = palettes.get(theme, palettes["corporate_blue"])

    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_calc = wb.create_sheet("_Calc")
    ws_calc.sheet_state = 'hidden'

    # 3. Process Data
    # Fallback data if none provided
    raw_data = kwargs.get("data", [
        {"Date": "2020-09", "Market": "India", "Product": "Chip", "Units": 1200, "Profit": 8500},
        {"Date": "2020-09", "Market": "India", "Product": "Sugar", "Units": 800, "Profit": 3200},
        {"Date": "2020-09", "Market": "USA", "Product": "Chip", "Units": 3100, "Profit": 21000},
        {"Date": "2020-10", "Market": "India", "Product": "Chip", "Units": 1400, "Profit": 9100},
        {"Date": "2020-10", "Market": "USA", "Product": "Sugar", "Units": 1500, "Profit": 6000},
        {"Date": "2020-11", "Market": "India", "Product": "Sugar", "Units": 900, "Profit": 3800},
        {"Date": "2020-11", "Market": "USA", "Product": "Chip", "Units": 4200, "Profit": 29000},
        {"Date": "2020-12", "Market": "USA", "Product": "Sugar", "Units": 2000, "Profit": 8500},
    ])

    profit_by_mp = defaultdict(lambda: defaultdict(float))
    units_by_m = defaultdict(float)
    profit_by_m = defaultdict(float)
    markets, products, months = set(), set(), set()

    for row in raw_data:
        mkt, prod, mo = row.get("Market", "N/A"), row.get("Product", "N/A"), row.get("Date", "N/A")
        profit, units = float(row.get("Profit", 0)), float(row.get("Units", 0))
        
        profit_by_mp[mkt][prod] += profit
        units_by_m[mo] += units
        profit_by_m[mo] += profit
        markets.add(mkt); products.add(prod); months.add(mo)

    markets = sorted(list(markets))
    products = sorted(list(products))
    months = sorted(list(months))

    # 4. Write Aggregations to Calc Sheet
    # Block 1: Stacked Bar Data
    ws_calc.append(["Market"] + products)
    for mkt in markets:
        ws_calc.append([mkt] + [profit_by_mp[mkt][p] for p in products])
    
    # Block 2: Units Line Data
    r_units = len(markets) + 4
    ws_calc.cell(row=r_units, column=1, value="Month")
    ws_calc.cell(row=r_units, column=2, value="Units Sold")
    for i, m in enumerate(months):
        ws_calc.cell(row=r_units+1+i, column=1, value=m)
        ws_calc.cell(row=r_units+1+i, column=2, value=units_by_m[m])

    # Block 3: Profit Line Data
    r_profit = r_units + len(months) + 3
    ws_calc.cell(row=r_profit, column=1, value="Month")
    ws_calc.cell(row=r_profit, column=2, value="Total Profit")
    for i, m in enumerate(months):
        ws_calc.cell(row=r_profit+1+i, column=1, value=m)
        ws_calc.cell(row=r_profit+1+i, column=2, value=profit_by_m[m])

    # 5. Dashboard Visual Design
    ws_dash.sheet_view.showGridLines = False
    ws_dash.merge_cells("A1:Q2")
    header_cell = ws_dash["A1"]
    header_cell.value = title.upper()
    header_cell.fill = PatternFill(start_color=colors["primary"], end_color=colors["primary"], fill_type="solid")
    header_cell.font = Font(color=colors["text"], size=20, bold=True)
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 6. Chart 1: Stacked Column (Left Pane)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.overlap = 100
    c1.title = "Profit by Market & Product"
    c1.width = 17.5
    c1.height = 11.5
    
    cats1 = Reference(ws_calc, min_col=1, min_row=2, max_row=len(markets)+1)
    data1 = Reference(ws_calc, min_col=2, min_row=1, max_row=len(markets)+1, max_col=len(products)+1)
    c1.add_data(data1, titles_from_data=True)
    c1.set_categories(cats1)
    ws_dash.add_chart(c1, "B4")

    # 7. Chart 2: Line Chart Units (Top Right Pane)
    c2 = LineChart()
    c2.title = "Units sold each month"
    c2.width = 15.5
    c2.height = 5.5
    c2.legend = None
    
    data2 = Reference(ws_calc, min_col=2, min_row=r_units, max_row=r_units+len(months))
    cats2 = Reference(ws_calc, min_col=1, min_row=r_units+1, max_row=r_units+len(months))
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats2)
    ws_dash.add_chart(c2, "J4")

    # 8. Chart 3: Line Chart Profit (Bottom Right Pane)
    c3 = LineChart()
    c3.title = "Profit by month"
    c3.width = 15.5
    c3.height = 5.5
    c3.legend = None
    
    data3 = Reference(ws_calc, min_col=2, min_row=r_profit, max_row=r_profit+len(months))
    cats3 = Reference(ws_calc, min_col=1, min_row=r_profit+1, max_row=r_profit+len(months))
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(cats3)
    ws_dash.add_chart(c3, "J15")
```