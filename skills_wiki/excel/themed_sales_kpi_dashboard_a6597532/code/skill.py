def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.chart import BarChart, Reference
    from openpyxl.formatting.rule import DataBarRule
    from openpyxl.utils import get_column_letter

    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Theme Configuration
    palette = {
        "header_bg": "4B286D",       # Deep Purple
        "canvas_bg": "F2EFF5",       # Light Purple
        "card_bg": "FFFFFF",         # White
        "accent_yellow": "FFC000",   # Gold/Yellow
        "accent_purple": "7030A0",   # Purple
        "text_light": "FFFFFF",      # White
        "text_dark": "333333",       # Dark Grey
        "text_muted": "666666"       # Medium Grey
    }

    # 2. Paint Canvas & Header Zones
    canvas_fill = PatternFill(start_color=palette["canvas_bg"], fill_type="solid")
    header_fill = PatternFill(start_color=palette["header_bg"], fill_type="solid")

    for row in range(1, 45):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = canvas_fill

    for row in range(1, 9):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = header_fill

    # Set uniform column widths
    ws.column_dimensions['A'].width = 3
    for c in range(2, 20):
        ws.column_dimensions[get_column_letter(c)].width = 11

    # Add Titles
    title_cell = ws.cell(row=2, column=2, value=title)
    title_cell.font = Font(size=28, bold=True, color=palette["text_light"])
    
    subtitle_cell = ws.cell(row=4, column=2, value="Evaluating Sales Agent Performance")
    subtitle_cell.font = Font(size=14, color=palette["accent_yellow"])

    # 3. KPI Cards Layout
    kpis = [
        {"label": "CALLS", "value": 16749, "fmt": "#,##0", "color": palette["accent_yellow"]},
        {"label": "REACHED", "value": 3328, "fmt": "#,##0", "color": palette["accent_yellow"]},
        {"label": "CLOSED", "value": 1203, "fmt": "#,##0", "color": palette["accent_purple"]},
        {"label": "VALUE", "value": 646979, "fmt": "$#,##0", "color": palette["accent_purple"]}
    ]
    
    col_offsets = [2, 6, 10, 14] # B, F, J, N
    for kpi, c_start in zip(kpis, col_offsets):
        # Left Accent Bar
        ws.merge_cells(start_row=10, start_column=c_start, end_row=13, end_column=c_start)
        bar_cell = ws.cell(row=10, column=c_start)
        bar_cell.fill = PatternFill(start_color=kpi["color"], fill_type="solid")
        
        # Content Area
        ws.merge_cells(start_row=10, start_column=c_start+1, end_row=13, end_column=c_start+2)
        for r in range(10, 14):
            for c in range(c_start+1, c_start+3):
                ws.cell(row=r, column=c).fill = PatternFill(start_color=palette["card_bg"], fill_type="solid")
                
        val_cell = ws.cell(row=11, column=c_start+1, value=kpi["value"])
        val_cell.font = Font(size=20, bold=True, color=palette["text_dark"])
        val_cell.alignment = Alignment(horizontal="center", vertical="bottom")
        val_cell.number_format = kpi["fmt"]
        
        lbl_cell = ws.cell(row=12, column=c_start+1, value=kpi["label"])
        lbl_cell.font = Font(size=12, color=palette["text_muted"])
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")

    # 4. Agent Performance Table with DataBars
    agent_data = [
        ["Name", "Total Calls", "Calls Reached", "Deals Closed", "Deal Value"],
        ["Alice", 1031, 56, 37, 13519],
        ["Bob", 661, 73, 28, 40092],
        ["Charlie", 610, 86, 67, 45236],
        ["Diana", 566, 163, 26, 38593],
        ["Evan", 722, 168, 91, 11093]
    ]
    
    for r_idx, row_data in enumerate(agent_data, start=16):
        for c_idx, val in enumerate(row_data, start=2): # Col B
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            if r_idx == 16:
                cell.font = Font(bold=True, color=palette["text_light"])
                cell.fill = PatternFill(start_color=palette["header_bg"], fill_type="solid")
            else:
                cell.fill = PatternFill(start_color=palette["card_bg"], fill_type="solid")
                if c_idx > 2:
                    cell.number_format = "#,##0"
                if c_idx == 6:
                    cell.number_format = "$#,##0"

    # Apply Conditional Formatting DataBars
    ws.conditional_formatting.add(f"C17:C21", DataBarRule(start_type='min', end_type='max', color=palette["accent_purple"]))
    ws.conditional_formatting.add(f"D17:D21", DataBarRule(start_type='min', end_type='max', color=palette["accent_yellow"]))
    ws.conditional_formatting.add(f"E17:E21", DataBarRule(start_type='min', end_type='max', color=palette["accent_purple"]))

    # 5. Hidden Data & Charts
    trend_data = [
        ["Month", "Calls Reached", "Deals Closed", "Total Sales"],
        ["Jan", 301, 115, 57863],
        ["Feb", 311, 110, 59230],
        ["Mar", 300, 112, 60127],
        ["Apr", 298, 113, 58684],
        ["May", 307, 110, 58261],
        ["Jun", 305, 110, 59025]
    ]
    
    # Write to hidden columns AA:AD (27:30)
    for r_idx, row_data in enumerate(trend_data, start=16):
        for c_idx, val in enumerate(row_data, start=27):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # Chart 1: Overlay Column Chart
    overlay_chart = BarChart()
    overlay_chart.type = "col"
    overlay_chart.overlap = 100  # Key to the visual overlay effect
    overlay_chart.gapWidth = 50
    overlay_chart.title = "Reached vs Closed"
    overlay_chart.height = 7.5
    overlay_chart.width = 14
    
    data_reached = Reference(ws, min_col=28, min_row=16, max_row=22)
    overlay_chart.add_data(data_reached, titles_from_data=True)
    
    data_closed = Reference(ws, min_col=29, min_row=16, max_row=22)
    overlay_chart.add_data(data_closed, titles_from_data=True)
    
    cats = Reference(ws, min_col=27, min_row=17, max_row=22)
    overlay_chart.set_categories(cats)
    
    # Set explicit colors for the series
    overlay_chart.series[0].graphicalProperties.solidFill = palette["accent_yellow"]
    overlay_chart.series[1].graphicalProperties.solidFill = palette["accent_purple"]
    
    ws.add_chart(overlay_chart, "H16")

    # Chart 2: Standard Sales Trend
    sales_chart = BarChart()
    sales_chart.type = "col"
    sales_chart.title = "Total Sales"
    sales_chart.height = 7.5
    sales_chart.width = 14
    
    data_sales = Reference(ws, min_col=30, min_row=16, max_row=22)
    sales_chart.add_data(data_sales, titles_from_data=True)
    sales_chart.set_categories(cats)
    sales_chart.series[0].graphicalProperties.solidFill = palette["header_bg"]
    
    ws.add_chart(sales_chart, "H26")
