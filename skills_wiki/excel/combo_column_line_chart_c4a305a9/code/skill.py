from openpyxl.chart import BarChart, LineChart, Reference

def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a Combo Chart (Column + Line on Secondary Axis) at the given anchor.
    This pattern is typically used in dashboards to show Volume (Bars) vs Count/Margin (Line).
    """
    # 1. Setup sample data for the combo chart
    # In practice, this data would refer to a Pivot Table or an aggregation table.
    data = [
        ["Sales Rep", "Sum of Sales Value", "Count of Sales Value"],
        ["Alex", 6085, 10],
        ["Chang", 1711, 3],
        ["Glen", 2725, 5],
        ["Jenny", 3639, 9],
        ["Martha", 3107, 8],
        ["Mike", 2482, 5],
        ["Rose", 2356, 6]
    ]
    
    # Write data to a separate area (e.g., starting at column AA) to keep the dashboard visual clean
    start_row = kwargs.get("data_start_row", 1)
    start_col = kwargs.get("data_start_col", 27)  # Column AA
    
    for r_idx, row in enumerate(data, start=start_row):
        for c_idx, val in enumerate(row, start=start_col):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # 2. Create the Primary Bar Chart (Column)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.title = "Sales Rep Performance - Value and Count"
    bar_chart.style = 10  # Standard clean preset style
    
    # Turn off legend and gridlines for a cleaner dashboard look
    bar_chart.legend = None
    bar_chart.y_axis.majorGridlines = None
    bar_chart.y_axis.title = "Sales Value ($)"
    
    # 3. Create the Secondary Line Chart
    line_chart = LineChart()
    
    # Configure secondary axis to appear on the right
    line_chart.y_axis.axId = 200
    line_chart.y_axis.title = "Sales Count"
    line_chart.y_axis.crosses = "max" 
    
    # 4. Define data references
    max_r = start_row + len(data) - 1
    cats = Reference(ws, min_col=start_col, min_row=start_row + 1, max_row=max_r)
    bar_data = Reference(ws, min_col=start_col + 1, min_row=start_row, max_row=max_r)
    line_data = Reference(ws, min_col=start_col + 2, min_row=start_row, max_row=max_r)
    
    # 5. Add data and categories to charts
    bar_chart.add_data(bar_data, titles_from_data=True)
    bar_chart.set_categories(cats)
    
    line_chart.add_data(line_data, titles_from_data=True)
    line_chart.set_categories(cats)
    
    # 6. Combine the charts
    bar_chart += line_chart
    
    # Set chart dimensions to fit nicely in a dashboard grid
    bar_chart.width = 16
    bar_chart.height = 8
    
    # 7. Place on worksheet
    ws.add_chart(bar_chart, anchor)
