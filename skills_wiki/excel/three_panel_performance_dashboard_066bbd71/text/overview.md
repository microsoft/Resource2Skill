### 1. High-level Skill Pattern Extraction

> **Skill Name**: Three-Panel Performance Dashboard

* **Tier**: archetype
* **Core Mechanism**: Decouples presentation from data by using a dedicated "Dashboard" sheet with gridlines disabled. It aggregates raw data on a hidden calculation sheet, generating a three-chart layout (one large stacked bar, two smaller stacked line charts) perfectly snapped to a grid layout.
* **Applicability**: Best for executive summaries where you need to display multiple dimensions (e.g., market & product breakdown) alongside trend data (e.g., monthly sales & profit). 

### 2. Structural Breakdown

- **Data Layout**: 
  - `Data` sheet contains raw records.
  - `Calc` sheet (hidden) stores python-aggregated summary tables (mocking PivotTables).
  - `Dashboard` sheet acts as the clean canvas.
- **Formula Logic**: Aggregation is performed in Python prior to chart rendering, replicating the "PivotChart" behavior natively in `openpyxl` without requiring external add-ins or unsupported XML extensions.
- **Visual Design**: Gridlines are hidden (`sheet_view.showGridLines = False`), and a prominent merged header uses a dark theme color with white text. 
- **Charts/Tables**: 
  - Chart 1: Stacked Column Chart (`type="col"`, `grouping="stacked"`).
  - Chart 2 & 3: Line Charts.
  - All charts have removed legends where redundant, titles applied, and are physically sized to form a clean grid.
