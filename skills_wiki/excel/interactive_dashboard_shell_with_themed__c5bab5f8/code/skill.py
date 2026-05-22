import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Helper functions (assumed to be available in a _helpers module or similar)
def get_theme_colors(theme_name: str):
    # This is a placeholder. In a real implementation, this would load actual theme colors.
    # For demonstration, we use hardcoded greens and white/dark grey.
    if theme_name == "VivaCalif":
        return {
            "bg_main": "EEF9EE",  # Light green for main content
            "bg_sidebar": "2B542B",  # Dark green for sidebar
            "text_light": "FFFFFF",
            "text_dark": "2B542B",
            "accent1": "8CD19D",
            "accent2": "4CAF50",
            "accent3": "FF9800",
            "accent4": "F44336",
            "accent5": "2196F3",
            "accent6": "9C27B0",
            # Add more specific color codes as needed from the video's custom theme
            "chart_series1": "E06041",
            "chart_series2": "4B878E",
            "heatmap_blue": "ADD8E6",
            "heatmap_red": "FFCCCB",
            "heatmap_white": "FFFFFF",
            "map_quantity": "FFD700", # Golden for map
            "map_amount": "8FBC8F", # Darker green for map
        }
    else:
        return { # Default corporate blue theme
            "bg_main": "FFFFFF",
            "bg_sidebar": "002060",
            "text_light": "FFFFFF",
            "text_dark": "000000",
            "accent1": "4472C4",
            "accent2": "ED7D31",
            "accent3": "A5A5A5",
            "accent4": "FFC000",
            "accent5": "5B9BD5",
            "accent6": "70AD47",
            "chart_series1": "4472C4",
            "chart_series2": "ED7D31",
            "heatmap_blue": "ADD8E6",
            "heatmap_red": "FFCCCB",
            "heatmap_white": "FFFFFF",
            "map_quantity": "4472C4",
            "map_amount": "ED7D31",
        }

def set_cell_fill(cell, color_hex):
    cell.fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")

def set_cell_font(cell, name, size, bold, color_hex):
    cell.font = Font(name=name, size=size, bold=bold, color=color_hex)

def set_cell_border(cell, style="thin", color_hex="000000"):
    side = Side(border_style=style, color=color_hex)
    cell.border = Border(left=side, right=side, top=side, bottom=side)

def create_shape(ws, shape_type, anchor, width, height, fill_color, border_color=None, shadow=True):
    # This is a simplification. Openpyxl doesn't directly support shapes as in Excel UI.
    # We'll represent shapes as merged cells for the purpose of the sheet shell.
    start_cell_str = anchor
    start_col = openpyxl.utils.column_index_from_string(start_cell_str[:-1])
    start_row = int(start_cell_str[-1])

    end_col = start_col + width - 1
    end_row = start_row + height - 1

    end_cell_str = get_column_letter(end_col) + str(end_row)

    ws.merge_cells(f"{start_cell_str}:{end_cell_str}")
    merged_cell = ws[start_cell_str]

    if fill_color:
        set_cell_fill(merged_cell, fill_color)
    if border_color:
        set_cell_border(merged_cell, color_hex=border_color)

    # For shadowing, we just represent the effect via a slightly darker border or background if possible
    # For true shadow, it's not directly supported by openpyxl for arbitrary shapes.
    # This is a limitation of openpyxl compared to Excel's UI.
    pass


