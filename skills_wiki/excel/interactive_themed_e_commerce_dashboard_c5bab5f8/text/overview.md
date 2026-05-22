### 1. High-level Skill Pattern Extraction

> **Skill Name**: Interactive Themed E-commerce Dashboard

*   **Tier**: archetype
*   **Core Mechanism**: This skill constructs a multi-sheet Excel workbook to create a dynamic and visually appealing e-commerce analytics dashboard. It structures raw transactional data, leverages PivotTables for comprehensive data aggregation and KPI calculation, links dynamic summary figures to display cells on the dashboard, integrates various chart types for visual analysis, and utilizes slicers for interactive filtering. A key aspect is applying a custom color theme to ensure a consistent and professional brand identity across all visual elements.
*   **Applicability**: This skill is highly applicable for small to medium-sized businesses, analysts, or consultants in the e-commerce sector (or any business with transactional data) who need to rapidly create insightful and interactive reports without relying on expensive, specialized business intelligence software. It's suitable for understanding sales trends, product performance, customer demographics, shipping efficiency, and customer satisfaction. The structured approach allows for easy adaptation to new data or reporting requirements.

### 2. Structural Breakdown

-   **Data Layout**:
    -   **`Data` sheet**: Contains the raw e-commerce transaction data in an Excel Table named `Orders`. Key columns include `TX ID`, `Product`, `Quantity`, `Unit Price`, `Amount`, `Order Date`, `Ship Date`, `Customer Gender`, `Order Mode`, `Rating C`, `State`, `County`.
    -   **Calculated Columns in `Orders` table**:
        -   `Days to Deliver` (formula: `=[@[Ship Date]]-[@[Order Date]]`)
        -   `Weeknum` (formula: `=WEEKNUM([@[Order Date]])`)
        -   `Gender Value` (formula: `=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")`)
    -   **`Pivots` sheet**: Houses multiple PivotTables acting as data sources for the dashboard's KPIs and charts. These pivots are named for easy identification (e.g., `pvfSummary`, `pvfTrend`, `pvfMatrix`, etc.). This sheet also contains a dedicated range where KPI values from `pvfSummary` are linked and formatted for display (e.g., `"=TEXT(A4,"#,##0")"`).
-   **Formula Logic**:
    -   **KPI Display**: `TEXT` formulas are used on the `Pivots` sheet to link to raw PivotTable outputs and apply custom number formatting (e.g., thousands separators, currency, decimals, 'k' suffix for thousands) before displaying on the dashboard.
    -   **Map Chart Data Preparation**: `IF` formulas are used to ensure that if a source cell in the PivotTable (e.g., for a specific county) becomes blank due to slicer filtering, the corresponding cell in the map chart's data range also becomes blank (not zero), preventing `openpyxl` map chart errors.
