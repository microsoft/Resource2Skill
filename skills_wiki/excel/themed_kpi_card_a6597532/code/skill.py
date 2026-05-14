from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.units import cm_to_pixels, pixels_to_EMU, pixels_to_points
from openpyxl.drawing.image import Image # Not used for icons due to limitations
from openpyxl.drawing.shapes import Shape, CustomShape
from openpyxl.drawing.text import Paragraph, TextCharacterProperties, RichText
from openpyxl.drawing.geometry import Point2D, PositiveSize2D, PresetGeometry2D, ShapeProperties, AdjustHandleList
from openpyxl.drawing.spreadsheet_drawing import AbsoluteAnchor
from openpyxl.worksheet.drawing import Drawing

# Helper function to load theme colors (from _helpers.py in seed skills)
def _get_theme_colors(theme_name: str) -> dict:
    """Loads a simplified color palette for a given theme."""
    palettes = {
        "corporate_blue": {
            "header_bg_dark": "FF336699", "header_bg_light": "FF6699CC",
            "accent_1": "FF4472C4", "accent_2": "FFED7D31",
            "text_fg_dark": "FF000000", "text_fg_light": "FFFFFFFF",
            "border_light": "FFD0D0D0", "shadow": "FF808080"
        },
        "aspect": {
            "header_bg_dark": "FF581E6F", # Dark purple
            "header_bg_light": "FFE2D1ED", # Lighter purple
            "accent_1": "FFFFA500", # Gold
            "accent_2": "FF800080", # Purple (used for text/icons)
            "text_fg_dark": "FF581E6F", # Dark purple for text
            "text_fg_light": "FFFFFFFF",
            "border_light": "FFD0D0D0",
            "shadow": "FF808080" # Placeholder for shadow effect color
        }
    }
    return palettes.get(theme_name, palettes["corporate_blue"])

