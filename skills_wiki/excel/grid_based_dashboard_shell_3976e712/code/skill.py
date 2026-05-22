from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Fallback palette mapped to a modern dashboard style
    bg_canvas = "F3F4F6" # Light Gray canvas
    bg_card = "FFFFFF"   # White cards
    text_main = "111827" # Dark Slate for text
    text_muted = "6B7280"# Muted Gray
    accent = "2563EB"    # Blue accent
    
    fill_canvas = PatternFill(start_color=bg_canvas, end_color=bg_canvas, fill_type="solid")
    fill_card = PatternFill(start_color=bg_card, end_color=bg_card, fill_type="solid")
    
    font_title = Font(color="FFFFFF", bold=True, size=18)
    font_card_title = Font(color=text_main, bold=True, size=12)
    font_kpi_val = Font(color=accent, bold=True, size=24)
    font_kpi_label = Font(color=text_muted, size=11, italic=True)
    
    # Apply canvas background to the working area
    for row in ws.iter_rows(min_row=1, max_row=30, min_col=1, max_col=15):
        for cell in row:
            cell.fill = fill_canvas
            
    # Top Header Strip
    ws.merge_cells("B2:M3")
    header_cell = ws["B2"]
    header_cell.value = title
    header_cell.font = font_title
    header_cell.fill = PatternFill(start_color=text_main, end_color=text_main, fill_type="solid")
    header_cell.alignment = Alignment(vertical="center", indent=1)
    
    # Helper to paint a card area with an outline border
    def draw_card(min_col, min_row, max_col, max_row, card_title):
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_card
                
                # Outer borders for the card
                top = Side(style='thin', color="D1D5DB") if r == min_row else None
                bottom = Side(style='thin', color="D1D5DB") if r == max_row else None
                left = Side(style='thin', color="D1D5DB") if c == min_col else None
                right = Side(style='thin', color="D1D5DB") if c == max_col else None
                
                # Divider under the title
                if r == min_row:
                    bottom = Side(style='thin', color="E5E7EB")
                    
                cell.border = Border(top=top, bottom=bottom, left=left, right=right)
        
        # Card Header
        ws.merge_cells(start_row=min_row, start_column=min_col, end_row=min_row, end_column=max_col)
        title_cell = ws.cell(row=min_row, column=min_col)
        title_cell.value = card_title
        title_cell.font = font_card_title
        title_cell.alignment = Alignment(vertical="center", horizontal="left", indent=1)

    # 1. KPI Cards Row
    draw_card(2, 5, 4, 8, "Total Sales")
    draw_card(6, 5, 8, 8, "Net Profit")
    draw_card(10, 5, 12, 8, "Customers")
    
    # Populate KPI Values
    kpis = [
        ("B7", "D7", "$2,544M"),
        ("F7", "H7", "$890M"),
        ("J7", "L7", "87.0M")
    ]
    for start_cell, end_cell, val in kpis:
        ws[start_cell] = val
        ws[start_cell].font = font_kpi_val
        ws[start_cell].alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(f"{start_cell}:{end_cell}")

    # 2. Chart Cards Row
    draw_card(2, 10, 8, 25, "Sales Trend (2021-2022)")
    draw_card(10, 10, 14, 25, "Sales by Country")
    
    # Create a hidden sheet for chart data
    ws_data = wb.create_sheet("Dashboard_Data")
    ws_data.sheet_state = 'hidden'
    
    # Inject Trend Data
    trend_data = [
        ["Month", "2021", "2022"],
        ["Jan", 201.9, 215.3],
        ["Feb", 204.2, 217.6],
        ["Mar", 198.6, 220.1],
        ["Apr", 199.2, 206.4],
        ["May", 206.4, 204.3],
        ["Jun", 201.5, 215.3],
        ["Jul", 192.4, 201.5],
        ["Aug", 186.3, 200.6],
        ["Sep", 194.2, 210.6]
    ]
    for row in trend_data:
        ws_data.append(row)
        
    line_chart = LineChart()
    line_chart.title = None
    line_chart.style = 13
    line_chart.y_axis.title = "Sales (M)"
    
    data_ref = Reference(ws_data, min_col=2, min_row=1, max_col=3, max_row=11)
    cats_ref = Reference(ws_data, min_col=1, min_row=2, max_row=11)
    line_chart.add_data(data_ref, titles_from_data=True)
    line_chart.set_categories(cats_ref)
    
    # Position Line Chart in first large card
    line_chart.width = 13.5
    line_chart.height = 7.5
    ws.add_chart(line_chart, "B12")
    
    # Inject Categorical Data
    country_data = [
        ["Country", "Sales"],
        ["Argentina", 953.3],
        ["Brazil", 553.2],
        ["Colombia", 432.4],
        ["Ecuador", 445.1],
        ["Peru", 425.1],
        ["Chile", 217.8]
    ]
    for row in country_data:
        ws_data.append(row)
        
    bar_chart = BarChart()
    bar_chart.type = "bar"
    bar_chart.title = None
    bar_chart.style = 10
    bar_chart.legend = None
    
    bar_data_ref = Reference(ws_data, min_col=2, min_row=12, max_row=18)
    bar_cats_ref = Reference(ws_data, min_col=1, min_row=13, max_row=18)
    bar_chart.add_data(bar_data_ref, titles_from_data=True)
    bar_chart.set_categories(bar_cats_ref)
    
    # Position Bar Chart in second large card
    bar_chart.width = 9.0
    bar_chart.height = 7.5
    ws.add_chart(bar_chart, "J12")
    
    # Polish grid sizing
    ws.column_dimensions['A'].width = 3
    for col in "BCDEFGHJKLMN":
        ws.column_dimensions[col].width = 11
