from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference

def render_workbook(wb, *, title: str = "Regional Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Builds an interactive KPI dashboard with a side navigation pane, metric cards, and charts.
    """
    # 1. Setup Sheets
    if "Sheet" in wb.sheetnames:
        ws_dash = wb["Sheet"]
        ws_dash.title = "Dashboard"
    else:
        ws_dash = wb.create_sheet("Dashboard")
        
    ws_data = wb.create_sheet("Data")
    
    # 2. Populate Data Sheet (Backend)
    data_kpis = [
        ["Metric", "Value", "Target", "Progress"],
        ["Sales", 2544, 3000, 0.848],
        ["Profit", 890, 1000, 0.890],
        ["Customers", 87, 100, 0.870],
    ]
    for r, row in enumerate(data_kpis, 1):
        for c, val in enumerate(row, 1):
            ws_data.cell(row=r, column=c, value=val)

    data_trend = [
        ["Month", "Sales"],
        ["Jan", 201], ["Feb", 204], ["Mar", 198], ["Apr", 199],
        ["May", 206], ["Jun", 195], ["Jul", 192], ["Aug", 189],
        ["Sep", 194], ["Oct", 196], ["Nov", 205], ["Dec", 204]
    ]
    for r, row in enumerate(data_trend, 6):
        for c, val in enumerate(row, 1):
            ws_data.cell(row=r, column=c, value=val)

    data_country = [
        ["Country", "Sales"],
        ["Argentina", 953],
        ["Colombia", 432],
        ["Brazil", 553],
        ["Ecuador", 445],
        ["Peru", 425],
        ["Chile", 253]
    ]
    for r, row in enumerate(data_country, 6):
        for c, val in enumerate(row, 4):
            ws_data.cell(row=r, column=c, value=val)

    # 3. Format Dashboard Shell Canvas
    ws_dash.sheet_view.showGridLines = False
    dash_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")
    
    # Fill dashboard background (Rows 1-30, Cols 2-20)
    for r in range(1, 32):
        for c in range(2, 21):
            ws_dash.cell(row=r, column=c).fill = dash_fill
            
    # Set uniform column widths for the grid layout
    for col_letter in "BCDEFGHIJKLMNOPQRST":
        ws_dash.column_dimensions[col_letter].width = 9

    # 4. Interactive Side Navigation
    ws_dash.column_dimensions['A'].width = 8
    nav_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    for r in range(1, 32):
        ws_dash.cell(row=r, column=1).fill = nav_fill

    nav_icons = [
        (4, "🏠", "#Dashboard!A1"),
        (8, "📊", "#Data!A1"),
        (12, "✉️", "#Data!A1")
    ]
    for row, icon, link in nav_icons:
        cell = ws_dash.cell(row=row, column=1)
        cell.value = icon
        cell.font = Font(size=20, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.hyperlink = link

    # 5. Dashboard Header
    ws_dash.merge_cells("B2:K2")
    header = ws_dash.cell(row=2, column=2)
    header.value = title
    header.font = Font(name="Arial", size=22, bold=True, color="111827")
    header.alignment = Alignment(vertical="center")

    # Helper function to draw elevated KPI Cards
    def create_card(ws, sr, sc, er, ec, card_title, value_ref, val_format="#,##0"):
        fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        bd = Side(border_style="thin", color="D1D5DB")
        for r in range(sr, er + 1):
            for c in range(sc, ec + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill
                # Apply outer border only
                cell.border = Border(
                    top=bd if r == sr else None,
                    bottom=bd if r == er else None,
                    left=bd if c == sc else None,
                    right=bd if c == ec else None
                )
        
        ws.merge_cells(start_row=sr, start_column=sc, end_row=sr, end_column=ec)
        ws.merge_cells(start_row=sr+1, start_column=sc, end_row=er, end_column=ec)

        title_cell = ws.cell(row=sr, column=sc)
        title_cell.value = " " + card_title
        title_cell.font = Font(name="Arial", size=11, color="6B7280")
        title_cell.alignment = Alignment(vertical="center", horizontal="left")

        val_cell = ws.cell(row=sr+1, column=sc)
        val_cell.value = f"={value_ref}"
        val_cell.font = Font(name="Arial", size=24, color="111827", bold=True)
        val_cell.number_format = val_format
        val_cell.alignment = Alignment(vertical="center", horizontal="center")

    # 6. Build KPI Cards
    create_card(ws_dash, 4, 2, 6, 6, "Total Sales (M)", "Data!B2", "$#,##0")
    create_card(ws_dash, 4, 8, 6, 12, "Net Profit (M)", "Data!B3", "$#,##0")
    create_card(ws_dash, 4, 14, 6, 18, "Active Customers", "Data!B4", "#,##0")

    # 7. Add Charts
    # Trend Chart
    lc = LineChart()
    lc.title = "Sales Trend"
    lc.style = 13
    lc.width = 14
    lc.height = 8
    lc.legend = None
    lc.x_axis.majorTickMark = "none"
    lc.y_axis.majorTickMark = "none"
    
    data_ref = Reference(ws_data, min_col=2, min_row=6, max_row=18)
    cats_ref = Reference(ws_data, min_col=1, min_row=7, max_row=18)
    lc.add_data(data_ref, titles_from_data=True)
    lc.set_categories(cats_ref)
    ws_dash.add_chart(lc, "B8")

    # Country Bar Chart
    bc = BarChart()
    bc.type = "bar"
    bc.direction = "bar"
    bc.title = "Sales by Country"
    bc.style = 10
    bc.width = 14
    bc.height = 8
    bc.legend = None
    bc.x_axis.majorTickMark = "none"
    bc.y_axis.majorTickMark = "none"
    
    data_ref2 = Reference(ws_data, min_col=5, min_row=6, max_row=13)
    cats_ref2 = Reference(ws_data, min_col=4, min_row=7, max_row=13)
    bc.add_data(data_ref2, titles_from_data=True)
    bc.set_categories(cats_ref2)
    ws_dash.add_chart(bc, "K8")

    # 8. Tidy up the Data sheet
    ws_data.sheet_view.showGridLines = False
    
    # Hide the data sheet for a true "app" feel (optional but recommended)
    # ws_data.sheet_state = 'hidden'
