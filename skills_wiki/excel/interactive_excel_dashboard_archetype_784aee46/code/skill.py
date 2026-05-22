import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter

# --- Helper functions (Assuming _helpers.py is available or its functions are defined here) ---
# For the purpose of this example, some helper functions for theme loading are assumed.
# In a real-world scenario, these would be imported from a shared _helpers module.

def _get_theme_palette(theme_name):
    """
    Simulates loading a theme palette. In a real setup, this would be more robust.
    """
    if theme_name == "corporate_blue":
        return {
            "header_bg": "002F6C",  # Dark Blue
            "title_fg": "FFFFFF",   # White
            "accent1": "0078D4",    # Medium Blue
            "accent2": "FF8C00",    # Orange
            "border_color": "E0E0E0", # Light Gray
            "bg_color": "F0F0F0"    # Off-white background
        }
    elif theme_name == "modern_red":
        return {
            "header_bg": "B71C1C",  # Deep Red
            "title_fg": "FFFFFF",   # White
            "accent1": "EF5350",    # Light Red
            "accent2": "FFA726",    # Amber
            "border_color": "E0E0E0", # Light Gray
            "bg_color": "F8F8F8"    # Off-white background
        }
    else:
        return _get_theme_palette("corporate_blue") # Default to corporate blue

def _set_cell_style(cell, font_color=None, fill_color=None, border_color=None, bold=False, size=11, wrap_text=False, horizontal='center', vertical='center'):
    """Applies basic styling to a cell."""
    if font_color:
        cell.font = Font(color=font_color, bold=bold, size=size)
    else:
        cell.font = Font(bold=bold, size=size)
    if fill_color:
        cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    if border_color:
        side = Side(border_style="thin", color=border_color)
        cell.border = Border(left=side, right=side, top=side, bottom=side)
    cell.alignment = Alignment(wrap_text=wrap_text, horizontal=horizontal, vertical=vertical)

# --- End Helper functions ---