def render(ws, anchor: str, *, kpi_value_cell: str, kpi_label: str, icon_name: str, theme: str = "aspect", **kwargs) -> None:
    """
    Renders a single themed KPI card with a dynamic value link.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell where the KPI card should be placed (e.g., "B4").
        kpi_value_cell: The cell reference (e.g., "Analysis!B4") containing the KPI's numeric value.
                        Note: Openpyxl inserts this as literal text. For dynamic linking in Excel,
                        you would manually enter '=Analysis!B4' in the shape's formula bar after generation.
        kpi_label: The descriptive label for the KPI (e.g., "CALLS").
        icon_name: A descriptive name for the icon (e.g., "phone", "target").
                   Note: Openpyxl does not support Excel's built-in icon library.
                   A text 'Icon Placeholder' is used.
        theme: The color theme to use (e.g., "aspect", "corporate_blue").
    """
    theme_colors = _get_theme_colors(theme)

    # --- Card Dimensions (approximate based on video, converted from CM) ---
    CARD_HEIGHT_CM = 6.5
    CARD_WIDTH_CM = 3.5
    GOLD_TAB_WIDTH_CM = 1.0
    SHAPE_OVERLAP_CM = 0.2
    
    # Text positioning offsets
    VALUE_TEXT_Y_OFFSET_CM = 1.5 # From top of white shape
    LABEL_TEXT_Y_OFFSET_FROM_VALUE_CM = 0.3 # From bottom of value text
    ICON_TEXT_SIZE_POINTS = 24
    VALUE_TEXT_SIZE_POINTS = 32
    LABEL_TEXT_SIZE_POINTS = 18

    card_height_emu = pixels_to_EMU(cm_to_pixels(CARD_HEIGHT_CM))
    card_width_emu = pixels_to_EMU(cm_to_pixels(CARD_WIDTH_CM))
    gold_tab_width_emu = pixels_to_EMU(cm_to_pixels(GOLD_TAB_WIDTH_CM))
    shape_overlap_emu = pixels_to_EMU(cm_to_pixels(SHAPE_OVERLAP_CM))

    # Calculate anchor cell's top-left EMU coordinates (assuming default cell sizes)
    # This is an approximation. For exact positioning, real cell dimensions should be queried.
    start_col_idx = ws.cell(anchor).column - 1
    start_row_idx = ws.cell(anchor).row - 1
    
    # Approximate cell dimensions for positioning (e.g., default Excel)
    default_col_width_pixels = 64
    default_row_height_pixels = 18

    # Calculate absolute start X, Y for the card based on anchor cell
    # Summing up previous column/row dimensions is more robust.
    # For a component, it might be expected that the caller handles precise X,Y placement in EMUs.
    # For this reproduction, we will calculate based on anchor cell string for simplicity.
    x_offset_from_sheet_left = sum(pixels_to_EMU(ws.column_dimensions[col].width * (default_col_width_pixels/8.43)) 
                                   for col in (openpyxl.utils.get_column_letter(c) for c in range(1, start_col_idx + 1)))
    y_offset_from_sheet_top = sum(pixels_to_EMU(ws.row_dimensions[r].height * (default_row_height_pixels/15)) 
                                  for r in range(1, start_row_idx + 1))
    
    # --- Gold "Tab" Shape ---
    gold_shape = CustomShape(
        prstGeom=PresetGeometry2D(
            'roundRect',
            ah_lst=AdjustHandleList([Point2D(x=100000, y=50000)]) # Roundness
        ),
        spPr=ShapeProperties(
            noFill=False,
            ln={'w': 0}, # No line
            solidFill={'rgb': theme_colors['accent_1'][2:]} # Gold
        )
    )
    gold_shape.width = gold_tab_width_emu
    gold_shape.height = card_height_emu

    # --- White Content Area Shape ---
    white_shape = CustomShape(
        prstGeom=PresetGeometry2D(
            'roundRect',
            ah_lst=AdjustHandleList([Point2D(x=100000, y=50000)])
        ),
        spPr=ShapeProperties(
            noFill=False,
            ln={'w': 0},
            solidFill={'rgb': theme_colors['text_fg_light'][2:]}, # White
            # Optional: Add shadow effect (Openpyxl has limited direct support for advanced shape effects)
            # You would need to manipulate raw XML for full control.
        )
    )
    white_shape.width = card_width_emu
    white_shape.height = card_height_emu

    # --- Text Boxes (CustomShape with RichText for content) ---
    # Icon Placeholder Text Box (within gold tab)
    icon_text_height_emu = pixels_to_EMU(pixels_to_points(ICON_TEXT_SIZE_POINTS) * 1.5) # Approx. height for 2 lines
    icon_placeholder_text_shape = CustomShape(
        prstGeom=PresetGeometry2D('rect'), # Simple rectangle for text
        txs=RichText(
            p=[Paragraph(pPr={"algn": "ctr"},
                         endParaRPr=TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(ICON_TEXT_SIZE_POINTS)),
                         r=[TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(ICON_TEXT_SIZE_POINTS),
                                                    solidFill={'rgb': theme_colors['accent_2'][2:]}, # Purple for icon
                                                    t="Icon\nPlaceholder")])]
        ),
        spPr=ShapeProperties(noFill=True, noStroke=True) # Transparent
    )
    icon_placeholder_text_shape.width = gold_tab_width_emu - pixels_to_EMU(cm_to_pixels(0.2))
    icon_placeholder_text_shape.height = icon_text_height_emu # Enough for two lines

    # KPI Value Text Box (within white shape)
    kpi_value_text_height_emu = pixels_to_EMU(pixels_to_points(VALUE_TEXT_SIZE_POINTS) * 1.2) # Approx. height for one line
    kpi_value_text_shape = CustomShape(
        prstGeom=PresetGeometry2D('rect'),
        txs=RichText(
            p=[Paragraph(pPr={"algn": "ctr"},
                         endParaRPr=TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(VALUE_TEXT_SIZE_POINTS)),
                         r=[TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(VALUE_TEXT_SIZE_POINTS),
                                                    solidFill={'rgb': theme_colors['text_fg_dark'][2:]}, # Dark purple for value
                                                    t=f"={kpi_value_cell}")])] # Literal formula string
        ),
        spPr=ShapeProperties(noFill=True, noStroke=True) # Transparent
    )
    kpi_value_text_shape.width = card_width_emu - gold_tab_width_emu - pixels_to_EMU(cm_to_pixels(0.5)) # Width inside white area
    kpi_value_text_shape.height = kpi_value_text_height_emu

    # KPI Label Text Box (within white shape)
    kpi_label_text_height_emu = pixels_to_EMU(pixels_to_points(LABEL_TEXT_SIZE_POINTS) * 1.2)
    kpi_label_text_shape = CustomShape(
        prstGeom=PresetGeometry2D('rect'),
        txs=RichText(
            p=[Paragraph(pPr={"algn": "ctr"},
                         endParaRPr=TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(LABEL_TEXT_SIZE_POINTS)),
                         r=[TextCharacterProperties(latin="Aptos Narrow", sz=pixels_to_points(LABEL_TEXT_SIZE_POINTS),
                                                    solidFill={'rgb': theme_colors['text_fg_dark'][2:]}, # Dark purple for label
                                                    t=kpi_label)])]
        ),
        spPr=ShapeProperties(noFill=True, noStroke=True) # Transparent
    )
    kpi_label_text_shape.width = kpi_value_text_shape.width # Same width as value
    kpi_label_text_shape.height = kpi_label_text_height_emu

    # --- Positioning (AbsoluteAnchor relative to worksheet origin) ---
    # These calculations position relative to the top-left of the anchor cell.
    # The x,y for AbsoluteAnchor are in EMUs from the top-left of the *worksheet*.
    # For a clean component, it's best to define a clear top-left reference point for the entire card.
    
    # Calculate the pixel position of the top-left corner of the anchor cell (e.g., 'B4')
    # This is approximate and depends on default row/col dimensions.
    # For robust code, one would sum up actual row heights and col widths.
    anchor_col_pixels = (start_col_idx) * default_col_width_pixels # Pixels from left edge of worksheet
    anchor_row_pixels = (start_row_idx) * default_row_height_pixels # Pixels from top edge of worksheet
    
    # Convert to EMUs for the drawing objects
    anchor_x_emu = pixels_to_EMU(anchor_col_pixels)
    anchor_y_emu = pixels_to_EMU(anchor_row_pixels)
    
    # Positions for shapes relative to the calculated anchor_x_emu, anchor_y_emu
    
    # White shape (main content area) is placed first
    white_shape_x = anchor_x_emu + gold_tab_width_emu - shape_overlap_emu
    white_shape_y = anchor_y_emu
    
    # Gold tab is to the left, slightly overlapping
    gold_shape_x = anchor_x_emu
    gold_shape_y = anchor_y_emu

    # Text box positions (centered within their respective areas)
    icon_x = gold_shape_x + (gold_tab_width_emu - icon_placeholder_text_shape.width) // 2
    icon_y = gold_shape_y + (card_height_emu - icon_placeholder_text_shape.height) // 2

    value_text_x = white_shape_x + (white_shape.width - kpi_value_text_shape.width) // 2
    value_text_y = white_shape_y + pixels_to_EMU(cm_to_pixels(VALUE_TEXT_Y_OFFSET_CM))

    label_text_x = white_shape_x + (white_shape.width - kpi_label_text_shape.width) // 2
    label_text_y = value_text_y + kpi_value_text_shape.height + pixels_to_EMU(cm_to_pixels(LABEL_TEXT_Y_OFFSET_FROM_VALUE_CM))


    # Create a Drawing object to hold all shapes
    dr = Drawing()

    # Add shapes to the drawing object
    dr.add_picture(
        AbsoluteAnchor(
            pos=Point2D(x=gold_shape_x, y=gold_shape_y),
            ext=PositiveSize2D(cx=gold_shape.width, cy=gold_shape.height),
            sp=gold_shape
        )
    )

    dr.add_picture(
        AbsoluteAnchor(
            pos=Point2D(x=white_shape_x, y=white_shape_y),
            ext=PositiveSize2D(cx=white_shape.width, cy=white_shape.height),
            sp=white_shape
        )
    )
    
    dr.add_picture(
        AbsoluteAnchor(
            pos=Point2D(x=icon_x, y=icon_y),
            ext=PositiveSize2D(cx=icon_placeholder_text_shape.width, cy=icon_placeholder_text_shape.height),
            sp=icon_placeholder_text_shape
        )
    )

    dr.add_picture(
        AbsoluteAnchor(
            pos=Point2D(x=value_text_x, y=value_text_y),
            ext=PositiveSize2D(cx=kpi_value_text_shape.width, cy=kpi_value_text_shape.height),
            sp=kpi_value_text_shape
        )
    )

    dr.add_picture(
        AbsoluteAnchor(
            pos=Point2D(x=label_text_x, y=label_text_y),
            ext=PositiveSize2D(cx=kpi_label_text_shape.width, cy=kpi_label_text_shape.height),
            sp=kpi_label_text_shape
        )
    )
    
    ws.add_drawing(dr)

