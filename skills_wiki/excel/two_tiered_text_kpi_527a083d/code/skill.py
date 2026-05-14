from openpyxl.drawing.shapes import Shape
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichText
from openpyxl.drawing.geometry import Xfrm, Point2D
from openpyxl.drawing.fill import SolidFill
from openpyxl.drawing.line import Outline, NoFill
from openpyxl.styles.colors import Color
from openpyxl.utils.units import cm_to_EMU, pixels_to_EMU

# Simplified theme loader for demonstration purposes
class DefaultTheme:
    def __init__(self):
        self.header_bg = "000000"  # Black
        self.header_fg = "FFFFFF"  # White
        self.body_bg = "FFFFFF"   # White
        self.body_fg = "000000"   # Black
        self.border_color = "000000" # Black

def get_theme_colors(theme_name: str):
    """Returns a theme object with colors based on the theme_name."""
    if theme_name == "corporate_blue":
        return type('Theme', (object,), {
            'header_bg': '0D1B2A',  # Navy
            'header_fg': 'FFFFFF',  # White
            'body_bg': 'FFFFFF',    # White
            'body_fg': '000000',    # Black
            'border_color': '000000' # Black
        })()
    return DefaultTheme() # Fallback theme

def render(ws, anchor: str, *, title: str = "Revenue", value: str = "$7,708,632", theme: str = "corporate_blue", **kwargs) -> None:
    """
    Renders a two-tiered text KPI using shapes on the specified worksheet.

    Note: Due to openpyxl limitations, the text values within the shapes are set statically
    at the time of generation rather than being dynamically linked to Excel cells via formulas.
    Additionally, openpyxl does not directly support grouping arbitrary Shape objects.

    :param ws: The worksheet to render on.
    :param anchor: The approximate top-left cell anchor for the KPI (e.g., "E2").
                   Shapes are placed using absolute EMUs; this is a conceptual anchor.
    :param title: The text for the upper tier (e.g., "Revenue").
    :param value: The text for the lower tier (e.g., "$7,708,632").
    :param theme: The name of the color theme to use.
    """
    current_theme = get_theme_colors(theme)

    # Define KPI dimensions in centimeters for consistent sizing
    kpi_width_cm = 6.0
    kpi_height_cm = 3.5

    # Split height between title and value sections
    title_section_height_cm = kpi_height_cm * 0.4
    value_section_height_cm = kpi_height_cm * 0.6

    # Define anchor offset for shapes in EMUs (absolute placement on sheet)
    # This is a general placement. For precise cell anchoring,
    # complex calculations based on column widths and row heights would be needed.
    anchor_x_emu = cm_to_EMU(15)
    anchor_y_emu = cm_to_EMU(0.5)

    # 1. Create the top shape (for the title)
    shape_title = Shape(
        prst="rect",  # Predefined rectangular shape
        xfrm=Xfrm(
            off=Point2D(x=anchor_x_emu, y=anchor_y_emu),
            ext=Point2D(x=cm_to_EMU(kpi_width_cm), y=cm_to_EMU(title_section_height_cm))
        ),
        fill=SolidFill(
            srgbClr=Color(rgb=current_theme.header_bg)
        ),
        outline=NoFill(), # No outline for the title section
        text=RichText(
            p=[
                Paragraph(
                    pPr=ParagraphProperties(
                        algn='ctr',  # Horizontal center alignment
                        defRPr=CharacterProperties(
                            b=True,     # Bold font
                            sz=3400,    # Font size 34pt (value * 100)
                            srgbClr=Color(rgb=current_theme.header_fg)
                        )
                    ),
                    r=[
                        RichText.Run(t=title)
                    ]
                )
            ]
        )
    )
    ws.add_drawing(shape_title)

    # 2. Create the bottom shape (for the value)
    shape_value = Shape(
        prst="rect",  # Predefined rectangular shape
        xfrm=Xfrm(
            off=Point2D(x=anchor_x_emu, y=anchor_y_emu + cm_to_EMU(title_section_height_cm)),
            ext=Point2D(x=cm_to_EMU(kpi_width_cm), y=cm_to_EMU(value_section_height_cm))
        ),
        fill=SolidFill(
            srgbClr=Color(rgb=current_theme.body_bg)
        ),
        outline=Outline(
            solidFill=Color(rgb=current_theme.border_color),
            w=pixels_to_EMU(1.0) # 1 pixel width border
        ),
        text=RichText(
            p=[
                Paragraph(
                    pPr=ParagraphProperties(
                        algn='ctr',  # Horizontal center alignment
                        defRPr=CharacterProperties(
                            b=True,     # Bold font
                            sz=1600,    # Font size 16pt (value * 100)
                            srgbClr=Color(rgb=current_theme.body_fg)
                        )
                    ),
                    r=[
                        RichText.Run(t=value)
                    ]
                )
            ]
        )
    )
    ws.add_drawing(shape_value)

