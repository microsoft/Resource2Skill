def render(ws, anchor: str, *, kpi_name: str = "Customer Satisfaction", actual_val: float = 87, target_val: float = 100, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.chart import DoughnutChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.utils import coordinate_to_tuple
    
    # 1. Resolve theme colors
    theme_colors = {
        "corporate_blue": {"primary": "1F4E78", "muted": "D9D9D9"},
        "modern_green": {"primary": "385723", "muted": "E2EFDA"},
        "alert_red": {"primary": "C00000", "muted": "F2DCDB"}
    }
    palette = theme_colors.get(theme, theme_colors["corporate_blue"])
    
    row, col = coordinate_to_tuple(anchor)
    
    # 2. Calculate percentages
    pct_complete = min(actual_val / target_val, 1.0) if target_val > 0 else 0
    pct_remaining = max(1.0 - pct_complete, 0)
    
    # 3. Write backing data grid
    ws.cell(row=row, column=col, value="Category")
    ws.cell(row=row, column=col+1, value="Value")
    
    c_label = ws.cell(row=row+1, column=col, value="Completed")
    c_val = ws.cell(row=row+1, column=col+1, value=pct_complete)
    c_val.number_format = '0%'
    
    r_label = ws.cell(row=row+2, column=col, value="Remaining")
    r_val = ws.cell(row=row+2, column=col+1, value=pct_remaining)
    r_val.number_format = '0%'
    
    # 4. Create and configure the Doughnut Chart
    chart = DoughnutChart()
    # Embed the percentage directly in the title to mimic a floating center text box
    chart.title = f"{kpi_name}\n{pct_complete*100:.0f}%"
    
    labels = Reference(ws, min_col=col, min_row=row+1, max_row=row+2)
    data = Reference(ws, min_col=col+1, min_row=row+1, max_row=row+2)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(labels)
    
    # 5. Styling: Thicker ring and no legend
    chart.holeSize = 65 
    chart.legend = None 
    
    # 6. Apply individual slice colors
    series = chart.series[0]
    
    # Slice 0: Completed (Primary color)
    pt0 = DataPoint(idx=0)
    pt0.graphicalProperties.solidFill = palette["primary"]
    series.dPt.append(pt0)
    
    # Slice 1: Remaining (Muted color)
    pt1 = DataPoint(idx=1)
    pt1.graphicalProperties.solidFill = palette["muted"]
    series.dPt.append(pt1)
    
    # 7. Position and sizing
    chart.width = 6.5
    chart.height = 6.5
    
    # Add chart directly over the backing data to hide it
    ws.add_chart(chart, anchor)
