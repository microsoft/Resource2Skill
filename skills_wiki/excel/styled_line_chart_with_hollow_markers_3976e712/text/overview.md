### 1. High-level Skill Pattern Extraction

> **Skill Name**: Styled Line Chart With Hollow Markers

* **Tier**: component
* **Core Mechanism**: Generates a dual-series line chart with customized axis bounds to emphasize narrow variances. Upgrades standard line markers to a clean, "hollow" aesthetic by applying a white solid fill and a colored border that matches the connecting line stroke.
* **Applicability**: Best used for Year-over-Year (YoY) trend analysis or multi-period comparison where default chart markers feel cluttered, and specific value variations need to be emphasized without visual noise.

### 2. Structural Breakdown

- **Data Layout**: A 3-column table containing categories (Months) in the first column, and series values (Year 1, Year 2) in the adjacent columns.
- **Formula Logic**: None required (driven by native chart data references).
- **Visual Design**: Series lines are explicitly colored (e.g., Red and Dark Blue). Markers are customized as size-5 circles with a white inner fill and a 1pt colored border mirroring the series color. Major horizontal gridlines are hidden.
- **Charts/Tables**: `LineChart` placed adjacent to the data block. Y-axis minimum and maximum are manually clipped (e.g., 180 to 230) to highlight variance. Legend is anchored to the bottom.
- **Theme Hooks**: The line colors and marker borders should ideally map to `theme.primary` and `theme.secondary` (or an accent color) if a dynamic theme payload is provided.

### 3. Reproduction Code

```python
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.marker import Marker
from openpyxl.utils import coordinate_to_tuple, get_column_letter

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    r_idx, c_idx = coordinate_to_tuple(anchor)
    
    # 1. Insert Sample YoY Data
    headers = ["Month", "2021", "2022"]
    data = [
        ["Jan", 201.9, 215.3],
        ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3],
        ["Jun", 195.1, 201.0],
        ["Jul", 192.4, 201.6],
        ["Aug", 186.3, 200.6],
        ["Sep", 194.2, 210.6],
        ["Oct", 220.0, 223.3],
        ["Nov", 205.2, 222.3],
        ["Dec", 204.3, 225.8],
    ]
    
    ws.cell(row=r_idx, column=c_idx, value=headers[0])
    ws.cell(row=r_idx, column=c_idx+1, value=headers[1])
    ws.cell(row=r_idx, column=c_idx+2, value=headers[2])
    
    for i, row in enumerate(data):
        ws.cell(row=r_idx+i+1, column=c_idx, value=row[0])
        ws.cell(row=r_idx+i+1, column=c_idx+1, value=row[1])
        ws.cell(row=r_idx+i+1, column=c_idx+2, value=row[2])
        
    # 2. Initialize Line Chart
    chart = LineChart()
    chart.title = None
    chart.width = 16
    chart.height = 8
    
    # Manual axis bounds to highlight narrow variance (as demonstrated in the tutorial)
    chart.y_axis.scaling.min = 180
    chart.y_axis.scaling.max = 230
    chart.y_axis.majorGridlines = None
    
    # 3. Reference Data & Categories
    data_ref = Reference(ws, min_col=c_idx+1, min_row=r_idx, max_col=c_idx+2, max_row=r_idx+12)
    cats_ref = Reference(ws, min_col=c_idx, min_row=r_idx+1, max_row=r_idx+12)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    # Palette definition (Fallback colors mapping to tutorial styles)
    color_s1 = "C0504D" # Red for prior year
    color_s2 = "1F497D" # Dark Blue for current year
    
    # 4. Style Series 1 with Hollow Markers
    s1 = chart.series[0]
    s1.graphicalProperties.line.solidFill = color_s1
    s1.marker = Marker(symbol="circle", size=5)
    s1.marker.graphicalProperties.solidFill = "FFFFFF"  # White hollow fill
    s1.marker.graphicalProperties.line.solidFill = color_s1 # Matching border
    
    # 5. Style Series 2 with Hollow Markers
    s2 = chart.series[1]
    s2.graphicalProperties.line.solidFill = color_s2
    s2.marker = Marker(symbol="circle", size=5)
    s2.marker.graphicalProperties.solidFill = "FFFFFF"  # White hollow fill
    s2.marker.graphicalProperties.line.solidFill = color_s2 # Matching border
    
    # Bottom legend position
    chart.legend.position = "b"
    
    # 6. Place Chart adjacent to the data table
    chart_col = get_column_letter(c_idx + 4)
    ws.add_chart(chart, f"{chart_col}{r_idx}")
```