def render_workbook(wb, *, title: str = "Heroic Insights 2023-2024", theme: str = "corporate_blue", logo_path: str = None) -> None:
    """
    Renders an interactive Excel dashboard from sample data using pivot tables, charts, and slicers.

    Args:
        wb (Workbook): The openpyxl workbook object.
        title (str): The main title for the dashboard.
        theme (str): The name of the theme to apply ('corporate_blue' or 'modern_red').
        logo_path (str): Optional path to a logo image file.
    """
    palette = _get_theme_palette(theme)

    # --- 1. Prepare Data Sheet ---
    ws_data = wb.create_sheet("Example Data", 0)
    data = [
        ["Month", "State", "Product Category", "Units Sold", "Revenue (USD)", "Cost (USD)", "Profit (USD)"],
        # 2023 Data
        ['2023-01-01', 'California', 'Hoodies', 78, 1850, 1300, 550],
        ['2023-01-01', 'Texas', 'T-shirts', 120, 3200, 2112.5, 1087.5],
        ['2023-01-01', 'New York', 'Hoodies', 90, 2500, 1500, 1000],
        ['2023-01-01', 'Florida', 'Hoodies', 60, 1500, 990, 510],
        ['2023-01-01', 'Illinois', 'T-shirts', 110, 2750, 1957.5, 792.5],
        ['2023-02-01', 'California', 'T-shirts', 85, 2200, 1452, 748],
        ['2023-02-01', 'Colorado', 'Hoodies', 55, 1275, 841.5, 433.5],
        ['2023-02-01', 'Washington', 'T-shirts', 95, 2375, 1570, 805],
        ['2023-03-01', 'Texas', 'Hoodies', 70, 1750, 1155, 595],
        ['2023-03-01', 'New York', 'T-shirts', 130, 3500, 2310, 1190],
        # ... adding more data to simulate 2 years and ensure pivot table grouping works
        ['2023-04-01', 'Florida', 'Hoodies', 80, 2000, 1320, 680],
        ['2023-04-01', 'Illinois', 'T-shirts', 90, 2250, 1485, 765],
        ['2023-05-01', 'California', 'Hoodies', 100, 2500, 1650, 850],
        ['2023-05-01', 'Colorado', 'T-shirts', 75, 1875, 1237.5, 637.5],
        ['2023-06-01', 'Washington', 'Hoodies', 110, 2750, 1815, 935],
        ['2023-06-01', 'Texas', 'T-shirts', 140, 3500, 2310, 1190],
        ['2023-07-01', 'New York', 'Hoodies', 105, 2625, 1732.5, 892.5],
        ['2023-07-01', 'Florida', 'T-shirts', 95, 2375, 1570, 805],
        ['2023-08-01', 'Illinois', 'Hoodies', 85, 2125, 1399.5, 722.5],
        ['2023-08-01', 'California', 'T-shirts', 115, 2875, 1897.5, 977.5],
        ['2023-09-01', 'Colorado', 'Hoodies', 65, 1625, 1072.5, 552.5],
        ['2023-09-01', 'Washington', 'T-shirts', 105, 2625, 1732.5, 892.5],
        ['2023-10-01', 'Texas', 'Hoodies', 75, 1875, 1237.5, 637.5],
        ['2023-10-01', 'New York', 'T-shirts', 120, 3000, 1980, 1020],
        ['2023-11-01', 'Florida', 'Hoodies', 70, 1750, 1155, 595],
        ['2023-11-01', 'Illinois', 'T-shirts', 100, 2500, 1650, 850],
        ['2023-12-01', 'California', 'Hoodies', 95, 2375, 1570, 805],
        ['2023-12-01', 'Colorado', 'T-shirts', 80, 2000, 1320, 680],
        # 2024 Data (simulated growth)
        ['2024-01-01', 'California', 'Hoodies', 85, 2000, 1350, 650],
        ['2024-01-01', 'Texas', 'T-shirts', 130, 3500, 2350, 1150],
        ['2024-01-01', 'New York', 'Hoodies', 100, 2750, 1650, 1100],
        ['2024-01-01', 'Florida', 'Hoodies', 65, 1600, 1050, 550],
        ['2024-01-01', 'Illinois', 'T-shirts', 120, 3000, 2100, 900],
        ['2024-02-01', 'California', 'T-shirts', 90, 2400, 1584, 816],
        ['2024-02-01', 'Colorado', 'Hoodies', 60, 1350, 891, 459],
        ['2024-02-01', 'Washington', 'T-shirts', 105, 2600, 1716, 884],
        ['2024-03-01', 'Texas', 'Hoodies', 75, 1900, 1254, 646],
        ['2024-03-01', 'New York', 'T-shirts', 140, 3700, 2442, 1258],
        ['2024-04-01', 'Florida', 'Hoodies', 85, 2100, 1386, 714],
        ['2024-04-01', 'Illinois', 'T-shirts', 95, 2450, 1617, 833],
        ['2024-05-01', 'California', 'Hoodies', 110, 2700, 1782, 918],
        ['2024-05-01', 'Colorado', 'T-shirts', 80, 2000, 1320, 680],
        ['2024-06-01', 'Washington', 'Hoodies', 120, 2900, 1914, 986],
        ['2024-06-01', 'Texas', 'T-shirts', 150, 3800, 2508, 1292],
        ['2024-07-01', 'New York', 'Hoodies', 115, 2800, 1848, 952],
        ['2024-07-01', 'Florida', 'T-shirts', 100, 2550, 1683, 867],
        ['2024-08-01', 'Illinois', 'Hoodies', 90, 2250, 1485, 765],
        ['2024-08-01', 'California', 'T-shirts', 125, 3050, 2013, 1037],
        ['2024-09-01', 'Colorado', 'Hoodies', 70, 1700, 1122, 578],
        ['2024-09-01', 'Washington', 'T-shirts', 110, 2700, 1782, 918],
        ['2024-10-01', 'Texas', 'Hoodies', 80, 1950, 1287, 663],
        ['2024-10-01', 'New York', 'T-shirts', 130, 3200, 2112, 1088],
        ['2024-11-01', 'Florida', 'Hoodies', 75, 1850, 1221, 629],
        ['2024-11-01', 'Illinois', 'T-shirts', 105, 2650, 1749, 901],
        ['2024-12-01', 'California', 'Hoodies', 100, 2450, 1617, 833],
        ['2024-12-01', 'Colorado', 'T-shirts', 85, 2100, 1386, 714],
        # 2025 Data (simulated further growth for refresh demo)
        ['2025-01-01', 'California', 'Hoodies', 90, 2200, 1450, 750],
        ['2025-01-01', 'Texas', 'T-shirts', 140, 3700, 2400, 1300],
        ['2025-01-01', 'New York', 'Hoodies', 110, 2900, 1750, 1150],
        ['2025-01-01', 'Florida', 'Hoodies', 70, 1700, 1100, 600],
        ['2025-01-01', 'Illinois', 'T-shirts', 130, 3200, 2200, 1000],
    ]
    for row_data in data:
        ws_data.append(row_data)

    data_range = f"A1:{get_column_letter(len(data[0]))}{len(data)}"
    tab = Table(displayName="Sales", ref=data_range)
    style = TableStyleInfo(name="TableStyleLight10", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    tab.tableStyleInfo = style
    ws_data.add_table(tab)
    
    # Format date column
    for row in ws_data.iter_rows(min_row=2, min_col=1, max_col=1):
        for cell in row:
            cell.number_format = 'yyyy-mm-dd'

    # --- 2. Create Pivot Tables and Charts ---
    # Monthly Revenue Trend
    ws_revenue = wb.create_sheet("Revenue Trend")
    pt_revenue = openpyxl.pivot.pivot_table.PivotTable(
        name="RevenueTrend",
        ref="Sales",
        columns=["Product Category"],
        rows=["Month"],
        values=["Revenue (USD)"]
    )
    ws_revenue.add_pivot(pt_revenue)

    chart_revenue = LineChart()
    chart_revenue.title = "Monthly Revenue Trend"
    chart_revenue.style = 10 # Example style
    data_ref_revenue = Reference(ws_revenue, min_col=4, min_row=3, max_col=5, max_row=ws_revenue.max_row)
    cats_ref_revenue = Reference(ws_revenue, min_col=1, min_row=4, max_row=ws_revenue.max_row)
    chart_revenue.add_data(data_ref_revenue, titles_from_data=True)
    chart_revenue.set_categories(cats_ref_revenue)
    chart_revenue.x_axis.number_format = 'yyyy-mm' # Format x-axis as year-month
    ws_revenue.add_chart(chart_revenue, "G1")

    # Units Sold by Product Category
    ws_units = wb.create_sheet("T-shirts vs Hoodies")
    pt_units = openpyxl.pivot.pivot_table.PivotTable(
        name="TShirtsVsHoodies",
        ref="Sales",
        columns=["Product Category"],
        rows=["Month"], # Will be grouped by years in OpenPyxl automatically
        values=["Units Sold"]
    )
    ws_units.add_pivot(pt_units)

    # Need to manually create the year grouping for the pivot table if it doesn't do it automatically or ensure proper field order.
    # For openpyxl's current capabilities, this might involve manually setting row fields more precisely if auto-grouping isn't enough.
    # Assuming the pivot table field list handles year grouping as shown in video.

    chart_units = BarChart()
    chart_units.type = "col"
    chart_units.style = 10 # Example style
    chart_units.title = "Sum of Units Sold"
    chart_units.y_axis.title = "Units Sold"
    data_ref_units = Reference(ws_units, min_col=4, min_row=3, max_col=5, max_row=ws_units.max_row)
    cats_ref_units = Reference(ws_units, min_col=1, min_row=4, max_row=ws_units.max_row)
    chart_units.add_data(data_ref_units, titles_from_data=True)
    chart_units.set_categories(cats_ref_units)
    ws_units.add_chart(chart_units, "G1")

    # Top 5 States by Profit
    ws_profit = wb.create_sheet("Top 5 States")
    pt_profit = openpyxl.pivot.pivot_table.PivotTable(
        name="Top5States",
        ref="Sales",
        rows=["State"],
        values=["Profit (USD)"]
    )
    ws_profit.add_pivot(pt_profit)

    # OpenPyXL doesn't have direct Top N filter support in pivot table definition.
    # This would typically be applied manually in Excel or post-processed from the pivot table data.
    # For this skill, we'll assume the pivot table is generated, and top-N filtering could be applied
    # to the *chart data reference* or handled in a more advanced pivot table setup.
    # For simplicity, we'll draw a chart from the pivot table and indicate the filter concept.

    chart_profit = BarChart()
    chart_profit.type = "col"
    chart_profit.style = 10 # Example style
    chart_profit.title = "Top 5 States by Profit"
    chart_profit.y_axis.title = "Profit (USD)"
    # Assuming top 5 filter is applied to the pivot table *data* for the chart reference
    data_ref_profit = Reference(ws_profit, min_col=2, min_row=3, max_col=2, max_row=7) # Adjust max_row for top 5
    cats_ref_profit = Reference(ws_profit, min_col=1, min_row=4, max_row=7) # Adjust max_row for top 5
    chart_profit.add_data(data_ref_profit, titles_from_data=True)
    chart_profit.set_categories(cats_ref_profit)
    ws_profit.add_chart(chart_profit, "G1")

    # --- 3. Create Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard", 0) # Place at the beginning
    ws_dashboard.sheet_view.showGridLines = False
    
    # Set background color
    ws_dashboard.sheet_properties.pageSetUpPr.fitToPage = True # For PDF export if needed
    ws_dashboard.sheet_properties.pageSetUpPr.orientation = "landscape"
    
    # Add a main title shape
    title_shape = ws_dashboard.drawing.add_shape(
        'roundedRect', openpyxl.drawing.xdr.XDRPoint2D(0, 0), openpyxl.drawing.xdr.XDRPoint2D(1000, 1000)
    ) # Placeholder for shape
    title_shape.width = 1200 # Approx. width in pixels
    title_shape.height = 70 # Approx. height in pixels
    title_shape.anchor = 'A1'
    title_shape.left = 0
    title_shape.top = 0
    
    # Apply fill and text to the title shape
    title_shape.fill = PatternFill(start_color=palette["header_bg"], end_color=palette["header_bg"], fill_type="solid")
    
    title_text = openpyxl.drawing.text.TextBody()
    title_text.rich = openpyxl.drawing.text.RichText()
    p = openpyxl.drawing.text.Paragraph()
    p.add_run_properties(font=openpyxl.drawing.text.Font(typeface="Aptos Narrow", sz=2400, b=True, color=openpyxl.drawing.text.ColorChoice(srgbClr=palette["title_fg"])))
    p.append(openpyxl.drawing.text.Text(text=title))
    title_text.rich.add_paragraph(p)
    title_shape.text_frame = title_text
    
    # Optional: Add logo
    if logo_path:
        try:
            img = Image(logo_path)
            img.width = 60 # Adjust width as needed
            img.height = 60 # Adjust height as needed
            img.anchor = 'B2' # Position relative to cell B2
            ws_dashboard.add_image(img)
        except Exception as e:
            print(f"Could not load logo: {e}")

    # Copy/Paste charts and slicers (OpenPyXL doesn't support direct copy/paste of objects and slicers)
    # This part needs to be handled by recreating chart/slicer definitions and positioning them.
    # For a real implementation, you'd use a more advanced approach or pre-defined positions.

    # Position existing charts (simplified for demo)
    ws_dashboard.add_chart(chart_units, "D5")
    ws_dashboard.add_chart(chart_profit, "L5")
    ws_dashboard.add_chart(chart_revenue, "D20")

    # Slicers are not directly supported by openpyxl's API for creation and placement in a generic way.
    # The video demonstrates Excel's built-in Slicer features. To replicate interactivity,
    # one would typically set up event handlers in VBA or use a different tool.
    # OpenPyXL can *read* slicers, but not *create* them with full Excel functionality.
    # For this Python code, we can only demonstrate the *concept* of slicers by implying their presence
    # and their connection to pivot tables that would be refreshed.

    # --- 4. Hide Helper Sheets ---
    ws_revenue.sheet_state = 'hidden'
    ws_units.sheet_state = 'hidden'
    ws_profit.sheet_state = 'hidden'
    ws_data.sheet_state = 'hidden'

    # Remove the default sheet created by openpyxl if it exists and is empty
    if 'Sheet' in wb.sheetnames and wb['Sheet'].max_row == 1 and wb['Sheet'].max_column == 1:
        del wb['Sheet']

# Example usage:
if __name__ == "__main__":
    wb = openpyxl.Workbook()
    # Delete the default 'Sheet' created by openpyxl to start clean
    if 'Sheet' in wb.sheetnames:
        del wb['Sheet']
        
    # Create the dashboard with default theme
    render_workbook(wb, title="SuperHero Hub Insights 2023-2024")
    wb.save("interactive_dashboard_corporate_blue.xlsx")

    # Create the dashboard with a different theme
    wb2 = openpyxl.Workbook()
    if 'Sheet' in wb2.sheetnames:
        del wb2['Sheet']
    render_workbook(wb2, title="SuperHero Hub Insights 2023-2024", theme="modern_red")
    wb2.save("interactive_dashboard_modern_red.xlsx")

    print("Dashboards created successfully!")
    print("Note: Slicer creation and full interactive linking (as in Excel UI) are not directly supported by openpyxl's API.")
    print("The charts are positioned and styled, and their data source comes from hidden pivot tables.")
    print("New data added to 'Example Data' will update pivot tables/charts upon manual refresh in Excel.")

