from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.chart import LineChart, BarChart, DoughnutChart, Reference
from openpyxl.utils import get_column_letter
import _helpers

def render_sheet(wb, sheet_name: str, *, title: str = "Sales Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    palette = _helpers.get_theme_palette(theme)
    bg_hex = "F3F3F3"
    card_hex = "FFFFFF"
    
    bg_fill = PatternFill(start_color=bg_hex, fill_type="solid")
    card_fill = PatternFill(start_color=card_hex, fill_type="solid")
    sidebar_fill = PatternFill(start_color=palette.get("primary", "1F4E78"), fill_type="solid")
    
    # Base background simulation
    for row in ws.iter_rows(min_row=1, max_row=32, min_col=1, max_col=15):
        for cell in row:
            cell.fill = bg_fill

    # Left Navigation Sidebar
    ws.column_dimensions['A'].width = 8
    for r in range(1, 33):
        ws.cell(row=r, column=1).fill = sidebar_fill

    # Set uniform column widths for the main dashboard grid
    for col in range(2, 15):
        ws.column_dimensions[get_column_letter(col)].width = 11

    def make_card(min_col, max_col, min_row, max_row):
        for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
            for cell in row:
                cell.fill = card_fill

    # Title Card
    make_card(2, 13, 2, 4)
    ws.merge_cells("C3:M3")
    title_cell = ws.cell(row=3, column=3, value=title)
    title_cell.font = Font(name="Calibri", size=22, bold=True, color=palette.get("primary", "1F4E78"))
    title_cell.alignment = Alignment(vertical="center")

    # Data staging area (to be hidden)
    data_col = 20
    ws.cell(row=1, column=data_col, value="Dashboard Data").font = Font(bold=True)
    
    # KPI Cards Definition
    kpis = [
        {"name": "Sales (M)", "val": 2544, "target": 3000, "col": 2, "fmt": "$#,##0"},
        {"name": "Profit (M)", "val": 890, "target": 1000, "col": 6, "fmt": "$#,##0"},
        {"name": "Customers", "val": 87, "target": 100, "col": 10, "fmt": "#,##0"}
    ]
    
    for i, kpi in enumerate(kpis):
        c_start = kpi["col"]
        c_end = c_start + 3
        make_card(c_start, c_end, 6, 12)
        
        # Typography Labels
        lbl_cell = ws.cell(row=7, column=c_start+1, value=kpi["name"])
        lbl_cell.font = Font(name="Calibri", size=14, color="595959")
        
        val_cell = ws.cell(row=8, column=c_start+1, value=kpi["val"])
        val_cell.font = Font(name="Calibri", size=20, bold=True, color=palette.get("text", "000000"))
        val_cell.number_format = kpi["fmt"]
        
        # Doughnut Chart Data Formatting
        pct = kpi["val"] / kpi["target"]
        dr = 3 + i*3
        ws.cell(row=dr, column=data_col, value="Achieved")
        ws.cell(row=dr, column=data_col+1, value=pct)
        ws.cell(row=dr+1, column=data_col, value="Remaining")
        ws.cell(row=dr+1, column=data_col+1, value=max(0, 1 - pct))
        
        chart = DoughnutChart()
        chart.width = 6
        chart.height = 4
        chart.legend = None
        data = Reference(ws, min_col=data_col+1, min_row=dr, max_row=dr+1)
        chart.add_data(data, titles_from_data=False)
        
        ws.add_chart(chart, f"{get_column_letter(c_start+2)}7")

    # Trend Chart Card
    make_card(2, 9, 14, 30)
    ws.cell(row=15, column=3, value="Sales Trend 2022").font = Font(name="Calibri", size=16, bold=True)
    
    trend_data = [
        ("Jan", 201), ("Feb", 204), ("Mar", 198), ("Apr", 199), 
        ("May", 206), ("Jun", 195), ("Jul", 192), ("Aug", 189),
        ("Sep", 194), ("Oct", 190), ("Nov", 205), ("Dec", 204)
    ]
    tr_start = 15
    for r, (m, v) in enumerate(trend_data):
        ws.cell(row=tr_start+r, column=data_col, value=m)
        ws.cell(row=tr_start+r, column=data_col+1, value=v)
        
    line_chart = LineChart()
    line_chart.width = 14
    line_chart.height = 7
    line_chart.legend = None
    data = Reference(ws, min_col=data_col+1, min_row=tr_start, max_row=tr_start+len(trend_data)-1)
    cats = Reference(ws, min_col=data_col, min_row=tr_start, max_row=tr_start+len(trend_data)-1)
    line_chart.add_data(data, titles_from_data=False)
    line_chart.set_categories(cats)
    ws.add_chart(line_chart, "C17")

    # Breakdown Chart Card
    make_card(10, 13, 14, 30)
    ws.cell(row=15, column=11, value="Sales by Country").font = Font(name="Calibri", size=16, bold=True)
    
    breakdown_data = [
        ("Argentina", 953), ("Brazil", 553), ("Colombia", 432), 
        ("Ecuador", 445), ("Peru", 425), ("Chile", 253)
    ]
    br_start = 30
    for r, (c, v) in enumerate(breakdown_data):
        ws.cell(row=br_start+r, column=data_col, value=c)
        ws.cell(row=br_start+r, column=data_col+1, value=v)
        
    bar_chart = BarChart()
    bar_chart.type = "bar" 
    bar_chart.width = 7
    bar_chart.height = 7
    bar_chart.legend = None
    data = Reference(ws, min_col=data_col+1, min_row=br_start, max_row=br_start+len(breakdown_data)-1)
    cats = Reference(ws, min_col=data_col, min_row=br_start, max_row=br_start+len(breakdown_data)-1)
    bar_chart.add_data(data, titles_from_data=False)
    bar_chart.set_categories(cats)
    ws.add_chart(bar_chart, "J17")
    
    # Hide staging data columns to maintain clean layout
    ws.column_dimensions[get_column_letter(data_col)].hidden = True
    ws.column_dimensions[get_column_letter(data_col+1)].hidden = True