def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", data_table_name: str = "Orders") -> None:
    """
    Renders an interactive dashboard sheet with KPIs, chart placeholders, and slicer placeholders.

    Args:
        wb: The openpyxl workbook object.
        sheet_name: The name for the dashboard sheet.
        title: The title for the dashboard (e.g., "VIVA CALIF").
        theme: The name of the custom color theme to use (e.g., "VivaCalif").
        data_table_name: The name of the Excel Table containing the raw data.
    """
    ws = wb.create_sheet(sheet_name)
    theme_colors = get_theme_colors(theme)

    # --- 1. Sheet Setup and Layout ---
    ws.sheet_view.showGridLines = False

    # Set column widths
    ws.column_dimensions['A'].width = 3  # Narrow column
    ws.column_dimensions['B'].width = 20 # Sidebar width
    ws.column_dimensions['C'].width = 3  # Narrow column
    for col_idx in range(4, 27): # Columns D to Z for main content
        ws.column_dimensions[get_column_letter(col_idx)].width = 12

    # Create background shapes (represented by merged cells for openpyxl)
    # Left sidebar
    create_shape(ws, "rectangle", "A1", width=3, height=45, fill_color=theme_colors["bg_sidebar"])
    # Main dashboard area
    create_shape(ws, "rectangle", "C1", width=25, height=45, fill_color=theme_colors["bg_main"])


    # --- 2. Title and Logo ---
    # Assuming logo is inserted via image in a real scenario.
    # For text, we'll place the title directly.
    ws['B1'].value = title
    set_cell_font(ws['B1'], "Aptos Narrow", 24, True, theme_colors["text_light"])
    ws['B1'].alignment = Alignment(horizontal='left', vertical='center')

    # --- 3. KPI Display (Side Panel) ---
    kpi_start_row = 4
    kpis = [
        ("Orders", "Pivots!G4", "🛒"),
        ("Quantity", "Pivots!H4", "👕"),
        ("Amount", "Pivots!I4", "💵"),
        ("Avg. Rating", "Pivots!J4", "⭐"),
        ("Avg. Days to Deliver", "Pivots!K4", "⏱️")
    ]

    for i, (label, cell_ref, emoji) in enumerate(kpis):
        # KPI Label
        ws[f'B{kpi_start_row + i*3}'].value = f"{emoji} {label}"
        set_cell_font(ws[f'B{kpi_start_row + i*3}'], "Aptos Narrow", 11, True, theme_colors["text_light"])

        # KPI Value (linked to formatted cells in Pivots sheet)
        # Assuming Pivots!G4, H4, I4, J4, K4 are already formatted as shown in video
        linked_value_cell = ws[f'B{kpi_start_row + i*3 + 1}']
        linked_value_cell.value = f"='{cell_ref}'" # Direct link using formula
        set_cell_font(linked_value_cell, "Aptos Narrow", 18, True, theme_colors["text_light"])
        # Special color for Amount
        if label == "Amount":
            set_cell_font(linked_value_cell, "Aptos Narrow", 18, True, theme_colors["map_quantity"])


    # --- 4. Chart Placeholders (Main Content Area) ---
    # Row 1 Charts
    create_shape(ws, "rectangle", "D2", width=6, height=13, fill_color=theme_colors["text_light"]) # Last 13 Week Trends
    create_shape(ws, "rectangle", "J2", width=6, height=13, fill_color=theme_colors["text_light"]) # How they like to buy (Heatmap)
    create_shape(ws, "rectangle", "P2", width=6, height=13, fill_color=theme_colors["text_light"]) # How many they buy (Qty Dist)

    # Row 2 Charts
    create_shape(ws, "rectangle", "D16", width=6, height=13, fill_color=theme_colors["text_light"]) # Which Products are Popular
    create_shape(ws, "rectangle", "J16", width=6, height=13, fill_color=theme_colors["text_light"]) # Where our customers live (Map)
    create_shape(ws, "rectangle", "P16", width=6, height=13, fill_color=theme_colors["text_light"]) # How long to ship

    # Row 3 Charts
    create_shape(ws, "rectangle", "D30", width=6, height=13, fill_color=theme_colors["text_light"]) # Overall Gender Split
    create_shape(ws, "rectangle", "J30", width=6, height=13, fill_color=theme_colors["text_light"]) # (Second Map)
    create_shape(ws, "rectangle", "P30", width=6, height=13, fill_color=theme_colors["text_light"]) # Customer Satisfaction

    # Add placeholder titles
    ws['D2'].value = "Last 13 Week Trends - Qty & Amount"
    ws['J2'].value = "How they like to buy?"
    ws['P2'].value = "How many they buy?"
    ws['D16'].value = "Which Products are Popular? Breakdown by Gender"
    ws['J16'].value = "Where our customers live?"
    ws['P16'].value = "How long we take to ship?"
    ws['D30'].value = "Overall Gender Split"
    ws['J30'].value = "(Optional Second Map)" # Video shows one main map, but implies another small one.
    ws['P30'].value = "How satisfied are our customers?"

    for r in ['D2', 'J2', 'P2', 'D16', 'J16', 'P16', 'D30', 'J30', 'P30']:
        set_cell_font(ws[r], "Aptos Narrow", 11, True, theme_colors["text_dark"])
        ws[r].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
        set_cell_border(ws[r], color_hex=theme_colors["text_light"]) # Make shapes look like cards with borders.


    # --- 5. Slicer Placeholders (Side Panel) ---
    slicer_start_row = 28 # Adjust based on actual KPI count
    create_shape(ws, "rectangle", f"B{slicer_start_row}", width=1, height=7, fill_color=theme_colors["text_light"]) # Order Mode Slicer
    ws[f'B{slicer_start_row}'].value = "Order Mode"
    set_cell_font(ws[f'B{slicer_start_row}'], "Aptos Narrow", 11, True, theme_colors["text_dark"])
    ws[f'B{slicer_start_row}'].alignment = Alignment(horizontal='left', vertical='top')


    create_shape(ws, "rectangle", f"B{slicer_start_row + 8}", width=1, height=7, fill_color=theme_colors["text_light"]) # Customer Gender Slicer
    ws[f'B{slicer_start_row + 8}'].value = "Customer Gender"
    set_cell_font(ws[f'B{slicer_start_row + 8}'], "Aptos Narrow", 11, True, theme_colors["text_dark"])
    ws[f'B{slicer_start_row + 8}'].alignment = Alignment(horizontal='left', vertical='top')

    # In a real scenario, these would be actual slicer objects linked to named pivot tables.
    # Example for linking slicers to pivot tables:
    # Right-click slicer -> Report Connections... -> Check relevant pivot tables (by their names).
    # The pivot tables must exist and be named correctly (e.g., pvfSummary, pvfTrend, etc.)
    # This cannot be directly replicated with openpyxl as it does not support creating interactive slicers.


    # --- 6. Heatmap Linked Picture (Placeholder for conditional formatting magic) ---
    # Assuming 'Pivots'!H5:M9 contains the conditionally formatted data from pvfOrderModeGender
    # For openpyxl, this is a picture object that links to a range.
    # The actual conditional formatting would be set on the 'Pivots' sheet.
    # This is a representation of its placement and dynamic nature.
    # (openpyxl.drawing.image.Image for a static image, or a custom approach for linked pictures)
    # Since direct linked pictures are complex, we'll represent it as a styled merged cell.
    create_shape(ws, "rectangle", "J2", width=6, height=13, fill_color=theme_colors["text_light"], border_color=theme_colors["text_dark"])
    ws['J2'].value = "Heatmap (linked picture)" # Text to indicate it's a linked picture
    ws['J2'].alignment = Alignment(horizontal='center', vertical='center')
    set_cell_font(ws['J2'], "Aptos Narrow", 11, True, theme_colors["text_dark"])

    # Final cleanup (adjusting column widths of dashboard content to align with shapes)
    ws.column_dimensions['C'].width = 1.5 # Space before first chart column
    ws.column_dimensions['D'].width = 12 # Chart column
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 1.5 # Space between charts
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 12
    ws.column_dimensions['K'].width = 1.5 # Space between charts
    ws.column_dimensions['L'].width = 12
    ws.column_dimensions['M'].width = 12
    ws.column_dimensions['N'].width = 12
    ws.column_dimensions['O'].width = 1.5 # Space after last chart column

    print(f"Dashboard '{sheet_name}' created with basic layout and KPI links.")

