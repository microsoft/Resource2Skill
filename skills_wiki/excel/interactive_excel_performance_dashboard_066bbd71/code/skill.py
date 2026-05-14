from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import Series
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles.colors import Color
from openpyxl.pivot.table import PivotTable, PivotField, DataField

import datetime
import calendar

# Standard helper for loading theme colors
def _load_theme_colors(wb, theme_name="corporate_blue"):
    theme_palettes = {
        "corporate_blue": {
            "header_bg": "FF1E3F58", "header_fg": "FFFFFFFF",
            "accent1": "FF4472C4", "accent2": "FFED7D31", "accent3": "FFB5B5B5",
            "text_color": "FF000000", "background_color": "FFFFFFFF",
            "slicer_bg": "FFDEEAF6", "slicer_item_bg": "FFD9D9D9",
            "chart_bg": "FFFFFFFF", "chart_border": "FFD9D9D9",
            "gridline_color": "FFD9D9D9"
        },
        "minimalist_gray": {
            "header_bg": "FF666666", "header_fg": "FFFFFFFF",
            "accent1": "FF8E8E8E", "accent2": "FFBDBDBD", "accent3": "FFDDDDDD",
            "text_color": "FF000000", "background_color": "FFFFFFFF",
            "slicer_bg": "FFEEEEEE", "slicer_item_bg": "FFC0C0C0",
            "chart_bg": "FFFFFFFF", "chart_border": "FFC0C0C0",
            "gridline_color": "FFC0C0C0"
        }
    }
    return theme_palettes.get(theme_name, theme_palettes["corporate_blue"])

def _create_fill(hex_color):
    return PatternFill(start_color=hex_color, end_color=hex_color, fill_type="solid")

def _create_font(name="Calibri", size=11, bold=False, color="FF000000"):
    return Font(name=name, size=size, bold=bold, color=color)

