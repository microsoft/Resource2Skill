from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a 3-panel dashboard layout (1 large stacked bar, 2 smaller line charts).
    Generates realistic backing data in a hidden region off-screen.
    """
    ws = wb.create_sheet(sheet_name)
    
    # 1. Dashboard Canvas Prep
    ws.sheet_view.showGridLines = False
    
    # Standard theme fallback logic
    theme_colors = {
        "corporate_blue": "1F4E78",
        "emerald_green": "27AE60",
        "slate_gray": "2C3E50"
    }
    bg_color = theme_colors.get(theme, "1F4E78")
    
    # 2. Header Bar
    ws.merge_cells("A1:P2")
    header = ws["A1"]
    header.value = title
    header.font = Font(size=24, bold=True, color="FFFFFF")
    header.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    header.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 25

    # 3. Write Backing Data (Off-screen in columns AA+)
    # Stacked Bar Data
    bar_data = [
        ["Market", "Chocolate Chip", "Sugar", "Oatmeal"],
        ["India", 62000, 23000, 21000],
        ["United States", 46000, 24000, 22000],
        ["United Kingdom", 36000, 14000, 19000],
        ["Philippines", 54000, 8000, 11000],
    ]
    for r_idx, row in enumerate(bar_data, 1):
        for c_idx, val in enumerate(row, 27): # Col 27 = AA
            ws.cell(row=r_idx, column=c_idx, value=val)

    # Line Chart Data
    line_data = [
        ["Month", "Units Sold", "Profit"],
        ["Sep", 50600, 124000],
        ["Oct", 95600, 228000],
        ["Nov", 65400, 160000],
        ["Dec", 52900, 136000],
    ]
    for r_idx, row in enumerate(line_data, 10):
        for c_idx, val in enumerate(row, 27):
            ws.cell(row=r_idx, column=c_idx, value=val)
            
    # Hide backing data columns
    for col in ['AA', 'AB', 'AC', 'AD']:
        ws.column_dimensions[col].hidden = True

    # 4. Chart 1: Stacked Bar (Left Panel)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "stacked"
    bar_chart.overlap = 100
    bar_chart.title = "Profit by Market & Cookie Type"
    
    # Data spans AA1:AD5 (Cols 27-30)
    bar_data_ref = Reference(ws, min_col=28, min_row=1, max_col=30, max_row=5)
    bar_cats_ref = Reference(ws, min_col=27, min_row=2, max_row=5)
    bar_chart.add_data(bar_data_ref, titles_from_data=True)
    bar_chart.set_categories(bar_cats_ref)
    
    bar_chart.width = 17
    bar_chart.height = 11
    ws.add_chart(bar_chart, "B4")

    # 5. Chart 2: Line - Volume (Right Panel Top)
    line1 = LineChart()
    line1.title = "Units sold each month"
    line1.legend = None # Remove legend for cleaner look
    
    # Data spans AB10:AB14 (Col 28)
    line1_data_ref = Reference(ws, min_col=28, min_row=10, max_col=28, max_row=14)
    line1_cats_ref = Reference(ws, min_col=27, min_row=11, max_row=14)
    line1.add_data(line1_data_ref, titles_from_data=True)
    line1.set_categories(line1_cats_ref)
    
    line1.width = 11
    line1.height = 5.3
    ws.add_chart(line1, "K4")

    # 6. Chart 3: Line - Profit (Right Panel Bottom)
    line2 = LineChart()
    line2.title = "Profit by month"
    line2.legend = None 
    
    # Data spans AC10:AC14 (Col 29)
    line2_data_ref = Reference(ws, min_col=29, min_row=10, max_col=29, max_row=14)
    line2_cats_ref = Reference(ws, min_col=27, min_row=11, max_row=14)
    line2.add_data(line2_data_ref, titles_from_data=True)
    line2.set_categories(line2_cats_ref)
    
    line2.width = 11
    line2.height = 5.3
    ws.add_chart(line2, "K10")
