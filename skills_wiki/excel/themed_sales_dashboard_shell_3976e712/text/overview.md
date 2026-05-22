### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Sales Dashboard Shell

* **Tier**: sheet_shell
* **Core Mechanism**: Arranges KPI metric cards using structured cell formatting (simulating floating cards with borders) and embeds custom-styled line and radar charts. Drives a dark sidebar for navigation layout. Backing data is stored out-of-view to keep the dashboard clean.
* **Applicability**: Best for executive summaries and high-level business dashboards where multiple chart types (time-series trends, multidimensional satisfaction scores) need to be presented cleanly alongside key metrics on a single screen.

### 2. Structural Breakdown

- **Data Layout**: Places dashboard visuals in rows 1-40. Injects backing data out-of-view (rows 50+) to cleanly decouple the presentation layer from the data source.
- **Formula Logic**: N/A (Data is statically injected for charting).
- **Visual Design**: Uses a dark sidebar (Column A) and light gray background to simulate a web app interface. Emulates card UI using white cell backgrounds with thin gray borders.
- **Charts/Tables**: Includes a Line Chart with styled markers (circle, white fill, colored outline) and bounded Y-axis (min=180). Includes a Radar Chart for multidimensional metrics with a hidden legend.
- **Theme Hooks**: Uses standard hex codes (adaptable to themes) for background (`F3F4F6`), sidebar (`1E293B`), text (`0F172A`), and accent colors for chart series.

### 3. Reproduction Code

```python
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.chart import LineChart, RadarChart, Reference
from openpyxl.chart.marker import Marker
from openpyxl.drawing.line import LineProperties

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Theme colors (can be hooked to a theme palette)
    bg_color = "F3F4F6"      # Light gray dashboard background
    card_color = "FFFFFF"    # White cards
    sidebar_color = "1E293B" # Dark sidebar
    text_color = "0F172A"    # Dark text
    accent1 = "2563EB"       # Blue
    accent2 = "E11D48"       # Red
    
    # Apply Dashboard Background
    bg_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=18):
        for cell in row:
            cell.fill = bg_fill
            
    # Sidebar Navigation Column
    sidebar_fill = PatternFill(start_color=sidebar_color, end_color=sidebar_color, fill_type="solid")
    ws.column_dimensions['A'].width = 8
    for row in range(1, 41):
        ws.cell(row=row, column=1).fill = sidebar_fill
        
    # Dashboard Header
    title_cell = ws.cell(row=2, column=3, value=title)
    title_cell.font = Font(size=20, bold=True, color=sidebar_color)
    ws.cell(row=3, column=3, value="Figures in millions of USD").font = Font(size=10, italic=True, color="64748B")
    
    # KPI Cards Structure
    kpis = [
        ("Sales", "$2,544", 3),
        ("Profit", "$890", 7),
        ("# of Customers", "87.0", 11)
    ]
    card_fill = PatternFill(start_color=card_color, end_color=card_color, fill_type="solid")
    border_side = Side(style='thin', color="CBD5E1")
    
    for title_str, val_str, start_col in kpis:
        end_col = start_col + 2
        
        # Apply card fill and layout
        for r in range(5, 10):
            for c in range(start_col, end_col + 1):
                ws.cell(row=r, column=c).fill = card_fill
        
        # Apply outer borders to simulate a floating card
        for r in range(5, 10):
            ws.cell(row=r, column=start_col).border = Border(left=border_side)
            ws.cell(row=r, column=end_col).border = Border(right=border_side)
        for c in range(start_col, end_col + 1):
            ws.cell(row=5, column=c).border = Border(top=border_side)
            ws.cell(row=9, column=c).border = Border(bottom=border_side)
            
        # Fix corners
        ws.cell(row=5, column=start_col).border = Border(top=border_side, left=border_side)
        ws.cell(row=5, column=end_col).border = Border(top=border_side, right=border_side)
        ws.cell(row=9, column=start_col).border = Border(bottom=border_side, left=border_side)
        ws.cell(row=9, column=end_col).border = Border(bottom=border_side, right=border_side)
        
        # Populate text
        ws.cell(row=6, column=start_col, value=title_str).font = Font(size=12, bold=True, color=text_color)
        val_cell = ws.cell(row=8, column=start_col, value=val_str)
        val_cell.font = Font(size=18, bold=True, color=accent1)
        
    # Inject Backing Data (Hidden below dashboard visual area)
    data_start_row = 50
    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3], ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1], ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3], ["Jun", 195.1, 201.0],
        ["Jul", 192.4, 210.6], ["Aug", 186.3, 200.6],
        ["Sep", 194.2, 210.6], ["Oct", 205.2, 222.3],
        ["Nov", 204.3, 225.8], ["Dec", 201.5, 230.1]
    ]
    for r_idx, row in enumerate(trend_data, start=data_start_row):
        for c_idx, val in enumerate(row, start=2): # Columns B, C, D
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    radar_data = [
        ["Metric", "Score"],
        ["Speed", 54], ["Availability", 90],
        ["Quality", 86], ["Hygiene", 93],
        ["Service", 53]
    ]
    for r_idx, row in enumerate(radar_data, start=data_start_row):
        for c_idx, val in enumerate(row, start=6): # Columns F, G
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # Line Chart for Trend
    line_chart = LineChart()
    line_chart.title = "2021-2022 Sales Trend (in millions)"
    line_chart.height = 10
    line_chart.width = 16
    
    trend_data_ref = Reference(ws, min_col=3, min_row=data_start_row, max_col=4, max_row=data_start_row+12)
    trend_cats_ref = Reference(ws, min_col=2, min_row=data_start_row+1, max_row=data_start_row+12)
    line_chart.add_data(trend_data_ref, titles_from_data=True)
    line_chart.set_categories(trend_cats_ref)
    
    for idx, series in enumerate(line_chart.series):
        color = accent1 if idx == 0 else accent2
        series.graphicalProperties.line = LineProperties(solidFill=color)
        series.marker = Marker(symbol="circle", size=5)
        series.marker.graphicalProperties.solidFill = "FFFFFF"
        series.marker.graphicalProperties.line = LineProperties(solidFill=color)
        
    line_chart.y_axis.scaling.min = 180
    line_chart.y_axis.scaling.max = 240
    line_chart.legend.position = 'b'
    
    ws.add_chart(line_chart, "C11")
    
    # Radar Chart for Satisfaction
    radar_chart = RadarChart()
    radar_chart.title = "Customer Satisfaction"
    radar_chart.height = 10
    radar_chart.width = 10
    
    radar_data_ref = Reference(ws, min_col=7, min_row=data_start_row, max_row=data_start_row+5)
    radar_cats_ref = Reference(ws, min_col=6, min_row=data_start_row+1, max_row=data_start_row+5)
    radar_chart.add_data(radar_data_ref, titles_from_data=True)
    radar_chart.set_categories(radar_cats_ref)
    radar_chart.legend = None
    
    if radar_chart.series:
        radar_chart.series[0].graphicalProperties.line = LineProperties(solidFill=accent1)
        
    ws.add_chart(radar_chart, "K11")
```