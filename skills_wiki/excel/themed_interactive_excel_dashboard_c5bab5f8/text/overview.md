### 1. High-level Skill Pattern Extraction

> **Skill Name**: Themed Interactive Excel Dashboard

*   **Tier**: archetype
*   **Core Mechanism**: This skill demonstrates the end-to-end creation of a fully interactive and dynamically updating Excel dashboard. It integrates various Excel features including structured data tables, calculated columns, multiple pivot tables for data aggregation, dynamic KPI display using `TEXT()` functions linked to pivot outputs, diverse chart types for visual analysis, slicers for interactivity, and custom theme colors for consistent branding. A notable technique is the "Paste as Linked Picture" for heatmaps, which allows advanced conditional formatting from a helper sheet to be dynamically displayed on the dashboard.
*   **Applicability**: This approach is ideal for individuals or small businesses needing powerful, interactive data visualization and reporting without investing in complex Business Intelligence software. It is particularly well-suited for summarizing key business metrics, identifying trends, analyzing customer behavior, and presenting geographical data breakdowns. The dynamic nature ensures the dashboard updates automatically with new data, reducing manual effort.

### 2. Structural Breakdown

-   **Data Layout**:
    -   `Data` sheet: Stores raw transactional data as an Excel Table. Contains columns for `TX ID`, `Product`, `Quantity`, `Unit Price`, `Amount`, `Order Date`, `Ship Date`, `Customer Gender` (single-letter codes), `Order Mode`, `Rating C`, `State`, `County`.
    -   Calculated columns added to the `Data` table: `Days to Deliver` (calculated from `Ship Date` - `Order Date`), `Weeknum` (using `WEEKNUM()` on `Order Date`), `Gender Value` (using `IFS()` to expand single-letter gender codes to full words like "Male", "Female", "Other", "Unknown" for better slicer/chart labels).
    -   `Pivots` sheet: A dedicated sheet containing multiple pivot tables, each configured to calculate specific KPIs or aggregations needed for the dashboard's charts and summary. These are given descriptive names (e.g., `pvtSummary`, `pvtTrends`, `pvtProduct`).
    -   `Questions & KPIs` sheet: A simple reference sheet listing the key performance indicators (KPIs) and business questions the dashboard aims to answer.
    -   `Matrix` sheet (or part of `Pivots`): A helper area where data for the heatmap chart is prepared by linking to a pivot table and applying conditional formatting.
    -   `Dashboard` sheet: The final presentation layer, composed of shapes, linked text boxes, charts, and slicers.

-   **Formula Logic**:
    -   **Dynamic KPI Display on Dashboard**: `TEXT()` function is used to link to pivot table aggregated values and apply specific number formats. Examples:
        -   `=TEXT(Pivots!A4,"#,##0")` for formatting large integers with comma separators.
        -   `=TEXT(Pivots!C4,"$#,##0,.0k")` for formatting currency values to thousands with a dollar sign.
        -   `=TEXT(Pivots!D4,"0.0")` for formatting decimal numbers to one decimal place.
    -   **Heatmap Data Preparation**: `IF(cell_reference="", "", cell_reference)` is used in the `Matrix` sheet to prevent `#VALUE!` or `0` errors when pivot table cells are blank due to filtering, ensuring map charts display correctly.

-   **Visual Design**:
    -   **Dashboard Structure**: Utilizes two large `Rectangle` shapes for the dashboard background: a narrow, dark green left panel and a wider, light green main content area, both with drop shadows.
    -   **KPI Panel Styling**: Text boxes on the left panel are linked to KPI display formulas, formatted with a bold font, larger size, gradient text fill (white to a light grey/silver), and drop shadow for visual depth. Emojis are used for quick identification of each KPI.
    -   **Chart Backgrounds**: Each chart on the main dashboard area is placed on top of a simple white `Rectangle` shape to give it a clean, modular appearance and visual separation.
    -   **Color Consistency**: A custom theme color palette (`VivaCalif`) is defined and applied via `Page Layout > Colors > Customize Colors`, ensuring all charts, shapes, and conditional formatting automatically align with the corporate branding.
    -   **Heatmap Highlighting**: Conditional formatting (diverging color scale, e.g., blue-white-red) is applied to the percentage values in the `Matrix` sheet, with thick white cell borders for clarity.

