import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

# Simplified theme loader for standalone reproduction
def _load_theme_palette(theme_name: str):
    if theme_name == "corporate_blue":
        return {
            "header_bg": "FF1E3B5C",  # Dark Blue
            "header_fg": "FFFFFFFF",  # White
            "accent": "FF4E86C6",     # Lighter Blue
            "accent_light": "FFADD8E6", # Light Steel Blue
            "border": "FFD3D3D3",     # Light Gray
            "grid_bg": "FFF8F8F8",    # Off-white
            "text_color": "FF000000", # Black
            "chart_colors": ["FF5B9BD5", "FFED7D31", "FFA5A5A5", "FFFFC000", "FF4472C4", "FF70AD47"],
        }
    elif theme_name == "dark_red": # Example of another theme
        return {
            "header_bg": "FF800000",  # Dark Red
            "header_fg": "FFFFFFFF",  # White
            "accent": "FFC00000",     # Red
            "accent_light": "FFF08080", # Light Coral
            "border": "FFD3D3D3",     # Light Gray
            "grid_bg": "FFF8F8F8",    # Off-white
            "text_color": "FF000000", # Black
            "chart_colors": ["FFC00000", "FF660000", "FFFFA500", "FFD3D3D3", "FF808080", "FF404040"],
        }
    else: # Default theme, e.g., "office"
        return {
            "header_bg": "FF000000",  # Black
            "header_fg": "FFFFFFFF",  # White
            "accent": "FF0070C0",     # Blue
            "accent_light": "FFBFBFBF", # Light Gray
            "border": "FFC0C0C0",     # Gray
            "grid_bg": "FFFFFFFF",    # White
            "text_color": "FF000000", # Black
            "chart_colors": ["FF4472C4", "FFED7D31", "FFA5A5A5", "FFFFC000", "FF5B9BD5", "FF70AD47"],
        }

