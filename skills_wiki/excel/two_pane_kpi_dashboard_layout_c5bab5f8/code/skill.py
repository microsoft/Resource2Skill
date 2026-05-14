from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", kpis: list = None, **kwargs) -> None:
    """
    Renders a two-pane dashboard shell with a dark KPI side-panel on the left 
    and a light chart canvas on the right.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Attempt to load theme palette, falling back to the video's green aesthetic
    try:
        from skills_library.excel.components._helpers import get_theme_palette
        palette = get_theme_palette(theme)
        primary_color = palette.get("primary_color", "1E3F20").replace("#", "")
        bg_color = palette.get("bg_color", "E8F5E9").replace("#", "")
    except ImportError:
        primary_color = "1E3F20"  # Dark forest green
        bg_color = "E8F5E9"       # Light mint green
        
    text_light = "FFFFFF"
    text_dark = "000000"

    # 1. Set up Layout Panes
    ws.column_dimensions['A'].width = 2
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 2
    ws.column_dimensions['D'].width = 2
    
    left_fill = PatternFill("solid", fgColor=primary_color)
    main_fill = PatternFill("solid", fgColor=bg_color)

    # Fill backgrounds to simulate a standalone app interface (Rows 1 to 50)
    for row in range(1, 51):
        for col in range(1, 4):  # Cols A, B, C
            ws.cell(row=row, column=col).fill = left_fill
        for col in range(4, 25): # Cols D through X
            ws.cell(row=row, column=col).fill = main_fill

    # 2. Dashboard Title in Side Panel
    title_cell = ws.cell(row=2, column=2, value=title.upper())
    title_cell.font = Font(name="Arial", size=18, bold=True, color=text_light)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 3. KPI Side Panel Setup
    if not kpis:
        kpis = [
            {"label": "Total Orders", "value": "2,400"},
            {"label": "Total Revenue", "value": "$649.0K"},
            {"label": "Avg. Rating", "value": "4.0"},
            {"label": "Avg. Days to Deliver", "value": "2.3"}
        ]

    start_row = 6
    for kpi in kpis:
        label_cell = ws.cell(row=start_row, column=2, value=kpi["label"])
        label_cell.font = Font(name="Arial", size=10, bold=False, color=text_light)
        label_cell.alignment = Alignment(horizontal="center")

        val_cell = ws.cell(row=start_row + 1, column=2, value=kpi["value"])
        val_cell.font = Font(name="Arial", size=20, bold=True, color=text_light)
        val_cell.alignment = Alignment(horizontal="center")

        start_row += 4

    # 4. Main Canvas Setup (Demonstration Chart)
    ws.cell(row=2, column=5, value="Last 3 Months Trend").font = Font(name="Arial", size=14, bold=True, color=primary_color)
    
    # Hidden data for the chart (typically this would live on a separate 'Pivots' sheet)
    chart_data = [
        ("Month", "Orders"),
        ("Jan", 730),
        ("Feb", 861),
        ("Mar", 809)
    ]
    
    for r_idx, row_data in enumerate(chart_data, start=40):
        for c_idx, value in enumerate(row_data, start=5):
            ws.cell(row=r_idx, column=c_idx, value=value).font = Font(color=text_dark)

    chart = BarChart()
    chart.title = None
    chart.style = 11
    
    data_ref = Reference(ws, min_col=6, min_row=40, max_row=43)
    cats_ref = Reference(ws, min_col=5, min_row=41, max_row=43)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 15
    chart.height = 7.5
    chart.legend = None
    
    # Place the chart gracefully in the light canvas area
    ws.add_chart(chart, "E4")
