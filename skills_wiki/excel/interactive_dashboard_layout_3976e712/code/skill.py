import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.geometry import PresetGeometry2D, GEOM_RECT, AdjustHandleList
from openpyxl.drawing.shape import Shape as XDRShape, ShapeProperties, TextBody, NoFillProperties, Outline
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorPoint
from openpyxl.drawing.xdr import NvSpPr, NvPr, CNvSpPr
from openpyxl.drawing.text import RichText, Paragraph, ParagraphProperties, CharacterProperties
from openpyxl.utils.units import pixels_to_EMU
from openpyxl.utils import get_column_letter, column_index_from_string

# Helper for theme colors (simplified based on video's aesthetic)
def get_theme_colors(theme_name):
    themes = {
        "mcdonalds_blue": {
            "sidebar_bg": "FF002060", # Dark blue for sidebar
            "header_bg": "FFFFFFFF",   # White for main shapes
            "header_fg": "FF002060",   # Dark blue for text
            "text_dark": "FF002060",   # Dark blue for general text
            "shadow_color": "FF808080",# Gray for shadow (conceptual in OpenPyXL for shapes)
        }
    }
    return themes.get(theme_name, themes["mcdonalds_blue"])


def create_dashboard_shape(ws, anchor_cell_str: str, width_px: int, height_px: int,
                           text_lines: list, theme_name: str,
                           title_font_size: int = 14, subtitle_font_size: int = 10):
    """
    Creates and places a rounded rectangular shape with multiple lines of text, fill, and shadow.
    
    Args:
        ws: The worksheet to add the shape to.
        anchor_cell_str: The top-left cell where the shape will be anchored (e.g., "B2").
        width_px: The desired width of the shape in pixels.
        height_px: The desired height of the shape in pixels.
        text_lines: A list of strings, where the first is the main title and subsequent are subtitles.
        theme_name: The name of the color theme.
        title_font_size: Font size for the first line of text (title).
        subtitle_font_size: Font size for subsequent lines of text (subtitles).
        (Note: shadow effect is conceptual as direct shadow property on simple shapes is limited in openpyxl)
    """
    colors = get_theme_colors(theme_name)
    fill_color = colors["header_bg"][2:]
    text_color = colors["header_fg"][2:]

    # Text body with multiple paragraphs for title and subtitles
    text_body = TextBody(bodyPr=ParagraphProperties(rot=0, vertOverflow="clip", horzOverflow="clip", vert="ea", wrap="square",
                                                   lIns=0, tIns=0, rIns=0, bIns=0, anchor="ctr", anchorCtr=True),
                         lstStyle=None)
    
    # First line (main title)
    cp_title = CharacterProperties(latin="Calibri", sz=pixels_to_EMU(title_font_size)/100, b=True, solidFill=text_color)
    p_title = Paragraph(pPr=ParagraphProperties(algn="ctr"), endParaRPr=cp_title)
    p_title.add_run_text(text_lines[0])
    text_body.append(p_title)

    # Subsequent lines (subtitles/descriptions)
    for i in range(1, len(text_lines)):
        cp_sub = CharacterProperties(latin="Calibri", sz=pixels_to_EMU(subtitle_font_size)/100, b=False, solidFill=text_color)
        p_sub = Paragraph(pPr=ParagraphProperties(algn="ctr"), endParaRPr=cp_sub)
        p_sub.add_run_text(text_lines[i])
        text_body.append(p_sub)

    # Shape properties
    shape_props = ShapeProperties(
        solidFill=fill_color,
        ln=Outline(noFill=True), # No outline
        presetGeom=PresetGeometry2D(geom=GEOM_RECT, avLst=AdjustHandleList())
    )
    # Note: Adding a shadow effect to generic shapes directly via openpyxl's ShapeProperties
    # as seen in the video is complex and not directly supported for simple XDRShape objects
    # like it is for charts or via graphicFrame properties. This visual effect is noted in the description.

    # Non-visual shape properties (id and name will be handled by add_drawing)
    nv_sp_pr = NvSpPr(cNvPr=NvPr(id=0, name="DashboardShape"), cNvSpPr=CNvSpPr(txBox=True))

    xdr_shape = XDRShape(nvSpPr=nv_sp_pr, spPr=shape_props, txBody=text_body)

    # Calculate anchor points for the shape
    col_idx, row_idx = column_index_from_string(anchor_cell_str[0]), int(anchor_cell_str[1:])
    col_from, row_from = col_idx - 1, row_idx - 1 # 0-indexed for AnchorPoint
    
    # Create a OneCellAnchor: This positions the shape starting at the given cell,
    # and extends it by the specified pixel width/height relative to the cell's top-left.
    shape_anchor = OneCellAnchor(
        _from=AnchorPoint(col=col_from, colOff=0, row=row_from, rowOff=0),
        _to=AnchorPoint(col=col_from, colOff=pixels_to_EMU(width_px),
                        row=row_from, rowOff=pixels_to_EMU(height_px)),
        _shape=xdr_shape
    )
    ws.add_drawing(shape_anchor)