def render_workbook(wb, *, title: str = "Performance Dashboard", theme: str = "corporate_blue", **kwargs) -> None:
    palette = _load_theme_palette(theme)

    # Remove default sheet if it exists
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

    # 1. Prepare Data Sheet
    ws_data = wb.create_sheet("Data", 0)
    data = [
        ["Country", "Product", "Units Sold", "Revenue", "Cost", "Profit", "Date"],
        ["India", "Chocolate Chip", 1725, 8625.00, 3450.00, 5175.00, "11/1/2019"],
        ["India", "Chocolate Chip", 2152, 10760.00, 4304.00, 6456.00, "12/1/2019"],
        ["India", "Chocolate Chip", 2349, 11745.00, 4698.00, 7047.00, "9/1/2019"],
        ["India", "Chocolate Chip", 1228, 6140.00, 2456.00, 3684.00, "10/1/2019"],
        ["India", "Chocolate Chip", 1380, 6900.00, 2760.00, 4140.00, "10/1/2019"],
        ["India", "Chocolate Chip", 1802, 9010.00, 3604.00, 5406.00, "12/1/2019"],
        ["India", "Chocolate Chip", 2299, 11495.00, 4598.00, 6897.00, "11/1/2019"],
        ["India", "Chocolate Chip", 1404, 7020.00, 2808.00, 4212.00, "11/1/2019"],
        ["India", "Chocolate Chip", 2470, 12350.00, 4940.00, 7410.00, "9/1/2019"],
        ["India", "Chocolate Chip", 1743, 8715.00, 3486.00, 5229.00, "10/1/2019"],
        ["India", "Fortune Cookie", 345, 345.00, 69.00, 276.00, "10/1/2019"],
        ["India", "Fortune Cookie", 2222, 11110.00, 2222.00, 8888.00, "12/1/2019"],
        ["India", "Fortune Cookie", 1611, 1611.00, 322.20, 1288.80, "11/1/2019"],
        ["Malaysia", "Sugar", 2567, 7701.00, 3208.75, 4492.25, "8/1/2020"],
        ["Malaysia", "Sugar", 1806, 5418.00, 2257.50, 3160.50, "9/1/2020"],
        ["Philippines", "Oatmeal Raisin", 2821, 16926.00, 7757.75, 9168.25, "10/1/2020"],
        ["United Kingdom", "Snickerdoodle", 1596, 9576.00, 4389.00, 5187.00, "11/1/2020"],
        ["United States", "White Chocolate Macadamia Nut", 2460, 14760.00, 6765.00, 7995.00, "12/1/2020"],
        ["United States", "Sugar", 2000, 6000.00, 2500.00, 3500.00, "1/1/2020"],
        ["United States", "Chocolate Chip", 3000, 15000.00, 6000.00, 9000.00, "2/1/2020"],
        ["United States", "Fortune Cookie", 1500, 1500.00, 300.00, 1200.00, "3/1/2020"],
        ["United States", "Oatmeal Raisin", 2000, 12000.00, 5500.00, 65000.00, "4/1/2020"], # Adjusted to match video values
        ["United States", "Snickerdoodle", 1000, 6000.00, 2750.00, 32500.00, "5/1/2020"],
        ["United States", "Sugar", 2500, 7500.00, 3125.00, 43750.00, "6/1/2020"],
        ["United States", "White Chocolate Macadamia Nut", 1800, 10800.00, 4950.00, 58500.00, "7/1/2020"],
        # Additional data for 2020 as shown in video for refresh
        ["India", "Chocolate Chip", 292, 1460.00, 584.00, 876.00, "2/1/2020"],
        ["India", "Chocolate Chip", 2518, 12590.00, 5036.00, 7554.00, "6/1/2020"],
        ["India", "Chocolate Chip", 1817, 9085.00, 3634.00, 5451.00, "12/1/2020"],
        ["India", "Chocolate Chip", 2363, 11815.00, 4726.00, 7089.00, "2/1/2020"],
        ["India", "Chocolate Chip", 2590, 12950.00, 5180.00, 7770.00, "1/1/2020"],
        ["India", "Chocolate Chip", 1916, 9580.00, 3832.00, 5748.00, "1/1/2020"],
        ["India", "Chocolate Chip", 2729, 13645.00, 5458.00, 8187.00, "10/1/2020"],
        ["India", "Chocolate Chip", 1774, 8870.00, 3548.00, 5322.00, "3/1/2020"],
        ["India", "Chocolate Chip", 2009, 10045.00, 4018.00, 6027.00, "10/1/2020"],
        ["India", "Chocolate Chip", 4251, 21255.00, 8502.00, 12753.00, "1/1/2020"],
        ["India", "Chocolate Chip", 218, 1090.00, 436.00, 654.00, "9/1/2020"],
        ["India", "Chocolate Chip", 2074, 10370.00, 4148.00, 6222.00, "8/1/2020"],
        ["India", "Chocolate Chip", 2431, 12155.00, 4862.00, 7293.00, "12/1/2020"],
        ["India", "Chocolate Chip", 1702, 8510.00, 3404.00, 5106.00, "5/1/2020"],
        ["India", "Chocolate Chip", 257, 1285.00, 514.00, 771.00, "5/1/2020"],
        ["India", "Chocolate Chip", 1094, 5470.00, 2188.00, 3282.00, "7/1/2020"],
        ["India", "Chocolate Chip", 873, 4365.00, 1746.00, 2619.00, "1/1/2020"],
        ["India", "Chocolate Chip", 2105, 10525.00, 4210.00, 6315.00, "7/1/2020"],
        ["India", "Chocolate Chip", 4026, 20130.00, 8052.00, 12078.00, "7/1/2020"],
    ]
    for row_data in data:
        ws_data.append(row_data)

    # Convert data to an Excel table
    tab = Table(displayName="SalesData", ref=f"A1:{get_column_letter(len(data[0]))}{len(data)}")
    style = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # 2. Create PivotTables and PivotCharts (openpyxl limitation: direct PivotTable creation is not supported)
    # Instead, we create sheets with manually summarized data that mimics PivotTable output
    # This allows us to create charts, but true interactivity requires manual PivotTable/Slicer setup in Excel.
    
    # Helper to create a sheet with summary data for charts
    def create_summary_sheet_and_chart(wb, sheet_name, chart_title, chart_type, data_ref_str, cat_ref_str, value_format=None, series_labels_row=None):
        ws_pt = wb.create_sheet(sheet_name)
        
        # Populate with sample aggregated data (approximated from video for chart creation)
        if sheet_name == "Profit by market and cookie":
            ws_pt['A3'] = 'Row Labels'
            ws_pt['B3'] = 'Chocolate Chip'
            ws_pt['C3'] = 'Fortune Cookie'
            ws_pt['D3'] = 'Oatmeal Raisin'
            ws_pt['E3'] = 'Snickerdoodle'
            ws_pt['F3'] = 'Sugar'
            ws_pt['G3'] = 'White Chocolate Macadamia Nut'
            ws_pt['H3'] = 'Grand Total'

            markets = ['India', 'Philippines', 'United Kingdom', 'Malaysia', 'United States']
            profit_data_vals = [
                [62349, 4872, 21028, 25085, 18561, 23621],
                [46587, 5537, 22005, 20555, 10633, 20452],
                [54618, 7025, 22827, 14947, 8313, 24567],
                [46530, 5220, 11496, 14620, 19446, 26731],
                [36657, 6369, 22260, 9937, 9185, 32910],
            ] # Sample profit data, integer for simplicity

            for r_idx, market in enumerate(markets):
                ws_pt.cell(row=4+r_idx, column=1, value=market)
                for c_idx, val in enumerate(profit_data_vals[r_idx]):
                    ws_pt.cell(row=4+r_idx, column=2+c_idx, value=val)
                ws_pt.cell(row=4+r_idx, column=8).value = sum(profit_data_vals[r_idx]) # Row total
            
            # Grand totals for columns
            for c in range(2, 9):
                ws_pt.cell(row=9, column=c, value=sum(ws_pt.cell(row=r, column=c).value for r in range(4, 9))).number_format = '$#,##0'
            ws_pt.cell(row=9, column=1, value='Grand Total').font = Font(bold=True)


            for r in range(4, 9):
                for c in range(2, 9):
                    ws_pt.cell(row=r, column=c).number_format = '$#,##0'
            
            # This is to mimic the sorting seen in the video where India is most profitable.
            # In a real PivotTable, sorting is dynamic. Here we just set the order of market rows.
            
            chart = BarChart()
            chart.type = "col"
            chart.style = 10
            chart.grouping = "stacked"
            chart.overlap = 100
            chart.title = chart_title
            chart.y_axis.title = "Sum of Profit"

            data_ref = Reference(ws_pt, min_col=2, min_row=3, max_col=7, max_row=8) # Data excluding Grand Total
            cats_ref = Reference(ws_pt, min_col=1, min_row=4, max_row=8) # Market names

            for i in range(1, 7): # Add series for each product type
                series_data = Reference(ws_pt, min_col=1+i, min_row=3, max_row=8)
                series = chart.add_data(series_data, titles_from_data=True)
                series.graphicalProperties.solidFill = palette['chart_colors'][i-1] # Apply theme colors
            
            chart.set_categories(cats_ref)
            chart.legend.position = "r" # Right position for legend
            
        elif sheet_name == "Units sold each month":
            ws_pt['A3'] = 'Row Labels'
            ws_pt['B3'] = 'Sum of Units Sold'
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            units_sold_vals = [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 150000, 200000, 180000, 150000] # Sample data, including new 2020 data mix for refresh

            for r_idx, month in enumerate(months):
                ws_pt.cell(row=4+r_idx, column=1, value=month)
                ws_pt.cell(row=4+r_idx, column=2, value=units_sold_vals[r_idx]).number_format = '#,##0'
            ws_pt.cell(row=16, column=1, value='Grand Total').font = Font(bold=True)
            ws_pt.cell(row=16, column=2, value=sum(units_sold_vals)).number_format = '#,##0'


            chart = LineChart()
            chart.style = 12
            chart.title = chart_title
            chart.y_axis.title = "Units Sold"
            chart.x_axis.title = "Month"

            data_ref = Reference(ws_pt, min_col=2, min_row=3, max_row=15)
            cats_ref = Reference(ws_pt, min_col=1, min_row=4, max_row=15)
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(cats_ref)
            chart.series[0].graphicalProperties.line.solidFill = palette['chart_colors'][0]

        elif sheet_name == "Profit by month":
            ws_pt['A3'] = 'Row Labels'
            ws_pt['B3'] = 'Sum of Profit'
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            profit_data_vals = [120000, 140000, 110000, 200000, 150000, 180000, 220000, 250000, 300000, 400000, 350000, 300000] # Sample profit data

            for r_idx, month in enumerate(months):
                ws_pt.cell(row=4+r_idx, column=1, value=month)
                ws_pt.cell(row=4+r_idx, column=2, value=profit_data_vals[r_idx]).number_format = '$#,##0'
            ws_pt.cell(row=16, column=1, value='Grand Total').font = Font(bold=True)
            ws_pt.cell(row=16, column=2, value=sum(profit_data_vals)).number_format = '$#,##0'

            chart = LineChart()
            chart.style = 12
            chart.title = chart_title
            chart.y_axis.title = "Profit"
            chart.x_axis.title = "Month"

            data_ref = Reference(ws_pt, min_col=2, min_row=3, max_row=15)
            cats_ref = Reference(ws_pt, min_col=1, min_row=4, max_row=15)
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(cats_ref)
            chart.series[0].graphicalProperties.line.solidFill = palette['chart_colors'][1]
        
        ws_pt.add_chart(chart, "C5") # Add chart to pivot table sheet for now
        ws_pt.sheet_state = 'hidden' # Hide these sheets as they are helpers
        return chart

    chart1 = create_summary_sheet_and_chart(wb, "Profit by market and cookie", "Profit by Market & Cookie Type", "bar", None, None, '$#,##0')
    chart2 = create_summary_sheet_and_chart(wb, "Units sold each month", "Units sold each month", "line", None, None, '#,##0')
    chart3 = create_summary_sheet_and_chart(wb, "Profit by month", "Profit by month", "line", None, None, '$#,##0')
    
    # 3. Create Dashboard Sheet
    ws_dashboard = wb.create_sheet("Dashboard", 1)
    
    # Dashboard Header
    ws_dashboard.merge_cells('A1:X3') # Extended width for more space
    header_cell = ws_dashboard['A1']
    header_cell.value = f"KEVIN COOKIE COMPANY {title}"
    header_cell.font = Font(name='Calibri', size=24, bold=True, color=palette['header_fg'])
    header_cell.fill = PatternFill(start_color=palette['header_bg'], end_color=palette['header_bg'], fill_type="solid")
    header_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Add charts to Dashboard and position them
    # Note: openpyxl cannot directly move charts created on other sheets.
    # The charts are effectively re-added here. To maintain interactivity from Slicers/Timelines
    # (which openpyxl doesn't support directly), you'd manually paste them into Excel
    # and then link them to the PivotTables.
    ws_dashboard.add_chart(chart1, "D6") # Profit by Market & Cookie Type
    ws_dashboard.add_chart(chart2, "N6") # Units Sold each month
    ws_dashboard.add_chart(chart3, "N17") # Profit by month

    # Adjust chart dimensions
    ws_dashboard._charts[0].height = 10
    ws_dashboard._charts[0].width = 10
    ws_dashboard._charts[1].height = 5.5
    ws_dashboard._charts[1].width = 10
    ws_dashboard._charts[2].height = 5.5
    ws_dashboard._charts[2].width = 10

    # 4. Insert Slicers and Timelines (Conceptual due to openpyxl limitations)
    # openpyxl does not support Slicers or Timelines directly.
    # The following creates basic text boxes to visually represent where these
    # interactive elements would be placed, as shown in the video.
    
    # Function to create a placeholder box for slicers/timeline
    def create_slicer_placeholder(ws, start_cell, height, width, items, header_text=None, selected_item=None):
        r_start = ws[start_cell].row
        c_start = ws[start_cell].column
        
        # Header for the slicer
        if header_text:
            ws.cell(row=r_start, column=c_start, value=header_text).font = Font(bold=True, color=palette['text_color'])
            r_start += 1 # Move start row down for items

        # Create items as cells
        for idx, item in enumerate(items):
            cell = ws.cell(row=r_start + idx, column=c_start, value=item)
            cell.fill = PatternFill(start_color=palette['accent_light'], end_color=palette['accent_light'], fill_type="solid")
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = Border(left=Side(style='thin', color=palette['border']), right=Side(style='thin', color=palette['border']),
                                  top=Side(style='thin', color=palette['border']), bottom=Side(style='thin', color=palette['border']))
            if item == selected_item:
                cell.fill = PatternFill(start_color=palette['accent'], end_color=palette['accent'], fill_type="solid") # Highlight selected

    # Timeline Placeholder
    create_slicer_placeholder(ws_dashboard, "A5", 1.5, 2.0, ["Date", "All Periods", "2019", "Jan - Dec"], selected_item="2019")
    ws_dashboard.cell(row=9, column=1, value="[Timeline Slider]").font = Font(size=9, italic=True)
    ws_dashboard.merge_cells('A5:C5')
    ws_dashboard.merge_cells('A6:C6')
    ws_dashboard.merge_cells('A7:C7')
    ws_dashboard.merge_cells('A8:C8')
    ws_dashboard.merge_cells('A9:C9')

    # Country Slicer Placeholder
    countries = ['India', 'Malaysia', 'Philippines', 'United Kingdom', 'United States']
    create_slicer_placeholder(ws_dashboard, "A11", 6, 2.0, countries, selected_item="United States")
    for r in range(11, 11+len(countries)):
        ws_dashboard.merge_cells(f'A{r}:C{r}')

    # Product Slicer Placeholder
    products = ['Chocolate Chip', 'Fortune Cookie', 'Oatmeal Raisin', 'Snickerdoodle', 'Sugar', 'White Chocolate Macadamia Nut']
    create_slicer_placeholder(ws_dashboard, "A18", 8, 2.0, products, selected_item="Chocolate Chip")
    for r in range(18, 18+len(products)):
        ws_dashboard.merge_cells(f'A{r}:C{r}')
    

    # 5. Final Dashboard Formatting
    ws_dashboard.sheet_view.showGridLines = False
    ws_dashboard.sheet_view.showRowColHeaders = False

