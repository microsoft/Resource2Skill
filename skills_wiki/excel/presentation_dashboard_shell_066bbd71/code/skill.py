from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

def _get_theme(theme_name: str) -> dict:
    themes = {
        "corporate_blue": {
            "primary": "2F5597",
            "secondary": "8FAADC",
            "text_on_primary": "FFFFFF",
        },
        "emerald_green": {
            "primary": "385723",
            "secondary": "A9D08E",
            "text_on_primary": "FFFFFF",
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    theme_palette = _get_theme(theme)
    
    # 1. Clean UI Setup
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False
    ws.column_dimensions["A"].width = 2  # Left margin padding
    
    # 2. Header Banner
    ws.merge_cells("A1:V3")
    header_cell = ws["A1"]
    header_cell.value = title
    
    header_fill = PatternFill(start_color=theme_palette["primary"], end_color=theme_palette["primary"], fill_type="solid")
    header_font = Font(color=theme_palette["text_on_primary"], size=24, bold=True)
    header_alignment = Alignment(horizontal="left", vertical="center", indent=1)
    
    # Apply to all merged cells for reliable rendering
    for row in ws["A1:V3"]:
        for cell in row:
            cell.fill = header_fill
    header_cell.font = header_font
    header_cell.alignment = header_alignment

    # 3. Data Setup (Hidden Region AA:AD)
    
    # Chart 1 Data: Profit by Market & Product Type
    ws["AA1"] = "Market"
    ws["AB1"] = "Chocolate Chip"
    ws["AC1"] = "Sugar"
    ws["AD1"] = "Oatmeal"
    
    data1 = [
        ["India", 150000, 80000, 40000],
        ["United States", 120000, 90000, 50000],
        ["United Kingdom", 100000, 70000, 60000],
        ["Philippines", 80000, 60000, 70000],
    ]
    for r_idx, row_data in enumerate(data1, 2):
        for c_idx, val in enumerate(row_data, 27):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            if c_idx > 27:
                cell.number_format = '$#,##0'

    # Chart 2 Data: Units sold each month
    ws["AA10"] = "Month"
    ws["AB10"] = "Units Sold"
    data2 = [
        ["Sep", 50601],
        ["Oct", 95622],
        ["Nov", 65481],
        ["Dec", 52970]
    ]
    for r_idx, row_data in enumerate(data2, 11):
        ws.cell(row=r_idx, column=27, value=row_data[0])
        cell = ws.cell(row=r_idx, column=28, value=row_data[1])
        cell.number_format = '#,##0'

    # Chart 3 Data: Profit by month
    ws["AA20"] = "Month"
    ws["AB20"] = "Profit"
    data3 = [
        ["Sep", 124812],
        ["Oct", 228275],
        ["Nov", 160228],
        ["Dec", 136337]
    ]
    for r_idx, row_data in enumerate(data3, 21):
        ws.cell(row=r_idx, column=27, value=row_data[0])
        cell = ws.cell(row=r_idx, column=28, value=row_data[1])
        cell.number_format = '$#,##0'

    # Hide the data columns out of sight from the dashboard presentation
    for col in ["AA", "AB", "AC", "AD"]:
        ws.column_dimensions[col].hidden = True

    # 4. Chart Generation & Layout
    
    # Chart 1: Main Stacked Column (Left)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.grouping = "stacked"
    chart1.overlap = 100
    chart1.title = "Profit by Market & Cookie Type"
    cats1 = Reference(ws, min_col=27, min_row=2, max_row=5)
    data1_ref = Reference(ws, min_col=28, min_row=1, max_col=30, max_row=5)
    chart1.add_data(data1_ref, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.width = 16
    chart1.height = 13.5
    ws.add_chart(chart1, "B5")

    # Chart 2: Top Right Line Chart
    chart2 = LineChart()
    chart2.title = "Units sold each month"
    chart2.legend = None
    cats2 = Reference(ws, min_col=27, min_row=11, max_row=14)
    data2_ref = Reference(ws, min_col=28, min_row=10, max_row=14)
    chart2.add_data(data2_ref, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.width = 13
    chart2.height = 6.4
    ws.add_chart(chart2, "K5")

    # Chart 3: Bottom Right Line Chart
    chart3 = LineChart()
    chart3.title = "Profit by month"
    chart3.legend = None
    cats3 = Reference(ws, min_col=27, min_row=21, max_row=24)
    data3_ref = Reference(ws, min_col=28, min_row=20, max_row=24)
    chart3.add_data(data3_ref, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.width = 13
    chart3.height = 6.4
    ws.add_chart(chart3, "K18")