-   **Charts/Tables**:
    -   **Pivot Tables**: Used extensively for aggregation, grouping, and initial calculations. Naming pivots via `PivotTable Analyze > PivotTable Name` simplifies linking and management for slicers.
    -   **Line Chart**: Visualizes trends over time (e.g., "Last 13 Week Trends") with two series (Quantity, Amount) and a secondary axis to handle different scales.
    -   **Column Charts**: Used for distributions (e.g., "How many they buy?"), shipment durations, and customer satisfaction ratings, often with customized grouping of categories.
    -   **Stacked Bar Chart**: Displays product popularity broken down by gender. Categories are reversed for intuitive high-to-low reading.
    -   **Donut Chart**: Represents overall gender split for purchased quantities.
    -   **Map Charts**: Visualizes geographical distribution of quantity and amount for California counties. These are generated from dedicated ranges that mirror pivot table outputs (not directly from pivots) and are styled with custom sequential color scales (e.g., orange for quantity, green for amount) and solid line borders between counties.
    -   **Slicers**: Interactive filters (e.g., "Order Mode", "Gender Value") are inserted and connected to multiple pivot tables/charts via `Report Connections` (`Right-click slicer > Report Connections`), enabling dynamic filtering across the dashboard.
    -   **Linked Picture for Heatmap**: The conditionally formatted `Matrix` sheet data is copied and "Paste Special > As Linked Picture" onto the dashboard. This creates a dynamic image that updates when the underlying data or formatting changes.

-   **Theme Hooks**:
    -   `header_bg`: Used for the background color of the left dashboard panel.
    -   `background_light_1`: Used for the background color of the main dashboard area.
    -   `accent1` to `accent6`: These define the primary colors used across chart series, conditional formatting rules (e.g., heatmap divergence, map fill colors), and other visual elements, ensuring brand consistency.
    -   `text_light_1`, `text_dark_1`: Used for dynamic text elements and chart titles, adapting to background contrast.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import Picture
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime

# Assuming _helpers.py is available with get_theme_colors, apply_fill, apply_font helpers
# For this example, I'll simulate relevant parts of _helpers
class ThemeColors:
    def __init__(self, theme_name):
        # Simplified for demonstration based on video's greens and blues/reds
        if theme_name == "VivaCalif":
            self.header_bg = "FF27562D" # Dark Green
            self.background_light_1 = "FFDCF3DC" # Light Green
            self.text_dark_1 = "FF1C2023" # Almost Black
            self.text_light_1 = "FFFFFFFF" # White
            self.accent1 = "FF4F81BD" # Blue
            self.accent2 = "FFC0504D" # Red
            self.accent3 = "FF9BBB59" # Olive Green
            self.accent4 = "FF8064A2" # Purple
            self.accent5 = "FF4BACC6" # Teal
            self.accent6 = "FFF79646" # Orange
            self.diverging_low = "FF6D9EEB" # Light Blue for heatmap
            self.diverging_high = "FFDC635F" # Light Red for heatmap
        else: # Default corporate_blue
            self.header_bg = "FF2C3E50"
            self.background_light_1 = "FFEBF1F7"
            self.text_dark_1 = "FF1C2023"
            self.text_light_1 = "FFFFFFFF"
            self.accent1 = "FF4F81BD"
            self.accent2 = "FFC0504D"
            self.accent3 = "FF9BBB59"
            self.accent4 = "FF8064A2"
            self.accent5 = "FF4BACC6"
            self.accent6 = "FFF79646"
            self.diverging_low = "FF6D9EEB"
            self.diverging_high = "FFDC635F"

def apply_fill(cell, color_hex):
    cell.fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def apply_font(cell, color_hex, bold=False, size=11, name="Aptos Narrow"):
    cell.font = Font(color=color_hex, bold=bold, size=size, name=name)

def _setup_theme(theme_name):
    return ThemeColors(theme_name)

