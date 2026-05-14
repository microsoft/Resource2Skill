# Themed Line Chart Component

## Applicability

Best used for time-series data or trending metrics across multiple categories (like the store sales over time in the video) where consistent visual branding is required across multiple reports without relying on manual chart templates.

## Analysis

### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Line Chart Component

* **Tier**: component
* **Core Mechanism**: Programmatically constructs a consistently formatted line chart with markers, mimicking the application of a saved Excel chart template (`.crtx`). It loops through series to enforce marker styles, sets legend placement, and sizes the chart automatically.
* **Applicability**: Best used for time-series data or trending metrics across multiple categories (like the store sales over time in the video) where consistent visual branding is required across multiple reports without relying on manual chart templates.

### 2. Structural Breakdown

- **Data Layout**: Expects a standard tabular data layout where the first column contains categories (e.g., Dates) and subsequent columns contain series values, with headers in the first row.
- **Formula Logic**: None required.
- **Visual Design**: Enforces circular markers on line data points, standardizes line thickness, and locks the legend to the right side of the plot area.
- **Charts/Tables**: Uses `LineChart` from `openpyxl.chart`.
- **Theme Hooks**: Leverages Excel's built-in chart style preset (`13`) as a base, combined with explicit marker overrides.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, min_col: int = 1, min_row: int = 1, max_col: int = 5, max_row: int = 12, title: str = "Store Sales", theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import LineChart, Reference
    
    chart = LineChart()
    chart.title = title
    # Preset style 13 provides a clean, modern base with muted gridlines
    chart.style = 13  
    
    # Define data and categories based on standard table layout 
    # (Column 1: Categories, Columns 2-N: Series, Row 1: Headers)
    data = Reference(ws, min_col=min_col + 1, min_row=min_row, max_col=max_col, max_row=max_row)
    cats = Reference(ws, min_col=min_col, min_row=min_row + 1, max_row=max_row)
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    
    # Apply markers to all series (replicating the custom template style shown in the video)
    for series in chart.series:
        series.marker.symbol = "circle"
        series.marker.size = 5
        # Set line width slightly thicker (value is in EMUs, 20000 = ~1.5pt)
        if series.graphicalProperties:
            if not series.graphicalProperties.line:
                from openpyxl.drawing.line import LineProperties
                series.graphicalProperties.line = LineProperties()
            series.graphicalProperties.line.width = 20000 
        
    # Standardize legend placement to the right
    chart.legend.position = "r"
    
    # Standardize sizing for dashboard embedding
    chart.width = 22
    chart.height = 8.5
    
    ws.add_chart(chart, anchor)
```