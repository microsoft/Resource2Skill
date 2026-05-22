from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink

# Helper for theme colors (as in seed skills)
def get_theme_color(theme_name: str):
    # This dictionary would typically be loaded from a more comprehensive theme module.
    # For this skill, we define a minimal set of colors based on the video.
    theme_palettes = {
        "corporate_blue": {
            "dark_blue_hex": "1F4E79", # Example dark blue
            "white_hex": "FFFFFF",     # Example white
            "light_gray_hex": "D9D9D9",# Example light gray for subtle borders/shadows
            "text_color_1_hex": "1F4E79", # Text color for main content
            "header_bg_hex": "1F4E79",
            "header_fg_hex": "FFFFFF",
            "sidebar_bg_hex": "1F4E79",
            "shadow_color_hex": "C0C0C0" # Used for border simulation
        },
        # Add other themes if needed for future skills
    }
    return theme_palettes.get(theme_name, theme_palettes["corporate_blue"])

def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
    
    theme_colors = get_theme_color(theme)

    # Hide gridlines
    ws.sheet_view.showGridLines = False

    # Set column A for sidebar (approximate from video)
    ws.column_dimensions['A'].width = 12 # Wider to accommodate text "icons"

    # Set widths for content columns (B to M)
    for col_idx in range(2, 14): # Columns B through M
        ws.column_dimensions[get_column_letter(col_idx)].width = 10 # Default width, adjust for visual balance

    # --- 1. Navigation Sidebar (Column A) ---
    sidebar_fill = PatternFill(start_color=theme_colors["sidebar_bg_hex"], end_color=theme_colors["sidebar_bg_hex"], fill_type="solid")
    for row in range(1, 26): # Fill column A up to a reasonable height
        ws.cell(row=row, column=1).fill = sidebar_fill

    # Placeholder for McDonald's logo
    logo_cell = ws['A2']
    logo_cell.value = "McDonald's"
    logo_cell.font = Font(name='Calibri', sz=12, bold=True, color=theme_colors["header_fg_hex"])
    logo_cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Navigation "icons" (text with cell hyperlinks as shapes cannot be easily hyperlinked dynamically via openpyxl)
    nav_font = Font(name='Calibri', sz=10, bold=True, color=theme_colors["header_fg_hex"])
    nav_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    # Ensure target sheets exist for hyperlinks
    target_sheets = ["Dashboard", "Inputs", "Contacts"]
    for ts in target_sheets:
        if ts not in wb.sheetnames:
            wb.create_sheet(ts)

    nav_links = [
        ("Dashboard", "Dashboard"),
        ("Inputs", "Inputs"),
        ("Contacts", "Contacts"),
        ("Email", "Contacts"), # Simulate email/contacts link
        ("Help", "Dashboard")  # Simulate help/dashboard link
    ]
    
    for i, (text, target_sheet) in enumerate(nav_links):
        nav_cell = ws.cell(row=6 + i*2, column=1) # Place icons every 2 rows
        nav_cell.value = text
        nav_cell.font = nav_font
        nav_cell.alignment = nav_alignment
        
        # Add cell hyperlink
        nav_cell.hyperlink = Hyperlink(ref=nav_cell.coordinate, target=f"'{target_sheet}'!A1")
        nav_cell.style = "Hyperlink" # Apply standard Excel hyperlink style

    # --- 2. Main Title Bar (Merged Cells with Styling) ---
    # Unmerge cells before re-merging to avoid potential issues if already merged differently
    if ws.cell(row=2, column=2).is_merged: # Check if B2 is part of a merged cell
        ws.unmerge_cells('B2:M4') # Assuming the largest possible prior merge

    ws.merge_cells('B2:M2') # New main title range
    ws.merge_cells('B3:M3') # New subtitle range

    header_cell = ws['B2']
    header_cell.value = title
    header_cell.font = Font(name='Calibri', sz=18, bold=True, color=theme_colors["header_fg_hex"])
    header_cell.fill = PatternFill(start_color=theme_colors["header_bg_hex"], end_color=theme_colors["header_bg_hex"], fill_type="solid")
    header_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)
    # Simulate a border/shadow effect using cell borders
    thin_side = Side(style='thin', color=theme_colors["shadow_color_hex"])
    header_cell.border = Border(left=thin_side, top=thin_side, right=thin_side) # Only top/left/right for top row

    subtitle_cell = ws['B3']
    subtitle_cell.value = "Figures in millions of USD"
    subtitle_cell.font = Font(name='Calibri', sz=9, color=theme_colors["header_fg_hex"])
    subtitle_cell.fill = PatternFill(start_color=theme_colors["header_bg_hex"], end_color=theme_colors["header_bg_hex"], fill_type="solid")
    subtitle_cell.alignment = Alignment(horizontal='left', vertical='center', indent=1)
    subtitle_cell.border = Border(left=thin_side, bottom=thin_side, right=thin_side) # Only bottom/left/right for bottom row


    # --- 3. Content Areas (KPIs and Charts) - Merged Cells with Styling ---
    content_fill = PatternFill(start_color=theme_colors["fill_primary_hex"], end_color=theme_colors["fill_primary_hex"], fill_type="solid")
    content_text_font = Font(name='Calibri', sz=11, bold=True, color=theme_colors["text_color_1_hex"])
    content_text_alignment = Alignment(horizontal='left', vertical='top', indent=1)
    content_border = Border(left=thin_side, top=thin_side, right=thin_side, bottom=thin_side)

    # KPI 1: Sales (B5:D10 in video, adjusted to be below title and within reasonable rows)
    ws.merge_cells('B5:D9')
    kpi1_cell = ws['B5']
    kpi1_cell.fill = content_fill
    kpi1_cell.border = content_border
    kpi1_cell.value = "Sales"
    kpi1_cell.font = content_text_font
    kpi1_cell.alignment = content_text_alignment

    # KPI 2: Profit
    ws.merge_cells('E5:G9')
    kpi2_cell = ws['E5']
    kpi2_cell.fill = content_fill
    kpi2_cell.border = content_border
    kpi2_cell.value = "Profit"
    kpi2_cell.font = content_text_font
    kpi2_cell.alignment = content_text_alignment

    # KPI 3: # of Customers
    ws.merge_cells('H5:J9')
    kpi3_cell = ws['H5']
    kpi3_cell.fill = content_fill
    kpi3_cell.border = content_border
    kpi3_cell.value = "# of Customers"
    kpi3_cell.font = content_text_font
    kpi3_cell.alignment = content_text_alignment

    # Sales by Country (Map)
    ws.merge_cells('K5:M16') # K6:M17 in video
    map_cell = ws['K5']
    map_cell.fill = content_fill
    map_cell.border = content_border
    map_cell.value = "Sales by Country 2022"
    map_cell.font = content_text_font
    map_cell.alignment = content_text_alignment

    # 2021-2022 Sales Trend (Line Chart)
    ws.merge_cells('B11:J16') # B12:J17 in video
    trend_cell = ws['B11']
    trend_cell.fill = content_fill
    trend_cell.border = content_border
    trend_cell.value = "2021-2022 Sales Trend (in millions)"
    trend_cell.font = content_text_font
    trend_cell.alignment = content_text_alignment

    # Customer Satisfaction (Radar Chart)
    ws.merge_cells('B18:J24') # K19:M24 in video - adapting to available space
    satisfaction_cell = ws['B18']
    satisfaction_cell.fill = content_fill
    satisfaction_cell.border = content_border
    satisfaction_cell.value = "Customer Satisfaction"
    satisfaction_cell.font = content_text_font
    satisfaction_cell.alignment = content_text_alignment

    # Placeholder for another visual (e.g., smaller chart area on the right)
    ws.merge_cells('K18:M24') 
    other_visual_cell = ws['K18']
    other_visual_cell.fill = content_fill
    other_visual_cell.border = content_border
    other_visual_cell.value = "Other Visual" # Placeholder
    other_visual_cell.font = content_text_font
    other_visual_cell.alignment = content_text_alignment

    # Fill any remaining unmerged cells in the main content area with white
    for r in range(1, ws.max_row + 1):
        for c in range(2, ws.max_column + 1):
            cell = ws.cell(row=r, column=c)
            # Check if the cell is not part of a merged range or already styled by sidebar
            if not cell.fill.start_color.rgb and not cell.is_merged:
                cell.fill = PatternFill(start_color=theme_colors["white_hex"], end_color=theme_colors["white_hex"], fill_type="solid")

    # The actual charts and dynamic number text boxes would be placed into these merged cell areas.
    # This function provides the structural layout.
