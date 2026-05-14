import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import pandas as pd
from datetime import datetime
import io
import math

# Helper to load theme colors - assuming a _helpers.py exists
# For standalone, redefine it here or use a simplified color map
def _load_theme_colors(theme_name):
    themes = {
        "corporate_blue": {
            "header_bg_fill": "FF2E4064",  # Dark Blue
            "header_fg_font": "FFFFFFFF",  # White
            "sheet_bg_fill": "FFFFFFFF",   # White
            "chart_colors": [
                "FF4C78B1", "FF8EBC8F", "FFC19A6B", "FFDA7C80", "FF6A4A7C", "FF5E9C88"
            ]
        },
        "corporate_green": {
            "header_bg_fill": "FF4CAF50",  # Green
            "header_fg_font": "FFFFFFFF",  # White
            "sheet_bg_fill": "FFFFFFFF",   # White
            "chart_colors": [
                "FF8BC34A", "FFCDDC39", "FFFFA726", "FFFF7043", "FF00BCD4", "FF673AB7"
            ]
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def _create_chart_title_style(chart, title_text, font_size=14, font_bold=True):
    chart.title = title_text
    # Openpyxl doesn't have direct rich text manipulation for chart titles like VBA/UI
    # For more advanced styling, direct XML modification would be needed.
    # The font size and bold are basic attributes.

def render_workbook(wb, *, title: str, theme: str = "corporate_blue", data: pd.DataFrame = None) -> None:
    """
    Renders an interactive performance dashboard in Microsoft Excel.

    Args:
        wb: An openpyxl workbook object.
        title (str): The title of the dashboard.
        theme (str): The name of the theme to apply (e.g., "corporate_blue").
        data (pd.DataFrame): The raw data for the dashboard. If None, sample data is used.
    """
    theme_colors = _load_theme_colors(theme)

    # --- 1. Prepare Data Sheet ---
    if data is None:
        # Sample data matching video structure
        data_io = io.StringIO("""Country,Product,Units Sold,Revenue,Cost,Profit,Date
India,Chocolate Chip,1725,8625.00,3450.00,5175.00,11/1/2019
India,Chocolate Chip,2152,10760.00,4304.00,6456.00,11/1/2019
India,Chocolate Chip,2349,11745.00,4698.00,7047.00,10/1/2019
India,Chocolate Chip,1228,6140.00,2456.00,3684.00,10/1/2019
India,Chocolate Chip,1389,6945.00,2778.00,4167.00,10/1/2019
India,Chocolate Chip,1802,9010.00,3604.00,5406.00,12/1/2019
India,Chocolate Chip,2299,11495.00,4598.00,6897.00,12/1/2019
India,Chocolate Chip,2299,11495.00,4598.00,6897.00,9/1/2019
India,Chocolate Chip,1404,7020.00,2808.00,4212.00,9/1/2019
India,Chocolate Chip,2470,12350.00,4940.00,7410.00,9/1/2019
India,Chocolate Chip,1743,8715.00,3486.00,5229.00,10/1/2019
India,Chocolate Chip,2222,11110.00,4444.00,6666.00,11/1/2019
India,Fortune Cookie,345,345.00,69.00,276.00,10/1/2019
India,Fortune Cookie,1611,1611.00,322.20,1288.80,10/1/2019
India,Oatmeal Raisin,21028,21028.00,4205.60,16822.40,9/1/2019
India,Snickerdoodle,25085,25085.00,5017.00,20068.00,10/1/2019
India,Snickerdoodle,18561,18561.00,3712.20,14848.80,10/1/2019
India,Sugar,10633,10633.00,2126.60,8506.40,11/1/2019
India,Sugar,18561,18561.00,3712.20,14848.80,10/1/2019
India,White Chocolate Macadamia Nut,23621,23621.00,4724.20,18896.80,11/1/2019
India,White Chocolate Macadamia Nut,20452,20452.00,4090.40,16361.60,12/1/2019
Malaysia,Chocolate Chip,46587,46587.00,9317.40,37269.60,11/1/2019
Malaysia,Chocolate Chip,5537.6,5537.60,1107.52,4430.08,12/1/2019
Malaysia,Fortune Cookie,7025.6,7025.60,1405.12,5620.48,10/1/2019
Malaysia,Oatmeal Raisin,22005,22005.00,4401.00,17604.00,10/1/2019
Malaysia,Snickerdoodle,20555,20555.00,4111.00,16444.00,11/1/2019
Malaysia,Sugar,10633,10633.00,2126.60,8506.40,12/1/2019
Malaysia,White Chocolate Macadamia Nut,24567,24567.00,4913.40,19653.60,11/1/2019
Malaysia,White Chocolate Macadamia Nut,20452,20452.00,4090.40,16361.60,10/1/2019
Philippines,Chocolate Chip,54618,54618.00,10923.60,43694.40,11/1/2019
Philippines,Chocolate Chip,5220,5220.00,1044.00,4176.00,12/1/2019
Philippines,Fortune Cookie,7026,7026.00,1405.20,5620.80,10/1/2019
Philippines,Oatmeal Raisin,22005,22005.00,4401.00,17604.00,10/1/2019
Philippines,Snickerdoodle,20555,20555.00,4111.00,16444.00,11/1/2019
Philippines,Sugar,10633,10633.00,2126.60,8506.40,12/1/2019
Philippines,White Chocolate Macadamia Nut,24567,24567.00,4913.40,19653.60,11/1/2019
Philippines,White Chocolate Macadamia Nut,20452,20452.00,4090.40,16361.60,10/1/2019
United Kingdom,Chocolate Chip,46530,46530.00,9306.00,37224.00,11/1/2019
United Kingdom,Chocolate Chip,5538,5538.00,1107.60,4430.40,12/1/2019
United Kingdom,Fortune Cookie,7026,7026.00,1405.20,5620.80,10/1/2019
United Kingdom,Oatmeal Raisin,17536,17536.00,3507.20,14028.80,10/1/2019
United Kingdom,Snickerdoodle,19446,19446.00,3889.20,15556.80,11/1/2019
United Kingdom,Sugar,14947,14947.00,2989.40,11957.60,12/1/2019
United Kingdom,White Chocolate Macadamia Nut,26731,26731.00,5346.20,21384.80,11/1/2019
United Kingdom,White Chocolate Macadamia Nut,20452,20452.00,4090.40,16361.60,10/1/2019
United States,Chocolate Chip,36657,36657.00,7331.40,29325.60,11/1/2019
United States,Chocolate Chip,6369,6369.00,1273.80,5095.20,12/1/2019
United States,Fortune Cookie,29024,29024.00,5804.80,23219.20,10/1/2019
United States,Oatmeal Raisin,22260,22260.00,4452.00,17808.00,10/1/2019
United States,Snickerdoodle,9938,9938.00,1987.60,7950.40,11/1/2019
United States,Sugar,8313,8313.00,1662.60,6650.40,12/1/2019
United States,White Chocolate Macadamia Nut,32910,32910.00,6582.00,26328.00,11/1/2019
United States,White Chocolate Macadamia Nut,20452,20452.00,4090.40,16361.60,10/1/2019
India,Chocolate Chip,292,1460.00,584.00,876.00,2/1/2020
India,Chocolate Chip,2518,12590.00,5036.00,7554.00,6/1/2020
India,Chocolate Chip,1817,9085.00,3634.00,5451.00,12/1/2020
India,Chocolate Chip,2363,11815.00,4726.00,7089.00,2/1/2020
India,Chocolate Chip,1295,6475.00,2590.00,3885.00,1/1/2020
India,Chocolate Chip,1916,9580.00,3832.00,5748.00,1/1/2022
India,Chocolate Chip,252,1260.00,504.00,756.00,1/1/2022
India,Chocolate Chip,2729,13645.00,5458.00,8187.00,1/1/2020
India,Chocolate Chip,1774,8870.00,3548.00,5322.00,3/1/2020
India,Chocolate Chip,2009,10045.00,4018.00,6027.00,10/1/2020
India,Chocolate Chip,4251,21255.00,8502.00,12753.00,4/1/2020
India,Chocolate Chip,218,1090.00,436.00,654.00,9/1/2020
India,Chocolate Chip,2074,10370.00,4148.00,6222.00,8/1/2020
India,Chocolate Chip,2431,12155.00,4862.00,7293.00,12/1/2020
India,Chocolate Chip,1702,8510.00,3404.00,5106.00,5/1/2020
India,Chocolate Chip,257,1285.00,514.00,771.00,5/1/2020
India,Chocolate Chip,1094,5470.00,2188.00,3282.00,3/1/2020
India,Chocolate Chip,873,4365.00,1746.00,2619.00,1/1/2020
India,Chocolate Chip,2105,10525.00,4210.00,6315.00,7/1/2020
India,Chocolate Chip,4026,20130.00,8052.00,12078.00,7/1/2020
""")
        data = pd.read_csv(data_io)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Months'] = data['Date'].dt.strftime('%b') # Add Months column for pivot table grouping

    ws_data = wb.create_sheet("Data", 0)
    for r_idx, row in enumerate(data.itertuples(index=False), 1):
        if r_idx == 1:
            ws_data.append(data.columns.tolist())
        ws_data.append(row)

    # Convert to Excel Table
    table_ref = f"A1:{get_column_letter(data.shape[1])}{data.shape[0] + 1}"
    tab = Table(displayName="Data", ref=table_ref) # Renamed to 'Data' to match video's logic
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)

    # --- 2. Create Pivot Tables and Charts on separate sheets ---
    pivot_sheets_config = [
        {"name": "Profit by market and cookie", "rows": ["Country"], "cols": ["Product"], "values": ["Profit"], "chart_type": "stackedColumn"},
        {"name": "Units sold each month", "rows": ["Months"], "values": ["Units Sold"], "chart_type": "line"},
        {"name": "Profit by month", "rows": ["Months"], "values": ["Profit"], "chart_type": "line"}
    ]

    charts_to_dashboard = []

    for idx, p_config in enumerate(pivot_sheets_config):
        ws_pivot = wb.create_sheet(f"Pivot_{p_config['name'].replace(' ', '_')}")
        
        # Simplified direct data output for charts to avoid complex PivotTable XML structure
        # which openpyxl doesn't fully abstract for complex pivot table reports yet.
        # This section will directly prepare data for charts based on p_config.
        if p_config["name"] == "Profit by market and cookie":
            pivot_data = data.groupby([p_config["rows"][0], p_config["cols"][0]])[p_config["values"][0]].sum().unstack(fill_value=0)
            pivot_data.loc['Grand Total'] = pivot_data.sum()
            pivot_data['Grand Total'] = pivot_data.sum(axis=1) # Calculate row totals
            pivot_data = pivot_data.sort_values(by='Grand Total', ascending=False)
            pivot_data = pivot_data.drop('Grand Total', axis=1) # Drop the overall grand total column from sorting
            
            # Sort columns by their total profit in descending order for display
            col_order = data.groupby(p_config["cols"][0])[p_config["values"][0]].sum().sort_values(ascending=False).index
            pivot_data = pivot_data[col_order]
            
            ws_pivot.append([p_config["rows"][0]] + pivot_data.columns.tolist())
            for country, row_data in pivot_data.iterrows():
                ws_pivot.append([country] + row_data.tolist())
            ws_pivot.append(["Grand Total"] + pivot_data.sum().tolist())
            
            # Format as currency
            for col_idx in range(1, ws_pivot.max_column + 1):
                col_letter = get_column_letter(col_idx)
                for row_idx in range(2, ws_pivot.max_row + 1):
                    cell = ws_pivot[f"{col_letter}{row_idx}"]
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '$#,##0'
        
        elif p_config["name"] == "Units sold each month":
            pivot_data = data.groupby(p_config["rows"][0])[p_config["values"][0]].sum()
            ws_pivot.append([p_config["rows"][0], f"Sum of {p_config['values'][0]}"])
            for month, units in pivot_data.items():
                ws_pivot.append([month, units])
            ws_pivot.append(["Grand Total", pivot_data.sum()])
            
            # Format as number
            for col_idx in range(2, ws_pivot.max_column + 1):
                col_letter = get_column_letter(col_idx)
                for row_idx in range(2, ws_pivot.max_row + 1):
                    cell = ws_pivot[f"{col_letter}{row_idx}"]
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '#,##0'

        elif p_config["name"] == "Profit by month":
            pivot_data = data.groupby(p_config["rows"][0])[p_config["values"][0]].sum()
            ws_pivot.append([p_config["rows"][0], f"Sum of {p_config['values'][0]}"])
            for month, profit in pivot_data.items():
                ws_pivot.append([month, profit])
            ws_pivot.append(["Grand Total", pivot_data.sum()])

            # Format as currency
            for col_idx in range(2, ws_pivot.max_column + 1):
                col_letter = get_column_letter(col_idx)
                for row_idx in range(2, ws_pivot.max_row + 1):
                    cell = ws_pivot[f"{col_letter}{row_idx}"]
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '$#,##0'

        # Create Chart
        if p_config["chart_type"] == "stackedColumn":
            chart = BarChart()
            chart.type = "col"
            chart.style = 10
            chart.varyColors = True
            chart.grouping = "stacked"
            chart.overlap = 100
            chart.height = 10
            chart.width = 16
            
            # Chart data and categories
            data_ref = Reference(ws_pivot, min_col=2, min_row=1, max_col=ws_pivot.max_column -1 , max_row=ws_pivot.max_row -1) # Exclude Grand Total Col/Row
            cat_ref = Reference(ws_pivot, min_col=1, min_row=2, max_row=ws_pivot.max_row - 1)
            
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(cat_ref)
            
            # Hide specific items that clutter the chart
            # This would typically be handled by Slicers or PivotTable field properties in Excel
            chart.dLbls = openpyxl.chart.data_label.DataLabelList() # Remove data labels
            chart.dLbls.showVal = False
            
            chart.x_axis.delete = True # Hide X-axis, as countries will be labels
            chart.y_axis.title = p_config["values"][0]
            chart.y_axis.scaling.min = 0

            _create_chart_title_style(chart, p_config["name"])
            
        elif p_config["chart_type"] == "line":
            chart = LineChart()
            chart.style = 10
            chart.varyColors = True
            chart.height = 9
            chart.width = 12

            # Chart data and categories
            data_ref = Reference(ws_pivot, min_col=2, min_row=1, max_col=ws_pivot.max_column, max_row=ws_pivot.max_row -1)
            cat_ref = Reference(ws_pivot, min_col=1, min_row=2, max_row=ws_pivot.max_row -1)
            
            chart.add_data(data_ref, titles_from_data=True)
            chart.set_categories(cat_ref)
            
            chart.dLbls = openpyxl.chart.data_label.DataLabelList() # Remove data labels
            chart.dLbls.showVal = False

            chart.x_axis.title = "Month"
            chart.y_axis.title = p_config["values"][0]
            chart.y_axis.scaling.min = 0
            
            _create_chart_title_style(chart, p_config["name"])
            
        charts_to_dashboard.append(chart)


    # --- 3. Create Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard")
    ws_dashboard.sheet_view.showGridLines = False
    ws_dashboard.sheet_view.showRowColHeaders = False

    # Header section
    ws_dashboard.merge_cells('A1:P6')
    header_cell = ws_dashboard['A1']
    header_cell.value = "KEVIN COOKIE COMPANY Performance Dashboard"
    header_cell.font = Font(name='Calibri', size=28, bold=True, color=theme_colors["header_fg_font"])
    header_cell.fill = PatternFill(start_color=theme_colors["header_bg_fill"], end_color=theme_colors["header_bg_fill"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Add charts to dashboard
    # Chart dimensions and positions from video
    chart_1_pos = "D8" # Profit by Market & Cookie Type
    chart_2_pos = "K8" # Units sold each month
    chart_3_pos = "K25" # Profit by month

    ws_dashboard.add_chart(charts_to_dashboard[0], chart_1_pos)
    ws_dashboard.add_chart(charts_to_dashboard[1], chart_2_pos)
    ws_dashboard.add_chart(charts_to_dashboard[2], chart_3_pos)

    # --- 4. Add Slicers and Timelines (Placeholders) ---
    # openpyxl does not directly support inserting Slicers or Timelines,
    # as these are interactive UI elements controlled by Excel's application layer.
    # The positions are based on the video for visual representation.
    # We will create merged cells with labels to indicate their presence.

    # Timeline (Date) Placeholder
    ws_dashboard.merge_cells(start_row=8, start_column=1, end_row=13, end_column=3)
    timeline_cell = ws_dashboard.cell(row=8, column=1)
    timeline_cell.value = "Date Timeline (Manual)"
    timeline_cell.font = Font(bold=True)
    timeline_cell.alignment = Alignment(horizontal='center', vertical='center', wrapText=True)
    timeline_cell.fill = PatternFill(start_color="FFF0F0F0", end_color="FFF0F0F0", fill_type="solid")


    # Country Slicer Placeholder
    ws_dashboard.merge_cells(start_row=15, start_column=1, end_row=21, end_column=3)
    country_slicer_cell = ws_dashboard.cell(row=15, column=1)
    country_slicer_cell.value = "Country Slicer (Manual)"
    country_slicer_cell.font = Font(bold=True)
    country_slicer_cell.alignment = Alignment(horizontal='center', vertical='center', wrapText=True)
    country_slicer_cell.fill = PatternFill(start_color="FFF0F0F0", end_color="FFF0F0F0", fill_type="solid")


    # Product Slicer Placeholder
    ws_dashboard.merge_cells(start_row=23, start_column=1, end_row=30, end_column=3)
    product_slicer_cell = ws_dashboard.cell(row=23, column=1)
    product_slicer_cell.value = "Product Slicer (Manual)"
    product_slicer_cell.font = Font(bold=True)
    product_slicer_cell.alignment = Alignment(horizontal='center', vertical='center', wrapText=True)
    product_slicer_cell.fill = PatternFill(start_color="FFF0F0F0", end_color="FFF0F0F0", fill_type="solid")


    # --- Final sheet organization ---
    # Hide all auxiliary sheets
    for ws_name in wb.sheetnames:
        if ws_name.startswith("Pivot_"):
            wb[ws_name].sheet_state = 'hidden'

    # Delete initial empty sheet if it exists and is not the only sheet
    if 'Sheet' in wb.sheetnames:
        if len(wb.sheetnames) > 1:
            wb.remove(wb['Sheet'])
        else: # If it's the only sheet, rename it
            wb['Sheet'].title = 'Initial_Empty_Sheet' # Fallback for edge cases

    wb.active = ws_dashboard # Set Dashboard as the active sheet
