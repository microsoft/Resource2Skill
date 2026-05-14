### 1. High-level Skill Pattern Extraction

> **Skill Name**: Dynamic KPI Block via Shapes

*   **Tier**: component
*   **Core Mechanism**: This skill creates a visually appealing and reusable KPI block by combining and styling multiple geometric shapes in Excel. It involves inserting a main rectangle for a primary metric and a smaller oval for a secondary metric, applying theme-consistent colors, and then grouping these elements to function as a single unit. While the video demonstrates direct cell linking within shapes via the Excel formula bar, the `openpyxl` reproduction focuses on establishing the visual structure and aesthetic, with text placeholders for later manual linkage in Excel.
*   **Applicability**: Useful for dashboard creation, executive summaries, and any report requiring a clear, concise, and visually emphasized display of key performance indicators or single-point metrics. It allows for quick visual scanning of important numbers, making reports more engaging than plain cell values.

### 2. Structural Breakdown

-   **Data Layout**: Assumes a source table with `Region`, `Revenue`, and `Market Share` columns. The skill's output is a graphical element, which, in the tutorial, is designed to dynamically reflect data from specific cells (e.g., `B2` for revenue, `C2` for market share). For `openpyxl`, this requires manual linking post-generation or a more complex approach with transparent shapes over cells.
-   **Formula Logic**: The tutorial demonstrates linking shape text directly to cell references (e.g., `=$B$2` for revenue, `=$C$2` for market share) using the Excel formula bar when the shape is selected. This allows the KPI to update dynamically with data changes. `openpyxl` does not directly support this programmatic linking of shape text to cell formulas.
-   **Visual Design**:
    -   **Main KPI Rectangle (Rounded Corners)**:
        -   Shape Fill: Dark blue (e.g., `theme.accent_2`).
        -   Shape Outline: No outline.
        -   Text (inside): Region (e.g., "Asia"), "Revenue", and numerical value. Font color white (e.g., `theme.text_light`), bold, centered. Font size for the entire block is made consistent (e.g., 14).
    -   **Secondary KPI Oval**:
        -   Shape Fill: White (e.g., `theme.text_light`).
        -   Shape Outline: Black outline (e.g., `theme.border_color`).
        -   Text (inside): Percentage value (e.g., "5%"). Font color black (e.g., `theme.text_dark`), bold, centered. Font size (e.g., 14).
-   **Charts/Tables**: This skill does not generate charts or tables. It uses values from an existing data table.
-   **Theme Hooks**: `accent_2`, `text_light`, `text_dark`, `border_color`.

### 3. Reproduction Code

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.geometry import Rectangle, Shape as DrawingShape, GEOM_SHAPE_TYPES
from openpyxl.drawing.fill import ColorChoice, SolidFill
from openpyxl.drawing.drawing import Drawing
from openpyxl.drawing.text import Paragraph, CharacterProperties, RichText, TextBody, Font as TextFont
from openpyxl.utils import get_column_letter
from openpyxl.utils.units import EMU_per_PIXEL, pixels_to_EMU

class ThemePalette:
    """A placeholder for theme color definitions."""
    def __init__(self, theme_name="corporate_blue"):
        if theme_name == "corporate_blue":
            self.header_bg = "1F4E79"  # Dark Blue
            self.text_light = "FFFFFF"  # White
            self.text_dark = "000000"  # Black
            self.border_color = "000000" # Black
            self.accent_1 = "4472C4" # Blue
            self.accent_2 = "2F5597" # Darker Blue, similar to video
        else: # Default or other themes
            self.header_bg = "4F81BD"
            self.text_light = "FFFFFF"
            self.text_dark = "000000"
            self.border_color = "000000"
            self.accent_1 = "5B9BD5"
            self.accent_2 = "336699"

def _create_text_body(text, font_size, font_color, bold=False, wrap_text=True, align='center', valign='middle'):
    """Helper to create a TextBody for a shape."""
    cp = CharacterProperties(latin=TextFont(typeface='Calibri', sz=font_size * 100),
                             b=bold,
                             solidFill=ColorChoice(srgbClr=font_color))
    p = Paragraph(pPr=Paragraph.pPr(algn=align),
                  defRPr=cp,
                  r=[Paragraph.r(t=text)])
    
    body_pr = TextBody.bodyPr(anchor=valign, vert='horz', wrap=wrap_text, lIns=0, tIns=0, rIns=0, bIns=0)
    lst_style = TextBody.lstStyle()

    return TextBody(body_pr=body_pr, lst_style=lst_style, p=[p])

