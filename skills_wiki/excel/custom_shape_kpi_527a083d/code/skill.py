from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.shapes import Shape as OpxlShape
from openpyxl.drawing.fill import ColorChoice, RGBColor, SolidColorFill
from openpyxl.drawing.line import LineProperties, NoFillProperties
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichText, TextBody, Font as TxtFont
from openpyxl.drawing.geometry import PresetGeometry, Point2D, PositiveSize2D
from openpyxl.drawing.xdr import CT_TextBodyProperties, CT_TextListStyle

# Helper function for theme (minimal implementation for demonstration)
class Theme:
    def __init__(self, name="corporate_blue"):
        self.palette = {
            "corporate_blue": {
                "header_bg": "002060",  # Dark Blue
                "accent_bg": "0070C0",  # Lighter Blue
                "neutral_bg": "FFFFFF", # White
                "header_text_color": "FFFFFF", # White
                "text_color": "000000",   # Black
                "border_color": "C0C0C0" # Light Gray
            },
            "modern_teal": { # Example theme
                "header_bg": "004D40", # Dark Teal
                "accent_bg": "00BFA5", # Bright Teal
                "neutral_bg": "F5F5F5", # Light Gray
                "header_text_color": "FFFFFF",
                "text_color": "212121",
                "border_color": "BDBDBD"
            }
        }
        self.name = name
        self.colors = self.palette.get(name, self.palette["corporate_blue"])

    def get_color(self, key):
        return self.colors.get(key)

    def get_rgb_color(self, key):
        hex_color = self.get_color(key)
        if hex_color:
            return RGBColor(hex_color)
        return None

def get_theme_colors(theme_name):
    return Theme(theme_name)

def render(ws, anchor: str, *, region_name: str, revenue_value: float, market_share_value: float, theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a KPI component with region name, revenue, and market share.
    The KPI consists of a main rounded rectangle and a smaller oval for market share.

    Note: The video demonstrates linking shape text to cell references (e.g., =$B$2)
    which provides dynamic updates in Excel. This direct linking functionality for
    shape text is an Excel UI feature and is not directly available via openpyxl's
    high-level API for shapes. The code below creates shapes with static text
    representing the *values* that would typically be dynamically linked.
    """
    current_theme = get_theme_colors(theme)
    main_fill_color_hex = current_theme.get_color("header_bg")
    main_text_color_hex = current_theme.get_color("header_text_color")
    circle_fill_color_hex = current_theme.get_color("neutral_bg")
    circle_text_color_hex = current_theme.get_color("text_color")

    # Define text styles for consistency with the video
    title_font = TxtFont(sz=1800, b=True, latin=TxtFont.LatinFont(typeface="Calibri")) # 18pt, Bold
    value_font = TxtFont(sz=1400, b=True, latin=TxtFont.LatinFont(typeface="Calibri")) # 14pt, Bold

    # --- Calculate initial position based on anchor cell ---
    # Convert anchor cell to a (column, row) tuple for positioning offset
    from openpyxl.utils.cell import column_index_from_string
    col_letter = anchor[0]
    row_num = int(anchor[1:])

    # Approximate default cell dimensions in EMUs (English Metric Units)
    # 1 inch = 914400 EMUs. Default Excel column width (8.43) is ~64 pixels. Default row height (15) is ~20 pixels.
    # 1 pixel = 9525 EMUs.
    DEFAULT_COL_WIDTH_EMU = 64 * 9525 # ~609600 EMUs
    DEFAULT_ROW_HEIGHT_EMU = 20 * 9525 # ~190500 EMUs

    # Calculate top-left absolute EMU coordinates for the KPI block
    # Start the KPI a bit offset from the anchor cell to not obscure its content
    # This places the KPI block starting roughly 1 column and 1 row after the anchor cell.
    offset_cols = (column_index_from_string(col_letter) - 1) * DEFAULT_COL_WIDTH_EMU + DEFAULT_COL_WIDTH_EMU
    offset_rows = (row_num - 1) * DEFAULT_ROW_HEIGHT_EMU + DEFAULT_ROW_HEIGHT_EMU

    # --- Main Rounded Rectangle Shape ---
    rect_width_emu = 2 * 914400 # ~2 inches
    rect_height_emu = 1.5 * 914400 # ~1.5 inches

    main_rect = OpxlShape.from_geometry(
        PresetGeometry(prst="roundRect"),
        Point2D(offset_cols, offset_rows),
        PositiveSize2D(rect_width_emu, rect_height_emu)
    )
    main_rect.fill = SolidColorFill(prgb=main_fill_color_hex)
    main_rect.outline = LineProperties(noFill=NoFillProperties())

    # Text body for the main rectangle (multiple paragraphs for lines)
    main_rect.text_body = TextBody(
        bodyPr=CT_TextBodyProperties(
            vert="horz", wrap="square", anchor="ctr", anchorCtr="0",
            # Set top/bottom/left/right text margins to avoid text clipping
            lIns=45720, tIns=45720, rIns=45720, bIns=45720 # ~5pt margins
        ),
        lstStyle=CT_TextListStyle(),
        p=[
            Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(font=title_font, solidFill=SolidColorFill(prgb=main_text_color_hex))), r=[RichText(text=region_name)]),
            Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(font=value_font, solidFill=SolidColorFill(prgb=main_text_color_hex))), r=[RichText(text="Revenue")]),
            Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(font=value_font, solidFill=SolidColorFill(prgb=main_text_color_hex))), r=[RichText(text=f"${revenue_value:,.0f}")])
        ]
    )
    ws.add_drawing(main_rect)

    # --- Market Share Oval Shape ---
    circle_diameter_emu = 0.8 * 914400 # ~0.8 inches
    
    # Position the circle relative to the main rectangle (bottom-right corner)
    # Calculate absolute position for the oval
    oval_x = offset_cols + rect_width_emu - circle_diameter_emu - (0.15 * 914400) # 0.15 inch margin from right
    oval_y = offset_rows + rect_height_emu - circle_diameter_emu - (0.15 * 914400) # 0.15 inch margin from bottom

    oval_shape = OpxlShape.from_geometry(
        PresetGeometry(prst="ellipse"),
        Point2D(oval_x, oval_y),
        PositiveSize2D(circle_diameter_emu, circle_diameter_emu)
    )
    oval_shape.fill = SolidColorFill(prgb=circle_fill_color_hex)
    oval_shape.outline = LineProperties(noFill=NoFillProperties())

    # Text body for the oval
    oval_shape.text_body = TextBody(
        bodyPr=CT_TextBodyProperties(
            vert="horz", wrap="square", anchor="ctr", anchorCtr="0",
            lIns=45720, tIns=45720, rIns=45720, bIns=45720
        ),
        lstStyle=CT_TextListStyle(),
        p=[
            Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(font=value_font, solidFill=SolidColorFill(prgb=circle_text_color_hex))), r=[RichText(text=f"{market_share_value:.0%}")])
        ]
    )
    ws.add_drawing(oval_shape)
