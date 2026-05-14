### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Interactive Dashboard

*   **Tier**: archetype
*   **Core Mechanism**: This skill demonstrates the comprehensive construction of an interactive dashboard in Excel. It encompasses structured data setup (using Excel Tables and calculated columns), creation of various analytical summaries (simulated pivot tables), dynamic display of key performance indicators (KPIs) through linked text boxes, generation and formatting of diverse charts (line, stacked bar, column, donut, map) to visualize trends and distributions, and integration of interactive slicers for dynamic filtering. A key aspect is the application of a custom corporate color theme for a professional and cohesive visual identity.
*   **Applicability**: This pattern is ideal for creating robust and visually appealing business intelligence dashboards in Excel, particularly when raw transactional data needs to be summarized, analyzed, and presented interactively. It's suitable for sales performance tracking, customer behavior analysis, product popularity, geographical insights, and measuring operational metrics. The emphasis on Excel 2016 compatibility means it's accessible to a broad user base without requiring the latest Excel 365 features. While `openpyxl` can't directly create interactive pivots or slicers, this skill outlines how to prepare data and structure output to mimic such a dashboard, assuming the pivot outputs can be derived or exist.

### 2. Structural Breakdown

-   **Data Layout**:
    -   **'Data' Sheet**: Contains the raw transactional data in an Excel Table. Key columns include 'TX ID', 'Product', 'Quantity', 'Unit Price', 'Amount', 'Order Date', 'Ship Date', 'Customer Gender', 'Order Mode', 'Rating C', 'State', 'County'.
    -   **Calculated Columns**: 'Days to Deliver' (`=[@[Ship Date]]-[@[Order Date]]`), 'Weeknum' (`=WEEKNUM([@[Order Date]])`), 'Gender Value' (`=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")`).
    -   **'Pivots' Sheet**: Contains the output ranges of multiple pivot tables, organized to serve as data sources for charts and KPI displays. These include summary KPIs, weekly trends, purchase patterns (order mode by gender), quantity distribution, popular products by gender, geographical analysis (county by quantity/amount), shipment duration, and customer satisfaction.
    -   **'Dashboard' Sheet**: Main visual interface. Divided into a left-side panel for overall KPIs and slicers (darker background) and a main grid area for various charts (lighter background).
-   **Formula Logic**:
    -   **KPI Display**: Cells on the dashboard linked directly or indirectly (via `TEXT` function for formatting) to cells in the pivot table output ranges. E.g., `=TEXT(Pivots!A4,"#,##0")` for orders, `=TEXT(Pivots!C4,"$#,##0,.0k")` for amount, `=TEXT(Pivots!D4,"0.0")` for average rating.
    -   **Heatmap Data**: A separate range on the 'Pivots' sheet replicates the pivot output for "Order Mode by Gender Value" as percentage. An `IF` formula (`=IF(Pivots!A86="","",Pivots!A86)`) is used to handle blank rows gracefully for charts, ensuring `0` values do not cause display errors.
-   **Visual Design**:
    -   **Theme Colors**: A custom color scheme is applied via "Page Layout -> Colors -> Customize Colors" for cohesive branding. This allows all charts and shapes to update colors in one click.
    -   **Dashboard Layout**: Two main shapes (rectangles) are used for the background (left panel darker, main canvas lighter). Drop shadows add depth.
    -   **KPI Section**: Text boxes are dynamically linked to pivot-derived values. Icons/emojis enhance readability. Formatting includes bold fonts, increased size, and gradient text fills for effect.
    -   **Heatmap**: Conditional formatting (divergent color scale, e.g., blue to red) applied to cells. A white border is added between cells for visual separation. "Paste as Linked Picture" is used to embed this dynamic range onto the dashboard.
    -   **Charts**: Charts are cleaned up by removing unnecessary field buttons, legends, and adjusting gap widths for columns/bars. Titles are dynamically linked or explicitly set to answer business questions.
-   **Charts/Tables**:
    -   **Line Chart**: Used for time series trends (e.g., weekly quantity/amount). Supports secondary axis.
    -   **Stacked Bar Chart**: Used for breakdown by categories and subcategories (e.g., popular products by gender). Category axis can be reversed for better readability.
    -   **Column Chart**: Used for distributions (e.g., quantity distribution, customer satisfaction over time). Gap width can be set to 0 for histograms.
    -   **Donut Chart**: Used for overall percentage splits (e.g., overall gender split). Data labels for percentages.
    -   **Map Chart**: Used for geographical analysis (e.g., county-level quantity/amount). Color scales represent magnitude. Small "inset" maps provide context.
    -   **Slicers**: Interactive filters (e.g., Order Mode, Gender Value) that connect to multiple underlying pivot tables via "Report Connections".