def render_workbook(wb: Workbook, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    colors = _load_theme_colors(wb, theme)

    # Prepare data sheet
    data_ws = wb.create_sheet("Data", 0)
    _prepare_data_sheet(data_ws)

    # Prepare dashboard sheet
    dashboard_ws = wb.create_sheet("Dashboard", 1)
    _prepare_dashboard_sheet(dashboard_ws, title, colors)

    # Create PivotTables and Charts
    # Note: openpyxl's native PivotTable creation is somewhat limited.
    # Date grouping, slicers, timelines, and linking across multiple PivotTables are largely UI-driven.
    # The code below sets up the PivotTables and Charts, but full interactivity (slicers/timelines)
    # would need to be added manually in Excel after generation.

    pivot_data_source = f"{data_ws.title}!SalesData"

    profit_by_market_ws = wb.create_sheet("Profit by market and cookie", 2)
    pt_profit_market = _create_pivot_table_sheet(
        profit_by_market_ws, pivot_data_source,
        row_fields=['Country'], column_fields=['Product'], value_fields=[('Profit', 'sum')],
        value_format='$#,##0'
    )
    _create_pivot_chart(
        profit_by_market_ws, profit_by_market_ws["A3"],
        'stacked_column', 'Profit by Market & Cookie Type', colors,
        chart_height=10, chart_width=12
    )
    profit_by_market_ws.sheet_state = 'hidden'

    units_sold_ws = wb.create_sheet("Units sold each month", 3)
    pt_units_sold = _create_pivot_table_sheet(
        units_sold_ws, pivot_data_source,
        row_fields=['Date'], value_fields=[('Units Sold', 'sum')],
        value_format='#,##0'
    )
    _create_pivot_chart(
        units_sold_ws, units_sold_ws["A3"],
        'line', 'Units sold each month', colors,
        chart_height=5, chart_width=10
    )
    units_sold_ws.sheet_state = 'hidden'

    profit_by_month_ws = wb.create_sheet("Profit by month", 4)
    pt_profit_month = _create_pivot_table_sheet(
        profit_by_month_ws, pivot_data_source,
        row_fields=['Date'], value_fields=[('Profit', 'sum')],
        value_format='$#,##0'
    )
    _create_pivot_chart(
        profit_by_month_ws, profit_by_month_ws["A3"],
        'line', 'Profit by month', colors,
        chart_height=5, chart_width=10
    )
    profit_by_month_ws.sheet_state = 'hidden'

    # Position charts on dashboard (simplified positioning)
    dashboard_ws.add_chart(profit_by_market_ws._charts[0], "B10")
    dashboard_ws.add_chart(units_sold_ws._charts[0], "N10")
    dashboard_ws.add_chart(profit_by_month_ws._charts[0], "N20")

    # Remove default sheet if it exists
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

def _prepare_data_sheet(ws):
    headers = ['Country', 'Product', 'Units Sold', 'Revenue', 'Cost', 'Profit', 'Date']
    ws.append(headers)

    # Generating sample data for 2019 and 2020
    countries = ['India', 'Malaysia', 'Philippines', 'United Kingdom', 'United States']
    products = ['Chocolate Chip', 'Fortune Cookie', 'Oatmeal Raisin', 'Snickerdoodle', 'Sugar', 'White Chocolate Macadamia Nut']

    # Data for 2019 (Aug-Dec for initial views)
    for year in [2019, 2020]:
        for month_num in range(1, 13):
            if year == 2019 and month_num < 8: continue # Start from August 2019

            for _ in range(20): # Generate 20 entries per month
                country = countries[_ % len(countries)]
                product = products[_ % len(products)]
                day = min(_ % calendar.monthrange(year, month_num)[1] + 1, calendar.monthrange(year, month_num)[1])
                date = datetime.date(year, month_num, day)

                units_sold = 500 + (_ * 10 % 1000)
                revenue = units_sold * (5 + (_ % 3)) + (_ * 5)
                cost = units_sold * (2 + (_ % 2)) + (_ * 2)
                profit = revenue - cost
                ws.append([country, product, units_sold, revenue, cost, profit, date])

    # Convert range to Excel Table for auto-expansion
    table_ref = f"A1:G{ws.max_row}"
    table = Table(displayName="SalesData", ref=table_ref)
    style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    table.tableStyleInfo = style
    ws.add_table(table)

    # Apply general number formatting (Excel Table handles currency for actual values)
    for col_idx in [3, 4, 5, 6]:
        for row_idx in range(2, ws.max_row + 1):
            ws.cell(row=row_idx, column=col_idx).number_format = '#,##0.00' if col_idx > 3 else '#,##0'

def _prepare_dashboard_sheet(ws, title, colors):
    ws.merge_cells('A1:AC7')
    header_cell = ws['A1']
    header_cell.value = f"Kevin Cookie Company\n{title}"
    header_cell.font = _create_font(name="Calibri", size=28, bold=True, color=colors["header_fg"])
    header_cell.fill = _create_fill(colors["header_bg"])
    header_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False

def _create_pivot_table_sheet(ws, data_source_range, row_fields, value_fields, column_fields=None, filters=None, value_format=None):
    pt = PivotTable(
        name=f"PivotTable_{ws.title.replace(' ', '_')}", # Unique name for PT
        ref="A3", # Anchor for the pivot table
        data_source=data_source_range
    )

    all_fields_map = {} # To keep track of field index
    field_idx_counter = 0

    # Add row fields
    for field_name in row_fields:
        pt.rowFields.append(PivotField(fld=field_idx_counter, showAll=False, compact=False, outline=False))
        pt.fields.append(PivotField(fld=field_idx_counter, name=field_name))
        all_fields_map[field_name] = field_idx_counter
        field_idx_counter += 1

    # Add column fields
    if column_fields:
        for field_name in column_fields:
            pt.colFields.append(PivotField(fld=field_idx_counter, showAll=False))
            pt.fields.append(PivotField(fld=field_idx_counter, name=field_name))
            all_fields_map[field_name] = field_idx_counter
            field_idx_counter += 1

    # Add data fields
    for field_name, agg_func in value_fields:
        pt.dataFields.append(DataField(fld=field_idx_counter, caption=f"{agg_func} of {field_name}", aggFunc=agg_func))
        pt.fields.append(PivotField(fld=field_idx_counter, name=field_name))
        all_fields_map[field_name] = field_idx_counter
        field_idx_counter += 1

    ws.add_pivot_table(pt)

    # Auto-apply value formatting based on pivot table
    if value_format:
        for row_idx in range(4, ws.max_row + 1): # Assuming data starts from row 4
            for col_idx in range(2, ws.max_column + 1): # Assuming data starts from column 2
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.number_format = value_format
    return pt

def _create_pivot_chart(ws, pt_anchor_cell, chart_type, title, colors, chart_height=8, chart_width=15):
    # This function creates a chart tied to a PivotTable.
    # Hiding field buttons is a UI-level action in Excel, not directly in openpyxl.

    if chart_type == 'stacked_column':
        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.grouping = "stacked"
        chart.overlap = 100
        chart.title = title
        chart.y_axis.title = "Profit"
        chart.x_axis.title = "Market"

        # Determine data series from pivot table layout
        # Assuming rows are categories, columns are series for stacked chart.
        # This requires pivot table to be rendered first to know max_row/max_col
        # For openpyxl, this often means creating the PT, saving, loading, then creating chart.
        # For simplicity in this template, we assume the PT structure.

        # Categories for X-axis (e.g., Countries)
        chart.set_categories(Reference(ws, min_col=1, min_row=pt_anchor_cell.row + 1, max_row=ws.max_row - 1))

        # Series for Y-axis (e.g., Profit per Product stacked)
        # Assuming product names are in row 3 (header row for columns) and data starts from row 4.
        for col_idx in range(2, ws.max_column): # Iterate through product columns
            if ws.cell(row=pt_anchor_cell.row, column=col_idx).value != "Grand Total":
                series = Series(
                    Reference(ws, min_col=col_idx, min_row=pt_anchor_cell.row + 1, max_row=ws.max_row -1),
                    title_from_data=True
                )
                chart.series.append(series)


    elif chart_type == 'line':
        chart = LineChart()
        chart.style = 10
        chart.title = title
        chart.y_axis.title = "Value" # Dynamic based on value field
        chart.x_axis.title = "Month"

        # Data for line chart (e.g., Units Sold or Profit over Months)
        # Assuming first column is months, second column is sum of values.
        series_ref = Reference(ws, min_col=2, min_row=pt_anchor_cell.row, max_row=ws.max_row -1) # -1 to exclude Grand Total row
        cat_ref = Reference(ws, min_col=1, min_row=pt_anchor_cell.row + 1, max_row=ws.max_row - 1)
        chart.add_data(series_ref, titles_from_data=True)
        chart.set_categories(cat_ref)
        chart.legend = None # Hide legend if there's only one series

    chart.width = chart_width
    chart.height = chart_height

    # Basic chart styling
    chart.plot_area.spPr.noFill = False
    chart.plot_area.spPr.solidFill = Color(colors["chart_bg"])
    chart.border.prstGeom = "rect"
    chart.border.w = 10000 # 1 point border
    chart.border.solidFill = Color(colors["chart_border"])

    ws.add_chart(chart, pt_anchor_cell.coordinate)
    return chart
