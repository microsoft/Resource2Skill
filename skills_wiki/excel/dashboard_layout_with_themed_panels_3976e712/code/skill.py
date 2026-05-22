from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.styles.colors import RGBColor

# Helper function for loading theme colors
def _get_theme_colors(theme_name: str):
    # This is a simplified placeholder. In a real setup, this would load a JSON or dictionary.
    themes = {
        "corporate_blue": {
            "header_bg": "FF002060",  # Dark Blue for sidebar
            "primary_bg": "FFFFFFFF", # White for general sheet background
            "panel_bg": "FFFFFFFF",   # White for panel backgrounds
            "panel_shadow": "FF808080", # Grey for subtle panel borders
            "text_color_dark": "FF002060", # Dark Blue for text
            "text_color_light": "FFFFFFFF", # White (unused in this specific skill)
            "accent_red": "FFE06666", # A shade of red (unused)
            "accent_orange": "FFF7A600" # A shade of orange (unused)
        }
    }
    return themes.get(theme_name, themes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ws = wb.create_sheet(sheet_name)
    colors = _get_theme_colors(theme)

    # Hide gridlines for a cleaner look
    ws.sheet_view.showGridLines = False

    # Define common styles for panels
    panel_fill = PatternFill(start_color=RGBColor(colors["panel_bg"][2:]), end_color=RGBColor(colors["panel_bg"][2:]), fill_type="solid")
    dark_text_color = RGBColor(colors["text_color_dark"][2:])
    thin_border_color = RGBColor(colors["panel_shadow"][2:])

    thin_border = Border(left=Side(style='thin', color=thin_border_color),
                         right=Side(style='thin', color=thin_border_color),
                         top=Side(style='thin', color=thin_border_color),
                         bottom=Side(style='thin', color=thin_border_color))
    
    # Set default column widths and row heights for visual spacing
    ws.column_dimensions['A'].width = 5 # Icon sidebar
    for col_letter in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
        ws.column_dimensions[col_letter].width = 10

    ws.row_dimensions[1].height = 10 # Top margin
    ws.row_dimensions[2].height = 25 # Main Title
    ws.row_dimensions[3].height = 15 # Subtitle
    ws.row_dimensions[4].height = 10 # Space below title/subtitle
    ws.row_dimensions[5].height = 15 # KPI Title row header
    for r_idx in range(6, 11): # KPI cells
        ws.row_dimensions[r_idx].height = 20
    ws.row_dimensions[10].height = 10 # Space below KPIs
    for r_idx in range(11, 20): # Chart cells
        ws.row_dimensions[r_idx].height = 20
    ws.row_dimensions[19].height = 10 # Bottom margin

    # Sidebar background (Column A)
    for r_idx in range(1, 20): # Apply to relevant rows
        ws.cell(row=r_idx, column=1).fill = PatternFill(start_color=RGBColor(colors["header_bg"][2:]), end_color=RGBColor(colors["header_bg"][2:]), fill_type="solid")

    # Helper function to create and style a merged cell panel
    def create_panel(sheet, cell_range_str, panel_title, font_size, bold, vertical_align='top'):
        sheet.merge_cells(cell_range_str)
        top_left_cell_coord = cell_range_str.split(':')[0]
        cell = sheet[top_left_cell_coord]
        cell.value = panel_title
        cell.font = Font(color=dark_text_color, bold=bold, size=font_size)
        cell.fill = panel_fill
        cell.alignment = Alignment(horizontal='left', vertical=vertical_align, wrap_text=True)
        # Apply border to all cells in the merged range to simulate a container
        for row_cells in sheet[cell_range_str]:
            for c in row_cells:
                c.border = thin_border
        return cell

    # Main Dashboard Title Panel
    create_panel(ws, 'B2:J2', f"{title} {kwargs.get('region', 'South America')} {kwargs.get('year', '2022')}", 18, True, 'center')
    # Main Dashboard Subtitle Panel
    create_panel(ws, 'B3:J3', "Figures in millions of USD", 11, False, 'center')

    # Sales by Country Panel (top right)
    create_panel(ws, 'K2:M9', 'Sales by Country 2022', 11, True, 'top')

    # KPI Panels (row 6-9)
    create_panel(ws, 'B6:D9', 'Sales', 11, True, 'top')
    create_panel(ws, 'E6:G9', 'Profit', 11, True, 'top')
    create_panel(ws, 'H6:J9', '# of Customers', 11, True, 'top')

    # 2021-2022 Sales Trend Panel (bottom left)
    create_panel(ws, 'B11:J18', '2021-2022 Sales Trend (in millions)', 11, True, 'top')

    # Customer Satisfaction Panel (bottom right)
    create_panel(ws, 'K11:M18', 'Customer Satisfaction', 11, True, 'top')

