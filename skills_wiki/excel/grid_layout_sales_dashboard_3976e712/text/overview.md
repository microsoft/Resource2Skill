### 1. High-level Skill Pattern Extraction

> **Skill Name**: Grid Layout Sales Dashboard

* **Tier**: sheet_shell
* **Core Mechanism**: Constructs a modern, shape-less dashboard layout by manipulating cell fill colors to create visual "cards" against a hidden-grid background. It populates charts with `noFill` transparency so that cell values underneath (like a bold KPI percentage) show perfectly through the center of a Doughnut chart.
* **Applicability**: Best for high-level executive summaries or KPI dashboards where you want a modern "web app" aesthetic (sidebar, cards) without relying on floating shapes that can misalign or break in Excel.

### 2. Structural Breakdown

- **Data Layout**: Raw data is populated in hidden or out-of-view columns (e.g., `AA:AD`). The dashboard occupies `A1:M25`.
- **Formula Logic**: Directly assigns values to the hidden data range, which feeds into the charts via `openpyxl.chart.Reference`.
- **Visual Design**: 
  - Uses a dark vertical strip (`Col A`) to simulate a sidebar.
  - Groups cells into gray "cards" surrounded by white gaps.
  - Gridlines are completely hidden via `ws.sheet_view.showGridLines = False`.
- **Charts/Tables**: 
  - A Doughnut chart for KPI tracking with the center hole positioned over a formatted cell to act as a dynamic text label.
  - A Line chart for trending data, with backgrounds completely disabled (`noFill=True`) so it blends directly into the card.
- **Theme Hooks**: Primary dark accent used for the sidebar and chart series lines, with neutral light grays used for card backgrounds.

### 3. Reproduction Code

```python
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.chart import LineChart, DoughnutChart, Reference
from openpyxl.chart.shapes import GraphicalProperties

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    
    # Hide gridlines to enhance the "web-app" dashboard feel
    ws.sheet_view.showGridLines = False
    
    # Theme fallbacks
    sidebar_color = "1E3A8A" # Dark blue
    card_color = "F3F4F6"    # Light gray
    text_color = "374151"    # Dark gray
    
    sidebar_fill = PatternFill("solid", fgColor=sidebar_color)
    card_fill = PatternFill("solid", fgColor=card_color)
    
    # 1. Setup grid dimensions to create "Gaps" and "Cards"
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 3
    ws.column_dimensions['F'].width = 3
    ws.column_dimensions['J'].width = 3
    for col in ['C', 'D', 'E', 'G', 'H', 'I', 'K', 'L', 'M']:
        ws.column_dimensions[col].width = 12
        
    for r in range(1, 25):
        ws.row_dimensions[r].height = 15
    ws.row_dimensions[2].height = 25
    ws.row_dimensions[4].height = 10
    ws.row_dimensions[10].height = 10
    
    # 2. Draw Navigation Sidebar
    for r in range(1, 25):
        ws.cell(row=r, column=1).fill = sidebar_fill
        
    # 3. Draw Title Header
    for row in ws.iter_rows(min_row=2, max_row=3, min_col=3, max_col=13):
        for cell in row:
            cell.fill = card_fill
    ws.merge_cells("C2:M3")
    title_cell = ws["C2"]
    title_cell.value = title
    title_cell.font = Font(size=20, bold=True, color=sidebar_color)
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # 4. Draw Layout Cards
    def draw_card(min_col, max_col, min_row, max_row, header_text):
        # Fill card area
        for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
            for cell in row:
                cell.fill = card_fill
        # Merge header row for title
        ws.merge_cells(start_row=min_row, start_column=min_col, end_row=min_row, end_column=max_col)
        h_cell = ws.cell(row=min_row, column=min_col)
        h_cell.value = header_text
        h_cell.font = Font(size=12, bold=True, color=text_color)
        h_cell.alignment = Alignment(horizontal="center", vertical="center")

    draw_card(3, 5, 5, 9, "Sales KPI")
    draw_card(7, 9, 5, 9, "Profit KPI")
    draw_card(11, 13, 5, 9, "Customers KPI")
    
    draw_card(3, 9, 11, 22, "2022 Sales Trend (in millions)")
    draw_card(11, 13, 11, 22, "Satisfaction")
    
    # 5. Populate Data Out-of-Bounds (Columns AA+)
    trend_data = [
        ["Month", "Sales"],
        ["Jan", 201], ["Feb", 204], ["Mar", 198], ["Apr", 199],
        ["May", 206], ["Jun", 195], ["Jul", 192], ["Aug", 189],
        ["Sep", 194], ["Oct", 196], ["Nov", 205], ["Dec", 204]
    ]
    for i, row in enumerate(trend_data, start=1):
        for j, val in enumerate(row, start=27): # AA is Col 27
            ws.cell(row=i, column=j, value=val)
            
    kpi_data = [
        ["Metric", "Value"],
        ["Complete", 0.85],
        ["Remainder", 0.15]
    ]
    for i, row in enumerate(kpi_data, start=1):
        for j, val in enumerate(row, start=30): # AD is Col 30
            ws.cell(row=i, column=j, value=val)
            if i > 1 and j == 31:
                ws.cell(row=i, column=j).number_format = "0%"

    # 6. Create Sales Trend Line Chart
    lc = LineChart()
    lc.style = 2
    lc.title = None
    data = Reference(ws, min_col=28, min_row=1, max_row=13)
    cats = Reference(ws, min_col=27, min_row=2, max_row=13)
    lc.add_data(data, titles_from_data=True)
    lc.set_categories(cats)
    
    # Make chart transparent so the gray card fill acts as the background
    lc.graphicalProperties = GraphicalProperties(noFill=True)
    lc.graphicalProperties.line.noFill = True
    lc.legend = None
    lc.width = 14
    lc.height = 5.5
    
    s1 = lc.series[0]
    s1.graphicalProperties.line.solidFill = sidebar_color
    s1.graphicalProperties.line.width = 30000
    
    ws.add_chart(lc, "C12")
    
    # 7. Create Doughnut Chart for KPI
    dc = DoughnutChart()
    dc.style = 10
    dc.title = None
    data = Reference(ws, min_col=31, min_row=1, max_row=3)
    cats = Reference(ws, min_col=30, min_row=2, max_row=3)
    dc.add_data(data, titles_from_data=True)
    dc.set_categories(cats)
    
    # Transparency trick to let the grid cell value show through the doughnut hole
    dc.graphicalProperties = GraphicalProperties(noFill=True)
    dc.graphicalProperties.line.noFill = True
    dc.legend = None
    dc.holeSize = 65
    dc.width = 5.5
    dc.height = 3.5
    
    ws.add_chart(dc, "C6")
    
    # Write the KPI center-label directly to the grid beneath the chart
    center_cell = ws["D7"]
    center_cell.value = 0.85
    center_cell.number_format = "0%"
    center_cell.font = Font(size=20, bold=True, color=sidebar_color)
    center_cell.alignment = Alignment(horizontal="center", vertical="center")
```