def render_workbook(wb, *, title: str = "E-commerce Dashboard", theme: str = "VivaCalif", **kwargs) -> None:
    colors = _setup_theme(theme)

    # --- 1. Data Sheet Setup ---
    ws_data = wb.create_sheet("Data")
    # Simulate data - in a real scenario, this would be loaded from a source
    header = ["TX ID", "Product", "Quantity", "Unit Price", "Amount", "Order Date", "Ship Date", "Customer Gender", "Order Mode", "Rating C", "State", "County", "Days to Deliver", "Weeknum", "Gender Value"]
    ws_data.append(header)
    
    # Sample data for 3 months (Jan-Mar 2025)
    products = ["Shorts", "Tank Tops", "Sweatshirts", "Jeans", "T-Shirts", "Sandals", "Bikinis", "Graphic Tees"]
    order_modes = ["App", "Website", "Instagram", "Target.com", "Partner App"]
    genders = ["M", "F", "O", ""] # Male, Female, Other, Unknown
    states = ["California"]
    counties = ["Los Angeles County", "San Diego County", "Orange County", "Alameda County", "Sacramento County", "San Bernardino County", "Fresno County", "Santa Clara County"]
    ratings = [1, 2, 3, 4, 5]

    for i in range(2400): # Simulating 2400 orders
        tx_id = f"TX{i+1:05d}"
        product = products[i % len(products)]
        quantity = (i % 5) + 1
        unit_price = round(10 + (i / 100), 2)
        amount = round(quantity * unit_price, 2)
        order_date = datetime(2025, 1 + (i % 3), 1 + (i % 28))
        ship_date = datetime(2025, 1 + (i % 3), 1 + (i % 28)) # Same day for simplicity, real data would vary
        if i % 10 < 3: # 30% of orders shipped next day
            ship_date = datetime(2025, 1 + (i % 3), 1 + (i % 28) + 1)
        customer_gender = genders[i % len(genders)]
        order_mode = order_modes[i % len(order_modes)]
        rating_c = ratings[i % len(ratings)]
        state = states[i % len(states)]
        county = counties[i % len(counties)]
        
        ws_data.append([tx_id, product, quantity, unit_price, amount, order_date, ship_date, customer_gender, order_mode, rating_c, state, county, None, None, None]) # Fill calculated columns later

    # Convert to Excel Table and add calculated columns
    table = Table(displayName="Data", ref=f"A1:{get_column_letter(len(header))}{ws_data.max_row}")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    table.tableStyleInfo = style
    ws_data.add_table(table)

    # Add formulas for calculated columns
    for row_idx in range(2, ws_data.max_row + 1):
        ws_data[f"M{row_idx}"] = f"=[@[Ship Date]]-[@[Order Date]]"
        ws_data[f"N{row_idx}"] = f"=WEEKNUM([@[Order Date]])"
        ws_data[f"O{row_idx}"] = f'=IFS([@[Customer Gender]]="M","Male",[@[Customer Gender]]="F","Female",[@[Customer Gender]]="O","Other",TRUE,"Unknown")'

    # --- 2. Pivots Sheet Setup ---
    ws_pivots = wb.create_sheet("Pivots")
    
    # Function to create a pivot table (simplified)
    def create_pivot(ws_pivots, pivot_name, data_range, row_fields, value_fields, col_fields=None, filter_fields=None):
        pivot_table = openpyxl.worksheet.pivot.PivotTable(
            name=pivot_name,
            table=data_range,
            row_fields=row_fields,
            value_fields=value_fields,
            col_fields=col_fields if col_fields else [],
            filter_fields=filter_fields if filter_fields else []
        )
        # Simplified placement, real implementation needs more precise positioning
        return pivot_table

    # Data range for pivots
    pivot_source_range = f"Data!A1:{get_column_letter(ws_data.max_column)}{ws_data.max_row}"

    # Pivot 1: Summary KPIs
    ws_pivots.cell(row=1, column=1, value="pvtSummary")
    pvt_summary = create_pivot(ws_pivots, "pvtSummary", pivot_source_range, 
                               row_fields=[], 
                               value_fields=[
                                   openpyxl.worksheet.pivot.PivotField(sourceField="TX ID", compact=False, function="count"),
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Quantity", compact=False, function="sum"),
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Amount", compact=False, function="sum"),
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Rating C", compact=False, function="average"),
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Days to Deliver", compact=False, function="average")
                               ],
                               col_fields=[]
                              )
    ws_pivots.add_pivot(pvt_summary, "A2")

    # Pivot 2: Trends
    ws_pivots.cell(row=10, column=1, value="pvtTrends")
    pvt_trends = create_pivot(ws_pivots, "pvtTrends", pivot_source_range, 
                               row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Weeknum")], 
                               value_fields=[
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Quantity", function="sum"),
                                   openpyxl.worksheet.pivot.PivotField(sourceField="Amount", function="sum")
                               ],
                               col_fields=[]
                              )
    ws_pivots.add_pivot(pvt_trends, "A11")

    # Pivot 3: Order Mode vs Gender (for heatmap)
    ws_pivots.cell(row=25, column=1, value="pvtModeGender")
    pvt_mode_gender = create_pivot(ws_pivots, "pvtModeGender", pivot_source_range, 
                                   row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Order Mode")], 
                                   value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Amount", function="sum", showDataAs="pctGrandTotal")],
                                   col_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Gender Value")]
                                  )
    ws_pivots.add_pivot(pvt_mode_gender, "A26")

    # Pivot 4: Quantity Distribution
    ws_pivots.cell(row=35, column=1, value="pvtQtyDist")
    pvt_qty_dist = create_pivot(ws_pivots, "pvtQtyDist", pivot_source_range, 
                                row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Quantity")], 
                                value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="TX ID", function="count")],
                                col_fields=[]
                               )
    ws_pivots.add_pivot(pvt_qty_dist, "A36")
    # Simulate grouping for Quantity (manual action needed in UI or more complex openpyxl for field grouping)
    # E.g. select A37:A41, right-click, Group (1-5), then A42:A46 (6-10), then A47:A80 (>10)
    # Then drag "Quantity2" (new grouped field) to rows and remove original "Quantity"

    # Pivot 5: Popular Products
    ws_pivots.cell(row=50, column=1, value="pvtProducts")
    pvt_products = create_pivot(ws_pivots, "pvtProducts", pivot_source_range, 
                                row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Product")], 
                                value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Quantity", function="sum")],
                                col_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Gender Value")]
                               )
    ws_pivots.add_pivot(pvt_products, "A51")

    # Pivot 6: Overall Gender Split (for donut)
    ws_pivots.cell(row=50, column=10, value="pvtGenderSplit")
    pvt_gender_split = create_pivot(ws_pivots, "pvtGenderSplit", pivot_source_range, 
                                   row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Gender Value")], 
                                   value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Quantity", function="sum")],
                                   col_fields=[]
                                  )
    ws_pivots.add_pivot(pvt_gender_split, "J51")

    # Pivot 7 & 8: Geographical Analysis (for map charts)
    ws_pivots.cell(row=80, column=1, value="pvtGeoQty")
    pvt_geo_qty = create_pivot(ws_pivots, "pvtGeoQty", pivot_source_range,
                               row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="State"), openpyxl.worksheet.pivot.PivotField(sourceField="County")],
                               value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Quantity", function="sum")],
                               col_fields=[]
                              )
    ws_pivots.add_pivot(pvt_geo_qty, "A81")
    # For map charts, data needs to be outside pivot. Simulating linking.
    # Map Chart Stuff (Qty)
    ws_pivots["G81"] = "State"
    ws_pivots["H81"] = "County"
    ws_pivots["I81"] = "Qty"
    for r_idx in range(82, ws_pivots.max_row + 1):
        ws_pivots[f"G{r_idx}"] = f'=IF(Pivots!A{r_idx}="","",Pivots!A{r_idx})' # State
        ws_pivots[f"H{r_idx}"] = f'=IF(Pivots!B{r_idx}="","",Pivots!B{r_idx})' # County
        ws_pivots[f"I{r_idx}"] = f'=IF(Pivots!C{r_idx}=0,"",Pivots!C{r_idx})' # Quantity

    ws_pivots.cell(row=80, column=10, value="pvtGeoAmount")
    pvt_geo_amount = create_pivot(ws_pivots, "pvtGeoAmount", pivot_source_range,
                                  row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="State"), openpyxl.worksxl.pivot.PivotField(sourceField="County")],
                                  value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Amount", function="sum")],
                                  col_fields=[]
                                 )
    ws_pivots.add_pivot(pvt_geo_amount, "J81")
    # Map Chart Stuff (Amount)
    ws_pivots["L81"] = "State"
    ws_pivots["M81"] = "County"
    ws_pivots["N81"] = "Amount"
    for r_idx in range(82, ws_pivots.max_row + 1):
        ws_pivots[f"L{r_idx}"] = f'=IF(Pivots!J{r_idx}="","",Pivots!J{r_idx})' # State
        ws_pivots[f"M{r_idx}"] = f'=IF(Pivots!K{r_idx}="","",Pivots!K{r_idx})' # County
        ws_pivots[f"N{r_idx}"] = f'=IF(Pivots!L{r_idx}=0,"",Pivots!L{r_idx})' # Amount

    # Pivot 9: Shipment Duration
    ws_pivots.cell(row=160, column=1, value="pvtShipDuration")
    pvt_ship_duration = create_pivot(ws_pivots, "pvtShipDuration", pivot_source_range, 
                                     row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Days to Deliver")], 
                                     value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="TX ID", function="count")],
                                     col_fields=[]
                                    )
    ws_pivots.add_pivot(pvt_ship_duration, "A161")

    # Pivot 10: Customer Satisfaction
    ws_pivots.cell(row=185, column=1, value="pvtRating")
    pvt_rating = create_pivot(ws_pivots, "pvtRating", pivot_source_range, 
                              row_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Order Date", compact=False, subtotal=False, groupItem="months")], 
                              value_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="TX ID", function="count")],
                              col_fields=[openpyxl.worksheet.pivot.PivotField(sourceField="Rating C")]
                             )
    ws_pivots.add_pivot(pvt_rating, "A186")
    
    # --- 3. Dashboard Sheet Setup ---
    ws_dash = wb.create_sheet("Dashboard")
    ws_dash.sheet_view.showGridLines = False

    # Set column widths
    ws_dash.column_dimensions['A'].width = 2
    ws_dash.column_dimensions['B'].width = 18
    ws_dash.column_dimensions['C'].width = 2
    for col_idx in range(4, 27): # Columns D to Z
        ws_dash.column_dimensions[get_column_letter(col_idx)].width = 7.5

    # Background rectangles
    rect1 = ws_dash.drawing.add_drawing(openpyxl.drawing.ms.Shape(
        shape_type="rect",
        r_param=openpyxl.drawing.xdr.OneCellAnchor(
            openpyxl.drawing.xdr.From(col=0, colOff=0, row=0, rowOff=0),
            openpyxl.drawing.xdr.To(col=2, colOff=0, row=40, rowOff=0) # Adjust rows as needed
        )
    ))
    rect1.shape.add_text(' ', text_body=None) # Empty text body
    rect1.shape.fill = openpyxl.drawing.ms.SolidColorFill(openpyxl.drawing.colors.ColorChoice(srgbClr=colors.header_bg))
    
    rect2 = ws_dash.drawing.add_drawing(openpyxl.drawing.ms.Shape(
        shape_type="rect",
        r_param=openpyxl.drawing.xdr.OneCellAnchor(
            openpyxl.drawing.xdr.From(col=2, colOff=0, row=0, rowOff=0),
            openpyxl.drawing.xdr.To(col=26, colOff=0, row=40, rowOff=0) # Adjust rows as needed
        )
    ))
    rect2.shape.add_text(' ', text_body=None)
    rect2.shape.fill = openpyxl.drawing.ms.SolidColorFill(openpyxl.drawing.colors.ColorChoice(srgbClr=colors.background_light_1))

    # Simulate KPI display
    ws_dash["B2"] = "VIVA CALIF"
    apply_font(ws_dash["B2"], colors.text_light_1, bold=True, size=24)

    kpi_labels = ["Orders", "Quantity", "Amount", "Avg. Rating", "Avg. Days to Deliver"]
    kpi_cell_refs = ["D4", "B4", "C4", "D4", "E4"] # References to pvtSummary output
    kpi_formats = ["#,##0", "#,##0", "$#,##0,.0k", "0.0", "0.0"]
    kpi_emojis = ["🛒", "👕", "💰", "⭐", "🗓️"]

    row_offset = 5
    for i, label in enumerate(kpi_labels):
        ws_dash.cell(row=row_offset + i * 3, column=2, value=f"{kpi_emojis[i]} {label}")
        apply_font(ws_dash.cell(row=row_offset + i * 3, column=2), colors.text_light_1, bold=True, size=11)
        
        # Linked value
        linked_value_cell = ws_dash.cell(row=row_offset + i * 3 + 1, column=2)
        linked_value_cell.value = f'=TEXT(Pivots!{kpi_cell_refs[i]},"{kpi_formats[i]}")'
        apply_font(linked_value_cell, colors.text_light_1, bold=True, size=18)

    # Add charts and slicers (simplified positioning and styling)
    # A real implementation would place these precisely using anchor points and shape properties
    
    # Simulate chart placement by creating rectangles for background
    def add_chart_background(ws, col, row, width_cols, height_rows):
        start_col = col
        start_row = row
        end_col = col + width_cols - 1
        end_row = row + height_rows - 1

        chart_bg = ws.drawing.add_drawing(openpyxl.drawing.ms.Shape(
            shape_type="rect",
            r_param=openpyxl.drawing.xdr.OneCellAnchor(
                openpyxl.drawing.xdr.From(col=start_col, colOff=0, row=start_row, rowOff=0),
                openpyxl.drawing.xdr.To(col=end_col, colOff=0, row=end_row, rowOff=0)
            )
        ))
        chart_bg.shape.add_text(' ', text_body=None)
        chart_bg.shape.fill = openpyxl.drawing.ms.SolidColorFill(openpyxl.drawing.colors.ColorChoice(srgbClr="FFFFFFFF")) # White background
        chart_bg.shape.line = openpyxl.drawing.ms.NoFillProperties() # No border
        return chart_bg # Return to allow adding charts on top or linking

    chart_positions = {
        "trend": (3, 0, 8, 10),
        "heatmap": (11, 0, 8, 5),
        "qty_dist": (17, 0, 8, 5),
        "products": (3, 10, 8, 10),
        "gender_split": (3, 20, 8, 5),
        "map_qty": (11, 10, 8, 5),
        "map_amount": (17, 10, 8, 5),
        "ship_duration": (11, 20, 8, 5),
        "rating": (17, 20, 8, 5)
    }

    # Creating charts and adding them to the dashboard
    # This part needs manual placement and formatting as openpyxl chart API is complex for exact visual replica
    # The video shows dragging charts created on 'Pivots' sheet to 'Dashboard' sheet

    # Placeholder for actual charts (to be moved and formatted from Pivots sheet)
    # For a real implementation, you would create the charts, cut them from Pivots,
    # and paste them onto the Dashboard sheet, then apply formatting.

    # Slicers - these will be added to the dashboard and connected to pivots
    # Select a pivot table cell (e.g., A2 for pvtSummary)
    # PivotTable Analyze > Insert Slicer > Order Mode, Gender Value
    # Then drag and drop to the dashboard sheet.
    # Connect to relevant pivots via Right-click Slicer > Report Connections.

    # Simulating slicer placement
    slicer_order_mode = ws_dash.drawing.add_drawing(openpyxl.drawing.ms.Shape(
        shape_type="rect",
        r_param=openpyxl.drawing.xdr.OneCellAnchor(
            openpyxl.drawing.xdr.From(col=1, colOff=0, row=22, rowOff=0),
            openpyxl.drawing.xdr.To(col=2, colOff=0, row=30, rowOff=0)
        )
    ))
    slicer_order_mode.shape.add_text("Order Mode\n(Slicer Placeholder)", text_body=None)
    slicer_order_mode.shape.fill = openpyxl.drawing.ms.SolidColorFill(openpyxl.drawing.colors.ColorChoice(srgbClr=colors.accent1))
    slicer_order_mode.shape.line = openpyxl.drawing.ms.NoFillProperties()


    slicer_gender = ws_dash.drawing.add_drawing(openpyxl.drawing.ms.Shape(
        shape_type="rect",
        r_param=openpyxl.drawing.xdr.OneCellAnchor(
            openpyxl.drawing.xdr.From(col=1, colOff=0, row=32, rowOff=0),
            openpyxl.drawing.xdr.To(col=2, colOff=0, row=40, rowOff=0)
        )
    ))
    slicer_gender.shape.add_text("Gender Value\n(Slicer Placeholder)", text_body=None)
    slicer_gender.shape.fill = openpyxl.drawing.ms.SolidColorFill(openpyxl.drawing.colors.ColorChoice(srgbClr=colors.accent1))
    slicer_gender.shape.line = openpyxl.drawing.ms.NoFillProperties()

    # --- 4. Matrix Sheet for Heatmap (conceptual) ---
    # This would typically be a section in the Pivots sheet or a separate sheet
    ws_matrix = wb.create_sheet("Matrix")
    ws_matrix.sheet_view.showGridLines = False

    # Simulate data for heatmap (copy from pvtModeGender and apply conditional formatting)
    # A real implementation would dynamically copy from pvtModeGender
    data_for_heatmap = [
        ["", "Female", "Male", "Other", "Unknown", "Grand Total"],
        ["App", 0.19, 0.123, 0.011, 0.031, 0.355],
        ["Instagram", 0.05, 0.043, 0.002, 0.018, 0.113],
        ["Partner App", 0.063, 0.048, 0.002, 0.004, 0.117],
        ["Target.com", 0.096, 0.068, 0.005, 0.013, 0.182],
        ["Website", 0.125, 0.093, 0.006, 0.012, 0.236],
        ["Grand Total", 0.529, 0.375, 0.026, 0.078, 1.0]
    ]
    for r_idx, row_data in enumerate(data_for_heatmap):
        for c_idx, cell_value in enumerate(row_data):
            ws_matrix.cell(row=r_idx+1, column=c_idx+1, value=cell_value)
            if isinstance(cell_value, (float, int)) and r_idx > 0 and c_idx > 0:
                ws_matrix.cell(row=r_idx+1, column=c_idx+1).number_format = "0.0%"

    # Apply conditional formatting for heatmap
    ws_matrix.conditional_formatting.add('B2:E6', ColorScaleRule(
        start_type='min', start_color=openpyxl.styles.colors.Color(rgb=colors.diverging_low),
        mid_type='percentile', mid_value=50, mid_color=openpyxl.styles.colors.Color(rgb="FFFFFFFF"), # White
        end_type='max', end_color=openpyxl.worksheet.colors.Color(rgb=colors.diverging_high)
    ))
    
    # Add borders for cells in heatmap
    thick_white_border = Border(left=Side(style='thick', color="FFFFFFFF"), 
                                right=Side(style='thick', color="FFFFFFFF"), 
                                top=Side(style='thick', color="FFFFFFFF"), 
                                bottom=Side(style='thick', color="FFFFFFFF"))
    for r in range(2, 7):
        for c in range(2, 6):
            ws_matrix.cell(row=r, column=c).border = thick_white_border

    # The linked picture would be created on the dashboard by copying this range from Matrix
    # and using Paste Special > Linked Picture.
    # E.g., ws_dash.insert_image(Image("path_to_screenshot_of_heatmap_from_matrix_sheet.png"))
    # Or for actual linked picture, it's a specific paste option via Excel UI, not directly in openpyxl.

    # Remove the default sheet created by openpyxl
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

# Helper function to generate dummy data for pivots (simplified)
def generate_pivot_data():
    pass

# Initialize the workbook (for testing purposes)
# wb = openpyxl.Workbook()
# render_workbook(wb, title="My E-commerce Dashboard", theme="VivaCalif")
# wb.save("ecommerce_dashboard.xlsx")
# print("Dashboard created successfully!")
```