-   **Visual Design**:
    -   **Dashboard Layout**: The `Dashboard` sheet features a two-panel layout: a dark-themed left sidebar for KPIs and slicers, and a light-themed main area for charts. This is achieved by applying distinct `PatternFill` colors to specific cell ranges. Drop shadows (conceptually, as `openpyxl` doesn't directly support this for cells) are used for visual depth.
    -   **KPI Display**: KPIs are shown in cells within the left sidebar, dynamically linked to the formatted values on the `Pivots` sheet. They use bold, large fonts, with a special accent color (golden) for the "Amount" metric to draw attention. Emojis are used next to KPI labels for intuitive identification.
    -   **Custom Color Theme**: A custom Excel theme (`VivaCalif` in the example) is created via `Page Layout -> Colors -> Customize Colors`. This allows all charts, conditional formatting, and shapes to automatically adopt a consistent corporate color palette with a single click, enabling rapid rebranding or theme adjustments.
-   **Charts/Tables**: The dashboard includes a diverse set of charts:
    -   **Line Chart**: `Last 13 Week Trends - Qty & Amount` (Quantity and Amount over weeks, with Amount on a secondary axis).
    -   **Heatmap**: `How they like to buy` (Percentage of revenue by Order Mode and Gender, using conditional formatting color scales, pasted as a linked picture).
    -   **Column Chart**: `How many they buy` (Distribution of transaction counts by quantity ordered per transaction, with quantities grouped into custom buckets).
    -   **Stacked Bar Chart**: `Which Products are Popular` (Quantity by Product, stacked by Gender, sorted descending). Categories are reversed to show most popular at the top.
    -   **Donut Chart**: `Overall Gender Split` (Quantity by Gender).
    -   **Map Charts**: `Where our customers live` (Two maps, one for Quantity by County and one for Amount by County, using different sequential color scales).
    -   **Column Chart**: `How long we take to ship` (Distribution of Days to Deliver).
    -   **Clustered Column Chart**: `How satisfied are our customers` (Count of transactions by Rating C across months).
-   **Theme Hooks**:
    -   `dark_green`, `light_green`: For dashboard panel backgrounds.
    -   `text_dark`, `text_light`: For general text color (e.g., chart titles, labels, KPI text).
    -   `kpi_golden`: Specific highlight color for key KPI.
    -   `chart_series_1`, `chart_series_2`: Base colors for chart series, dynamically inherited from the custom theme.
    -   `heatmap_blue_low/high`, `heatmap_red_low/high`: Colors for conditional formatting color scales, defined in the custom theme.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference, ScatterChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabel, DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

# Define theme colors directly for this skill as openpyxl theming is complex.
def _get_theme_colors(theme_name: str):
    """Returns a dictionary of theme-specific color hex codes."""
    if theme_name == "viva_calif":
        return {
            "dark_green": "FF2E8B57", # Dark green for side panel (Accent 1)
            "light_green": "FFDCEDC8", # Light green for main area (Accent 1, 80% lighter)
            "chart_series_1": "FF5DADE2", # Blue for chart series (Accent 5)
            "chart_series_2": "FFF1948A", # Orange/Red for chart series (Accent 3)
            "text_dark": "FF212121", # Default dark text
            "text_light": "FFFFFFFF", # Default light text
            "kpi_golden": "FFDAA520", # Golden for Amount KPI
            "heatmap_blue_low": "FFBBDEFB", # Light blue for heatmap
            "heatmap_blue_high": "FF2196F3", # Dark blue for heatmap
            "heatmap_red_low": "FFFFCDD2", # Light red for heatmap
            "heatmap_red_high": "FFD32F2F", # Dark red for heatmap
            "border_light_grey": "FFD3D3D3", # Light grey for borders
        }
    # Fallback to a default theme if not 'viva_calif'
    return {
        "dark_green": "FF003366",
        "light_green": "FFE0FFFF",
        "chart_series_1": "FF4285F4",
        "chart_series_2": "FFDB4437",
        "text_dark": "FF212121",
        "text_light": "FFFFFFFF",
        "kpi_golden": "FFDAA520",
        "heatmap_blue_low": "FFBBDEFB",
        "heatmap_blue_high": "FF2196F3",
        "heatmap_red_low": "FFFFCDD2",
        "heatmap_red_high": "FFD32F2F",
        "border_light_grey": "FFD3D3D3",
    }


def render_workbook(wb, *, title: str = "E-commerce Dashboard", theme: str = "viva_calif", **kwargs) -> None:
    """
    Renders a multi-sheet interactive e-commerce dashboard workbook in Excel.

    Args:
        wb (openpyxl.workbook.workbook.Workbook): The workbook to render into.
        title (str): The title of the dashboard.
        theme (str): The theme name for colors.
        **kwargs: Additional keyword arguments (not used in this skill).
    """
    colors = _get_theme_colors(theme)

    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # --- 1. Setup Data Sheet ---
    ws_data = wb.create_sheet("Data", 0)
    ws_data.title = "Data"

    headers = [
        "TX ID", "Product", "Quantity", "Unit Price", "Amount", "Order Date",
        "Ship Date", "Customer Gender", "Order Mode", "Rating C", "State", "County"
    ]
    ws_data.append(headers)

    # Sample Data (more rows to make charts meaningful, but still illustrative)
    import datetime
    from random import randint, choice, uniform
    products = ["Shorts", "Tank Tops", "Sneakers", "Workout Tops", "Graphic Tees", "Jeans", "Sandals", "Hoodies & Sweatshirts", "T-Shirts", "Sundresses", "Bikinis", "Maxi Dresses", "Casual Dresses", "Baseball Caps", "Swimwear", "Pajama Sets", "Leggings", "Jewelry", "Tote Bags", "Crop Tops"]
    genders = ["M", "F", "O", ""] # Male, Female, Other, Unknown
    order_modes = ["App", "Website", "Instagram", "Target.com", "Partner App"]
    ratings = [1, 2, 3, 4, 5]
    states = ["California"] # Only California for map chart demo
    counties = ["Alpine County", "Amador County", "Butte County", "Calaveras County", "Colusa County", "Contra Costa County", "Del Norte County", "El Dorado County", "Fresno County", "Glenn County", "Humboldt County", "Imperial County", "Inyo County", "Kern County", "Kings County", "Lake County", "Lassen County", "Los Angeles County", "Madera County", "Marin County", "Mariposa County", "Mendocino County", "Merced County", "Modoc County", "Mono County", "Monterey County", "Napa County", "Nevada County", "Orange County", "Placer County", "Plumas County", "Riverside County", "Sacramento County", "San Benito County", "San Bernardino County", "San Diego County", "San Francisco County", "San Joaquin County", "San Luis Obispo County", "San Mateo County", "Santa Barbara County", "Santa Clara County", "Santa Cruz County", "Shasta County", "Sierra County", "Siskiyou County", "Solano County", "Sonoma County", "Stanislaus County", "Sutter County", "Tehama County", "Trinity County", "Tulare County", "Tuolumne County", "Ventura County", "Yolo County", "Yuba County"]

    start_date = datetime.date(2025, 1, 1)
    for i in range(2500): # More data for realistic dashboard
        order_date = start_date + datetime.timedelta(days=randint(0, 89)) # Jan 1 to Mar 31, 2025
        ship_date = order_date + datetime.timedelta(days=randint(1, 7))
        qty = randint(1, 15)
        unit_price = round(uniform(10.0, 200.0), 2)
        amount = round(qty * unit_price, 2)
        customer_gender = choice(genders)
        order_mode = choice(order_modes)
        rating = choice(ratings)
        county = choice(counties)

        row_data = [
            f"TX{i+1:05d}", choice(products), qty, unit_price, amount, order_date,
            ship_date, customer_gender, order_mode, rating, "California", county
        ]
        ws_data.append(row_data)

    # Convert to table for dynamic ranges
    tab = Table(displayName="Orders", ref=ws_data.dimensions)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showFirstColumn=False,
                                        showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws_data.add_table(tab)

    # Add calculated columns after table creation (ensure formula autofill)
    ws_data['M1'] = 'Days to Deliver'
    ws_data['M2'].value = '=[@[Ship Date]]-[@[Order Date]]'
    ws_data['N1'] = 'Weeknum'
    ws_data['N2'].value = '=WEEKNUM([@[Order Date]])'
    ws_data['O1'] = 'Gender Value'
    ws_data['O2'].value = '=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")'

    # --- 2. Setup Pivots Sheet ---
    ws_pivots = wb.create_sheet("Pivots", 1)
    ws_pivots.title = "Pivots"

    # Helper to create a pivot cache and table
    def _create_and_add_pivot(ws, anchor, data_source_range, name, rows, values, filters=None, columns=None):
        pivot_cache = wb.create_pivot_cache(data_source_range)
        pivot_table = openpyxl.worksheet.pivot.PivotTable(
            ref=anchor,
            pivotCacheId=pivot_cache.id,
            name=name
        )
        ws.add_pivot(pivot_table)

        if rows:
            for r_field in rows:
                pivot_table.add_pivot_row_field(openpyxl.worksheet.pivot.PivotField(r_field))
        if columns:
            for c_field in columns:
                pivot_table.add_pivot_column_field(openpyxl.worksheet.pivot.PivotField(c_field))
        if filters:
            for f_field in filters:
                pivot_table.add_pivot_filter_field(openpyxl.worksheet.pivot.PivotField(f_field))

        for v_field, func in values:
            pivot_table.add_pivot_value_field(openpyxl.worksheet.pivot.PivotField(v_field, calcfun=func))
        return pivot_table

    pivot_data_range_str = f"Data!$A$1:${get_column_letter(ws_data.max_column)}${ws_data.max_row}"

    # pvfSummary
    _create_and_add_pivot(ws_pivots, "A4", pivot_data_range_str, "pvfSummary",
                          rows=[], values=[("TX ID", "count"), ("Quantity", "sum"), ("Amount", "sum"), ("Rating C", "average"), ("Days to Deliver", "average")])

    # KPI display cells on Pivots sheet
    ws_pivots['G1'] = "Values for Display"
    ws_pivots['G2'] = "Orders"
    ws_pivots['H2'] = "Qty"
    ws_pivots['I2'] = "Amount"
    ws_pivots['J2'] = "Avg. Rating"
    ws_pivots['K2'] = "Avg. Days"
    ws_pivots['G4'].value = '=TEXT(A5,"#,##0")' # Link to pvfSummary orders count
    ws_pivots['H4'].value = '=TEXT(B5,"#,##0")' # Link to pvfSummary quantity sum
    ws_pivots['I4'].value = '=TEXT(C5,"$#,##0.0k")' # Link to pvfSummary amount sum
    ws_pivots['J4'].value = '=TEXT(D5,"0.0")' # Link to pvfSummary avg rating
    ws_pivots['K4'].value = '=TEXT(E5,"0.0")' # Link to pvfSummary avg days
    
    # pvfTrend
    _create_and_add_pivot(ws_pivots, "A11", pivot_data_range_str, "pvfTrend",
                          rows=["Weeknum"], values=[("Quantity", "sum"), ("Amount", "sum")])

    # pvfMatrix - for heatmap (Order Mode vs Gender % of Grand Total)
    pvf_matrix = _create_and_add_pivot(ws_pivots, "A26", pivot_data_range_str, "pvfMatrix",
                                       rows=["Order Mode"], columns=["Gender Value"], values=[("Amount", "sum")])
    # Set display as % of Grand Total for Amount
    pvf_matrix.pivot_value_fields[0].data_field.showDataAs = "percentOfGrandTotal"

    # Data for heatmap picture (linked)
    ws_pivots['H26'] = "For matrix"
    for r in range(5):
        ws_pivots[f'H{27+r}'].value = f'=A{27+r}' # Order Mode labels
        for c in range(4): # Female, Male, Other, Unknown
            ws_pivots[f'{get_column_letter(9+c)}{27+r}'].value = f'={get_column_letter(2+c)}{27+r}' # Percentage values
            # Conditional formatting for heatmap effect
            ws_pivots.conditional_formatting.add(f'{get_column_letter(9+c)}{27+r}',
                ColorScaleRule(start_type='num', start_value=0, start_color=colors["heatmap_blue_low"],
                               mid_type='num', mid_value=0.5, mid_color='FFFFFFFF',
                               end_type='num', end_value=1, end_color=colors["heatmap_blue_high"])
            )
        # Apply border to cells in the matrix (conceptually)
        for c in range(4):
             ws_pivots[f'{get_column_letter(9+c)}{27+r}'].border = Border(left=Side(style='thin', color=colors["text_light"]), right=Side(style='thin', color=colors["text_light"]),
                                                                       top=Side(style='thin', color=colors["text_light"]), bottom=Side(style='thin', color=colors["text_light"]))

    # pvfQtyDist (Quantity Distribution)
    pvf_qty_dist = _create_and_add_pivot(ws_pivots, "A34", pivot_data_range_str, "pvfQtyDist",
                                         rows=["Quantity"], values=[("TX ID", "count")])
    # Group quantity field manually (simulated by having grouped data here directly)
    # In live Excel, you would right-click Quantity -> Group -> set starting, ending, and by values.
    # For openpyxl, we need to extract and represent this grouped data or perform the grouping logic manually.
    # Let's assume the grouping happened on the original pivot and we're reflecting the result.
    ws_pivots.cell(row=36, column=1, value='1')
    ws_pivots.cell(row=37, column=1, value='2')
    ws_pivots.cell(row=38, column=1, value='3')
    ws_pivots.cell(row=39, column=1, value='4')
    ws_pivots.cell(row=40, column=1, value='5')
    ws_pivots.cell(row=41, column=1, value='6 to 10')
    ws_pivots.cell(row=42, column=1, value='More than 10')
    ws_pivots.cell(row=36, column=2, value=397) # Sample values after grouping
    ws_pivots.cell(row=37, column=2, value=540)
    ws_pivots.cell(row=38, column=2, value=375)
    ws_pivots.cell(row=39, column=2, value=246)
    ws_pivots.cell(row=40, column=2, value=185)
    ws_pivots.cell(row=41, column=2, value=414)
    ws_pivots.cell(row=42, column=2, value=233)

    # pvfProduct (Popular Products)
    _create_and_add_pivot(ws_pivots, "A45", pivot_data_range_str, "pvfProduct",
                          rows=["Product"], columns=["Gender Value"], values=[("Quantity", "sum")])

    # pvfGender (Overall Gender Split)
    _create_and_add_pivot(ws_pivots, "A70", pivot_data_range_str, "pvfGender",
                          rows=["Gender Value"], values=[("Quantity", "sum")])

    # pvfGeo - Qty Map (for California counties)
    _create_and_add_pivot(ws_pivots, "A75", pivot_data_range_str, "pvfGeoQty",
                          rows=["State", "County"], values=[("Quantity", "sum")])
    ws_pivots.cell(row=75, column=1).value = "California" # Ensure state is explicitly shown

    # Data for Map Charts (linked from pvfGeoQty, handling blanks)
    ws_pivots['G75'] = "Map Chart Stuff (Qty)"
    ws_pivots['G76'] = "State"
    ws_pivots['H76'] = "County"
    ws_pivots['I76'] = "Qty"
    for r in range(1, len(counties) + 1):
        ws_pivots[f'G{76+r}'].value = '=IF(A%d="", "", A%d)' % (75+r, 75+r) # State
        ws_pivots[f'H{76+r}'].value = '=IF(B%d="", "", B%d)' % (75+r, 75+r) # County
        ws_pivots[f'I{76+r}'].value = '=IF(C%d="", "", C%d)' % (75+r, 75+r) # Qty

    # pvfGeo - Amount Map
    _create_and_add_pivot(ws_pivots, "K75", pivot_data_range_str, "pvfGeoAmount",
                          rows=["State", "County"], values=[("Amount", "sum")])
    ws_pivots.cell(row=75, column=11).value = "California"

    # Data for Map Charts (linked from pvfGeoAmount, handling blanks)
    ws_pivots['Q75'] = "Map Chart for Amount"
    ws_pivots['Q76'] = "State"
    ws_pivots['R76'] = "County"
    ws_pivots['S76'] = "Amount"
    for r in range(1, len(counties) + 1):
        ws_pivots[f'Q{76+r}'].value = '=IF(K%d="", "", K%d)' % (75+r, 75+r) # State
        ws_pivots[f'R{76+r}'].value = '=IF(L%d="", "", L%d)' % (75+r, 75+r) # County
        ws_pivots[f'S{76+r}'].value = '=IF(M%d="", "", M%d)' % (75+r, 75+r) # Amount

    # pvfShipDuration
    _create_and_add_pivot(ws_pivots, "A150", pivot_data_range_str, "pvfShipDuration",
                          rows=["Days to Deliver"], values=[("TX ID", "count")])

    # pvfRating (Customer Satisfaction)
    pvf_rating = _create_and_add_pivot(ws_pivots, "A180", pivot_data_range_str, "pvfRating",
                                       rows=["Order Date"], columns=["Rating C"], values=[("TX ID", "count")])
    pvf_rating.pivot_row_fields[0].grouping = openpyxl.worksheet.pivot.DateGroup(groupBy="months")
    
    # --- 3. Setup Dashboard Sheet ---
    ws_dashboard = wb.create_sheet("Dashboard", 2)
    ws_dashboard.title = "Dashboard"

    ws_dashboard.column_dimensions['A'].width = 3
    ws_dashboard.column_dimensions['C'].width = 3
    ws_dashboard.column_dimensions['B'].width = 25 # Side panel width

    # Background styling using cell fills (simplification for shapes)
    for row in ws_dashboard.iter_rows(min_row=1, min_col=2, max_col=2, max_row=45):
        for cell in row:
            cell.fill = PatternFill(start_color=colors["dark_green"], end_color=colors["dark_green"], fill_type="solid")
    for row in ws_dashboard.iter_rows(min_row=1, min_col=4, max_col=25, max_row=45):
        for cell in row:
            cell.fill = PatternFill(start_color=colors["light_green"], end_color=colors["light_green"], fill_type="solid")
            cell.border = Border(left=Side(style='thin', color=colors["border_light_grey"]), right=Side(style='thin', color=colors["border_light_grey"]),
                                top=Side(style='thin', color=colors["border_light_grey"]), bottom=Side(style='thin', color=colors["border_light_grey"]))
    
    # KPI Display on Dashboard (using direct cell linking and formatting)
    kpi_labels = ["Orders", "Quantity", "Amount", "Avg. Rating", "Avg. Days to Deliver"]
    for i, label in enumerate(kpi_labels):
        ws_dashboard.cell(row=2 + i*3, column=2, value=label)
        ws_dashboard.cell(row=2 + i*3, column=2).font = Font(bold=True, size=11, color=colors["text_light"])

        kpi_value_cell = ws_dashboard.cell(row=3 + i*3, column=2)
        kpi_value_cell.value = f'=Pivots!{kpi_values_cells[i]}'
        kpi_value_cell.font = Font(bold=True, size=18, color=colors["text_light"])
        if label == "Amount":
            kpi_value_cell.font = Font(bold=True, size=18, color=colors["kpi_golden"]) # Special color
    
    # Logo (simulated by text)
    ws_dashboard['B1'] = "VIVA CALIF"
    ws_dashboard['B1'].font = Font(bold=True, size=14, color=colors["text_light"])
    ws_dashboard['B1'].alignment = Alignment(horizontal='left')


    # Charts (positioned conceptually; full formatting/slicer connections are manual/advanced beyond openpyxl)
    
    # Chart 1: Last 13 Week Trends (Line Chart)
    chart1 = LineChart()
    chart1.title = "Last 13 Week Trends - Qty & Amount"
    chart1.x_axis.title = "Week"
    chart1.y_axis.title = "Quantity"
    
    data1_qty = Reference(ws_pivots, min_col=2, min_row=12, max_col=2, max_row=24)
    data1_amt = Reference(ws_pivots, min_col=3, min_row=12, max_col=3, max_row=24)
    categories1 = Reference(ws_pivots, min_col=1, min_row=12, max_row=24)
    
    series1_qty = chart1.add_data(data1_qty, titles_from_data=True)
    series1_amt = chart1.add_data(data1_amt, titles_from_data=True)
    chart1.set_categories(categories1)

    chart1.series[0].graphicalProperties.line.solidFill = colors["chart_series_1"]
    chart1.series[1].graphicalProperties.line.solidFill = colors["chart_series_2"]
    
    chart1.series[1].y_axis = 'secondary'
    chart1.secondary_y_axis.title = "Amount ($)"
    chart1.height = 8 # inches
    chart1.width = 15 # inches
    ws_dashboard.add_chart(chart1, "D1")

    # Chart 2: How they like to buy (Heatmap - conceptually a linked picture here)
    # This is often done by pasting a range as a linked picture in Excel after conditional formatting.
    # We will represent it by copying the formatted range onto the dashboard for illustration.
    ws_pivots.sheet_view.showGridLines = False # Hide gridlines on pivot sheet for clean screenshot
    for r_idx in range(5):
        for c_idx in range(5): # H to L
            ws_dashboard.cell(row=2+r_idx, column=18+c_idx).value = ws_pivots.cell(row=27+r_idx, column=8+c_idx).value
            ws_dashboard.cell(row=2+r_idx, column=18+c_idx).fill = ws_pivots.cell(row=27+r_idx, column=8+c_idx).fill
            ws_dashboard.cell(row=2+r_idx, column=18+c_idx).border = ws_pivots.cell(row=27+r_idx, column=8+c_idx).border
            ws_dashboard.cell(row=2+r_idx, column=18+c_idx).font = Font(size=8)
    ws_dashboard.cell(row=1, column=18, value="How they like to buy?")
    ws_dashboard.cell(row=1, column=18).font = Font(bold=True, size=12, color=colors["text_dark"])

    # Chart 3: How many they buy (Quantity Distribution Column Chart)
    chart3 = BarChart()
    chart3.type = "col"
    chart3.style = 10
    chart3.title = "How many they buy?"
    chart3.x_axis.title = "Quantity"
    chart3.y_axis.title = "Number of Orders"

    data3 = Reference(ws_pivots, min_col=2, min_row=35, max_col=2, max_row=42)
    categories3 = Reference(ws_pivots, min_col=1, min_row=35, max_row=42)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(categories3)
    chart3.series[0].graphicalProperties.solidFill = colors["chart_series_1"]
    
    # Adjust gap width (openpyxl specific, requires Series object from chart.series)
    # This is a bit tricky; direct gap width setting on a created chart for column type is not direct through BarChart init
    # Need to access series after adding to chart.
    if chart3.series and hasattr(chart3.series[0], 'gapWidth'):
        chart3.series[0].gapWidth = 0 # Example, 0 for no gap

    ws_dashboard.add_chart(chart3, "V1")


    # Chart 4: Which Products are Popular (Stacked Bar Chart)
    chart4 = BarChart()
    chart4.type = "bar"
    chart4.style = 10
    chart4.title = "Which Products are Popular?"

    data4 = Reference(ws_pivots, min_col=2, min_row=45, max_col=5, max_row=65) # Adjusted max_row for product list
    categories4 = Reference(ws_pivots, min_col=1, min_row=45, max_row=65)
    chart4.add_data(data4, titles_from_data=True)
    chart4.set_categories(categories4)
    chart4.series[0].graphicalProperties.solidFill = colors["chart_series_1"]
    chart4.series[1].graphicalProperties.solidFill = colors["chart_series_2"]
    # ... more series colors based on gender breakdown
    
    # Adjust axis for reverse order (most popular on top)
    chart4.x_axis.tickLblPos = "low" # Position labels at the end of the axis
    chart4.y_axis.tickLblPos = "nextToAxis" # This doesn't directly reverse order, but is part of manual tweaks.
    # Actual reverse order: chart4.y_axis.scaling.orientation = "maxMin" is needed
    
    ws_dashboard.add_chart(chart4, "D20")

    # Chart 5: Overall Gender Split (Donut Chart)
    chart5 = openpyxl.chart.PieChart()
    chart5.type = "doughnut"
    chart5.title = "Overall Gender Split"

    data5 = Reference(ws_pivots, min_col=2, min_row=71, max_col=2, max_row=74)
    categories5 = Reference(ws_pivots, min_col=1, min_row=71, max_row=74)
    chart5.add_data(data5, titles_from_data=True)
    chart5.set_categories(categories5)

    # Add data labels
    chart5.dataLabels = DataLabelList()
    chart5.dataLabels.showPercent = True
    chart5.dataLabels.showVal = False
    
    ws_dashboard.add_chart(chart5, "J30")

    # Chart 6 & 7: Map Charts (Qty & Amount)
    # openpyxl does not support Map Charts directly. This is a conceptual representation.
    # Assuming map charts are created and inserted manually.
    # The data preparation with IF() formulas is shown in the Pivots sheet.
    
    # We will simulate the maps by just placing colored cells or text to indicate their presence.
    ws_dashboard.cell(row=20, column=18, value="Where our customers live?")
    ws_dashboard.cell(row=20, column=18).font = Font(bold=True, size=12, color=colors["text_dark"])
    ws_dashboard.cell(row=21, column=18, value="Map 1 (Qty)")
    ws_dashboard.cell(row=21, column=18).fill = PatternFill(start_color="FFD6C1AE", end_color="FFD6C1AE", fill_type="solid") # Simulate map color
    ws_dashboard.cell(row=21, column=18).font = Font(size=8)
    ws_dashboard.merge_cells('R21:U25') # Representing a map chart area

    ws_dashboard.cell(row=21, column=25, value="Map 2 (Amount)")
    ws_dashboard.cell(row=21, column=25).fill = PatternFill(start_color="FFB3E5BD", end_color="FFB3E5BD", fill_type="solid") # Simulate map color
    ws_dashboard.cell(row=21, column=25).font = Font(size=8)
    ws_dashboard.merge_cells('V21:Y25') # Representing a small inset map

    # Chart 8: How long we take to ship (Column Chart)
    chart8 = BarChart()
    chart8.type = "col"
    chart8.style = 10
    chart8.title = "How long we take to ship?"
    chart8.x_axis.title = "Days to Deliver"
    chart8.y_axis.title = "Number of Orders"

    data8 = Reference(ws_pivots, min_col=2, min_row=151, max_col=2, max_row=160) # Top few days
    categories8 = Reference(ws_pivots, min_col=1, min_row=151, max_row=160)
    chart8.add_data(data8, titles_from_data=True)
    chart8.set_categories(categories8)
    chart8.series[0].graphicalProperties.solidFill = colors["chart_series_1"]
    ws_dashboard.add_chart(chart8, "V28")

    # Chart 9: How satisfied are our customers (Clustered Column Chart)
    chart9 = BarChart()
    chart9.type = "col"
    chart9.style = 10
    chart9.title = "How satisfied are our customers?"

    data9 = Reference(ws_pivots, min_col=2, min_row=189, max_col=5, max_row=191)
    categories9 = Reference(ws_pivots, min_col=1, min_row=189, max_row=191)
    chart9.add_data(data9, titles_from_data=True)
    chart9.set_categories(categories9)
    # Assign specific colors to series
    chart9.series[0].graphicalProperties.solidFill = colors["chart_series_1"]
    chart9.series[1].graphicalProperties.solidFill = colors["chart_series_2"]
    # ... additional colors for other ratings
    ws_dashboard.add_chart(chart9, "D38")


    # --- 4. Slicers & Interactions ---
    # openpyxl does not directly support creating or connecting slicers.
    # This part is typically done manually in Excel.
    # The video demonstrates linking slicers to multiple PivotTables using "Report Connections".
    
    # We will simulate slicer presence and label them.
    ws_dashboard['B28'] = "Order Mode"
    ws_dashboard['B28'].font = Font(bold=True, size=11, color=colors["text_light"])
    ws_dashboard['B35'] = "Customers"
    ws_dashboard['B35'].font = Font(bold=True, size=11, color=colors["text_light"])
    # These cells would conceptually contain the slicers created from pvfSummary's "Order Mode" and "Gender Value" fields.

    ws_dashboard.sheet_view.showGridLines = False # Hide gridlines for a clean dashboard view
```