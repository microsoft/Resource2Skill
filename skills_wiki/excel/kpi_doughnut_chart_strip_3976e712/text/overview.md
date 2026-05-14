### 1. High-level Skill Pattern Extraction

> **Skill Name**: KPI Doughnut Chart Strip

* **Tier**: component
* **Core Mechanism**: Generates a horizontal layout of KPI summary cards. Each card pairs a large absolute metric value with a Doughnut chart showing percentage completion. The doughnut hole size is adjusted to 65% for a modern, thick-ringed look, with legends and titles hidden to minimize visual clutter.
* **Applicability**: Ideal for the top summary row of an executive dashboard to highlight primary metrics and their target attainment rates at a glance.

### 2. Structural Breakdown

- **Data Layout**: Renders the presentation labels and absolute values directly at the anchor. Stashes the percentage data (Actual and Remainder) securely below the visible area to feed the charts without cluttering the UI.
- **Formula Logic**: Uses a dynamic remainder formula (`=1 - Actual`) in the hidden data cells so the Doughnut chart updates automatically if the actual percentage is modified.
- **Visual Design**: Employs a clean spatial layout, placing text to the left and the chart to the right of each KPI block. Uses bold, contrasting fonts for the metric titles and values.
- **Charts/Tables**: Standard Doughnut charts with `.holeSize = 65`. Chart titles and legends are explicitly disabled for a cleaner aesthetic.
- **Theme Hooks**: Utilizes standard color assignments, mapping titles and values to deep accent colors and dark grays to ensure readability.

### 3. Reproduction Code

```python
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.styles import Font

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    start_row = ws[anchor].row
    start_col = ws[anchor].column
    
    kpis = [
        {"title": "Sales", "val": "$2,544", "pct": 0.85},
        {"title": "Profit", "val": "$890", "pct": 0.89},
        {"title": "# of Customers", "val": "87.0", "pct": 0.87},
    ]
    
    # Hidden data area for chart sources (placed 12 rows below the visual cards)
    data_row = start_row + 12
    ws.cell(row=data_row, column=start_col, value="KPI Data Source").font = Font(italic=True)
    
    for i, kpi in enumerate(kpis):
        col_offset = i * 4
        col = start_col + col_offset
        
        # Display Text
        title_cell = ws.cell(row=start_row, column=col)
        title_cell.value = kpi["title"]
        title_cell.font = Font(size=12, bold=True, color="1F497D")
        
        val_cell = ws.cell(row=start_row+1, column=col)
        val_cell.value = kpi["val"]
        val_cell.font = Font(size=18, bold=True, color="333333")
        
        # Chart Data & Formula Logic
        ws.cell(row=data_row+1, column=col, value="Actual")
        ws.cell(row=data_row+2, column=col, value="Remainder")
        
        actual_cell = ws.cell(row=data_row+1, column=col+1, value=kpi["pct"])
        actual_cell.number_format = "0%"
        
        rem_cell = ws.cell(row=data_row+2, column=col+1, value=f"=1-{actual_cell.coordinate}")
        rem_cell.number_format = "0%"
        
        # Generate Doughnut Chart
        chart = DoughnutChart()
        labels = Reference(ws, min_col=col, min_row=data_row+1, max_row=data_row+2)
        data = Reference(ws, min_col=col+1, min_row=data_row+1, max_row=data_row+2)
        
        chart.add_data(data, titles_from_data=False)
        chart.set_categories(labels)
        
        # Formatting specific to the minimalist dashboard style
        chart.legend = None
        chart.title = None
        chart.holeSize = 65  # Key design adjustment for thicker rings
        
        # Position chart next to the text
        chart.anchor = ws.cell(row=start_row, column=col+1).coordinate
        chart.width = 4.5
        chart.height = 3.0
        
        ws.add_chart(chart)
```