- **Theme Hooks**: Uses `primary_bg` for the dashboard header, `primary_fg` for the text, and leverages default Excel chart palettes which automatically inherit workbook theme colors.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference, Series
from collections import defaultdict

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a complete three-panel performance dashboard.
    Includes a hidden calculation sheet to aggregate data for the charts.
    """
    # 1. Basic Theme Palette Fallback
    themes = {
        "corporate_blue": {"primary_bg": "203764", "primary_fg": "FFFFFF"},
        "emerald_green": {"primary_bg": "005826", "primary_fg": "FFFFFF"},
        "slate_gray": {"primary_bg": "2F3538", "primary_fg": "FFFFFF"}
    }
    palette = themes.get(theme, themes["corporate_blue"])

    # 2. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_data = wb.create_sheet("Data")
    ws_calc = wb.create_sheet("Calc")
    
    # Hide gridlines on dashboard for a clean web-like feel
    ws_dash.sheet_view.showGridLines = False
    ws_calc.sheet_state = 'hidden'

    # 3. Generate Mock Data (if none provided)
    # Realistic cookie company data as seen in the tutorial
    raw_data = kwargs.get('raw_data', [
        {"market": "United States", "product": "Chocolate Chip", "month": "Jan", "units": 1500, "profit": 4500},
        {"market": "United States", "product": "Oatmeal Raisin", "month": "Jan", "units": 800, "profit": 2400},
        {"market": "India", "product": "Chocolate Chip", "month": "Jan", "units": 2200, "profit": 6600},
        {"market": "United Kingdom", "product": "Snickerdoodle", "month": "Feb", "units": 1200, "profit": 3600},
        {"market": "United States", "product": "Chocolate Chip", "month": "Feb", "units": 1800, "profit": 5400},
        {"market": "India", "product": "Chocolate Chip", "month": "Feb", "units": 2400, "profit": 7200},
        {"market": "United Kingdom", "product": "Snickerdoodle", "month": "Mar", "units": 1300, "profit": 3900},
        {"market": "United States", "product": "Oatmeal Raisin", "month": "Mar", "units": 900, "profit": 2700},
        {"market": "India", "product": "Chocolate Chip", "month": "Mar", "units": 2500, "profit": 7500},
        {"market": "Philippines", "product": "Fortune Cookie", "month": "Apr", "units": 3000, "profit": 1500},
        {"market": "United States", "product": "Chocolate Chip", "month": "Apr", "units": 2100, "profit": 6300},
        {"market": "India", "product": "Chocolate Chip", "month": "Apr", "units": 2700, "profit": 8100},
    ])

    # Write Raw Data
    ws_data.append(["Market", "Product", "Month", "Units Sold", "Profit"])
    for row in raw_data:
        ws_data.append([row["market"], row["product"], row["month"], row["units"], row["profit"]])

    # 4. Data Aggregation (Simulating PivotTables)
    market_product_profit = defaultdict(lambda: defaultdict(int))
    month_units = defaultdict(int)
    month_profit = defaultdict(int)

    months_order = []
    markets = set()
    products = set()

    for r in raw_data:
        mkt, prod, mo, units, prof = r["market"], r["product"], r["month"], r["units"], r["profit"]
        markets.add(mkt)
        products.add(prod)
        if mo not in months_order:
            months_order.append(mo)
        
        market_product_profit[mkt][prod] += prof
        month_units[mo] += units
        month_profit[mo] += prof

    markets = sorted(list(markets))
    products = sorted(list(products))

    # Write Aggregation 1: Market x Product (Stacked Bar source)
    ws_calc.append(["Market"] + products)
    for mkt in markets:
        row_data = [mkt] + [market_product_profit[mkt][p] for p in products]
        ws_calc.append(row_data)
    
    table1_end_row = len(markets) + 1

    # Write Aggregation 2: Time Series (Line charts source)
    start_row_t2 = table1_end_row + 3
    ws_calc.cell(row=start_row_t2, column=1, value="Month")
    ws_calc.cell(row=start_row_t2, column=2, value="Units Sold")
    ws_calc.cell(row=start_row_t2, column=3, value="Profit")
    
    for i, mo in enumerate(months_order):
        ws_calc.cell(row=start_row_t2 + i + 1, column=1, value=mo)
        ws_calc.cell(row=start_row_t2 + i + 1, column=2, value=month_units[mo])
        ws_calc.cell(row=start_row_t2 + i + 1, column=3, value=month_profit[mo])

    table2_end_row = start_row_t2 + len(months_order)

    # 5. Build Dashboard Header
    ws_dash.merge_cells('A1:R2')
    header_cell = ws_dash['A1']
    header_cell.value = title
    header_cell.font = Font(size=24, bold=True, color=palette["primary_fg"])
    header_cell.fill = PatternFill(start_color=palette["primary_bg"], end_color=palette["primary_bg"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    # 6. Chart 1: Profit by Market & Cookie Type (Stacked Bar)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    bar_chart.style = 2
    bar_chart.height = 12
    bar_chart.width = 18

    data_ref = Reference(ws_calc, min_col=2, min_row=1, max_col=len(products)+1, max_row=table1_end_row)
    cats_ref = Reference(ws_calc, min_col=1, min_row=2, max_row=table1_end_row)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    ws_dash.add_chart(bar_chart, "B4")

    # 7. Chart 2: Units Sold Each Month (Line)
    line_units = LineChart()
    line_units.title = "Units Sold Each Month"
    line_units.style = 13
    line_units.height = 6
    line_units.width = 12
    line_units.legend = None

    data_units = Reference(ws_calc, min_col=2, min_row=start_row_t2, max_row=table2_end_row)
    cats_time = Reference(ws_calc, min_col=1, min_row=start_row_t2+1, max_row=table2_end_row)
    line_units.add_data(data_units, titles_from_data=True)
    line_units.set_categories(cats_time)
    ws_dash.add_chart(line_units, "K4")

    # 8. Chart 3: Profit by Month (Line)
    line_profit = LineChart()
    line_profit.title = "Profit by Month"
    line_profit.style = 13
    line_profit.height = 6
    line_profit.width = 12
    line_profit.legend = None

    data_profit = Reference(ws_calc, min_col=3, min_row=start_row_t2, max_row=table2_end_row)
    line_profit.add_data(data_profit, titles_from_data=True)
    line_profit.set_categories(cats_time)
    ws_dash.add_chart(line_profit, "K16")
```