-   **Theme Hooks**:
    -   `header_bg`: Used for the left dashboard panel.
    -   `canvas_bg`: Used for the main dashboard canvas.
    -   `accent_1` through `accent_6`: Used for chart series colors and conditional formatting color scales.
    -   `text_dark`, `text_light`: Used for font colors in KPIs and chart elements.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.axis import ChartLines, DisplayUnitsLabel
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import Series, marker
from openpyxl.chart.label import DataLabel, DataLabelList
from datetime import datetime, timedelta

# Helper to get theme colors (simplified for demonstration)
def _get_theme_colors(theme_name="viva_calif"):
    colors = {
        "viva_calif": {
            "header_bg": "FF2E4E42",  # Dark Green
            "canvas_bg": "FFE5F0DE",  # Light Green
            "accent_1": "FF4CAF50",   # Green
            "accent_2": "FFFF9800",   # Orange
            "accent_3": "FF2196F3",   # Blue
            "accent_4": "FFF44336",   # Red
            "accent_5": "FF9C27B0",   # Purple
            "accent_6": "FF00BCD4",   # Cyan
            "text_dark": "FF000000",
            "text_light": "FFFFFFFF",
            "text_gold": "FFFFD700"
        }
    }
    return colors.get(theme_name, colors["viva_calif"])

