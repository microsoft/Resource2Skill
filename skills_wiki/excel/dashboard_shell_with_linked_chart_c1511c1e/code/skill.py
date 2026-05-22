from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Theme palette logic (matches the "Awesome Chocolates" orange theme from the video by default)
    palettes = {
        "corporate_blue": {
            "header_bg": "4F81BD", "header_fg": "FFFFFF", 
            "row_light": "DCE6F1", "total_bg": "B8CCE4", "text": "000000"
        },
        "warm_orange": {
            "header_bg": "E26B0A", "header_fg": "FFFFFF", 
            "row_light": "FCE4D6", "total_bg": "F7CBAC", "text": "000000"
        }
    }
    # Fallback to orange if theme not matched, to mimic tutorial visual
    theme_colors = palettes.get(theme, palettes["warm_orange"])

    # 1. Dashboard Title
    ws["B2"] = title
    ws["B2"].font = Font(size=20, bold=True, color=theme_colors["header_bg"])

    # 2. Summary Data (Mimicking Pivot Table Output)
    headers = ["Row Labels", "Sum of Amount"]
    data = [
        ["Barr Faughny", 270914],
        ["Brien Boise", 253813],
        ["Carla Molina", 253078],
        ["Ches Bonnell", 274680],
        ["Curtice Advani", 305599],
        ["Gigi Bohling", 294280],
        ["Gunar Cocksnoot", 250677]
    ]
    total = sum(row[1] for row in data)

    # Write Headers
    for col_idx, text in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_idx, value=text)
        cell.fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")
        cell.font = Font(color=theme_colors["header_fg"], bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Write Data
    thin_border = Border(bottom=Side(style="thin", color="D9D9D9"))
    for r_idx, row in enumerate(data, start=5):
        # Sales Person Name
        name_cell = ws.cell(row=r_idx, column=2, value=row[0])
        name_cell.border = thin_border
        
        # Sales Amount
        val_cell = ws.cell(row=r_idx, column=3, value=row[1])
        val_cell.number_format = '"$"#,##0'
        val_cell.border = thin_border
        
        # Alternating row colors
        if r_idx % 2 == 0:
            name_cell.fill = PatternFill(start_color=theme_colors["row_light"], end_color=theme_colors["row_light"], fill_type="solid")
            val_cell.fill = PatternFill(start_color=theme_colors["row_light"], end_color=theme_colors["row_light"], fill_type="solid")

    # Write Grand Total
    total_row = 5 + len(data)
    ws.cell(row=total_row, column=2, value="Grand Total").font = Font(bold=True)
    total_val_cell = ws.cell(row=total_row, column=3, value=total)
    total_val_cell.font = Font(bold=True)
    total_val_cell.number_format = '"$"#,##0'
    
    ws.cell(row=total_row, column=2).fill = PatternFill(start_color=theme_colors["total_bg"], end_color=theme_colors["total_bg"], fill_type="solid")
    total_val_cell.fill = PatternFill(start_color=theme_colors["total_bg"], end_color=theme_colors["total_bg"], fill_type="solid")

    # Set column widths
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 16

    # 3. Add Linked Column Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Sales Amount by Person"
    chart.y_axis.title = "Amount"
    chart.height = 10
    chart.width = 18

    # Define chart data references
    cats = Reference(ws, min_col=2, min_row=5, max_row=total_row-1)
    data_ref = Reference(ws, min_col=3, min_row=4, max_row=total_row-1)

    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)

    # 4. Dashboard Layout Positioning
    # Place chart to the right, leaving rows 4-7 open for Slicer placement
    ws.add_chart(chart, "E8")

    # Placeholder/instruction indicating where interactive Slicers should go
    ws["E4"] = "⮡ Insert Excel Slicers Here (e.g., Geography, Product) to filter the chart below"
    ws["E4"].font = Font(italic=True, color="7F7F7F")
