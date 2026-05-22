from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, ColumnChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", data: dict = None, **kwargs) -> None:
    """
    Renders a unified Sales KPI Dashboard using a cell-grid layout to simulate UI panels.
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    
    # Theme palette mapping (simulated for standalone execution)
    palette = {
        "bg_canvas": "F3F4F6",
        "bg_panel": "FFFFFF",
        "text_title": "1F2937",
        "text_label": "6B7280",
        "text_value": "111827",
        "border": "D1D5DB"
    }
    
    # Default mock data if none provided
    if data is None:
        data = {
            "kpis": [
                {"label": "TOTAL SALES", "value": "$19,288k"},
                {"label": "TOTAL PROFIT", "value": "$2,477k"},
                {"label": "CUSTOMERS", "value": "2,319"}
            ],
            "profit_by_year": [
                ["Year", "Profit"],
                ["2021", 49556], ["2022", 61618], ["2023", 81786], ["2024", 54999]
            ],
            "sales_by_cat": [
                ["Category", "Sales"],
                ["Phones", 279464], ["Chairs", 277059], ["Storage", 188091], ["Tables", 167673]
            ],
            "sales_by_month": [
                ["Month", "Sales"],
                ["Jan", 80564], ["Feb", 59840], ["Mar", 102553], ["Apr", 137481]
            ]
        }

    # 1. Setup Column Geometry
    col_widths = {
        1: 4, 13: 4,  # A, M (Outer padding)
        5: 4, 9: 4,   # E, I (Inner panel gutters)
    }
    for c in range(1, 14):
        ws.column_dimensions[get_column_letter(c)].width = col_widths.get(c, 14)

    # 2. Paint Canvas
    fill_canvas = PatternFill("solid", fgColor=palette["bg_canvas"])
    for r in range(1, 33):
        for c in range(1, 14):
            ws.cell(row=r, column=c).fill = fill_canvas

    # Panel drawing helper
    def draw_panel(min_col, min_row, max_col, max_row):
        fill_panel = PatternFill("solid", fgColor=palette["bg_panel"])
        b_side = Side(style='thin', color=palette["border"])
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill_panel
                cell.border = Border(
                    top=b_side if r == min_row else None,
                    bottom=b_side if r == max_row else None,
                    left=b_side if c == min_col else None,
                    right=b_side if c == max_col else None
                )

    # 3. Draw Title Panel
    draw_panel(2, 2, 12, 3)
    ws.merge_cells("B2:L3")
    title_cell = ws["B2"]
    title_cell.value = title
    title_cell.font = Font(size=20, bold=True, color=palette["text_title"])
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 4. Draw KPI Panels
    kpi_coords = [
        (2, 5, 4, 5, 2, 6, 4, 7),     # B5:D5 (Label), B6:D7 (Value)
        (6, 5, 8, 5, 6, 6, 8, 7),     # F5:H5 (Label), F6:H7 (Value)
        (10, 5, 12, 5, 10, 6, 12, 7)  # J5:L5 (Label), J6:L7 (Value)
    ]
    for idx, kpi in enumerate(data["kpis"][:3]):
        c_lbl_col, c_lbl_row, c_lbl_max_c, c_lbl_max_r, c_val_col, c_val_row, c_val_max_c, c_val_max_r = kpi_coords[idx]
        
        draw_panel(c_lbl_col, c_lbl_row, c_val_max_c, c_val_max_r)
        
        ws.merge_cells(start_row=c_lbl_row, start_column=c_lbl_col, end_row=c_lbl_max_r, end_column=c_lbl_max_c)
        lbl_cell = ws.cell(row=c_lbl_row, column=c_lbl_col, value=kpi["label"])
        lbl_cell.font = Font(size=10, bold=True, color=palette["text_label"])
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        ws.merge_cells(start_row=c_val_row, start_column=c_val_col, end_row=c_val_max_r, end_column=c_val_max_c)
        val_cell = ws.cell(row=c_val_row, column=c_val_col, value=kpi["value"])
        val_cell.font = Font(size=18, bold=True, color=palette["text_value"])
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

    # 5. Stage Hidden Helper Data
    def write_chart_data(start_col, dataset):
        for r_idx, row in enumerate(dataset, start=1):
            for c_idx, val in enumerate(row, start=start_col):
                ws.cell(row=r_idx, column=c_idx, value=val)

    write_chart_data(27, data["profit_by_year"])  # AA
    write_chart_data(30, data["sales_by_cat"])    # AD
    write_chart_data(33, data["sales_by_month"])  # AG

    for c in range(27, 36):
        ws.column_dimensions[get_column_letter(c)].hidden = True

    # 6. Insert Charts (Sized to fit perfectly over the canvas geometry to simulate panels)
    
    # Chart 1: Profit by Year
    c1 = ColumnChart()
    c1.title = "Profit by Year"
    c1.width, c1.height = 11.5, 5.0  # Centimeters (Leaves slight uniform padding against B9:F18)
    c1.legend = None
    c1.add_data(Reference(ws, min_col=28, min_row=1, max_row=len(data["profit_by_year"])), titles_from_data=True)
    c1.set_categories(Reference(ws, min_col=27, min_row=2, max_row=len(data["profit_by_year"])))
    ws.add_chart(c1, "B9")

    # Chart 2: Sales by Category
    c2 = BarChart()
    c2.type = "bar"
    c2.title = "Sales by Category"
    c2.width, c2.height = 11.5, 5.0
    c2.legend = None
    c2.add_data(Reference(ws, min_col=31, min_row=1, max_row=len(data["sales_by_cat"])), titles_from_data=True)
    c2.set_categories(Reference(ws, min_col=30, min_row=2, max_row=len(data["sales_by_cat"])))
    ws.add_chart(c2, "H9")

    # Chart 3: Sales by Month (Wide full-span panel)
    c3 = ColumnChart()
    c3.title = "Sales by Month Trend"
    c3.width, c3.height = 25.5, 5.0 
    c3.legend = None
    c3.add_data(Reference(ws, min_col=34, min_row=1, max_row=len(data["sales_by_month"])), titles_from_data=True)
    c3.set_categories(Reference(ws, min_col=33, min_row=2, max_row=len(data["sales_by_month"])))
    ws.add_chart(c3, "B20")
