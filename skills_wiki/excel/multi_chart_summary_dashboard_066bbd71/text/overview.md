### 1. High-level Skill Pattern Extraction

> **Skill Name**: Multi-Chart Summary Dashboard

* **Tier**: archetype
* **Core Mechanism**: Simulates the visual layout of an interactive Pivot Dashboard by using Python to aggregate raw tabular data into a hidden calculation sheet. It projects this summary data onto a clean, gridline-free presentation sheet using multiple perfectly aligned openpyxl charts, topped with a themed header bar. 
* **Applicability**: Ideal for generating automated, read-only analytical reports where visual cleanliness and layout precision are paramount. Use this when you need to deliver a complete "dashboard" view programmatically without relying on manual PivotTable creation.

### 2. Structural Breakdown

- **Data Layout**: Consists of two sheets. The 'Dashboard' sheet is the active presentation layer with gridlines hidden. The 'Calc' sheet is hidden and holds the intermediate summarized data tables that drive the charts.
- **Formula Logic**: Aggregation (SUMs by category) is handled in memory via Python dictionaries before being written to the 'Calc' sheet as static values, acting as a programmatic PivotTable substitute.
- **Visual Design**: The dashboard features a full-width merged header block driven by theme colors, utilizing white bold text for contrast. Gridlines are explicitly disabled (`sheet_view.showGridLines = False`) to create a canvas-like feel.
- **Charts/Tables**: Employs a main Stacked Column chart for multi-dimensional data (e.g., Market + Product) and two smaller Line charts stacked vertically for time-series trends, mimicking a classic KPI dashboard layout. 
- **Theme Hooks**: Consumes `primary` for the header background and `text_light` for the header text. Chart colors default to the workbook's built-in palette.

### 3. Reproduction Code

```python
import random
from collections import defaultdict
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, Alignment, PatternFill

def render_workbook(wb, *, title: str = "Performance Dashboard", data: list[dict] = None, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds a multi-chart summary dashboard, aggregating raw data into a hidden 
    calculation sheet and projecting the results onto a clean presentation layer.
    """
    # 0. Generate mock data if none provided
    if not data:
        data = []
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        markets = ["United States", "United Kingdom", "India", "Philippines"]
        products = ["Chocolate Chip", "Sugar", "Oatmeal Raisin", "Snickerdoodle"]
        
        for i, m in enumerate(months):
            for mk in markets:
                for p in products:
                    units = random.randint(100, 2000)
                    profit = units * random.uniform(2.5, 6.0)
                    data.append({
                        "Month": m,
                        "MonthOrder": i,
                        "Market": mk,
                        "Product": p,
                        "Units": units,
                        "Profit": profit
                    })

    # 1. Setup Sheets
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.sheet_view.showGridLines = False

    ws_calc = wb.create_sheet("Calc")
    ws_calc.sheet_state = "hidden"

    # 2. Add Themed Title Bar to Dashboard
    # Fallback to standard corporate blue if no theme loader is present
    theme_primary = kwargs.get("theme_primary", "1F4E78") 
    theme_text = kwargs.get("theme_text_light", "FFFFFF")
    
    header_fill = PatternFill(start_color=theme_primary, end_color=theme_primary, fill_type="solid")
    ws_dash.merge_cells("A1:Q3")
    title_cell = ws_dash["A1"]
    title_cell.value = title
    title_cell.font = Font(size=24, bold=True, color=theme_text)
    title_cell.alignment = Alignment(vertical="center", horizontal="center")
    title_cell.fill = header_fill

    # 3. Aggregate Data in Python (simulating PivotTables)
    markets_set = sorted(list(set(d["Market"] for d in data)))
    products_set = sorted(list(set(d["Product"] for d in data)))
    
    month_data = defaultdict(lambda: {"units": 0, "profit": 0, "order": 0})
    for d in data:
        month_data[d["Month"]]["units"] += d["Units"]
        month_data[d["Month"]]["profit"] += d["Profit"]
        month_data[d["Month"]]["order"] = d.get("MonthOrder", 0)
        
    sorted_months = sorted(month_data.keys(), key=lambda k: month_data[k]["order"])

    # 4. Write Aggregated Data to Hidden 'Calc' Sheet
    # Table 1: Profit by Market & Product (for Stacked Bar)
    ws_calc.append(["Market"] + products_set)
    start_row_c1 = ws_calc.max_row
    for mk in markets_set:
        row = [mk]
        for p in products_set:
            val = sum(d["Profit"] for d in data if d["Market"] == mk and d["Product"] == p)
            row.append(val)
        ws_calc.append(row)
    end_row_c1 = ws_calc.max_row

    ws_calc.append([]) # Spacer

    # Table 2 & 3: Units and Profit by Month (for Line Charts)
    ws_calc.append(["Month", "Units Sold", "Profit"])
    start_row_c2 = ws_calc.max_row
    for m in sorted_months:
        ws_calc.append([m, month_data[m]["units"], month_data[m]["profit"]])
    end_row_c2 = ws_calc.max_row

    # 5. Build Charts
    # Chart 1: Stacked Bar (Main Visual)
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "stacked"
    c1.title = "Profit by Market & Product Type"
    c1.width = 18
    c1.height = 12

    data_ref1 = Reference(ws_calc, min_col=2, min_row=start_row_c1, max_col=1+len(products_set), max_row=end_row_c1)
    cats_ref1 = Reference(ws_calc, min_col=1, min_row=start_row_c1+1, max_row=end_row_c1)
    c1.add_data(data_ref1, titles_from_data=True)
    c1.set_categories(cats_ref1)

    # Chart 2: Line (Units Sold)
    c2 = LineChart()
    c2.title = "Units Sold Each Month"
    c2.width = 14
    c2.height = 6
    c2.legend = None # Clean look, title explains the metric

    data_ref2 = Reference(ws_calc, min_col=2, min_row=start_row_c2, max_row=end_row_c2)
    cats_ref2 = Reference(ws_calc, min_col=1, min_row=start_row_c2+1, max_row=end_row_c2)
    c2.add_data(data_ref2, titles_from_data=True)
    c2.set_categories(cats_ref2)

    # Chart 3: Line (Profit Trend)
    c3 = LineChart()
    c3.title = "Profit by Month"
    c3.width = 14
    c3.height = 6
    c3.legend = None

    data_ref3 = Reference(ws_calc, min_col=3, min_row=start_row_c2, max_row=end_row_c2)
    c3.add_data(data_ref3, titles_from_data=True)
    c3.set_categories(cats_ref2) # Reuse month categories

    # 6. Place Aligned Charts on Dashboard
    ws_dash.add_chart(c1, "B5")
    ws_dash.add_chart(c2, "K5")
    ws_dash.add_chart(c3, "K17")
```