### 1. High-level Skill Pattern Extraction

> **Skill Name**: Variance-Emphasized Trend Chart

* **Tier**: component
* **Core Mechanism**: Binds a `LineChart` to periodic data and explicitly sets `y_axis.scaling.min` and `y_axis.scaling.max` to tightly wrap the data range. This truncates the empty space below the minimum value, visually magnifying small Year-over-Year variances that would otherwise look flat on a standard 0-based axis. Adds explicit circular markers to highlight discrete data points along the trend.
* **Applicability**: Trend analysis comparing two periods (e.g., Year-over-Year revenue, Budget vs. Actuals) where absolute values are high but the deltas are small, making standard zero-bound charts ineffective for storytelling.

### 2. Structural Breakdown

- **Data Layout**: 3 columns (Categories/Months, Series 1, Series 2) placed in a hidden or off-screen range (e.g., Row 100+).
- **Formula Logic**: None required; relies on static or pre-calculated trend data.
- **Visual Design**: Clean chart style preset, with the legend moved to the top to maximize horizontal plot area and reduce visual clutter.
- **Charts/Tables**: `LineChart` with heavily customized `y_axis.scaling` and `Marker(symbol="circle")` applied to all rendered series.
- **Theme Hooks**: Utilizes openpyxl's built-in chart style preset (`style=13`) which automatically inherits workbook theme colors for both lines and markers.

### 3. Reproduction Code

```python
def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import LineChart, Reference
    from openpyxl.chart.marker import Marker
    
    # 1. Insert Sample Data
    # In a real dashboard, this would typically reside on a hidden 'Inputs' sheet
    data = [
        ["Month", "2021 Sales", "2022 Sales"],
        ["Jan", 201.9, 215.3],
        ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3],
        ["Jun", 205.1, 203.0],
        ["Jul", 192.4, 201.5],
        ["Aug", 189.3, 200.6],
        ["Sep", 194.2, 210.6],
        ["Oct", 186.5, 203.6],
        ["Nov", 205.2, 222.3],
        ["Dec", 204.3, 225.8]
    ]
    
    data_start_row = 100
    data_start_col = 1
    for r_idx, row_data in enumerate(data, start=data_start_row):
        for c_idx, val in enumerate(row_data, start=data_start_col):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # 2. Configure the Line Chart
    chart = LineChart()
    chart.title = "2021-2022 Sales Trend (in millions)"
    chart.style = 13  # Clean built-in preset
    chart.width = 16
    chart.height = 8
    
    # 3. CORE MECHANISM: Truncate Y-Axis to Emphasize Variance
    # The lowest data point is ~186, highest is ~225. 
    # Bounding strictly between 180 and 250 visually magnifies the gap between the lines.
    chart.y_axis.scaling.min = 180
    chart.y_axis.scaling.max = 250
    chart.y_axis.title = "Sales ($M)"
    
    # Move legend to top to free up plot area width
    chart.legend.position = "t"
    
    # 4. Map Data
    y_data = Reference(ws, min_col=data_start_col+1, min_row=data_start_row, max_col=data_start_col+2, max_row=data_start_row+12)
    x_data = Reference(ws, min_col=data_start_col, min_row=data_start_row+1, max_row=data_start_row+12)
    
    chart.add_data(y_data, titles_from_data=True)
    chart.set_categories(x_data)
    
    # 5. Enhance Data Points
    # Add explicit circular markers to make each discrete month's data point pop over the trendline
    for series in chart.series:
        series.marker = Marker(symbol="circle", size=5)
        
    # Place the chart on the dashboard sheet
    ws.add_chart(chart, anchor)
```