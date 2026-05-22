from typing import List, Dict, Any
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", subtitle: str = "Evaluating Sales Agent Performance", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a complete Sales Performance Dashboard shell with KPI cards, 
    a conditionally formatted performance table, and trend charts.
    """
    ws: Worksheet = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # 1. Theme Setup (Fallback to a deep purple/gold theme inspired by the video)
    colors = {
        "primary": "5A4A78",      # Deep Purple
        "bg_light": "F4F3F8",     # Very light purple/gray
        "accent": "D4AF37",       # Gold
        "card_bg": "FFFFFF",
        "text_light": "FFFFFF",
        "text_dark": "333333",
        "text_muted": "777777",
        "bar_blue": "5B9BD5",
        "bar_purple": "9E87CB"
    }

    fills = {
        "primary": PatternFill("solid", fgColor=colors["primary"]),
        "bg_light": PatternFill("solid", fgColor=colors["bg_light"]),
        "card": PatternFill("solid", fgColor=colors["card_bg"]),
        "table_header": PatternFill("solid", fgColor=colors["primary"])
    }

    fonts = {
        "title": Font(name="Calibri", size=26, color=colors["text_light"], bold=True),
        "subtitle": Font(name="Calibri", size=14, color=colors["accent"]),
        "kpi_val": Font(name="Calibri", size=18, color=colors["text_dark"], bold=True),
        "kpi_lbl": Font(name="Calibri", size=10, color=colors["text_muted"], bold=True),
        "th": Font(name="Calibri", size=11, color=colors["text_light"], bold=True),
        "td": Font(name="Calibri", size=11, color=colors["text_dark"])
    }

    # 2. Canvas Background
    for row in range(1, 9):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = fills["primary"]
            
    for row in range(9, 45):
        for col in range(1, 20):
            ws.cell(row=row, column=col).fill = fills["bg_light"]

    # Column Widths
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 15  # Names
    for c in ['C', 'D', 'E', 'F']:
        ws.column_dimensions[c].width = 12

    # 3. Header Text
    ws["B2"] = title
    ws["B2"].font = fonts["title"]
    ws["B3"] = subtitle
    ws["B3"].font = fonts["subtitle"]

    # 4. KPI Strip
    kpis = [
        ("CALLS", "16,749"),
        ("REACHED", "3,328"),
        ("CLOSED", "1,203"),
        ("VALUE", "$646,979")
    ]

    border_card_outer = Border(
        top=Side(style='thin', color="DDDDDD"),
        bottom=Side(style='thin', color="DDDDDD"),
        left=Side(style='thin', color="DDDDDD"),
        right=Side(style='thin', color="DDDDDD")
    )
    border_kpi_divider = Border(
        left=Side(style='thick', color=colors["accent"]),
        top=Side(style='thin', color="DDDDDD"),
        bottom=Side(style='thin', color="DDDDDD"),
        right=Side(style='thin', color="DDDDDD")
    )

    for i, (label, val) in enumerate(kpis):
        start_col = 3 + (i * 3)  # C, F, I, L
        icon_cell = ws.cell(row=5, column=start_col)
        val_cell = ws.cell(row=5, column=start_col + 1)
        lbl_cell = ws.cell(row=7, column=start_col + 1)

        # Merge blocks
        ws.merge_cells(start_row=5, start_column=start_col, end_row=7, end_column=start_col)
        ws.merge_cells(start_row=5, start_column=start_col+1, end_row=6, end_column=start_col+1)

        # Apply fills & borders
        for r in range(5, 8):
            ws.cell(row=r, column=start_col).fill = fills["card"]
            ws.cell(row=r, column=start_col).border = border_card_outer
            ws.cell(row=r, column=start_col+1).fill = fills["card"]
            ws.cell(row=r, column=start_col+1).border = border_kpi_divider

        # Inject Data
        icon_cell.value = "📊" # Simulated icon
        icon_cell.alignment = Alignment(horizontal="center", vertical="center")
        icon_cell.font = Font(size=24)

        val_cell.value = val
        val_cell.font = fonts["kpi_val"]
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        lbl_cell.value = label
        lbl_cell.font = fonts["kpi_lbl"]
        lbl_cell.alignment = Alignment(horizontal="center", vertical="top")

    # 5. Agent Performance Table
    agents = [
        {"name": "Alice", "calls": 1031, "closed": 56, "value": 13519},
        {"name": "Bob", "calls": 661, "closed": 28, "value": 40092},
        {"name": "Charlie", "calls": 610, "closed": 67, "value": 45236},
        {"name": "Diana", "calls": 566, "closed": 26, "value": 38593},
        {"name": "Evan", "calls": 722, "closed": 16, "value": 17105},
        {"name": "Fiona", "calls": 840, "closed": 28, "value": 27234},
        {"name": "George", "calls": 927, "closed": 49, "value": 41200},
        {"name": "Hannah", "calls": 375, "closed": 48, "value": 2590},
        {"name": "Ian", "calls": 348, "closed": 14, "value": 17185},
        {"name": "Julia", "calls": 221, "closed": 16, "value": 13302},
    ]

    start_row = 10
    headers = ["Agent Name", "Total Calls", "Deals Closed", "Deal Value ($)"]
    for col_idx, header in enumerate(headers, start=2):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.fill = fills["table_header"]
        cell.font = fonts["th"]
        cell.alignment = Alignment(horizontal="center")

    for i, agent in enumerate(agents, start=1):
        r = start_row + i
        ws.cell(row=r, column=2, value=agent["name"]).font = fonts["td"]
        ws.cell(row=r, column=3, value=agent["calls"]).font = fonts["td"]
        ws.cell(row=r, column=4, value=agent["closed"]).font = fonts["td"]
        
        val_cell = ws.cell(row=r, column=5, value=agent["value"])
        val_cell.font = fonts["td"]
        val_cell.number_format = "$#,##0"

    # Add Conditional Formatting (Data Bars)
    calls_rule = DataBarRule(start_type='min', end_type='max', color=colors["bar_blue"], showValue=True)
    closed_rule = DataBarRule(start_type='min', end_type='max', color=colors["bar_purple"], showValue=True)
    value_rule = DataBarRule(start_type='min', end_type='max', color=colors["accent"], showValue=True)

    ws.conditional_formatting.add(f"C11:C{10+len(agents)}", calls_rule)
    ws.conditional_formatting.add(f"D11:D{10+len(agents)}", closed_rule)
    ws.conditional_formatting.add(f"E11:E{10+len(agents)}", value_rule)

    # 6. Charting (Hidden Data & Chart Object)
    # Write chart data far off to the right
    chart_data = [
        ["Month", "Total Sales"],
        ["Jan", 57863], ["Feb", 59230], ["Mar", 60127],
        ["Apr", 58604], ["May", 58261], ["Jun", 59025],
        ["Jul", 58846], ["Aug", 59868], ["Sep", 59025],
        ["Oct", 59137], ["Nov", 60654], ["Dec", 62000]
    ]
    
    for r_idx, row_data in enumerate(chart_data, start=10):
        ws.cell(row=r_idx, column=20, value=row_data[0])
        ws.cell(row=r_idx, column=21, value=row_data[1])

    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Total Sales Trend"
    chart.y_axis.title = "Revenue"
    chart.x_axis.title = "Month"
    chart.legend = None

    data_ref = Reference(ws, min_col=21, min_row=10, max_row=22)
    cats_ref = Reference(ws, min_col=20, min_row=11, max_row=22)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    
    # Change chart series color to primary theme color
    series = chart.series[0]
    series.graphicalProperties.solidFill = colors["primary"]

    ws.add_chart(chart, "H10")

