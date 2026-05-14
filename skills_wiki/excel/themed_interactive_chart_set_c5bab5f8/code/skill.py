from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference, Series, PieChart, MapChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.axis import ChartAxis
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
import datetime
from skills_library.excel._helpers import get_theme_colors, get_fill, get_font, get_border

def render_sheet(wb, sheet_name: str = "Dashboard", *, title: str = "VIVO CALIF Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    colors = get_theme_colors(theme)

    # --- Setup Sheet Dimensions and Visuals ---
    ws.column_dimensions['A'].width = 3
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 3
    for col_letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB']:
        ws.column_dimensions[col_letter].width = 10
    
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False

    # Simulate dashboard panel backgrounds with cell fills
    for row in range(1, 42):
        for col in range(1, 3): # Columns A and B for left panel
            ws.cell(row=row, column=col).fill = get_fill(colors.header_bg_dark)
    
    for row in range(1, 42):
        for col in range(3, 29): # Columns C to AB for main panel
            ws.cell(row=row, column=col).fill = get_fill(colors.header_bg_light)

    # --- Helper Sheets for Pivot Data and Derived Data ---
    # In a real scenario, pivots would be dynamically created from raw data.
    # For this skill, we simulate pivot outputs in helper sheets.

    # Pivots_Helper sheet (for KPIs, Trends, Qty Distribution, Customer Satisfaction)
    pivots_ws = wb.create_sheet("Pivots_Helper")
    pivots_ws.sheet_view.showGridLines = False
    
    # KPI Summary Data
    pivots_ws['A1'] = "Count of TX ID"; pivots_ws['B1'] = "Sum of Quantity"; pivots_ws['C1'] = "Sum of Amount"
    pivots_ws['D1'] = "Average of Rating C"; pivots_ws['E1'] = "Average of Days to Deliver"
    pivots_ws['A2'] = 2400; pivots_ws['B2'] = 11997; pivots_ws['C2'] = 649019.8
    pivots_ws['D2'] = 3.96; pivots_ws['E2'] = 2.34

    # Trend Data (mock for 13 weeks)
    pivots_ws['A10'] = "Weeknum"; pivots_ws['B10'] = "Quantity"; pivots_ws['C10'] = "Amount"
    for i in range(1, 14):
        pivots_ws.cell(row=10+i, column=1, value=i)
        pivots_ws.cell(row=10+i, column=2, value=300 + i*50 - (i%3)*10)
        pivots_ws.cell(row=10+i, column=3, value=30000 + i*5000 - (i%3)*1000)

    # Quantity Distribution Data (mock)
    pivots_ws['A30'] = "Quantity Range"; pivots_ws['B30'] = "Order Count"
    qty_ranges = {"1": 397, "2": 540, "3": 375, "4": 246, "5": 185, "6 to 10": 414, "More than 10": 233}
    row_idx = 31
    for r, c in qty_ranges.items():
        pivots_ws.cell(row=row_idx, column=1, value=r)
        pivots_ws.cell(row=row_idx, column=2, value=c)
        row_idx += 1

    # Customer Satisfaction Data (mock: Ratings by Month)
    pivots_ws['A45'] = "Month"; pivots_ws['B45'] = "Rating 1"; pivots_ws['C45'] = "Rating 2"
    pivots_ws['D45'] = "Rating 3"; pivots_ws['E45'] = "Rating 4"; pivots_ws['F45'] = "Rating 5"
    ratings_data = {
        "Jan": [37, 51, 150, 312, 224],
        "Feb": [39, 64, 182, 373, 247],
        "Mar": [51, 85, 163, 393, 261]
    }
    row_idx = 46
    for month, data_list in ratings_data.items():
        pivots_ws.cell(row=row_idx, column=1, value=month)
        for c_idx, val in enumerate(data_list):
            pivots_ws.cell(row=row_idx, column=2+c_idx, value=val)
        row_idx += 1
    
    # Prod_Piv_Helper sheet (for Popular Products)
    product_piv_ws = wb.create_sheet("Prod_Piv_Helper")
    product_piv_ws.sheet_view.showGridLines = False
    product_piv_ws['A1'] = "Product"; product_piv_ws['B1'] = "Female"; product_piv_ws['C1'] = "Male"
    product_piv_ws['D1'] = "Other"; product_piv_ws['E1'] = "Unknown"
    product_piv_data = {
        "T-Shirts": [764, 1645, 90, 18], "Jeans": [716, 1548, 88, 17], "Sneakers": [568, 1180, 62, 11],
        "Tank Tops": [303, 807, 39, 10], "Bikinis": [292, 812, 29, 8], "Shorts": [285, 788, 22, 7],
        "Sundresses": [202, 700, 14, 4], "Graphic Tees": [164, 647, 10, 4], "Hoodies & Sweatshirts": [140, 606, 9, 3],
        "Sandals": [114, 595, 7, 2], "Crop Tops": [111, 553, 7, 2], "Casual Dresses": [88, 370, 5, 1],
        "Workout Tops": [78, 370, 5, 1], "Maxi Dresses": [65, 258, 4, 1], "Pajama Sets": [60, 270, 4, 1],
        "Baseball Caps": [47, 167, 3, 1], "Tote Bags": [43, 179, 2, 1], "Leggings": [39, 265, 2, 1],
        "Jewelry": [36, 20, 2, 1], "Sunglasses": [28, 75, 1, 0]
    }
    for r_idx, (prod, qty_list) in enumerate(product_piv_data.items()):
        product_piv_ws.cell(row=2+r_idx, column=1, value=prod)
        for c_idx, qty in enumerate(qty_list):
            product_piv_ws.cell(row=2+r_idx, column=2+c_idx, value=qty)
    
    # Matrix_Helper sheet (for Purchase Patterns Heatmap)
    matrix_ws = wb.create_sheet("Matrix_Helper")
    matrix_ws.sheet_view.showGridLines = False
    matrix_ws['A1'] = "Order Mode"; matrix_ws['B1'] = "Female"; matrix_ws['C1'] = "Male"
    matrix_ws['D1'] = "Other"; matrix_ws['E1'] = "Unknown"
    modes = ["App", "Instagram", "Partner App", "Target.com", "Website"]
    gender_data = {
        "App": [0.19, 0.123, 0.011, 0.031], "Instagram": [0.05, 0.043, 0.002, 0.018],
        "Partner App": [0.063, 0.048, 0.002, 0.004], "Target.com": [0.096, 0.068, 0.005, 0.013],
        "Website": [0.125, 0.091, 0.006, 0.012],
    }
    for i, mode in enumerate(modes):
        matrix_ws.cell(row=2+i, column=1, value=mode)
        for j, val in enumerate(gender_data[mode]):
            cell = matrix_ws.cell(row=2+i, column=2+j, value=val)
            cell.number_format = '0.0%'
            # Apply conditional formatting for heat map
            color_scale_rule = ColorScaleRule(start_type='num', start_value=0, start_color=colors.accent1.color,
                                              mid_type='num', mid_value=0.05, mid_color=colors.neutral_mid.color,
                                              end_type='num', end_value=0.2, end_color=colors.accent6.color)
            matrix_ws.conditional_formatting.add(f'{get_column_letter(2+j)}{2+i}', color_scale_rule)
            cell.border = get_border(color="FFFFFF") # White border

    # Map_Data_Helper sheet (for California Counties Maps)
    map_data_ws = wb.create_sheet("Map_Data_Helper")
    map_data_ws.sheet_view.showGridLines = False
    map_data_ws['A1'] = "State"; map_data_ws['B1'] = "County"; map_data_ws['C1'] = "Quantity"; map_data_ws['D1'] = "Amount"
    counties_raw = [
        ("California", "Los Angeles County", 3981, 215501.2), ("California", "San Diego County", 700, 45676.2),
        ("California", "Orange County", 1479, 902.4), ("California", "Santa Clara County", 450, 2908.4),
        ("California", "Alameda County", 579, 33885), ("California", "Fresno County", 50, 1801),
        ("California", "Ventura County", 28, 650), ("California", "Yolo County", 4, 116),
        ("California", "", 0, 0), ("", "", 0, 0) # Blank rows for error testing
    ]
    # Use IF logic to handle blank/zero values from pivot data, preventing map chart errors
    row_offset = 2 # Start from row 2
    for r_idx, (state, county, qty, amount) in enumerate(counties_raw):
        map_data_ws.cell(row=row_offset + r_idx, column=1, value=f'=IF(ISBLANK(Pivots_Helper!$A${r_idx+100}),"",Pivots_Helper!$A${r_idx+100})') # Mock linking to pivot helper
        map_data_ws.cell(row=row_offset + r_idx, column=2, value=f'=IF(ISBLANK(Pivots_Helper!$B${r_idx+100}),"",Pivots_Helper!$B${r_idx+100})')
        map_data_ws.cell(row=row_offset + r_idx, column=3, value=f'=IF(ISBLANK(Pivots_Helper!$C${r_idx+100}),"",Pivots_Helper!$C${r_idx+100})')
        map_data_ws.cell(row=row_offset + r_idx, column=4, value=f'=IF(ISBLANK(Pivots_Helper!$D${r_idx+100}),"",Pivots_Helper!$D${r_idx+100})')
    # For actual values in Pivots_Helper for map_data_ws references:
    # This simulates a pivot output for State/County/Quantity/Amount
    pivots_ws['A100'] = "California"; pivots_ws['B100'] = "Los Angeles County"; pivots_ws['C100'] = 3981; pivots_ws['D100'] = 215501.2
    pivots_ws['A101'] = "California"; pivots_ws['B101'] = "San Diego County"; pivots_ws['C101'] = 700; pivots_ws['D101'] = 45676.2
    # Add more mocked pivot data as needed for all counties and their values.


    # --- KPIs Display Panel ---
    kpi_definitions = [
        {"label": "Orders", "value_cell": "A2", "format": "#,##0", "emoji": "🛒"},
        {"label": "Quantity", "value_cell": "B2", "format": "#,##0", "emoji": "📦"},
        {"label": "Amount", "value_cell": "C2", "format": "$#,##0,.0k", "emoji": "💰"},
        {"label": "Avg. Rating", "value_cell": "D2", "format": "0.0", "emoji": "⭐"},
        {"label": "Days to Deliver", "value_cell": "E2", "format": "0.0", "emoji": "⏱️"}
    ]
    
    current_row = 5
    for kpi in kpi_definitions:
        ws.cell(row=current_row, column=2, value=kpi["label"]).font = get_font(colors.text_light, size=11, bold=True)
        ws.cell(row=current_row+1, column=2, value=kpi["emoji"]).font = get_font(colors.accent5, size=18)
        ws.cell(row=current_row+2, column=2, value=f'=TEXT(Pivots_Helper!{kpi["value_cell"]},"{kpi["format"]}")').font = get_font(colors.text_light, size=18, bold=True)
        current_row += 4

    # --- Charts ---
    # Chart 1: Last 13 Weeks Trends (Quantity & Amount) - Line Chart
    chart1 = LineChart()
    chart1.title = "Last 13 Week Trends - Qty & Amount"
    chart1.style = 10 
    chart1.x_axis.title = "Weeknum"
    chart1.y_axis.title = "Quantity"
    
    data1 = Reference(pivots_ws, min_col=2, min_row=11, max_col=2, max_row=23)
    cats1 = Reference(pivots_ws, min_col=1, min_row=11, max_col=1, max_row=23)
    chart1.add_data(data1, titles_from_data=False)
    chart1.set_categories(cats1)
    
    s2 = Series(Reference(pivots_ws, min_col=3, min_row=11, max_col=3, max_row=23), title="Amount")
    chart1.series.append(s2)
    chart1.series[1].marker = chart1.series[0].marker
    chart1.y_axis[1] = ChartAxis(axId=200, crosses="max", title="Amount ($)") # Secondary axis
    ws.add_chart(chart1, "D3")

    # Chart 2: How they like to buy? (Heatmap, simulated with cells for openpyxl)
    # Since openpyxl doesn't directly support linked pictures, we place the helper range itself as an image substitute.
    # In a real scenario, this would involve image export/import or direct cell replication on the dashboard.
    # For demonstration, we simply show the data and its formatting in the helper sheet.
    # A cleaner solution for display would be creating a separate chart from this data,
    # or using external libraries for image embedding.
    ws.cell(row=3, column=13, value="How they like to buy?").font = get_font(colors.text_dark, size=11, bold=True)
    for r in range(2, 7):
        for c in range(1, 6):
            target_cell = ws.cell(row=r+2, column=c+12, value=matrix_ws.cell(row=r, column=c).value)
            target_cell.fill = matrix_ws.cell(row=r, column=c).fill
            target_cell.border = matrix_ws.cell(row=r, column=c).border
            target_cell.font = get_font(colors.text_dark, size=10)
            target_cell.number_format = '0.0%'
            target_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Chart 3: How many they buy? (Column Chart)
    chart3 = BarChart()
    chart3.title = "How many they buy?"
    chart3.style = 10
    chart3.x_axis.title = "Quantity Range"
    chart3.y_axis.title = "Number of Orders"
    
    bar_data3 = Reference(pivots_ws, min_col=2, min_row=31, max_col=2, max_row=38)
    bar_cats3 = Reference(pivots_ws, min_col=1, min_row=31, max_col=1, max_row=38)
    chart3.add_data(bar_data3, titles_from_data=False)
    chart3.set_categories(bar_cats3)
    chart3.type = "col"
    chart3.gapWidth = 0
    ws.add_chart(chart3, "V3")

    # Chart 4: Which Products are Popular? Breakdown by Gender (Stacked Bar Chart)
    chart4 = BarChart()
    chart4.title = "Which Products are Popular? Breakdown by Gender"
    chart4.style = 10
    chart4.x_axis.title = "Quantity"
    chart4.y_axis.title = "Product"
    
    bar_data4 = Reference(product_piv_ws, min_col=2, min_row=1, max_col=5, max_row=21)
    bar_cats4 = Reference(product_piv_ws, min_col=1, min_row=2, max_col=1, max_row=21)
    chart4.add_data(bar_data4, titles_from_data=True)
    chart4.set_categories(bar_cats4)
    chart4.type = "bar"
    chart4.grouping = "stacked"
    chart4.gapWidth = 10
    chart4.y_axis.scaling.orientation = "maxMin" # Reverses category order
    ws.add_chart(chart4, "D24")

    # Chart 5: Overall Gender Split (Donut Chart)
    chart5 = PieChart()
    chart5.title = "Overall Gender Split"
    chart5.style = 10
    
    labels5 = Reference(pivots_ws, min_col=7, min_row=2, max_row=5)
    data5 = Reference(pivots_ws, min_col=8, min_row=2, max_row=5)
    chart5.add_data(data5, titles_from_data=False)
    chart5.set_categories(labels5)
    chart5.dataLabels = DataLabelList()
    chart5.dataLabels.showPercent = True
    chart5.dataLabels.showCatName = True
    ws.add_chart(chart5, "M24")

    # Chart 6 & 7: Where our customers live? (Map Charts)
    chart6 = MapChart()
    chart6.title = "Where our customers live? (Quantity)"
    chart6.style = 10
    
    map_data_qty = Reference(map_data_ws, min_col=3, min_row=2, max_col=3, max_row=len(counties_raw)+1)
    map_cats_qty = Reference(map_data_ws, min_col=2, min_row=2, max_col=2, max_row=len(counties_raw)+1)
    chart6.add_data(map_data_qty, titles_from_data=False)
    chart6.set_categories(map_cats_qty)
    chart6.color_series = 'sequential_2_color'
    chart6.min_color = colors.accent3.color # Light orange
    chart6.max_color = colors.accent6.color # Dark orange
    chart6.series[0].map_projection = "albers"
    
    ws.add_chart(chart6, "V24") # Position on dashboard

    # Chart 8: How Satisfied Are Our Customers (Clustered Column Chart)
    chart8 = BarChart()
    chart8.title = "How Satisfied Are Our Customers"
    chart8.style = 10
    chart8.x_axis.title = "Month"
    chart8.y_axis.title = "Count of Ratings"
    
    data8 = Reference(pivots_ws, min_col=2, min_row=45, max_col=6, max_row=48)
    cats8 = Reference(pivots_ws, min_col=1, min_row=46, max_col=1, max_row=48)
    chart8.add_data(data8, titles_from_data=True)
    chart8.set_categories(cats8)
    chart8.type = "col"
    
    ws.add_chart(chart8, "AA24") # Position on dashboard

    # --- Slicers (Conceptual - not directly creatable with openpyxl) ---
    # Slicers are interactive UI elements connected to pivot tables.
    # The interaction logic is handled by Excel's UI.
    # In a full openpyxl solution, you would outline manual instructions for users to add slicers
    # and connect them, or use external libraries.

    # --- Final Cleanup ---
    # Delete helper sheets
    wb.remove(pivots_ws)
    wb.remove(matrix_ws)
    wb.remove(product_piv_ws)
    wb.remove(map_data_ws)

    # Move Dashboard sheet to the front
    wb.active = ws
