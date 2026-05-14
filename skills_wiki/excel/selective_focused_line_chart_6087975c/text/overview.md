# Selective Focused Line Chart

## Applicability

Best used when a data table contains multiple related time-series metrics (e.g., pessimistic, optimistic, and expected scenarios), but the visual narrative requires comparing just two key lines (e.g., expected demand vs. actual capacity).

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Selective Focused Line Chart

* **Tier**: component
* **Core Mechanism**: Instantiates a `LineChart` and explicitly appends `Series` objects for only a specific subset of rows, effectively filtering out visual noise (like high/low forecast bounds) without altering the underlying data table. Enforces professional readability by requiring explicit chart and axis titles.
* **Applicability**: Best used when a data table contains multiple related time-series metrics (e.g., pessimistic, optimistic, and expected scenarios), but the visual narrative requires comparing just two key lines (e.g., expected demand vs. actual capacity). 

### 2. Structural Breakdown

- **Data Layout**: A matrix where the first row contains categorical time labels (months), and subsequent rows contain different data series (High Forecast, Low Forecast, Expected, Capacity) stretching across columns.
- **Formula Logic**: None required in the chart itself; relies on pre-calculated rows (e.g., `AVERAGE` for Expected Forecast) existing in the worksheet.
- **Visual Design**: The chart focuses purely on readability—removing "spaghetti" lines to highlight a specific intersection point (when expected forecast exceeds capacity). 
- **Charts/Tables**: `LineChart`. Uses `Reference` targeting specific rows rather than a contiguous 2D block to achieve the "filtered" effect shown in the tutorial.
- **Theme Hooks**: Utilizes standard chart color sequences; can optionally be set to a dark theme index (e.g., `chart.style = 27`) to match the final aesthetic of the video.

### 3. Reproduction Code

```python
from openpyxl.chart import LineChart, Reference, Series

def render(ws, anchor: str, *, 
           title: str = "SALES VS PRODUCTION", 
           x_title: str = "MONTH", 
           y_title: str = "TOTAL PRODUCTS",
           cat_row: int = 3, 
           min_col: int = 2, 
           max_col: int = 13,
           series_rows: list[int] = None,
           series_titles: list[str] = None,
           theme: str = "corporate_blue", 
           **kwargs) -> None:
    """
    Renders a professional line chart that deliberately selects a subset 
    of data rows to reduce clutter and focus the analytical narrative.
    """
    
    # Setup default series targeting the 'Expected' and 'Capacity' rows
    if series_rows is None:
        series_rows = [6, 7]
    if series_titles is None:
        series_titles = ["Expected Forecast", "Production Capacity"]

    # 1. Generate example data if the sheet is empty (for reproducibility)
    if ws.max_row == 1 and ws.max_column == 1 and ws["A1"].value is None:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Header Row
        for i, m in enumerate(months):
            ws.cell(row=cat_row, column=min_col + i, value=m)
            
        # Data Matrix (includes noise rows we want to filter out)
        data = [
            ("High Forecast", [277, 301, 288, 258, 296, 288, 293, 358, 423, 532, 633, 650]),
            ("Low Forecast", [150, 190, 200, 101, 122, 60, 56, 66, 57, 66, 71, 71]),
            ("Expected Forecast", [214, 246, 244, 180, 209, 174, 175, 212, 240, 299, 352, 361]),
            ("Production Capacity", [175, 175, 175, 275, 275, 275, 275, 275, 275, 275, 275, 275])
        ]
        
        for r_idx, (r_title, r_vals) in enumerate(data, start=cat_row + 1):
            ws.cell(row=r_idx, column=1, value=r_title)
            for c_idx, val in enumerate(r_vals):
                ws.cell(row=r_idx, column=min_col + c_idx, value=val)

    # 2. Configure the Line Chart
    chart = LineChart()
    chart.title = title
    chart.y_axis.title = y_title
    chart.x_axis.title = x_title
    
    # Adjust sizing for better readability
    chart.width = 16
    chart.height = 8.5
    
    # Optional: Apply a dark chart style similar to the video's final output
    # chart.style = 27 

    # 3. Define Category Labels (X-Axis)
    cats = Reference(ws, min_col=min_col, max_col=max_col, min_row=cat_row, max_row=cat_row)
    chart.set_categories(cats)

    # 4. Explicitly add ONLY the desired series to "filter" the chart
    for row_idx, s_title in zip(series_rows, series_titles):
        data_ref = Reference(ws, min_col=min_col, max_col=max_col, min_row=row_idx, max_row=row_idx)
        series = Series(data_ref, title=s_title)
        chart.series.append(series)

    # 5. Render
    ws.add_chart(chart, anchor)
```