# Example Usage (create a dummy workbook and run)
# wb = openpyxl.Workbook()
# ws_data = wb.active
# ws_data.title = "Data"
# ws_data['A1'] = "TX ID" # Dummy data headers
# ws_data['B1'] = "Product"
# ws_data['C1'] = "Quantity"
# # ... add more dummy data or load from an actual source

# # Create dummy pivots sheet with placeholder data that the dashboard will link to
# ws_pivots = wb.create_sheet("Pivots")
# ws_pivots['G4'] = 2400 # Orders
# ws_pivots['H4'] = 11997 # Quantity
# ws_pivots['I4'] = 649019.8 # Amount
# ws_pivots['J4'] = 3.96 # Avg Rating
# ws_pivots['K4'] = 2.34 # Avg Days
# ws_pivots['G4'].number_format = '#,##0'
# ws_pivots['H4'].number_format = '#,##0'
# ws_pivots['I4'].number_format = '$#,##0,.0k'
# ws_pivots['J4'].number_format = '0.0'
# ws_pivots['K4'].number_format = '0.0'


# # Add placeholder for heatmap matrix on Pivots sheet
# ws_pivots['H5'].value = 0.19
# ws_pivots['H5'].number_format = '0.0%'
# set_cell_fill(ws_pivots['H5'], get_theme_colors("VivaCalif")['heatmap_blue'])
# set_cell_border(ws_pivots['H5'], color_hex=get_theme_colors("VivaCalif")['heatmap_white'])
# # ... (populate more cells for the matrix as needed by the actual data and conditional formatting)


# # Run the render_sheet function
# render_sheet(wb, "Dashboard", title="VIVA CALIF", theme="VivaCalif")

# # Save the workbook
# # wb.save("ecommerce_dashboard_distilled.xlsx")