def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "mcdonalds_blue", **kwargs) -> None:
    """
    Renders the main dashboard sheet structure with a dynamic navigation sidebar and content areas.
    The sidebar icons and their hyperlinks are conceptually described, as direct dynamic linking
    of icons/shapes to sheets via Excel's formula bar is not directly supported by OpenPyXL.
    """
    try: # Try to get the sheet if it exists, otherwise create
        ws = wb[sheet_name]
    except KeyError:
        ws = wb.create_sheet(sheet_name)
    ws.title = sheet_name

    colors = get_theme_colors(theme)
    sidebar_bg_color = colors["sidebar_bg"][2:]
    header_fg_color = colors["header_fg"] # Use full ARGB for cell font color

    # Hide gridlines for a cleaner dashboard look
    ws.sheet_view.showGridLines = False

    # 1. Setup Sidebar (Column A)
    ws.column_dimensions['A'].width = 8 # Wider column for icons
    for row_idx in range(1, 40): # Fill column A with sidebar background color for visual effect
        ws.cell(row=row_idx, column=1).fill = PatternFill(start_color=sidebar_bg_color, end_color=sidebar_bg_color, fill_type="solid")
    
    # Conceptual representation of sidebar icons and hyperlinks:
    # OpenPyXL cannot directly insert complex SVG icons or provide easy Excel-formula-bar-style
    # hyperlink functionality for drawing objects/shapes as shown in the video.
    # This section conceptually represents the sidebar's purpose and styling.
    ws.cell(row=1, column=1).value = title[0].upper() + title[1:].lower() # "McDonald's" -> "Mcdonald's"
    ws.cell(row=1, column=1).font = Font(name="Calibri", color="FFFF0000", bold=True, size=16) # McDs red "M"
    ws.cell(row=1, column=1).alignment = Alignment(horizontal='center', vertical='center')

    # 2. Setup Main Content Area Shapes (white rounded rectangles with titles)

    # Main Dashboard Title Bar
    create_dashboard_shape(ws, "B2", width_px=1000, height_px=60, # Roughly spans B2:M4
                           text_lines=[f"{title} Sales Dashboard South America 2022", "Figures in millions of USD"],
                           theme_name=theme, title_font_size=20, subtitle_font_size=10)
    
    # KPI Shapes (Sales, Profit, # Customers)
    kpi_width_px = 300
    kpi_height_px = 80
    
    create_dashboard_shape(ws, "B6", kpi_width_px, kpi_height_px, ["Sales"], theme_name, title_font_size=14)
    create_dashboard_shape(ws, "F6", kpi_width_px, kpi_height_px, ["Profit"], theme_name, title_font_size=14)
    create_dashboard_shape(ws, "J6", kpi_width_px, kpi_height_px, ["# of Customers"], theme_name, title_font_size=14)

    # 2021-2022 Sales Trend (line chart area)
    trend_width_px = 650
    trend_height_px = 250
    create_dashboard_shape(ws, "B15", trend_width_px, trend_height_px, ["2021-2022 Sales Trend (in millions)"], theme_name, title_font_size=14)

    # Customer Satisfaction (radar chart area)
    cust_sat_width_px = 300
    cust_sat_height_px = 250 
    create_dashboard_shape(ws, "J15", cust_sat_width_px, cust_sat_height_px, ["Customer Satisfaction"], theme_name, title_font_size=14)
    
    # Sales by Country (map chart area)
    map_width_px = 300
    map_height_px = 310 
    create_dashboard_shape(ws, "N6", map_width_px, map_height_px, ["Sales by Country 2022"], theme_name, title_font_size=14)

    # Adjust column widths for better visual spacing
    # These widths are approximations for a balanced dashboard layout.
    for col_idx in range(2, 17): # Columns B to P
        ws.column_dimensions[get_column_letter(col_idx)].width = 12 