def render_workbook(wb, *, title: str = "E-commerce Dashboard", theme: str = "viva_calif", **kwargs) -> None:
    # Get theme colors
    theme_colors = _get_theme_colors(theme)

    # --- 1. Data Sheet Setup (Simulated) ---
    ws_data = wb.create_sheet("Data", 0)
    ws_data.title = "Data"
    
    # Dummy Data for demonstration (simplified transaction data)
    headers = ["TX ID", "Product", "Quantity", "Unit Price", "Amount", "Order Date", "Ship Date", "Customer Gender", "Order Mode", "Rating C", "State", "County", "Days to Deliver", "Weeknum", "Gender Value"]
    ws_data.append(headers)
    
    # Generate some dummy data
    products = ["T-Shirts", "Jeans", "Shorts", "Tank Tops", "Sweatshirts", "Bikinis", "Graphic Tees"]
    genders = ["M", "F", "O", ""] # Male, Female, Other, Unknown
    order_modes = ["App", "Website", "Instagram", "Target.com", "Partner App"]
    states = ["California"]
    counties = ["Los Angeles County", "Orange County", "San Diego County", "Riverside County", "Sacramento County", "Alameda County"]
    
    start_date = datetime(2025, 1, 1)
    
    for i in range(1, 1001):
        tx_id = f"TX{i:05d}"
        product = products[i % len(products)]
        quantity = (i % 10) + 1
        unit_price = round(10.0 + (i % 50) * 0.5, 2)
        amount = round(quantity * unit_price, 2)
        order_date = start_date + timedelta(days=i % 90)
        ship_date = order_date + timedelta(days=i % 7)
        customer_gender_raw = genders[i % len(genders)]
        order_mode = order_modes[i % len(order_modes)]
        rating = (i % 5) + 1
        state = states[0]
        county = counties[i % len(counties)]
        
        # Calculated columns
        days_to_deliver = (ship_date - order_date).days
        weeknum = order_date.isocalendar()[1]
        gender_value = ""
        if customer_gender_raw == "M": gender_value = "Male"
        elif customer_gender_raw == "F": gender_value = "Female"
        elif customer_gender_raw == "O": gender_value = "Other"
        else: gender_value = "Unknown"

        ws_data.append([tx_id, product, quantity, unit_price, amount, order_date, ship_date, customer_gender_raw, order_mode, rating, state, county, days_to_deliver, weeknum, gender_value])

    # Convert data to an Excel Table
    table_ref = f"A1:{get_column_letter(len(headers))}{ws_data.max_row}"
    tab = Table(displayName="SalesData", ref=table_ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws_data.add_table(tab)

    # --- 2. Pivot Data Sheet Setup (Simulated) ---
    ws_pivots = wb.create_sheet("Pivots", 1)

    # --- Simulate PivotTable outputs (as static data for openpyxl chart creation) ---
    # Pivots don't directly generate in openpyxl, but we can set up the data as if they were.
    # This section would typically be driven by actual pivot tables in Excel.

    # pvfSummary (Overall KPIs)
    ws_pivots.cell(row=2, column=1, value="Overall KPIs")
    ws_pivots.cell(row=4, column=1, value="Count of TX ID")
    ws_pivots.cell(row=4, column=2, value=1000) # Dummy total orders
    ws_pivots.cell(row=4, column=3, value=5500) # Dummy total quantity
    ws_pivots.cell(row=4, column=4, value=55000) # Dummy total amount
    ws_pivots.cell(row=4, column=5, value=4.1) # Dummy avg rating
    ws_pivots.cell(row=4, column=6, value=2.5) # Dummy avg days to deliver

    # Display Values for KPIs (formatted)
    ws_pivots.cell(row=2, column=8, value="Values for Display")
    ws_pivots.cell(row=3, column=8, value="Orders")
    ws_pivots.cell(row=3, column=9, value="Qty")
    ws_pivots.cell(row=3, column=10, value="Amount")
    ws_pivots.cell(row=3, column=11, value="Avg. Rating")
    ws_pivots.cell(row=3, column=12, value="Avg. Days")

    ws_pivots.cell(row=4, column=8, value=f'=TEXT(B4,"#,##0")')
    ws_pivots.cell(row=4, column=9, value=f'=TEXT(C4,"#,##0")')
    ws_pivots.cell(row=4, column=10, value=f'=TEXT(D4,"$#,##0,.0k")')
    ws_pivots.cell(row=4, column=11, value=f'=TEXT(E4,"0.0")')
    ws_pivots.cell(row=4, column=12, value=f'=TEXT(F4,"0.0")')

    # pvfTrend (Last 13 Week Trends)
    ws_pivots.cell(row=7, column=1, value="For trends")
    ws_pivots.cell(row=9, column=1, value="Weeknum")
    ws_pivots.cell(row=9, column=2, value="Sum of Quantity")
    ws_pivots.cell(row=9, column=3, value="Sum of Amount")
    for r_idx in range(1, 14): # Simulate 13 weeks
        ws_pivots.cell(row=9 + r_idx, column=1, value=r_idx)
        ws_pivots.cell(row=9 + r_idx, column=2, value=100 + r_idx * 20) # Dummy quantity
        ws_pivots.cell(row=9 + r_idx, column=3, value=1000 + r_idx * 500) # Dummy amount

    # pvfPurchasePattern (How they like to buy - Heatmap source)
    ws_pivots.cell(row=2, column=15, value="For matrix")
    order_modes_full = ["App", "Instagram", "Partner App", "Target.com", "Website"]
    genders_full = ["Female", "Male", "Other", "Unknown"]

    ws_pivots.cell(row=3, column=16, value="Female")
    ws_pivots.cell(row=3, column=17, value="Male")
    ws_pivots.cell(row=3, column=18, value="Other")
    ws_pivots.cell(row=3, column=19, value="Unknown")

    # This part assumes pivot data is already calculated and conditionally formatted in Excel
    # We will simulate the values and apply conditional formatting in openpyxl directly
    # For openpyxl, this would be a regular cell range, not a linked picture directly from a pivot output.
    for r_idx, mode in enumerate(order_modes_full):
        ws_pivots.cell(row=4 + r_idx, column=15, value=mode)
        for c_idx, gender in enumerate(genders_full):
            value = round((r_idx * 0.02 + c_idx * 0.01) + 0.05, 3) # Dummy percentage
            ws_pivots.cell(row=4 + r_idx, column=16 + c_idx, value=value)
            # Apply conditional formatting color scale directly
            # This is illustrative, actual conditional formatting would be on Dashboard
            
    # Error handling for map chart (illustrative IF logic for cells)
    # This simulates the logic to prevent map chart errors if data vanishes
    ws_pivots.cell(row=2, column=21, value="Map Chart Stuff (Qty)")
    ws_pivots.cell(row=3, column=21, value="State")
    ws_pivots.cell(row=3, column=22, value="County")
    ws_pivots.cell(row=3, column=23, value="Qty")
    
    for r_idx, county in enumerate(counties):
        ws_pivots.cell(row=4 + r_idx, column=21, value=states[0])
        ws_pivots.cell(row=4 + r_idx, column=22, value=county)
        # Simulate quantity, some might be 0 if sliced
        ws_pivots.cell(row=4 + r_idx, column=23, value=(100 - r_idx * 5) if r_idx < 10 else 0)

    # --- 3. Dashboard Sheet Setup ---
    ws_dashboard = wb.create_sheet("Dashboard", 2)
    ws_dashboard.sheet_view.showGridLines = False

    # Set column widths for dashboard layout
    ws_dashboard.column_dimensions['A'].width = 2
    ws_dashboard.column_dimensions['B'].width = 20 # Left Panel
    ws_dashboard.column_dimensions['C'].width = 2
    ws_dashboard.column_dimensions['D'].width = 15 # Main Grid - Chart 1
    ws_dashboard.column_dimensions['E'].width = 15
    ws_dashboard.column_dimensions['F'].width = 15 # Main Grid - Chart 2
    ws_dashboard.column_dimensions['G'].width = 15
    ws_dashboard.column_dimensions['H'].width = 15 # Main Grid - Chart 3
    ws_dashboard.column_dimensions['I'].width = 15
    ws_dashboard.column_dimensions['J'].width = 15 # Main Grid - Chart 4
    ws_dashboard.column_dimensions['K'].width = 15
    ws_dashboard.column_dimensions['L'].width = 15 # Main Grid - Chart 5
    ws_dashboard.column_dimensions['M'].width = 15
    ws_dashboard.column_dimensions['N'].width = 15 # Main Grid - Chart 6
    ws_dashboard.column_dimensions['O'].width = 15

    # Background rectangles
    # Left Panel
    ws_dashboard.merge_cells('A1:B40')
    left_panel_rect = ws_dashboard['A1']
    left_panel_rect.fill = PatternFill(start_color=theme_colors["header_bg"], end_color=theme_colors["header_bg"], fill_type="solid")

    # Main Canvas
    ws_dashboard.merge_cells('C1:O40')
    main_canvas_rect = ws_dashboard['C1']
    main_canvas_rect.fill = PatternFill(start_color=theme_colors["canvas_bg"], end_color=theme_colors["canvas_bg"], fill_type="solid")

    # --- Add Logo and Title (Static for openpyxl) ---
    # In real Excel, you'd insert an image. Here, just text.
    ws_dashboard.cell(row=1, column=2, value="VIVO CALIF").font = Font(size=20, bold=True, color=theme_colors["text_light"])
    ws_dashboard.cell(row=2, column=2, value="E-COMMERCE DASHBOARD").font = Font(size=10, color=theme_colors["text_light"])

    # --- Add KPIs to Left Panel ---
    kpi_start_row = 4
    kpi_labels = ["Orders", "Quantity", "Amount", "Avg. Rating", "Avg. Days to Deliver"]
    kpi_icons = ["🛒", "📦", "💰", "⭐", "🗓️"] # Unicode emojis
    kpi_value_cells = ["H4", "I4", "J4", "K4", "L4"] # Cells in Pivots sheet

    for i, label in enumerate(kpi_labels):
        row = kpi_start_row + i * 3
        ws_dashboard.cell(row=row, column=2, value=f"{kpi_icons[i]} {label}").font = Font(size=10, color=theme_colors["text_light"])
        ws_dashboard.cell(row=row+1, column=2, value=f'=Pivots!{kpi_value_cells[i]}').font = Font(size=16, bold=True, color=theme_colors["text_gold"] if label=="Amount" else theme_colors["text_light"])
        ws_dashboard.cell(row=row+1, column=2).alignment = Alignment(horizontal='left')
        ws_dashboard.row_dimensions[row+1].height = 20 # Adjust height for icons

    # --- Add Slicers (Conceptual in openpyxl) ---
    # Slicers cannot be directly created in openpyxl. We only represent their intended location and purpose.
    slicer_start_row = 25
    ws_dashboard.cell(row=slicer_start_row, column=2, value="Order Mode").font = Font(size=10, bold=True, color=theme_colors["text_light"])
    ws_dashboard.cell(row=slicer_start_row+1, column=2, value="[Slicer Here]").font = Font(size=8, italic=True, color=theme_colors["text_light"])
    ws_dashboard.cell(row=slicer_start_row+5, column=2, value="Customers").font = Font(size=10, bold=True, color=theme_colors["text_light"])
    ws_dashboard.cell(row=slicer_start_row+6, column=2, value="[Slicer Here]").font = Font(size=8, italic=True, color=theme_colors["text_light"])


    # --- Add Charts to Main Grid ---
    chart_column_offset = 4 # Starting column D
    chart_row_offset = 2

    # Chart 1: Last 13 Week Trends (Line Chart)
    chart1_row = chart_row_offset
    chart1_col = chart_column_offset
    
    chart1 = LineChart()
    chart1.title = "Last 13 Week Trends - Qty & Amount"
    chart1.style = 10 # A predefined chart style
    chart1.x_axis.title = "Week"
    chart1.y_axis.title = "Quantity"
    
    # Data for Quantity
    data_qty = Reference(ws_pivots, min_col=2, min_row=10, max_col=2, max_row=22)
    # Data for Amount
    data_amount = Reference(ws_pivots, min_col=3, min_row=10, max_col=3, max_row=22)
    # Categories (Weeknum)
    categories = Reference(ws_pivots, min_col=1, min_row=10, max_col=1, max_row=22)

    series_qty = Series(data_qty, title="Quantity", xvalues=categories)
    series_amount = Series(data_amount, title="Amount", xvalues=categories)
    series_amount.marker = marker.Marker('circle') # Add markers
    series_amount.graphicalProperties.line.solidFill = theme_colors["accent_2"] # Orange
    series_qty.graphicalProperties.line.solidFill = theme_colors["accent_3"] # Blue

    chart1.series.append(series_qty)
    chart1.series.append(series_amount)
    
    # Set amount series to secondary axis
    chart1.set_y_axis_id(10) # arbitrary id
    chart1.y_axis[1].majorGridlines = None
    chart1.y_axis[1].title = "Amount ($)"
    
    ws_dashboard.add_chart(chart1, f"{get_column_letter(chart1_col)}{chart1_row}")
    chart1.width = 12
    chart1.height = 8

    # Chart 2: How they like to buy (Heatmap - conceptual via conditional formatting)
    # For openpyxl, we simulate the heatmap look with conditional formatting on a normal range.
    chart2_row = chart_row_offset
    chart2_col = chart_column_offset + 12 # Adjust columns for spacing
    
    # We will copy the formatted data from Pivots to Dashboard and apply conditional formatting
    for r_idx, mode in enumerate(order_modes_full):
        ws_dashboard.cell(row=chart2_row + 1 + r_idx, column=chart2_col, value=mode).font = Font(bold=True)
        for c_idx, gender in enumerate(genders_full):
            # Use IF logic to handle cases where pivot values might disappear
            formula = f'=IF(ISBLANK(Pivots!{get_column_letter(16+c_idx)}{4+r_idx}),"",Pivots!{get_column_letter(16+c_idx)}{4+r_idx})'
            cell_to_format = ws_dashboard.cell(row=chart2_row + 1 + r_idx, column=chart2_col + 1 + c_idx)
            cell_to_format.value = formula
            cell_to_format.number_format = "0.0%"
            cell_to_format.alignment = Alignment(horizontal='center', vertical='center')

    # Add gender headers
    for c_idx, gender in enumerate(genders_full):
        ws_dashboard.cell(row=chart2_row+1, column=chart2_col+1+c_idx, value=gender).font = Font(bold=True, color=theme_colors["text_dark"])
    
    # Apply Conditional Formatting for heatmap effect
    range_to_cf = f"{get_column_letter(chart2_col+1)}{chart2_row+2}:{get_column_letter(chart2_col+len(genders_full))}{chart2_row+1+len(order_modes_full)}"
    ws_dashboard.conditional_formatting.add(range_to_cf, ColorScaleRule(start_type='min', start_value=None, start_color=theme_colors["accent_3"],
                                                    mid_type='percentile', mid_value=50, mid_color='FFFFFFFF',
                                                    end_type='max', end_value=None, end_color=theme_colors["accent_4"]))

    # Add chart title for heatmap (using a simple text box)
    ws_dashboard.cell(row=chart2_row, column=chart2_col, value="How they like to buy").font = Font(size=12, bold=True)
    
    # Chart 3: Popular Products by Gender (Stacked Bar Chart)
    chart3_row = chart_row_offset + 10
    chart3_col = chart_column_offset
    
    chart3 = BarChart()
    chart3.type = "col"
    chart3.style = 10
    chart3.grouping = "stacked"
    chart3.overlap = 100
    chart3.x_axis.title = "Quantity"
    chart3.y_axis.title = "Product"

    # Data from a simulated pivot (Product, Male, Female, Other, Unknown quantity totals)
    # Max_row here assumes a certain number of products in the pivot output
    products_ref = Reference(ws_pivots, min_col=1, min_row=55, max_row=65) # Assuming Product data starts here
    male_data = Reference(ws_pivots, min_col=3, min_row=54, max_col=3, max_row=65)
    female_data = Reference(ws_pivots, min_col=2, min_row=54, max_col=2, max_row=65)
    other_data = Reference(ws_pivots, min_col=4, min_row=54, max_col=4, max_row=65)
    unknown_data = Reference(ws_pivots, min_col=5, min_row=54, max_col=5, max_row=65)

    chart3.add_data(female_data, titles_from_data=True) # Assuming header in 54
    chart3.add_data(male_data, titles_from_data=True)
    chart3.add_data(other_data, titles_from_data=True)
    chart3.add_data(unknown_data, titles_from_data=True)

    chart3.set_categories(products_ref)
    chart3.title = "Which Products are Popular? (Breakdown by Gender)"
    
    # Colors for series (assuming male/female/other/unknown)
    chart3.series[0].graphicalProperties.solidFill = theme_colors["accent_3"] # Female - Blue
    chart3.series[1].graphicalProperties.solidFill = theme_colors["accent_2"] # Male - Orange
    chart3.series[2].graphicalProperties.solidFill = theme_colors["accent_1"] # Other - Green
    chart3.series[3].graphicalProperties.solidFill = theme_colors["accent_4"] # Unknown - Red

    ws_dashboard.add_chart(chart3, f"{get_column_letter(chart3_col)}{chart3_row}")
    chart3.width = 12
    chart3.height = 8

    # Chart 4: Customer Satisfaction (Clustered Column Chart)
    chart4_row = chart_row_offset + 10
    chart4_col = chart_column_offset + 12

    chart4 = BarChart()
    chart4.type = "col"
    chart4.style = 10
    chart4.title = "How satisfied are our customers?"
    chart4.x_axis.title = "Month"
    chart4.y_axis.title = "Count of Ratings"

    # Data from a simulated pivot for customer satisfaction by month
    months_data = Reference(ws_pivots, min_col=1, min_row=189, max_col=1, max_row=192) # Jan, Feb, Mar
    ratings_data = Reference(ws_pivots, min_col=2, min_row=188, max_col=6, max_row=192) # Ratings 1-5
    
    chart4.add_data(ratings_data, titles_from_data=True)
    chart4.set_categories(months_data)

    # Set colors for ratings (example)
    chart4.series[0].graphicalProperties.solidFill = theme_colors["accent_4"] # Rating 1 (Red)
    chart4.series[1].graphicalProperties.solidFill = theme_colors["accent_2"] # Rating 2 (Orange)
    chart4.series[2].graphicalProperties.solidFill = theme_colors["accent_1"] # Rating 3 (Green)
    chart4.series[3].graphicalProperties.solidFill = theme_colors["accent_3"] # Rating 4 (Blue)
    chart4.series[4].graphicalProperties.solidFill = theme_colors["accent_5"] # Rating 5 (Purple)

    ws_dashboard.add_chart(chart4, f"{get_column_letter(chart4_col)}{chart4_row}")
    chart4.width = 12
    chart4.height = 8
    
    # --- Connect Slicers to Pivots (Conceptual) ---
    # In openpyxl, slicer connections cannot be programmatically created.
    # This functionality would be configured directly in Excel via "Report Connections"
    # Example report connections for 'Order Mode' slicer:
    # Right-click 'Order Mode' slicer -> Report Connections -> Select all relevant pivot tables
    # (e.g., pvfSummary, pvfTrend, pvfPurchasePattern, pvfPopularProducts, pvfGeoQty, pvfGeoAmount, pvfShipDuration, pvfSatisfaction)
    # Ensure to uncheck pivots where the slicer category is already a row/column field (e.g., pvfPurchasePattern and Gender Value)

    # --- Final Formatting and Cleanup ---
    # Hide pivot sheet if desired
    ws_pivots.sheet_state = 'hidden'

    # Set print area to dashboard
    ws_dashboard.page_setup.printArea = f"A1:O{ws_dashboard.max_row}"

# This example assumes the worksheet 'Data' and 'Pivots' are setup manually
# with the appropriate pivot tables and data as described in the breakdown.
# The code primarily focuses on the dashboard sheet generation and styling,
# including KPI linking and chart integration based on pre-existing pivot outputs.
```