def render(ws, anchor: str, *, theme: str = "corporate_blue", 
           region_name: str = "Asia", 
           revenue_label: str = "Revenue", 
           revenue_value_display: str = "$369,989", # Static for openpyxl; manual Excel linking required
           market_share_value_display: str = "5%", # Static for openpyxl; manual Excel linking required
           **kwargs) -> None:
    """
    Renders a KPI block with region, revenue, and market share using styled shapes.
    Note: Openpyxl does not directly support linking shape text to cell formulas
    or grouping shapes into a single movable unit as shown in the tutorial.
    The values rendered will be static strings. Manual linking (via Excel's formula bar
    when a shape is selected) and grouping (right-click -> Group) in Excel are
    required to achieve the full dynamic and unified behavior.

    Args:
        ws: The worksheet to render on.
        anchor: The top-left cell where the KPI block will be roughly positioned.
                (Note: Shapes are placed absolutely on the drawing layer within openpyxl;
                this anchor serves as a conceptual guide for manual adjustment).
        theme: The name of the theme to use for colors.
        region_name: The name of the region for the KPI.
        revenue_label: The label for the primary metric (e.g., "Revenue").
        revenue_value_display: The display string for the primary metric's value.
        market_share_value_display: The display string for the secondary metric's value.
    """
    
    palette = ThemePalette(theme)

    # Define dimensions and positions for the shapes (in pixels, then convert to EMUs)
    kpi_width_px = 250
    kpi_height_px = 120
    oval_size_px = 60
    padding_px = 10 # Padding for inner elements / relative positioning

    # Approximate starting position for the KPI block (absolute on drawing layer)
    # These values can be adjusted based on desired placement
    start_x_emu = pixels_to_EMU(300) 
    start_y_emu = pixels_to_EMU(100) 

    # --- Create Main KPI Rectangle (Rounded Corners) ---
    rect_shape = DrawingShape(
        shapetype=GEOM_SHAPE_TYPES['roundRect'],
        fill=SolidFill(srgbClr=palette.accent_2),
        text=_create_text_body(
            f"{region_name}\n\n{revenue_label}\n{revenue_value_display}",
            font_size=14, font_color=palette.text_light, bold=True,
            wrap_text=True, align='center', valign='middle'
        ),
        sz=Rectangle(pixels_to_EMU(kpi_width_px), pixels_to_EMU(kpi_height_px)),
        off=Rectangle(start_x_emu, start_y_emu)
    )
    rect_shape.spPr.ln = None # Remove outline

    # --- Create Market Share Oval ---
    # Position the oval relative to the rectangle (bottom right corner)
    oval_offset_x = start_x_emu + pixels_to_EMU(kpi_width_px - oval_size_px - padding_px)
    oval_offset_y = start_y_emu + pixels_to_EMU(kpi_height_px - oval_size_px - padding_px)

    oval_shape = DrawingShape(
        shapetype=GEOM_SHAPE_TYPES['ellipse'],
        fill=SolidFill(srgbClr=palette.text_light),
        text=_create_text_body(
            market_share_value_display,
            font_size=14, font_color=palette.text_dark, bold=True
        ),
        sz=Rectangle(pixels_to_EMU(oval_size_px), pixels_to_EMU(oval_size_px)),
        off=Rectangle(oval_offset_x, oval_offset_y)
    )
    # Add black outline
    oval_shape.spPr.ln.solidFill = ColorChoice(srgbClr=palette.border_color)

    # --- Add shapes to a Drawing object and then to the Worksheet ---
    drawing = Drawing()
    # openpyxl uses add_chart for DrawingShape objects to add them to the drawing canvas
    drawing.add_chart(rect_shape) 
    drawing.add_chart(oval_shape)

    # This anchors the entire drawing canvas to the specified cell.
    # Shapes within the drawing are still positioned using their absolute 'off' coordinates.
    drawing.anchor = anchor

    ws.add_drawing(drawing)

```