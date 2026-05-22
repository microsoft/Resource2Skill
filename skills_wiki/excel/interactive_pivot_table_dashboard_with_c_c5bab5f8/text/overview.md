### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Pivot Table Dashboard with Custom Theme

*   **Tier**: archetype
*   **Core Mechanism**: This skill constructs a multi-sheet Excel workbook that functions as a dynamic and interactive dashboard. It involves setting up raw data with calculated helper columns, creating numerous pivot tables for various aggregations and insights, and then presenting these insights on a dedicated dashboard sheet using linked text boxes, various chart types (bar, line, donut, column), and interactive slicers. A custom color theme is applied across the workbook for consistent branding and visual appeal.
*   **Applicability**: This skill is ideal for analysts, business users, or consultants who need to create professional, self-updating, and interactive data reports from raw data. It’s particularly useful for summarizing large datasets, tracking KPIs, visualizing trends and distributions, and enabling users to explore data through filtering, all within the familiar Excel environment without needing specialized BI software.

### 2. Structural Breakdown

-   **Data Layout**:
    -   `Data` Sheet: A structured Excel Table containing raw transaction data (TX ID, Product, Quantity, Unit Price, Amount, Order Date, Ship Date, Customer Gender, Order Mode, Rating, State, County).
    -   `Data` Sheet (Calculated Columns):
        -   `Days to Deliver`: `[@Ship Date]-[@Order Date]`
        -   `Weeknum`: `WEEKNUM([@Order Date])`
        -   `Gender Value`: `IFS([@Customer Gender]="M","Male",[@Customer Gender]="F","Female",[@Customer Gender]="O","Other",TRUE,"Unknown")`
    -   `Pivots` Sheet: A hidden sheet containing numerous pivot tables, each named for clarity (e.g., `PvtSummary`, `PvtTrends`, `PvtProducts`, `PvtGenderSplit`, `PvtQtyDist`, `PvtGeoQty`, `PvtGeoAmt`, `PvtShipment`, `PvtRating`).
    -   `Dashboard` Sheet: The main visual interface, with a custom background and layout.
    -   `Helper` Sheet: Used for specific data ranges for heatmap (as `openpyxl` doesn't directly support dynamic linked pictures with conditional formatting).

-   **Formula Logic**:
    -   KPI Display on Dashboard (linked to `PvtSummary` on `Pivots` sheet):
        -   Orders: `=TEXT(Pivots!A4,"#,##0")`
        -   Quantity: `=TEXT(Pivots!B4,"#,##0")`
        -   Amount: `=TEXT(Pivots!C4,"$#,##0,.0k")`
        -   Avg. Rating: `=TEXT(Pivots!D4,"0.0")`
        -   Avg. Days to Deliver: `=TEXT(Pivots!E4,"0.0")`
    -   Heatmap Data on `Helper` sheet (linked to `PvtPurchase` pivot): `=Pivots!B5` (example, for percentages), wrapped in `IF(ISBLANK(...),"",...)` to prevent `#REF!` errors.

-   **Visual Design**:
    -   Custom Color Theme: Defined at the workbook level (Page Layout > Colors > Customize Colors) to ensure all chart elements and shapes adhere to a corporate palette (e.g., shades of green, blue, red for accents).
    -   Dashboard Layout: A large rectangle shape for the main background (light green/white), a narrower rectangle for a left-side panel (dark green) with subtle drop shadows.
    -   KPI Section: Text boxes on the left panel display KPI values (linked via formulas), formatted with bold, large fonts, and appropriate icons/emojis.
    -   Chart Titles: Dynamic, clear, and descriptive, often echoing business questions.
    -   No Gridlines: Removed from the dashboard sheet.

-   **Charts/Tables**:
    -   **KPI Display**: Text boxes, linked to pivot table summary values.
    -   **Line Chart (Last 13 Week Trends)**: Displays `PvtTrends` (Sum of Quantity and Sum of Amount by Weeknum) with dual axes.
    -   **Heatmap (Purchase Patterns)**: A linked picture of a conditional-formatted range from the `Helper` sheet, displaying `PvtPurchase` percentages by Order Mode and Gender with divergent color scale.
    -   **Column Chart (Quantity Distribution)**: Displays `PvtQtyDist` (Count of Transactions by Quantity buckets), styled as a histogram with no gap between columns.
    -   **Stacked Bar Chart (Popular Products by Gender)**: Displays `PvtProducts` (Sum of Quantity by Product and Gender), sorted for most popular at the top.
    -   **Donut Chart (Overall Gender Split)**: Displays `PvtGenderSplit` (Sum of Quantity by Gender), with percentage data labels.
    -   **Map Charts (Customer Location)**: Two separate Map Charts (for Quantity and Amount) from `PvtGeoQty` and `PvtGeoAmt` (County vs. Quantity/Amount) in California, with custom color scales (orange for quantity, green for amount).
    -   **Column Chart (Shipping Duration)**: Displays `PvtShipment` (Count of Transactions by Days to Deliver), styled as a histogram.
    -   **Clustered Column Chart (Customer Satisfaction)**: Displays `PvtRating` (Count of Transactions by Month and Rating).
    -   **Slicers**: Inserted for 'Order Mode' and 'Gender Value', connected to all relevant pivot tables for cross-filtering.

-   **Theme Hooks**: `header_bg`, `accent1` to `accent6` for colors. The custom color palette is designed to match the 'Viva Calif' brand.

### 3. Reproduction Code

Due to the complexity of a full archetype skill involving multiple pivot tables, dynamic linked pictures (which openpyxl doesn't directly support dynamically as images of ranges with live conditional formatting), and advanced chart customizations/slicer connections (which are extensive in openpyxl for multiple pivots), a complete, concise code block for the entire dashboard is not feasible within typical code block limits.

Instead, the following `archetype` skill outlines the structure and creates key components using `openpyxl`, demonstrating data setup, pivot creation, linking KPIs, and adding some illustrative charts. It includes comments for advanced elements that would require significant additional `openpyxl` code or alternative approaches (e.g., VBA for linked pictures, external tools for complex map charts).

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference, series
from openpyxl.chart.label import DataLabelList
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta

# Helper to load theme colors (assuming _helpers module exists or theme colors are hardcoded for example)
def get_theme_colors(theme_name: str):
    colors = {
        "corporate_blue": {
            "dark_bg": "FF0F212D",
            "light_bg": "FFFFFFFF",
            "accent1": "FF0070C0", # Blue
            "accent2": "FFED7D31", # Orange
            "accent3": "FF70AD47", # Green
            "accent4": "FF7030A0", # Purple
            "accent5": "FF4472C4", # Lighter Blue
            "accent6": "FFB09010", # Goldish
            "text_dark": "FF000000",
            "text_light": "FFFFFFFF"
        },
        "viva_calif": { # Custom theme inspired by video
            "dark_bg": "FF2F5336", # Dark Green
            "light_bg": "FFE5F0E6", # Light Green
            "accent1": "FFB09010", # Gold (for amount)
            "accent2": "FFCC4C02", # Orange-Red
            "accent3": "FF008080", # Teal
            "accent4": "FF663399", # Darker Purple
            "accent5": "FF4682B4", # Steel Blue
            "accent6": "FFB8860B", # Dark Goldenrod
            "text_dark": "FF000000",
            "text_light": "FFFFFFFF"
        }
    }
    return colors.get(theme_name, colors["corporate_blue"])

def render_workbook(wb, *, title: str = "E-Commerce Dashboard", theme: str = "viva_calif", **kwargs) -> None:
    colors = get_theme_colors(theme)

    # --- 1. Data Sheet Setup ---
    ws_data = wb.active
    ws_data.title = "Data"

    # Create dummy data for 3 months (Jan-Mar 2025)
    header = ["TX ID", "Product", "Quantity", "Unit Price", "Amount", "Order Date", "Ship Date", "Customer Gender", "Order Mode", "Rating", "State", "County"]
    data_rows = []
    products = ["Shorts", "Tank Tops", "Graphic Tees", "Hoodies & Sweatshirts", "Jeans", "Sandals", "Bikinis", "Workout Tops", "Maxi Dresses", "Casual Dresses", "Pajama Sets", "Sunglasses", "Tote Bags", "Baseball Caps", "Jewelry"]
    order_modes = ["App", "Instagram", "Partner App", "Target.com", "Website"]
    genders = ["M", "F", "O", ""] # M-Male, F-Female, O-Other, Blank-Unknown
    california_counties = [
        "Los Angeles County", "San Diego County", "Orange County", "Riverside County",
        "San Bernardino County", "Santa Clara County", "Alameda County", "Sacramento County",
        "Contra Costa County", "Fresno County", "Kern County", "Ventura County"
    ]
    
    current_tx_id = 100001
    for m in range(1, 4): # Jan, Feb, Mar
        for d in range(1, 29): # Up to 28 days
            for _ in range(5): # 5 transactions per day
                order_date = datetime(2025, m, d)
                ship_date = order_date + timedelta(days=random.randint(0, 7))
                qty = random.randint(1, 20)
                unit_price = round(random.uniform(10.0, 100.0), 2)
                amount = round(qty * unit_price, 2)
                gender = random.choice(genders)
                mode = random.choice(order_modes)
                rating = random.randint(1, 5) if random.random() > 0.1 else "" # Some unknown ratings
                county = random.choice(california_counties)

                data_rows.append([
                    f"TX{current_tx_id:06d}",
                    random.choice(products),
                    qty, unit_price, amount,
                    order_date, ship_date,
                    gender, mode, rating, "California", county
                ])
                current_tx_id += 1

    ws_data.append(header)
    for row in data_rows:
        ws_data.append(row)

    # Convert to Excel Table
    data_table_range = f"A1:{get_column_letter(len(header))}{len(data_rows) + 1}"
    tab = Table(displayName="SalesData", ref=data_table_range)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws_data.add_table(tab)

    # Add calculated columns after table definition for proper formula integration
    # (In openpyxl, it's easier to add these as regular formulas and then they integrate into the table)
    ws_data.cell(row=1, column=len(header) + 1, value="Days to Deliver")
    ws_data.cell(row=1, column=len(header) + 2, value="Weeknum")
    ws_data.cell(row=1, column=len(header) + 3, value="Gender Value")
    
    for r_idx in range(2, len(data_rows) + 2):
        ws_data.cell(row=r_idx, column=len(header) + 1, value=f'=[@[Ship Date]]-[@[Order Date]]')
        ws_data.cell(row=r_idx, column=len(header) + 2, value=f'=WEEKNUM([@[Order Date]])')
        ws_data.cell(row=r_idx, column=len(header) + 3, value=f'=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")')

    # --- 2. Pivots Sheet Setup ---
    ws_pivots = wb.create_sheet("Pivots")
    ws_pivots.sheet_state = 'hidden' # Hide the pivots sheet

    # Placeholder for pivot table creation
    # In a real scenario, you'd create multiple pivot tables here,
    # each extracting different aggregations from 'SalesData'.
    # For openpyxl, pivot table creation is quite involved.
    # We will simulate the output for KPI display.

    # Simulate KPI pivot output for dashboard linking
    ws_pivots['A1'] = "KPIs for Display"
    ws_pivots['A3'] = "Count of TX ID"
    ws_pivots['B3'] = "Sum of Quantity"
    ws_pivots['C3'] = "Sum of Amount"
    ws_pivots['D3'] = "Average of Rating"
    ws_pivots['E3'] = "Average of Days to Deliver"

    # Dummy values for KPIs
    ws_pivots['A4'] = 2400 # Total Orders
    ws_pivots['B4'] = 11997 # Total Quantity
    ws_pivots['C4'] = 649019.8 # Total Amount
    ws_pivots['D4'] = 3.96 # Avg Rating
    ws_pivots['E4'] = 2.3425 # Avg Days to Deliver

    # --- 3. Dashboard Sheet Setup ---
    ws_dashboard = wb.create_sheet("Dashboard")
    
    # Background shapes
    ws_dashboard.column_dimensions['A'].width = 3
    ws_dashboard.column_dimensions['B'].width = 18
    ws_dashboard.column_dimensions['C'].width = 3
    
    # Left panel background
    left_panel_bg = ws_dashboard.drawing.spreadsheet.WorksheetDrawing()
    left_panel_bg.top = 0
    left_panel_bg.left = 0
    left_panel_bg.width = 1900000  # Approx column A-C width
    left_panel_bg.height = 10000000 # Enough to cover height
    
    shape = ws_dashboard.drawing.spreadsheet.Shape(
        f"{colors['dark_bg']}", # Using theme dark_bg color
        [0,0,1,1] # placeholder for position
    )
    left_panel_bg.add_shape(shape)
    
    # Main dashboard background (not fully implemented as one shape due to openpyxl limitations)
    for col_idx in range(4, 30): # Columns D onwards
        ws_dashboard.column_dimensions[get_column_letter(col_idx)].width = 15 # Example width
        for row_idx in range(1, 60): # Example row height
             ws_dashboard.cell(row=row_idx, column=col_idx).fill = PatternFill(start_color=colors['light_bg'][2:], end_color=colors['light_bg'][2:], fill_type="solid")

    # Disable gridlines for dashboard
    ws_dashboard.sheet_view.showGridLines = False

    # --- KPI Display on Dashboard ---
    kpi_start_row = 4
    kpi_names = ["Orders", "Quantity", "Amount", "Avg. Rating", "Avg. Days to Deliver"]
    kpi_cell_refs = ["Pivots!A4", "Pivots!B4", "Pivots!C4", "Pivots!D4", "Pivots!E4"]
    kpi_formats = ["#,##0", "#,##0", "$#,##0,.0k", "0.0", "0.0"]
    kpi_icons = ["🛒", "📦", "💰", "⭐", "🚚"] # Unicode emojis

    for i, name in enumerate(kpi_names):
        # Icon
        ws_dashboard.cell(row=kpi_start_row + i * 4, column=2, value=kpi_icons[i]).font = Font(size=18, bold=True, color=colors['accent1'][2:])
        # Label
        ws_dashboard.cell(row=kpi_start_row + i * 4 + 1, column=2, value=name).font = Font(size=12, bold=False, color=colors['text_light'][2:])
        # Value (linked from Pivots sheet)
        ws_dashboard.cell(row=kpi_start_row + i * 4 + 2, column=2, value=f'=TEXT({kpi_cell_refs[i]},"{kpi_formats[i]}")').font = Font(size=20, bold=True, color=colors['text_light'][2:])

    # --- Charts on Dashboard ---
    # Placeholder for chart data on Pivots sheet (you'd make actual pivots here)
    ws_pivots['G1'] = "Chart Data - Trends"
    for r in range(2, 15):
        ws_pivots.cell(row=r, column=7, value=r) # Weeknum
        ws_pivots.cell(row=r, column=8, value=random.randint(100, 1000)) # Quantity
        ws_pivots.cell(row=r, column=9, value=random.randint(5000, 50000)) # Amount

    # Line Chart for Trends
    chart1 = LineChart()
    chart1.title = "Last 13 Week Trends - Qty & Amount"
    chart1.style = 10
    chart1.y_axis.title = "Quantity"
    chart1.x_axis.title = "Week"

    data = Reference(ws_pivots, min_col=8, min_row=1, max_col=9, max_row=14)
    cats = Reference(ws_pivots, min_col=7, min_row=2, max_row=14)

    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)

    # For Amount, use secondary axis
    s2 = chart1.series[1]
    s2.y_axis = 'secondary'
    chart1.y_axis[1].title = "Amount ($)"

    ws_dashboard.add_chart(chart1, "D2")

    # Placeholder for Heatmap (Openpyxl does not natively support linked pictures with live conditional formatting)
    # This would typically involve copying a range with conditional formatting as a linked picture using VBA or manual paste.
    ws_dashboard.cell(row=2, column=13, value="Heatmap Placeholder").font = Font(size=14, bold=True)
    ws_dashboard.merge_cells("M3:R12")
    ws_dashboard["M3"].value = "Heatmap: Purchase Patterns (Linked Picture Simulation)"
    ws_dashboard["M3"].font = Font(size=10)
    ws_dashboard["M3"].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Map Charts (Openpyxl map charts are not dynamic/interactive like in Excel, and require external data)
    # This part would involve creating map chart data on a helper sheet and then inserting static map charts.
    ws_dashboard.cell(row=15, column=10, value="Map Chart Placeholder").font = Font(size=14, bold=True)
    ws_dashboard.merge_cells("J16:R25")
    ws_dashboard["J16"].value = "Map: Where our customers live (Static Image/Simulation)"
    ws_dashboard["J16"].font = Font(size=10)
    ws_dashboard["J16"].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # --- Slicer Placeholder ---
    # Slicers can be inserted in openpyxl but their connection to pivots
    # is usually managed by the Excel UI or more complex VBA.
    # This code creates placeholders that would represent slicers on the dashboard.
    ws_dashboard.cell(row=22, column=2, value="Order Mode Slicer").font = Font(size=12, bold=True)
    ws_dashboard.merge_cells("B23:B28")
    ws_dashboard["B23"].value = "App\nInstagram\nPartner App\nTarget.com\nWebsite"
    ws_dashboard["B23"].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

    ws_dashboard.cell(row=30, column=2, value="Customer Gender Slicer").font = Font(size=12, bold=True)
    ws_dashboard.merge_cells("B31:B35")
    ws_dashboard["B31"].value = "Female\nMale\nOther\nUnknown"
    ws_dashboard["B31"].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

    # --- Formatting and Polish ---
    # Apply theme colors to various elements (shapes, fonts etc.)
    # In a full solution, you'd iterate through all charts and set their series colors, backgrounds, etc.
    # to match the `colors` dict.

    print("Dashboard workbook structure created. Further styling and dynamic linking (especially for map charts and linked pictures) would require more complex openpyxl operations or VBA.")

```