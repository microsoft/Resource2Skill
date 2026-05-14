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
